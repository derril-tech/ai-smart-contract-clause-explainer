"""
Analysis service for orchestrating smart contract security analysis.
"""
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import structlog

from app.models.contract import Contract
from app.models.finding import SecurityFinding
from app.models.risk import RiskAssessment
from app.services.ai_service import ai_service
from app.services.static_analysis_service import static_analysis_service
from app.core.websocket import websocket_manager

logger = structlog.get_logger()


class AnalysisService:
    """Service for orchestrating comprehensive smart contract analysis."""
    
    async def analyze_contract_comprehensive(
        self,
        db: AsyncSession,
        contract: Contract,
        analysis_types: List[str] = None,
        use_ai: bool = True,
        use_static_analysis: bool = True
    ) -> Dict[str, Any]:
        """
        Perform comprehensive analysis combining AI and static analysis tools.
        
        Args:
            db: Database session
            contract: Contract to analyze
            analysis_types: Types of analysis to perform
            use_ai: Whether to use AI analysis
            use_static_analysis: Whether to use static analysis tools
            
        Returns:
            Combined analysis results
        """
        logger.info(
            "Starting comprehensive contract analysis",
            contract_id=contract.id,
            address=contract.address,
            use_ai=use_ai,
            use_static_analysis=use_static_analysis
        )
        
        if not analysis_types:
            analysis_types = ["security", "risk", "gas", "compliance"]
        
        try:
            # Update contract status
            contract.analysis_status = "analyzing"
            contract.analysis_started_at = datetime.utcnow()
            await db.commit()
            
            # Send initial progress update
            await websocket_manager.send_analysis_progress(
                contract.id,
                {
                    "status": "analyzing",
                    "progress": 0,
                    "message": "Initializing comprehensive analysis..."
                }
            )
            
            results = {}
            
            # Run static analysis and AI analysis in parallel
            tasks = []
            
            if use_static_analysis:
                tasks.append(self._run_static_analysis(contract, analysis_types))
            
            if use_ai:
                tasks.append(self._run_ai_analysis(db, contract, analysis_types))
            
            # Wait for both analyses to complete
            analysis_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            static_results = None
            ai_results = None
            
            if use_static_analysis and len(analysis_results) > 0:
                if isinstance(analysis_results[0], Exception):
                    logger.error("Static analysis failed", error=str(analysis_results[0]))
                else:
                    static_results = analysis_results[0]
            
            if use_ai:
                ai_index = 1 if use_static_analysis else 0
                if len(analysis_results) > ai_index:
                    if isinstance(analysis_results[ai_index], Exception):
                        logger.error("AI analysis failed", error=str(analysis_results[ai_index]))
                    else:
                        ai_results = analysis_results[ai_index]
            
            # Merge results
            results = self._merge_analysis_results(static_results, ai_results)
            
            # Save findings and risks to database
            await self._save_analysis_results(db, contract, results)
            
            # Calculate final risk score
            risk_score = self._calculate_combined_risk_score(results)
            
            # Update contract with final results
            contract.analysis_status = "completed"
            contract.analysis_completed_at = datetime.utcnow()
            contract.risk_score = risk_score
            contract.analysis_summary = self._generate_analysis_summary(results)
            
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
                    "summary": contract.analysis_summary,
                    "findings_count": len(results.get("findings", [])),
                    "risks_count": len(results.get("risks", [])),
                    "duration": contract.analysis_duration
                }
            )
            
            logger.info(
                "Comprehensive analysis completed",
                contract_id=contract.id,
                risk_score=risk_score,
                findings_count=len(results.get("findings", [])),
                risks_count=len(results.get("risks", [])),
                duration=contract.analysis_duration
            )
            
            return results
            
        except Exception as e:
            logger.error("Comprehensive analysis failed", error=str(e), contract_id=contract.id)
            
            # Update contract status
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
    
    async def _run_static_analysis(
        self,
        contract: Contract,
        analysis_types: List[str]
    ) -> Dict[str, Any]:
        """Run static analysis tools."""
        await websocket_manager.send_analysis_progress(
            contract.id,
            {
                "status": "analyzing",
                "progress": 25,
                "message": "Running static analysis tools..."
            }
        )
        
        return await static_analysis_service.analyze_contract(contract, analysis_types)
    
    async def _run_ai_analysis(
        self,
        db: AsyncSession,
        contract: Contract,
        analysis_types: List[str]
    ) -> Dict[str, Any]:
        """Run AI analysis."""
        await websocket_manager.send_analysis_progress(
            contract.id,
            {
                "status": "analyzing",
                "progress": 50,
                "message": "Running AI analysis..."
            }
        )
        
        return await ai_service.analyze_contract(db, contract, analysis_types)
    
    def _merge_analysis_results(
        self,
        static_results: Optional[Dict[str, Any]],
        ai_results: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Merge static analysis and AI analysis results."""
        merged_results = {
            "findings": [],
            "risks": [],
            "gas_optimizations": [],
            "compliance_issues": [],
            "static_analysis": static_results,
            "ai_analysis": ai_results
        }
        
        # Merge findings
        if static_results and "security" in static_results:
            static_findings = static_results["security"].get("findings", [])
            for finding in static_findings:
                finding["source"] = "static_analysis"
                merged_results["findings"].append(finding)
        
        if ai_results and "security" in ai_results:
            ai_findings = ai_results["security"].get("findings", [])
            for finding in ai_findings:
                if "source" not in finding:
                    finding["source"] = "ai_analysis"
                merged_results["findings"].append(finding)
        
        # Merge risks
        if static_results and "risk" in static_results:
            static_risks = static_results["risk"].get("risks", [])
            for risk in static_risks:
                risk["source"] = "static_analysis"
                merged_results["risks"].append(risk)
        
        if ai_results and "risk" in ai_results:
            ai_risks = ai_results["risk"].get("risks", [])
            for risk in ai_risks:
                if "source" not in risk:
                    risk["source"] = "ai_analysis"
                merged_results["risks"].append(risk)
        
        # Merge gas optimizations
        if static_results and "gas" in static_results:
            static_gas = static_results["gas"].get("optimizations", [])
            merged_results["gas_optimizations"].extend(static_gas)
        
        if ai_results and "gas" in ai_results:
            ai_gas = ai_results["gas"].get("optimizations", [])
            merged_results["gas_optimizations"].extend(ai_gas)
        
        # Merge compliance issues
        if static_results and "compliance" in static_results:
            static_compliance = static_results["compliance"].get("compliance_issues", [])
            merged_results["compliance_issues"].extend(static_compliance)
        
        if ai_results and "compliance" in ai_results:
            ai_compliance = ai_results["compliance"].get("compliance_issues", [])
            merged_results["compliance_issues"].extend(ai_compliance)
        
        # Deduplicate similar findings
        merged_results["findings"] = self._deduplicate_findings(merged_results["findings"])
        merged_results["risks"] = self._deduplicate_risks(merged_results["risks"])
        
        return merged_results
    
    async def _save_analysis_results(
        self,
        db: AsyncSession,
        contract: Contract,
        results: Dict[str, Any]
    ) -> None:
        """Save analysis results to database."""
        # Save security findings
        for finding_data in results.get("findings", []):
            finding = SecurityFinding(
                contract_id=contract.id,
                title=finding_data.get("title", "Unknown Issue"),
                description=finding_data.get("description", ""),
                recommendation=finding_data.get("recommendation", ""),
                severity=finding_data.get("severity", "low"),
                category=finding_data.get("category", "other"),
                line_number=finding_data.get("line_number"),
                function_name=finding_data.get("function_name"),
                file_name=finding_data.get("file_name"),
                tool=finding_data.get("source", "unknown"),
                confidence=finding_data.get("confidence"),
                metadata=finding_data
            )
            db.add(finding)
        
        # Save risk assessments
        for risk_data in results.get("risks", []):
            risk = RiskAssessment(
                contract_id=contract.id,
                title=risk_data.get("title", "Unknown Risk"),
                description=risk_data.get("description", ""),
                impact=risk_data.get("impact", ""),
                mitigation=risk_data.get("mitigation", ""),
                risk_level=risk_data.get("risk_level", "low"),
                category=risk_data.get("category", "technical"),
                probability=risk_data.get("probability", 0.5),
                impact_score=risk_data.get("impact_score"),
                risk_score=risk_data.get("risk_score"),
                metadata=risk_data
            )
            db.add(risk)
        
        await db.commit()
    
    def _deduplicate_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate findings based on similarity."""
        # Simple deduplication based on title and line number
        # TODO: Implement more sophisticated similarity matching
        seen = set()
        deduplicated = []
        
        for finding in findings:
            key = (
                finding.get("title", "").lower(),
                finding.get("line_number"),
                finding.get("severity")
            )
            
            if key not in seen:
                seen.add(key)
                deduplicated.append(finding)
        
        return deduplicated
    
    def _deduplicate_risks(self, risks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate risks based on similarity."""
        # Simple deduplication based on title and category
        seen = set()
        deduplicated = []
        
        for risk in risks:
            key = (
                risk.get("title", "").lower(),
                risk.get("category"),
                risk.get("risk_level")
            )
            
            if key not in seen:
                seen.add(key)
                deduplicated.append(risk)
        
        return deduplicated
    
    def _calculate_combined_risk_score(self, results: Dict[str, Any]) -> float:
        """Calculate combined risk score from all analysis results."""
        base_score = 0.0
        
        # Security findings impact
        findings = results.get("findings", [])
        for finding in findings:
            severity = finding.get("severity", "low")
            confidence = finding.get("confidence", 0.5)
            
            severity_weight = {
                "critical": 0.4,
                "high": 0.3,
                "medium": 0.15,
                "low": 0.05
            }.get(severity, 0.05)
            
            base_score += severity_weight * confidence
        
        # Risk assessments impact
        risks = results.get("risks", [])
        for risk in risks:
            risk_level = risk.get("risk_level", "low")
            probability = risk.get("probability", 0.5)
            
            risk_weight = {
                "critical": 0.35,
                "high": 0.25,
                "medium": 0.12,
                "low": 0.03
            }.get(risk_level, 0.03)
            
            base_score += risk_weight * probability
        
        # Gas optimization impact (minor)
        gas_optimizations = results.get("gas_optimizations", [])
        base_score += len(gas_optimizations) * 0.01
        
        # Compliance issues impact
        compliance_issues = results.get("compliance_issues", [])
        for issue in compliance_issues:
            severity = issue.get("severity", "low")
            severity_weight = {
                "high": 0.1,
                "medium": 0.05,
                "low": 0.02
            }.get(severity, 0.02)
            
            base_score += severity_weight
        
        # Cap at 1.0
        return min(base_score, 1.0)
    
    def _generate_analysis_summary(self, results: Dict[str, Any]) -> str:
        """Generate comprehensive analysis summary."""
        findings = results.get("findings", [])
        risks = results.get("risks", [])
        gas_optimizations = results.get("gas_optimizations", [])
        compliance_issues = results.get("compliance_issues", [])
        
        # Count by severity
        critical_findings = sum(1 for f in findings if f.get("severity") == "critical")
        high_findings = sum(1 for f in findings if f.get("severity") == "high")
        medium_findings = sum(1 for f in findings if f.get("severity") == "medium")
        low_findings = sum(1 for f in findings if f.get("severity") == "low")
        
        critical_risks = sum(1 for r in risks if r.get("risk_level") == "critical")
        high_risks = sum(1 for r in risks if r.get("risk_level") == "high")
        
        summary_parts = []
        
        # Security findings summary
        if critical_findings > 0:
            summary_parts.append(f"{critical_findings} critical security issues")
        if high_findings > 0:
            summary_parts.append(f"{high_findings} high-severity issues")
        if medium_findings > 0:
            summary_parts.append(f"{medium_findings} medium-severity issues")
        if low_findings > 0:
            summary_parts.append(f"{low_findings} low-severity issues")
        
        # Risk summary
        if critical_risks > 0:
            summary_parts.append(f"{critical_risks} critical risks")
        if high_risks > 0:
            summary_parts.append(f"{high_risks} high-level risks")
        
        # Additional analysis
        if gas_optimizations:
            summary_parts.append(f"{len(gas_optimizations)} gas optimization opportunities")
        
        if compliance_issues:
            summary_parts.append(f"{len(compliance_issues)} compliance issues")
        
        if not summary_parts:
            return "No significant security issues or risks identified"
        
        return ". ".join(summary_parts) + "."
    
    async def get_analysis_results(
        self,
        db: AsyncSession,
        contract_id: str
    ) -> Dict[str, Any]:
        """Get comprehensive analysis results for a contract."""
        contract = await db.get(Contract, contract_id)
        if not contract:
            raise ValueError("Contract not found")
        
        # Get findings and risks
        findings_result = await db.execute(
            "SELECT * FROM security_findings WHERE contract_id = :contract_id ORDER BY severity_score DESC",
            {"contract_id": contract_id}
        )
        findings = [dict(row) for row in findings_result.fetchall()]
        
        risks_result = await db.execute(
            "SELECT * FROM risk_assessments WHERE contract_id = :contract_id ORDER BY risk_level_score DESC",
            {"contract_id": contract_id}
        )
        risks = [dict(row) for row in risks_result.fetchall()]
        
        return {
            "contract": contract.to_dict(),
            "findings": findings,
            "risks": risks,
            "summary": {
                "total_findings": len(findings),
                "total_risks": len(risks),
                "risk_score": contract.risk_score,
                "analysis_duration": contract.analysis_duration,
                "status": contract.analysis_status
            }
        }


# Global analysis service instance
analysis_service = AnalysisService()
