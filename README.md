# 🤖 Medical Chatbot

A sophisticated medical chatbot built with Flask, LangChain, and OpenAI that provides intelligent responses to medical queries using RAG (Retrieval-Augmented Generation) technology.

## ✨ Features

- **Intelligent Medical Q&A**: Powered by OpenAI's GPT-4 and LangChain
- **RAG Technology**: Retrieves relevant medical information from your knowledge base
- **Modern UI**: Clean, responsive chat interface
- **Real-time Responses**: Instant answers to medical questions
- **Scalable**: Ready for production deployment on Vercel

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/medical-chatbot.git
   cd medical-chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```
   PINECONE_API_KEY=your_pinecone_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:8080`

## 🎯 Deployment

### Vercel Deployment (Recommended)

This application is optimized for Vercel deployment. Follow the detailed guide in [DEPLOYMENT.md](DEPLOYMENT.md).

**Quick Steps**:
1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy!

## 📁 Project Structure

```
Medical-Chatbot/
├── app.py                 # Main Flask application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── runtime.txt          # Python version specification
├── templates/
│   └── chat.html        # Chat interface template
├── static/
│   └── style.css        # CSS styles
├── src/
│   ├── helper.py        # Helper functions
│   └── prompt.py        # Prompt templates
├── data/
│   └── Medical_book.pdf # Medical knowledge base
└── DEPLOYMENT.md        # Detailed deployment guide
```

## 🔧 Configuration

### Environment Variables

- `PINECONE_API_KEY`: Your Pinecone API key for vector storage
- `OPENAI_API_KEY`: Your OpenAI API key for AI responses

### Dependencies

Key dependencies include:
- `flask==3.1.1`: Web framework
- `langchain==0.3.26`: AI framework
- `langchain-openai==0.3.24`: OpenAI integration
- `langchain-pinecone==0.2.8`: Pinecone integration
- `sentence-transformers==4.1.0`: Text embeddings

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8080/health
```
Should return: `{"status": "healthy"}`

### Chat Interface
Visit `http://localhost:8080` to access the chat interface.

## 🐛 Troubleshooting

### Common Issues

1. **Module Not Found**: Make sure all dependencies are installed
2. **Environment Variables**: Verify API keys are set correctly
3. **Pinecone Connection**: Check if your Pinecone index exists
4. **OpenAI API**: Ensure you have sufficient credits

### Debug Mode

Add this route to your app.py for debugging:
```python
@app.route('/debug')
def debug():
    return jsonify({
        "pinecone_key": bool(PINECONE_API_KEY),
        "openai_key": bool(OPENAI_API_KEY)
    })
```

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT.md) - Complete Vercel deployment instructions
- [LangChain Documentation](https://python.langchain.com/) - AI framework docs
- [Vercel Documentation](https://vercel.com/docs) - Deployment platform docs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [troubleshooting section](#-troubleshooting)
2. Review the [deployment guide](DEPLOYMENT.md)
3. Check Vercel logs for deployment issues
4. Ensure all environment variables are set correctly

## 🎉 Success!

Once deployed, your medical chatbot will be available at:
`https://your-app-name.vercel.app/`

The application will automatically scale and handle traffic for you!