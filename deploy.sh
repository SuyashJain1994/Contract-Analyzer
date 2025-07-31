#!/bin/bash

# Contract Analyzer Deployment Script
set -e

echo "🚀 Starting Contract Analyzer deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration (especially OPENAI_API_KEY)"
    read -p "Press Enter to continue after editing .env file..."
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads
mkdir -p ssl

# Generate secret key if not set
if grep -q "your-secret-key-change-in-production" .env; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    sed -i "s/your-secret-key-change-in-production/$SECRET_KEY/g" .env
    echo "🔐 Generated new secret key"
fi

# Build and start services
echo "🔨 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ Application is running successfully!"
    echo ""
    echo "🌐 Access your application at: http://localhost"
    echo "📊 API documentation at: http://localhost:8000/api/docs"
    echo "🔐 Default login: suyash@lawfirm.com / demo123"
    echo ""
    echo "📋 To view logs: docker-compose logs -f"
    echo "🛑 To stop: docker-compose down"
else
    echo "❌ Application failed to start. Check logs with: docker-compose logs"
    exit 1
fi