"""
AI service for smart contract analysis using OpenAI and Anthropic.
"""
import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import structlog
import openai
import anthropic
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.contract import Contract
from app.models.finding import SecurityFinding
from app.models.risk import RiskAssessment
from app.core.websocket import websocket_manager

logger = structlog.get_logger()

# Initialize AI clients
openai.api_key = settings.OPENAI_API_KEY
anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)


class AIAnalysisService:
    """Service for AI-powered smart contract analysis."""
    
    def __init__(self):
        self.openai_model = "gpt-4-1106-preview"
        self.anthropic_model = "claude-3-sonnet-20240229"
        self.max_tokens = 4000
        self.temperature = 0.1  # Low temperature for consistent analysis
    
    async def analyze_contract(
        self, 
        db: AsyncSession, 
        contract: Contract,
        analysis_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive AI analysis of a smart contract.
        
        Args:
            db: Database session
            contract: Contract to analyze
            analysis_types: Types of analysis to perform
            
        Returns:
            Dict containing analysis results
        """
        if not analysis_types:
            analysis_types = ["security", "risk", "gas", "compliance"]
        
        logger.info(
            "Starting AI contract analysis",
            contract_id=contract.id,
            address=contract.address,
            analysis_types=analysis_types
        )
        
        try:
            # Update contract status
            contract.analysis_status = "analyzing"
            contract.analysis_started_at = datetime.utcnow()
            await db.commit()
            
            # Send progress update via WebSocket
            await websocket_manager.send_analysis_progress(
                contract.id,
                {"status": "analyzing", "progress": 0, "message": "Starting analysis..."}
            )
            
            # Perform different types of analysis
            results = {}
            total_steps = len(analysis_types)
            
            for i, analysis_type in enumerate(analysis_types):
                logger.info(f"Performing {analysis_type} analysis", contract_id=contract.id)
                
                # Send progress update
                progress = int((i / total_steps) * 100)
                await websocket_manager.send_analysis_progress(
                    contract.id,
                    {
                        "status": "analyzing", 
                        "progress": progress, 
                        "message": f"Analyzing {analysis_type}..."
                    }
                )
                
                if analysis_type == "security":
                    results["security"] = await self._analyze_security(contract)
                elif analysis_type == "risk":
                    results["risk"] = await self._analyze_risk(contract)
                elif analysis_type == "gas":
                    results["gas"] = await self._analyze_gas_optimization(contract)
                elif analysis_type == "compliance":
                    results["compliance"] = await self._analyze_compliance(contract)
            
            # Generate overall summary
            results["summary"] = await self._generate_summary(contract, results)
            
            # Calculate overall risk score
            risk_score = self._calculate_risk_score(results)
            results["risk_score"] = risk_score
            
            # Update contract with results
            contract.analysis_status = "completed"
            contract.analysis_completed_at = datetime.utcnow()
            contract.risk_score = risk_score
            contract.analysis_summary = results["summary"]
            
            if contract.analysis_started_at:
                duration = (contract.analysis_completed_at - contract.analysis_started_at).total_seconds()
                contract.analysis_duration = int(duration)
            
            await db.commit()
            
            # Send completion notification
            await websocket_manager.send_analysis_complete(
                contract.id,
                {
                    "status": "completed",
                    "progress": 100,
                    "risk_score": risk_score,
                    "summary": results["summary"],
                    "findings_count": len(results.get("security", {}).get("findings", [])),
                    "risks_count": len(results.get("risk", {}).get("risks", []))
                }
            )
            
            logger.info(
                "Contract analysis completed",
                contract_id=contract.id,
                risk_score=risk_score,
                duration=contract.analysis_duration
            )
            
            return results
            
        except Exception as e:
            logger.error("Contract analysis failed", error=str(e), contract_id=contract.id)
            
            # Update contract status to failed
            contract.analysis_status = "failed"
            contract.analysis_completed_at = datetime.utcnow()
            await db.commit()
            
            # Send failure notification
            await websocket_manager.send_analysis_progress(
                contract.id,
                {
                    "status": "failed",
                    "progress": 0,
                    "message": f"Analysis failed: {str(e)}"
                }
            )
            
            raise
    
    async def _analyze_security(self, contract: Contract) -> Dict[str, Any]:
        """Perform security analysis using AI."""
        prompt = self._build_security_analysis_prompt(contract)
        
        # Use both OpenAI and Anthropic for comprehensive analysis
        openai_result = await self._call_openai(prompt)
        anthropic_result = await self._call_anthropic(prompt)
        
        # Merge and deduplicate results
        findings = self._merge_security_findings(openai_result, anthropic_result)
        
        return {
            "findings": findings,
            "openai_analysis": openai_result,
            "anthropic_analysis": anthropic_result
        }
    
    async def _analyze_risk(self, contract: Contract) -> Dict[str, Any]:
        """Perform risk analysis using AI."""
        prompt = self._build_risk_analysis_prompt(contract)
        
        # Use Anthropic for detailed risk analysis
        result = await self._call_anthropic(prompt)
        
        # Extract structured risk data
        risks = self._extract_risk_assessments(result)
        
        return {
            "risks": risks,
            "analysis": result
        }
    
    async def _analyze_gas_optimization(self, contract: Contract) -> Dict[str, Any]:
        """Analyze gas usage and optimization opportunities."""
        prompt = self._build_gas_analysis_prompt(contract)
        
        result = await self._call_openai(prompt)
        optimizations = self._extract_gas_optimizations(result)
        
        return {
            "optimizations": optimizations,
            "analysis": result
        }
    
    async def _analyze_compliance(self, contract: Contract) -> Dict[str, Any]:
        """Analyze regulatory compliance and best practices."""
        prompt = self._build_compliance_analysis_prompt(contract)
        
        result = await self._call_anthropic(prompt)
        compliance_issues = self._extract_compliance_issues(result)
        
        return {
            "compliance_issues": compliance_issues,
            "analysis": result
        }
    
    async def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API with error handling and retries."""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = await openai.ChatCompletion.acreate(
                    model=self.openai_model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a world-class smart contract security expert. Analyze the provided contract and return detailed, actionable findings in JSON format."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                logger.warning(f"OpenAI API call failed (attempt {attempt + 1})", error=str(e))
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (2 ** attempt))
                else:
                    raise
    
    async def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API with error handling and retries."""
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = await anthropic_client.messages.create(
                    model=self.anthropic_model,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    system="You are a world-class smart contract security expert. Analyze the provided contract and return detailed, actionable findings in JSON format.",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return response.content[0].text
                
            except Exception as e:
                logger.warning(f"Anthropic API call failed (attempt {attempt + 1})", error=str(e))
                if attempt < max_retries - 1:
                    await asyncio.sleep(retry_delay * (2 ** attempt))
                else:
                    raise
    
    def _build_security_analysis_prompt(self, contract: Contract) -> str:
        """Build prompt for security analysis."""
        return f"""
Analyze this Solidity smart contract for security vulnerabilities:

Contract Address: {contract.address}
Chain ID: {contract.chain_id}
Contract Name: {contract.name or 'Unknown'}

Source Code:
```solidity
{contract.source_code}
```

Please provide a comprehensive security analysis in the following JSON format:
{{
    "findings": [
        {{
            "title": "Brief title of the issue",
            "description": "Detailed description of the vulnerability",
            "severity": "critical|high|medium|low",
            "category": "access-control|arithmetic|reentrancy|gas|other",
            "line_number": 123,
            "function_name": "functionName",
            "recommendation": "How to fix this issue",
            "confidence": 0.95
        }}
    ]
}}

Focus on:
1. Reentrancy attacks
2. Access control issues
3. Integer overflow/underflow
4. Unchecked external calls
5. Gas limit issues
6. Logic errors
7. Best practice violations

Be thorough and provide actionable recommendations.
"""
    
    def _build_risk_analysis_prompt(self, contract: Contract) -> str:
        """Build prompt for risk analysis."""
        return f"""
Perform a comprehensive risk assessment for this smart contract:

Contract Address: {contract.address}
Chain ID: {contract.chain_id}
Contract Name: {contract.name or 'Unknown'}

Source Code:
```solidity
{contract.source_code}
```

Please provide a risk analysis in the following JSON format:
{{
    "risks": [
        {{
            "title": "Risk title",
            "description": "Detailed risk description",
            "category": "financial|operational|technical|regulatory",
            "risk_level": "critical|high|medium|low",
            "probability": 0.8,
            "impact": "Potential impact description",
            "mitigation": "Risk mitigation strategies"
        }}
    ]
}}

Analyze risks in these categories:
1. Financial risks (fund loss, economic attacks)
2. Operational risks (governance, upgrade risks)
3. Technical risks (bugs, dependency risks)
4. Regulatory risks (compliance issues)

Consider both current risks and potential future risks.
"""
    
    def _build_gas_analysis_prompt(self, contract: Contract) -> str:
        """Build prompt for gas optimization analysis."""
        return f"""
Analyze this smart contract for gas optimization opportunities:

Contract Address: {contract.address}
Source Code:
```solidity
{contract.source_code}
```

Provide gas optimization recommendations in JSON format:
{{
    "optimizations": [
        {{
            "title": "Optimization title",
            "description": "What can be optimized",
            "potential_savings": "High|Medium|Low",
            "implementation": "How to implement the optimization",
            "line_number": 123
        }}
    ]
}}

Focus on:
1. Storage optimization
2. Loop optimization
3. Function visibility
4. Data types optimization
5. Redundant operations
6. Batch operations
"""
    
    def _build_compliance_analysis_prompt(self, contract: Contract) -> str:
        """Build prompt for compliance analysis."""
        return f"""
Analyze this smart contract for regulatory compliance and best practices:

Contract Address: {contract.address}
Source Code:
```solidity
{contract.source_code}
```

Provide compliance analysis in JSON format:
{{
    "compliance_issues": [
        {{
            "title": "Compliance issue",
            "description": "Description of the issue",
            "severity": "high|medium|low",
            "regulation": "Which regulation/standard",
            "recommendation": "How to address the issue"
        }}
    ]
}}

Check for:
1. ERC standard compliance
2. Security best practices
3. Documentation requirements
4. Access control standards
5. Event logging requirements
6. Upgrade patterns
"""
    
    def _merge_security_findings(self, openai_result: str, anthropic_result: str) -> List[Dict[str, Any]]:
        """Merge and deduplicate security findings from both AI providers."""
        findings = []
        
        try:
            # Parse OpenAI results
            openai_data = json.loads(openai_result)
            if "findings" in openai_data:
                for finding in openai_data["findings"]:
                    finding["source"] = "openai"
                    findings.append(finding)
        except json.JSONDecodeError:
            logger.warning("Failed to parse OpenAI security analysis result")
        
        try:
            # Parse Anthropic results
            anthropic_data = json.loads(anthropic_result)
            if "findings" in anthropic_data:
                for finding in anthropic_data["findings"]:
                    finding["source"] = "anthropic"
                    findings.append(finding)
        except json.JSONDecodeError:
            logger.warning("Failed to parse Anthropic security analysis result")
        
        # TODO: Implement deduplication logic based on similarity
        return findings
    
    def _extract_risk_assessments(self, result: str) -> List[Dict[str, Any]]:
        """Extract risk assessments from AI result."""
        try:
            data = json.loads(result)
            return data.get("risks", [])
        except json.JSONDecodeError:
            logger.warning("Failed to parse risk analysis result")
            return []
    
    def _extract_gas_optimizations(self, result: str) -> List[Dict[str, Any]]:
        """Extract gas optimizations from AI result."""
        try:
            data = json.loads(result)
            return data.get("optimizations", [])
        except json.JSONDecodeError:
            logger.warning("Failed to parse gas analysis result")
            return []
    
    def _extract_compliance_issues(self, result: str) -> List[Dict[str, Any]]:
        """Extract compliance issues from AI result."""
        try:
            data = json.loads(result)
            return data.get("compliance_issues", [])
        except json.JSONDecodeError:
            logger.warning("Failed to parse compliance analysis result")
            return []
    
    async def _generate_summary(self, contract: Contract, results: Dict[str, Any]) -> str:
        """Generate overall analysis summary."""
        findings_count = len(results.get("security", {}).get("findings", []))
        risks_count = len(results.get("risk", {}).get("risks", []))
        
        critical_findings = sum(
            1 for f in results.get("security", {}).get("findings", [])
            if f.get("severity") == "critical"
        )
        
        high_risks = sum(
            1 for r in results.get("risk", {}).get("risks", [])
            if r.get("risk_level") == "high"
        )
        
        summary_parts = []
        
        if critical_findings > 0:
            summary_parts.append(f"{critical_findings} critical security issues found")
        
        if high_risks > 0:
            summary_parts.append(f"{high_risks} high-risk issues identified")
        
        summary_parts.append(f"{findings_count} total findings")
        summary_parts.append(f"{risks_count} risk assessments")
        
        return ". ".join(summary_parts) + "."
    
    def _calculate_risk_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall risk score (0.0 to 1.0)."""
        base_score = 0.0
        
        # Security findings impact
        findings = results.get("security", {}).get("findings", [])
        for finding in findings:
            severity = finding.get("severity", "low")
            if severity == "critical":
                base_score += 0.3
            elif severity == "high":
                base_score += 0.2
            elif severity == "medium":
                base_score += 0.1
            elif severity == "low":
                base_score += 0.05
        
        # Risk assessments impact
        risks = results.get("risk", {}).get("risks", [])
        for risk in risks:
            risk_level = risk.get("risk_level", "low")
            probability = risk.get("probability", 0.5)
            
            if risk_level == "critical":
                base_score += 0.25 * probability
            elif risk_level == "high":
                base_score += 0.15 * probability
            elif risk_level == "medium":
                base_score += 0.08 * probability
            elif risk_level == "low":
                base_score += 0.03 * probability
        
        # Cap at 1.0
        return min(base_score, 1.0)


# Global AI service instance
ai_service = AIAnalysisService()
