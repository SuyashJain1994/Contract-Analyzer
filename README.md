# LegalAI Pro - Contract Analyzer

An AI-powered legal contract analysis platform that helps legal professionals analyze contracts, identify risks, and get actionable insights.

![Contract Analyzer Dashboard](https://via.placeholder.com/800x400/1e293b/ffffff?text=LegalAI+Pro+Dashboard)

## ✨ Features

- **🤖 AI-Powered Analysis**: Uses OpenAI GPT-4 for intelligent contract analysis
- **📄 Multi-Format Support**: Supports PDF, DOC, DOCX, and TXT files
- **🔍 Risk Assessment**: Identifies potential risks and provides recommendations
- **📊 Compliance Scoring**: Evaluates contract compliance with industry standards
- **💡 Smart Insights**: Provides negotiation tips and market benchmarks
- **🔐 Secure Authentication**: JWT-based authentication system
- **📱 Responsive Design**: Beautiful, modern UI that works on all devices
- **⚡ Real-time Analysis**: Live analysis results with progress tracking

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- OpenAI API key (for AI analysis)

### One-Command Deployment

```bash
# Clone the repository
git clone <repository-url>
cd contract-analyzer

# Make deployment script executable
chmod +x deploy.sh

# Run deployment script
./deploy.sh
```

The script will:
1. Check dependencies
2. Create configuration files
3. Build Docker images
4. Start all services
5. Verify deployment

Access your application at: http://localhost

## 🛠️ Manual Setup

### 1. Environment Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

Required environment variables:
```env
OPENAI_API_KEY=your-openai-api-key-here
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://postgres:password@db:5432/contract_analyzer
```

### 2. Development Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run database migrations
python -m alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Production Deployment

```bash
# Build and start with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📋 API Documentation

Once deployed, access the interactive API documentation at:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Key Endpoints

- `POST /api/auth/login` - User authentication
- `POST /api/upload` - Upload and analyze contracts
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/health` - Health check

## 🔧 Configuration

### Database Options

**SQLite (Development)**
```env
DATABASE_URL=sqlite:///./contract_analyzer.db
```

**PostgreSQL (Production)**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/contract_analyzer
```

### AI Configuration

```env
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for cost savings
```

### Security Settings

```env
SECRET_KEY=your-secure-secret-key
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## 📁 Project Structure

```
contract-analyzer/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   ├── services/
│   │   ├── ai_analyzer.py   # AI analysis service
│   │   ├── auth.py          # Authentication service
│   │   └── document_processor.py # Document processing
│   └── utils/
│       └── exceptions.py    # Custom exceptions
├── static/
│   └── index.html          # Frontend application
├── docker-compose.yml      # Docker services
├── Dockerfile             # Application container
├── nginx.conf            # Nginx configuration
└── requirements.txt      # Python dependencies
```

## 🔐 Authentication

Default credentials for demo:
- **Email**: suyash@lawfirm.com
- **Password**: demo123

For production, implement proper user registration and management.

## 📊 Supported File Types

| Format | Extension | Max Size |
|--------|-----------|----------|
| PDF    | .pdf      | 50MB     |
| Word   | .docx, .doc | 50MB   |
| Text   | .txt      | 50MB     |

## 🚨 Contract Analysis Features

### Risk Assessment
- **Critical**: Immediate attention required
- **High**: Significant risk factors
- **Medium**: Moderate concerns
- **Low**: Minor issues

### Analysis Depths
- **Standard**: Quick overview and key points
- **Deep**: Detailed clause-by-clause analysis
- **Compliance**: Focus on regulatory compliance
- **Risk Assessment**: Comprehensive risk evaluation

### Contract Types
- Employment Agreements
- Service Contracts
- NDAs (Non-Disclosure Agreements)
- Lease Agreements
- Partnership Agreements
- General Contracts

## 🔧 Troubleshooting

### Common Issues

**1. OpenAI API Errors**
```bash
# Check API key configuration
docker-compose logs web | grep -i openai
```

**2. Database Connection Issues**
```bash
# Check database status
docker-compose ps db
docker-compose logs db
```

**3. File Upload Problems**
```bash
# Check upload directory permissions
ls -la uploads/
```

### Performance Optimization

**1. Database Optimization**
- Use PostgreSQL for production
- Configure connection pooling
- Add database indexes

**2. AI Analysis Optimization**
- Use GPT-3.5-turbo for faster analysis
- Implement caching for repeated analyses
- Add background job processing

## 🌐 Deployment Options

### Cloud Platforms

**1. AWS ECS/Fargate**
```bash
# Build and push to ECR
docker build -t contract-analyzer .
docker tag contract-analyzer:latest <ecr-uri>
docker push <ecr-uri>
```

**2. Google Cloud Run**
```bash
# Deploy to Cloud Run
gcloud run deploy contract-analyzer --source .
```

**3. DigitalOcean App Platform**
```yaml
# app.yaml
name: contract-analyzer
services:
- name: web
  source_dir: /
  github:
    repo: your-repo
    branch: main
  run_command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Self-Hosted

**1. VPS Deployment**
```bash
# Copy files to server
scp -r . user@server:/opt/contract-analyzer

# Run on server
cd /opt/contract-analyzer
./deploy.sh
```

**2. Kubernetes**
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## 📈 Monitoring & Logging

### Health Checks
- Application: http://localhost:8000/api/health
- Database: Check connection in logs
- Redis: Check connection in logs

### Logging
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f db
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review API documentation

## 🔮 Roadmap

- [ ] Advanced contract comparison
- [ ] Multi-language support
- [ ] Custom risk rules engine
- [ ] Integration with legal databases
- [ ] Mobile application
- [ ] Advanced reporting and analytics
- [ ] Webhook notifications
- [ ] API rate limiting and quotas

---

**Built with ❤️ for legal professionals**
