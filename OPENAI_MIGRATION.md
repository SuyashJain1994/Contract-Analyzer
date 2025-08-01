# OpenAI v1+ Migration Guide

This guide explains the changes made to support OpenAI v1+ and how to resolve migration issues.

## 🔄 Changes Made

### 1. **Import Changes**
```python
# Old (v0.x)
import openai
openai.api_key = "your-key"

# New (v1+)
from openai import AsyncOpenAI
client = AsyncOpenAI(api_key="your-key")
```

### 2. **API Call Changes**
```python
# Old (v0.x)
response = await openai.ChatCompletion.acreate(...)

# New (v1+)
response = await client.chat.completions.create(...)
```

### 3. **Client Initialization**
The new version uses a client-based approach instead of global configuration.

## 🚨 Common Issues & Solutions

### Issue 1: `AttributeError: module 'openai' has no attribute 'ChatCompletion'`

**Solution**: Update your OpenAI library and use the new client:
```bash
pip install openai>=1.0.0
```

### Issue 2: `openai.error.InvalidRequestError`

**Solution**: The new version has different error types:
```python
# Old
from openai.error import InvalidRequestError

# New
from openai import OpenAIError
```

### Issue 3: Environment Variable Issues

**Solution**: Ensure your `.env` file has the correct OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

## 🛠️ Updated Configuration

### Environment Variables (.env)
```env
# Required
OPENAI_API_KEY=sk-your-openai-api-key

# Optional - Model selection
OPENAI_MODEL=gpt-4  # or gpt-3.5-turbo for cost savings

# Other settings
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./contract_analyzer.db
```

### Supported Models
- `gpt-4` (recommended for best analysis)
- `gpt-4-turbo` (faster, cost-effective)
- `gpt-3.5-turbo` (budget option)

## 🔧 Testing Your Setup

### 1. Test OpenAI Connection
```python
import asyncio
from openai import AsyncOpenAI

async def test_openai():
    client = AsyncOpenAI(api_key="your-key")
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ OpenAI connection successful")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")

# Run test
asyncio.run(test_openai())
```

### 2. Test Contract Analysis
```bash
# Start the application
uvicorn app.main:app --reload

# Test the health endpoint
curl http://localhost:8000/api/health

# Test with a sample file upload
# (Use the web interface at http://localhost:8000)
```

## 🚀 Deployment Considerations

### 1. Update Requirements
Ensure your `requirements.txt` has:
```
openai>=1.51.0
```

### 2. Environment Variables
Set these in your deployment platform:
```bash
# Railway
railway variables set OPENAI_API_KEY=your-key

# Render
# Set in dashboard under Environment Variables

# Heroku
heroku config:set OPENAI_API_KEY=your-key
```

### 3. Error Handling
The updated code now handles:
- Rate limiting (429 errors)
- Quota exceeded (402 errors)
- Invalid API keys (401 errors)
- Network timeouts
- Empty responses

## 📊 Cost Optimization

### Model Comparison
| Model | Speed | Quality | Cost (per 1K tokens) |
|-------|-------|---------|---------------------|
| gpt-4 | Slow | Excellent | $0.03 |
| gpt-4-turbo | Fast | Excellent | $0.01 |
| gpt-3.5-turbo | Very Fast | Good | $0.002 |

### Recommendations
- **Development**: Use `gpt-3.5-turbo`
- **Production**: Use `gpt-4-turbo` or `gpt-4`
- **Budget**: Use `gpt-3.5-turbo` with longer prompts

## 🔍 Troubleshooting

### Debug Mode
Enable debug logging to see API calls:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Error Messages

**"Invalid API key"**
- Check your OpenAI API key is correct
- Ensure it starts with `sk-`
- Verify it's set in environment variables

**"Rate limit exceeded"**
- You're making too many requests
- Wait a few minutes and try again
- Consider upgrading your OpenAI plan

**"Insufficient quota"**
- Your OpenAI account is out of credits
- Add billing information to your OpenAI account
- Check your usage at platform.openai.com

**"Model not found"**
- Check the model name is correct
- Ensure you have access to the model
- Try `gpt-3.5-turbo` as a fallback

## 📚 Additional Resources

- [OpenAI Python Library Documentation](https://github.com/openai/openai-python)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Migration Guide from OpenAI](https://github.com/openai/openai-python/discussions/742)

## 🆘 Still Having Issues?

1. **Check your OpenAI account**: Visit [platform.openai.com](https://platform.openai.com)
2. **Verify API key**: Make sure it's active and has credits
3. **Test locally**: Run the test script above
4. **Check logs**: Look at application logs for specific errors

If you're still having issues, create an issue in the repository with:
- Your OpenAI library version (`pip show openai`)
- Error messages from logs
- Your configuration (without API keys)