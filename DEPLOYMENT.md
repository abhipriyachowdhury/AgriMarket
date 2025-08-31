# Deployment Guide for AgriMarket API

## Option 1: Deploy to Railway (Recommended - Free Tier)

### Steps:
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Initialize and Deploy:**
   ```bash
   railway init
   railway up
   ```

4. **Get your live URL:**
   ```bash
   railway domain
   ```

## Option 2: Deploy to Render (Free Tier) ⭐ RECOMMENDED

### Quick Deploy:
```bash
python deploy_render.py
```

### Manual Steps:
1. **Go to [render.com](https://render.com)**
2. **Sign up/Login** with GitHub account
3. **Click "New +" → "Web Service"**
4. **Connect GitHub repository** (AgriMarket)
5. **Configure service:**
   - Name: `agrimarket-api`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn APIwebScraping:app`
   - Plan: `Free`
6. **Click "Create Web Service"**
7. **Wait for build** (5-10 minutes)
8. **Get your live URL:** `https://your-app-name.onrender.com`

## Option 3: Deploy to Heroku

### Steps:
1. **Install Heroku CLI:**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI -e
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```

4. **Deploy:**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

## Option 4: Deploy to VPS/Cloud Server

### Steps:
1. **SSH into your server**
2. **Clone your repository:**
   ```bash
   git clone <your-repo-url>
   cd AgriMarket
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run with Gunicorn:**
   ```bash
   gunicorn --bind 0.0.0.0:8000 APIwebScraping:app
   ```

## Option 5: Deploy Locally with ngrok (For Testing)

### Steps:
1. **Run your Flask app:**
   ```bash
   python APIwebScraping.py
   ```

2. **In another terminal, expose with ngrok:**
   ```bash
   ngrok http 5000
   ```

3. **Use the ngrok URL for external access**

## Important Notes:

### For Cloud Deployment:
- **Selenium Issue**: Cloud platforms don't have GUI browsers
- **Solution**: Use headless Chrome or switch to requests + BeautifulSoup

### Environment Variables:
- Set `PORT` environment variable (Railway/Render will do this automatically)

## Testing Your Deployed API:

```bash
# Test the home endpoint
curl https://your-app-name.railway.app/

# Test the data endpoint
curl "https://your-app-name.railway.app/request?commodity=Rice&state=Maharashtra&market=Mumbai"
```
