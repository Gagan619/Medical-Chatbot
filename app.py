from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Load API keys
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize variables
embedding = None
docsearch = None
rag_chain = None

def initialize_services():
    """Initialize the AI services with proper error handling"""
    global embedding, docsearch, rag_chain
    
    try:
        # Check if API keys are available
        if not PINECONE_API_KEY or not OPENAI_API_KEY:
            logger.error("Missing API keys")
            return False
        
        # Import required modules with error handling
        try:
            from langchain_pinecone import PineconeVectorStore
            from langchain_openai import ChatOpenAI, OpenAIEmbeddings
            from langchain.chains import create_retrieval_chain
            from langchain.chains.combine_documents import create_stuff_documents_chain
            from langchain_core.prompts import ChatPromptTemplate
            from src.prompt import system_prompt
        except ImportError as e:
            logger.error(f"Import error: {str(e)}")
            return False
        
        logger.info("Loading OpenAI embeddings model...")
        embedding = OpenAIEmbeddings(
            openai_api_key=OPENAI_API_KEY,
            model="text-embedding-ada-002"
        )
        
        logger.info("Connecting to Pinecone...")
        index_name = "medical-chatbot"
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embedding
        )
        
        logger.info("Creating retrieval chain...")
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
        
        chatModel = ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        
        question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        logger.info("Services initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing services: {str(e)}")
        return False

# Simple test route
@app.route('/test')
def test():
    try:
        return jsonify({
            "status": "ok",
            "message": "App is working!",
            "pinecone_key": bool(PINECONE_API_KEY),
            "openai_key": bool(OPENAI_API_KEY)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Default route
@app.route('/')
def index():
    try:
        return render_template('chat.html')
    except Exception as e:
        logger.error(f"Error in index route: {str(e)}")
        return jsonify({"error": "Template not found"}), 500

# Route to handle chat requests
@app.route('/get', methods=['GET', 'POST'])
def chat():
    try:
        global rag_chain
        
        # Initialize services if not already done
        if rag_chain is None:
            logger.info("Initializing services...")
            if not initialize_services():
                return jsonify({"error": "Failed to initialize services. Please check your API keys."}), 500
        
        # Get the message from the request
        if request.method == 'POST':
            msg = request.form.get('msg', '')
        else:
            msg = request.args.get('msg', '')
        
        if not msg:
            return jsonify({"error": "No message provided"}), 400
        
        logger.info(f"Received message: {msg}")
        
        # Get response from RAG chain
        try:
            response = rag_chain.invoke({"input": msg})
            answer = response.get('answer', 'No answer generated')
            logger.info(f"Generated answer: {answer[:100]}...")
            return str(answer)
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error in RAG chain: {error_msg}")
            
            # Handle specific API errors
            if "insufficient_quota" in error_msg or "429" in error_msg:
                return jsonify({
                    "error": "OpenAI API quota exceeded. Please check your billing and try again later.",
                    "details": "You've exceeded your current OpenAI API quota. Please visit https://platform.openai.com/account/billing to add credits."
                }), 429
            elif "invalid_api_key" in error_msg:
                return jsonify({
                    "error": "Invalid OpenAI API key. Please check your configuration.",
                    "details": "The OpenAI API key is invalid or expired."
                }), 401
            else:
                return jsonify({"error": f"Error generating response: {error_msg}"}), 500
    
    except Exception as e:
        logger.error(f"Error in chat route: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Health check route for Vercel
@app.route('/health')
def health():
    try:
        return jsonify({
            "status": "healthy",
            "services_initialized": rag_chain is not None,
            "pinecone_key": bool(PINECONE_API_KEY),
            "openai_key": bool(OPENAI_API_KEY)
        }), 200
    except Exception as e:
        logger.error(f"Error in health route: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

# Debug route to check environment variables
@app.route('/debug')
def debug():
    try:
        return jsonify({
            "pinecone_key": bool(PINECONE_API_KEY),
            "openai_key": bool(OPENAI_API_KEY),
            "services_initialized": rag_chain is not None,
            "environment": "production" if os.getenv("VERCEL") else "development"
        })
    except Exception as e:
        logger.error(f"Error in debug route: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# Vercel handler
def handler(request):
    return app(request)

# Running the app on local host
if __name__ == '__main__':
    # Initialize services on startup for local development
    logger.info("Starting local development server...")
    initialize_services()
    app.run(host="0.0.0.0", port=8080, debug=True)