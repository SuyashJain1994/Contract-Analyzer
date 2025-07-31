import openai
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import uuid

from ..config import settings
from ..models.schemas import AnalysisResult, RiskItem, Insight, ContractType, AnalysisDepth, RiskLevel
from ..utils.exceptions import AIAnalysisException

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """Service for AI-powered contract analysis using OpenAI GPT"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured. AI analysis will not work.")
        else:
            openai.api_key = settings.OPENAI_API_KEY
    
    async def analyze_contract(
        self, 
        text: str, 
        contract_type: str, 
        analysis_depth: str, 
        filename: str
    ) -> AnalysisResult:
        """Analyze contract text using AI"""
        try:
            if not settings.OPENAI_API_KEY:
                raise AIAnalysisException(
                    "AI analysis not available: OpenAI API key not configured",
                    status_code=503
                )
            
            # Create analysis prompt based on contract type and depth
            prompt = self._create_analysis_prompt(text, contract_type, analysis_depth)
            
            # Call OpenAI API
            response = await self._call_openai(prompt)
            
            # Parse and structure the response
            analysis_data = self._parse_ai_response(response)
            
            # Create structured analysis result
            analysis_result = AnalysisResult(
                id=str(uuid.uuid4()),
                filename=filename,
                contract_type=ContractType(contract_type),
                analysis_depth=AnalysisDepth(analysis_depth),
                created_at=datetime.now(),
                **analysis_data
            )
            
            return analysis_result
            
        except AIAnalysisException:
            raise
        except Exception as e:
            logger.error(f"AI analysis error for {filename}: {str(e)}")
            raise AIAnalysisException(
                f"Failed to analyze contract: {str(e)}",
                status_code=500
            )
    
    def _create_analysis_prompt(self, text: str, contract_type: str, analysis_depth: str) -> str:
        """Create analysis prompt based on contract type and depth"""
        
        base_prompt = f"""
        You are an expert legal contract analyzer. Analyze the following {contract_type} contract with {analysis_depth} analysis depth.
        
        Contract Text:
        {text[:8000]}  # Truncate to avoid token limits
        
        Please provide a comprehensive analysis in the following JSON format:
        {{
            "summary": "Brief summary of the contract",
            "key_terms": [
                {{"term": "term name", "value": "term value", "importance": "high/medium/low"}}
            ],
            "risks": [
                {{
                    "type": "risk category",
                    "severity": "low/medium/high/critical",
                    "description": "detailed description",
                    "recommendation": "how to address this risk",
                    "confidence": 0.85,
                    "location": "section/clause reference"
                }}
            ],
            "insights": [
                {{
                    "category": "insight category",
                    "title": "insight title",
                    "description": "detailed description",
                    "impact": "potential impact",
                    "recommendation": "recommended action"
                }}
            ],
            "compliance_score": 0.75,
            "overall_risk_score": 0.65,
            "negotiation_points": ["point 1", "point 2"],
            "missing_clauses": ["clause 1", "clause 2"],
            "improvements": ["improvement 1", "improvement 2"]
        }}
        """
        
        # Add specific analysis based on contract type
        if contract_type == "employment":
            base_prompt += """
            
            Focus on:
            - Compensation and benefits
            - Termination clauses
            - Non-compete and confidentiality
            - Intellectual property rights
            - Work conditions and expectations
            """
        elif contract_type == "nda":
            base_prompt += """
            
            Focus on:
            - Definition of confidential information
            - Permitted disclosures
            - Term and survival
            - Return of information
            - Remedies for breach
            """
        elif contract_type == "service":
            base_prompt += """
            
            Focus on:
            - Scope of services
            - Payment terms
            - Performance standards
            - Liability and indemnification
            - Termination conditions
            """
        
        # Add depth-specific instructions
        if analysis_depth == "deep":
            base_prompt += """
            
            Provide detailed clause-by-clause analysis with legal precedents where applicable.
            """
        elif analysis_depth == "compliance":
            base_prompt += """
            
            Focus heavily on regulatory compliance, industry standards, and legal requirements.
            """
        elif analysis_depth == "risk_assessment":
            base_prompt += """
            
            Prioritize risk identification and mitigation strategies.
            """
        
        return base_prompt
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API with the analysis prompt"""
        try:
            response = await openai.ChatCompletion.acreate(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert legal contract analyzer. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4000,
                temperature=0.1,
                timeout=60
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise AIAnalysisException(
                f"AI service unavailable: {str(e)}",
                status_code=503
            )
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate AI response"""
        try:
            # Extract JSON from response (in case there's extra text)
            start = response.find('{')
            end = response.rfind('}') + 1
            if start == -1 or end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[start:end]
            data = json.loads(json_str)
            
            # Validate and convert to proper types
            parsed_data = {
                "summary": data.get("summary", "Analysis completed"),
                "key_terms": data.get("key_terms", []),
                "risks": [
                    RiskItem(
                        type=risk.get("type", "Unknown"),
                        severity=RiskLevel(risk.get("severity", "medium")),
                        description=risk.get("description", ""),
                        recommendation=risk.get("recommendation", ""),
                        confidence=float(risk.get("confidence", 0.5)),
                        location=risk.get("location")
                    )
                    for risk in data.get("risks", [])
                ],
                "insights": [
                    Insight(
                        category=insight.get("category", "General"),
                        title=insight.get("title", ""),
                        description=insight.get("description", ""),
                        impact=insight.get("impact", ""),
                        recommendation=insight.get("recommendation", "")
                    )
                    for insight in data.get("insights", [])
                ],
                "compliance_score": float(data.get("compliance_score", 0.5)),
                "overall_risk_score": float(data.get("overall_risk_score", 0.5)),
                "negotiation_points": data.get("negotiation_points", []),
                "missing_clauses": data.get("missing_clauses", []),
                "improvements": data.get("improvements", [])
            }
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {str(e)}")
            # Return fallback analysis
            return self._create_fallback_analysis()
        except Exception as e:
            logger.error(f"Error parsing AI response: {str(e)}")
            return self._create_fallback_analysis()
    
    def _create_fallback_analysis(self) -> Dict[str, Any]:
        """Create fallback analysis when AI parsing fails"""
        return {
            "summary": "Contract analysis completed with limited AI processing",
            "key_terms": [],
            "risks": [
                RiskItem(
                    type="Analysis",
                    severity=RiskLevel.MEDIUM,
                    description="AI analysis was incomplete. Manual review recommended.",
                    recommendation="Have a legal professional review this contract",
                    confidence=0.5
                )
            ],
            "insights": [
                Insight(
                    category="System",
                    title="Limited Analysis",
                    description="Full AI analysis was not available",
                    impact="May miss important contract details",
                    recommendation="Consider manual legal review"
                )
            ],
            "compliance_score": 0.5,
            "overall_risk_score": 0.5,
            "negotiation_points": ["Consider professional legal review"],
            "missing_clauses": [],
            "improvements": ["Obtain comprehensive legal analysis"]
        }