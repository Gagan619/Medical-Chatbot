from flask import Flask, render_template, jsonify, request
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

# Initialize Flask app
app = Flask(__name__)

# Load API keys
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Initialize variables
embedding = None
docsearch = None
rag_chain = None

def initialize_services():
    """Initialize the AI services"""
    global embedding, docsearch, rag_chain
    
    try:
        # Load the embeddings model
        embedding = download_embeddings()
        
        # Load the index
        index_name = "medical-chatbot"
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embedding
        )
        
        # Create the retrieval chain
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
        
        chatModel = ChatOpenAI(model="gpt-4o-mini")
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        
        question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        return True
    except Exception as e:
        print(f"Error initializing services: {e}")
        return False

# Default route
@app.route('/')
def index():
    return render_template('chat.html')

# Route to handle chat requests
@app.route('/get', methods=['GET', 'POST'])
def chat():
    try:
        if rag_chain is None:
            if not initialize_services():
                return jsonify({"error": "Services not initialized"}), 500
        
        msg = request.form['msg']
        input_text = msg
        print(f"Received message: {input_text}")
        
        response = rag_chain.invoke({"input": msg})
        return str(response['answer'])
    
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({"error": str(e)}), 500

# Health check route for Vercel
@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Vercel handler
def handler(request):
    return app(request)

# Running the app on local host
if __name__ == '__main__':
    # Initialize services on startup
    initialize_services()
    app.run(host="0.0.0.0", port=8080, debug=True)