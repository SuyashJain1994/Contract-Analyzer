#!/usr/bin/env python3
"""
Test script to verify OpenAI integration works with v1+ API
Run this script to test your OpenAI setup before deploying.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_openai_connection():
    """Test basic OpenAI connection and API call"""
    print("🔍 Testing OpenAI Integration...")
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   Please set your OpenAI API key in .env file")
        return False
    
    if not api_key.startswith("sk-"):
        print("❌ Invalid OpenAI API key format")
        print("   API key should start with 'sk-'")
        return False
    
    print(f"✅ API key found: {api_key[:7]}...")
    
    try:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=api_key)
        model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        
        print(f"🤖 Testing with model: {model}")
        
        # Test basic chat completion
        response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond with a brief confirmation."
                },
                {
                    "role": "user",
                    "content": "Hello, can you confirm this API is working?"
                }
            ],
            max_tokens=50,
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        print(f"✅ OpenAI API Response: {content}")
        
        # Test contract analysis prompt (simplified)
        print("\n🔍 Testing contract analysis capability...")
        
        contract_prompt = """
        Analyze this simple contract clause and respond with JSON:
        
        "The contractor agrees to complete the work within 30 days."
        
        Respond with JSON format:
        {
            "summary": "brief summary",
            "risks": [{"type": "timeline", "severity": "low", "description": "30-day deadline"}]
        }
        """
        
        analysis_response = await client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a legal contract analyzer. Always respond with valid JSON."
                },
                {
                    "role": "user",
                    "content": contract_prompt
                }
            ],
            max_tokens=200,
            temperature=0.1
        )
        
        analysis_content = analysis_response.choices[0].message.content
        print(f"✅ Contract Analysis Response: {analysis_content[:100]}...")
        
        # Try to parse JSON
        import json
        try:
            parsed = json.loads(analysis_content)
            print("✅ JSON parsing successful")
        except json.JSONDecodeError:
            print("⚠️  Response is not valid JSON, but API is working")
        
        print("\n🎉 OpenAI integration test completed successfully!")
        return True
        
    except ImportError:
        print("❌ OpenAI library not installed")
        print("   Run: pip install openai>=1.0.0")
        return False
        
    except Exception as e:
        error_msg = str(e).lower()
        print(f"❌ OpenAI API Error: {e}")
        
        if "rate limit" in error_msg:
            print("   → Rate limit exceeded. Wait and try again.")
        elif "insufficient_quota" in error_msg:
            print("   → OpenAI quota exceeded. Check your billing.")
        elif "invalid_api_key" in error_msg:
            print("   → Invalid API key. Check your configuration.")
        elif "model" in error_msg and "not found" in error_msg:
            print("   → Model not available. Try 'gpt-3.5-turbo'")
        else:
            print("   → Check your internet connection and OpenAI account.")
        
        return False

async def test_full_integration():
    """Test the full contract analyzer integration"""
    print("\n🧪 Testing Full Contract Analyzer Integration...")
    
    try:
        from app.services.ai_analyzer import AIAnalyzer
        
        analyzer = AIAnalyzer()
        
        if not analyzer.client:
            print("❌ AI Analyzer not properly initialized")
            return False
        
        # Test with sample contract text
        sample_contract = """
        SERVICE AGREEMENT
        
        This Service Agreement is entered into between Company A and Company B.
        
        1. Services: Company B will provide consulting services.
        2. Payment: $5,000 per month, payable within 30 days.
        3. Term: This agreement is valid for 12 months.
        4. Termination: Either party may terminate with 30 days notice.
        """
        
        result = await analyzer.analyze_contract(
            text=sample_contract,
            contract_type="service",
            analysis_depth="standard",
            filename="test_contract.txt"
        )
        
        print(f"✅ Contract analysis completed!")
        print(f"   Summary: {result.summary[:100]}...")
        print(f"   Risks found: {len(result.risks)}")
        print(f"   Insights: {len(result.insights)}")
        print(f"   Compliance score: {result.compliance_score}")
        
        return True
        
    except Exception as e:
        print(f"❌ Full integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Contract Analyzer - OpenAI Integration Test\n")
    
    async def run_tests():
        # Test basic OpenAI connection
        basic_test = await test_openai_connection()
        
        if basic_test:
            # Test full integration
            await test_full_integration()
        else:
            print("\n❌ Basic OpenAI test failed. Fix the issues above before proceeding.")
            
        print("\n" + "="*50)
        print("📋 Summary:")
        print("- Set OPENAI_API_KEY in your .env file")
        print("- Ensure you have OpenAI credits in your account")
        print("- Run: pip install -r requirements.txt")
        print("- Start app: uvicorn app.main:app --reload")
        print("="*50)
    
    asyncio.run(run_tests())