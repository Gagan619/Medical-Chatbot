# 🚀 Vercel Deployment Guide for Medical Chatbot

## ✅ Prerequisites

1. **GitHub Account**: Make sure your code is pushed to GitHub
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **Environment Variables**: You'll need these API keys:
   - `PINECONE_API_KEY`: Your Pinecone API key
   - `OPENAI_API_KEY`: Your OpenAI API key

## 🎯 Step-by-Step Deployment

### Step 1: Push Code to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com](https://github.com)
   - Click "New repository"
   - Name it `medical-chatbot`
   - Don't initialize with README (we already have one)

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/medical-chatbot.git
   git branch -M main
   git push -u origin main
   ```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**:
   - Visit [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"

2. **Import GitHub Repository**:
   - Click "Import Git Repository"
   - Select your `medical-chatbot` repository
   - Click "Import"

3. **Configure Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (leave as default)
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

4. **Set Environment Variables**:
   - Click "Environment Variables"
   - Add these variables:
     ```
     Name: PINECONE_API_KEY
     Value: your_pinecone_api_key_here
     Environment: Production, Preview, Development
     ```
     ```
     Name: OPENAI_API_KEY
     Value: your_openai_api_key_here
     Environment: Production, Preview, Development
     ```

5. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete (usually 2-3 minutes)

#### Option B: Using Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Environment Variables**:
   ```bash
   vercel env add PINECONE_API_KEY
   vercel env add OPENAI_API_KEY
   ```

5. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

## 🔧 Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/app.py"
    }
  ],
  "env": {
    "PYTHONPATH": "."
  }
}
```

### requirements.txt
```
langchain==0.3.26
flask==3.1.1 
sentence-transformers==4.1.0
pypdf==5.6.1 
python-dotenv==1.1.0
langchain-pinecone==0.2.8 
langchain-openai==0.3.24
langchain-community==0.3.26
langchain-core==0.3.72
langchain-text-splitters==0.3.9
```

### runtime.txt
```
python-3.10
```

## 🧪 Testing Your Deployment

1. **Health Check**:
   - Visit: `https://your-app-name.vercel.app/health`
   - Should return: `{"status": "healthy"}`

2. **Main Application**:
   - Visit: `https://your-app-name.vercel.app/`
   - Should show the chat interface

3. **Chat Functionality**:
   - Type a message in the chat
   - Should receive a response from the AI

## 🐛 Troubleshooting

### Common Issues:

1. **Module Not Found Errors**:
   - Make sure all dependencies are in `requirements.txt`
   - Check that `runtime.txt` specifies the correct Python version

2. **Environment Variables Not Set**:
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add missing variables

3. **Pinecone Connection Issues**:
   - Verify your Pinecone API key is correct
   - Check that your Pinecone index exists and is accessible

4. **OpenAI API Issues**:
   - Verify your OpenAI API key is correct
   - Check that you have sufficient credits

### Debug Steps:

1. **Check Vercel Logs**:
   - Go to Vercel Dashboard → Your Project → Functions
   - Click on the function to see logs

2. **Test Locally First**:
   ```bash
   python app.py
   ```
   - Visit `http://localhost:8080`
   - Make sure everything works locally

3. **Check Environment Variables**:
   - Add this to your app.py temporarily:
   ```python
   @app.route('/debug')
   def debug():
       return jsonify({
           "pinecone_key": bool(PINECONE_API_KEY),
           "openai_key": bool(OPENAI_API_KEY)
       })
   ```

## 📞 Support

If you encounter issues:

1. **Check Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
2. **Review Logs**: Vercel Dashboard → Functions → Logs
3. **Test Locally**: Make sure it works on your machine first

## 🎉 Success!

Once deployed successfully, your medical chatbot will be available at:
`https://your-app-name.vercel.app/`

The app will automatically scale and handle traffic for you! 