# 🚀 Deployment Guide - Contract Analyzer

This guide will help you deploy your Contract Analyzer to various cloud platforms. Choose the option that works best for you!

## 📋 Prerequisites

Before deploying, ensure you have:
- [ ] OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- [ ] GitHub account (for most platforms)
- [ ] Your code pushed to a GitHub repository

## 🏆 **Recommended: Railway (Easiest)**

Railway offers the simplest deployment with automatic HTTPS and database setup.

### Steps:
1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and Initialize**
   ```bash
   railway login
   railway init
   ```

3. **Set Environment Variables**
   ```bash
   railway variables set OPENAI_API_KEY=your-api-key-here
   railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   ```

4. **Deploy**
   ```bash
   railway up
   ```

5. **Add Database (Optional)**
   ```bash
   railway add postgresql
   ```

**Your app will be live at: `https://your-app-name.up.railway.app`**

---

## 🎨 **Option 2: Render (Free Tier)**

Render offers free hosting with automatic SSL and database integration.

### Steps:
1. **Push to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Go to [render.com](https://render.com)** and sign up

3. **Create New Web Service**
   - Connect your GitHub repository
   - Choose "Web Service"
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SECRET_KEY`: Generate a secure key
   - `ENVIRONMENT`: production

5. **Add Database (Optional)**
   - Create a PostgreSQL database
   - Connect it to your web service

**Your app will be live at: `https://your-app-name.onrender.com`**

---

## 🌊 **Option 3: DigitalOcean App Platform**

DigitalOcean offers robust hosting with integrated databases and monitoring.

### Steps:
1. **Install doctl CLI**
   ```bash
   # macOS
   brew install doctl
   
   # Linux
   wget https://github.com/digitalocean/doctl/releases/download/v1.94.0/doctl-1.94.0-linux-amd64.tar.gz
   tar xf doctl-*.tar.gz
   sudo mv doctl /usr/local/bin
   ```

2. **Authenticate**
   ```bash
   doctl auth init
   ```

3. **Update app.yaml**
   Edit `app.yaml` and replace `your-username/contract-analyzer` with your GitHub repo.

4. **Deploy**
   ```bash
   doctl apps create --spec app.yaml
   ```

5. **Set Environment Variables** via DigitalOcean dashboard
   - Navigate to your app in the DO dashboard
   - Go to Settings > App-Level Environment Variables
   - Add your `OPENAI_API_KEY`

**Your app will be live at: `https://your-app-name.ondigitalocean.app`**

---

## 🟣 **Option 4: Heroku (Classic)**

Heroku is a traditional PaaS with extensive add-on ecosystem.

### Steps:
1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install-ubuntu.sh | sh
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-contract-analyzer
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set OPENAI_API_KEY=your-api-key-here
   heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
   ```

4. **Add Database**
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

**Your app will be live at: `https://your-contract-analyzer.herokuapp.com`**

---

## ⚡ **Option 5: Vercel (Serverless)**

Vercel offers serverless deployment with automatic scaling.

### Steps:
1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login and Deploy**
   ```bash
   vercel login
   vercel
   ```

3. **Set Environment Variables**
   ```bash
   vercel env add OPENAI_API_KEY
   vercel env add SECRET_KEY
   ```

4. **Deploy**
   ```bash
   vercel --prod
   ```

**Your app will be live at: `https://your-app-name.vercel.app`**

---

## 🔧 **Post-Deployment Setup**

After deployment, you'll need to:

### 1. **Test Your Application**
- Visit your app URL
- Try logging in with: `suyash@lawfirm.com` / `demo123`
- Upload a test contract file
- Verify AI analysis works

### 2. **Configure Custom Domain (Optional)**
Most platforms allow you to add a custom domain:
- Railway: Dashboard > Settings > Domains
- Render: Dashboard > Settings > Custom Domains
- Heroku: `heroku domains:add yourdomain.com`

### 3. **Set up SSL Certificate**
All recommended platforms provide automatic HTTPS/SSL certificates.

### 4. **Monitor Your Application**
- Check logs: Most platforms provide log viewing in their dashboards
- Set up monitoring: Consider adding error tracking (Sentry, etc.)

---

## 🚨 **Troubleshooting**

### Common Issues:

**1. OpenAI API Errors**
- Ensure your API key is correctly set
- Check your OpenAI account has credits
- Verify the key has the right permissions

**2. Database Connection Issues**
- For SQLite: Works out of the box
- For PostgreSQL: Ensure DATABASE_URL is properly set

**3. File Upload Problems**
- Check file size limits (50MB default)
- Ensure upload directory permissions are correct

**4. Build Failures**
- Check Python version compatibility
- Verify all dependencies are in requirements.txt

### Getting Help:
- Check platform-specific documentation
- Review application logs
- Test locally first: `uvicorn app.main:app --reload`

---

## 🎯 **Recommended Setup for Production**

For a production deployment, I recommend:

1. **Railway or Render** for simplicity
2. **PostgreSQL database** for reliability
3. **Custom domain** for professionalism
4. **Environment variables** properly configured
5. **Error monitoring** (Sentry integration)

---

## 📊 **Cost Estimates**

| Platform | Free Tier | Paid Plans Start |
|----------|-----------|------------------|
| Railway | $5/month after trial | $5/month |
| Render | 750 hours/month | $7/month |
| DigitalOcean | $0 (with credits) | $5/month |
| Heroku | Limited hours | $7/month |
| Vercel | Generous free tier | $20/month |

Choose the platform that best fits your needs and budget!

---

**Need help with deployment? Create an issue in the repository or check the troubleshooting section above.**