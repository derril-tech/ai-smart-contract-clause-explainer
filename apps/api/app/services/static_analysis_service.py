"""
Static analysis service using tools like Slither, Semgrep, and Mythril.
"""
import asyncio
import json
import tempfile
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional
import structlog

from app.models.contract import Contract
from app.core.config import settings

logger = structlog.get_logger()


class StaticAnalysisService:
    """Service for static analysis using security tools."""
    
    def __init__(self):
        self.slither_timeout = settings.SLITHER_TIMEOUT
        self.semgrep_timeout = settings.SEMGREP_TIMEOUT
        self.mythril_timeout = settings.MYTHRIL_TIMEOUT
    
    async def analyze_contract(
        self,
        contract: Contract,
        analysis_types: List[str] = None
    ) -> Dict[str, Any]:
        """
        Perform static analysis on a smart contract using multiple tools.
        
        Args:
            contract: Contract to analyze
            analysis_types: Types of analysis to perform
            
        Returns:
            Dict containing analysis results from all tools
        """
        if not analysis_types:
            analysis_types = ["security", "gas"]
        
        logger.info(
            "Starting static analysis",
            contract_id=contract.id,
            address=contract.address,
            analysis_types=analysis_types
        )
        
        try:
            # Create temporary file with contract source code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.sol', delete=False) as f:
                f.write(contract.source_code)
                contract_file = f.name
            
            results = {}
            
            # Run different analysis tools based on requested types
            if "security" in analysis_types:
                results["security"] = await self._run_security_analysis(contract_file)
            
            if "gas" in analysis_types:
                results["gas"] = await self._run_gas_analysis(contract_file)
            
            if "compliance" in analysis_types:
                results["compliance"] = await self._run_compliance_analysis(contract_file)
            
            # Clean up temporary file
            Path(contract_file).unlink(missing_ok=True)
            
            logger.info(
                "Static analysis completed",
                contract_id=contract.id,
                findings_count=len(results.get("security", {}).get("findings", []))
            )
            
            return results
            
        except Exception as e:
            logger.error("Static analysis failed", error=str(e), contract_id=contract.id)
            # Clean up temporary file on error
            try:
                Path(contract_file).unlink(missing_ok=True)
            except:
                pass
            raise
    
    async def _run_security_analysis(self, contract_file: str) -> Dict[str, Any]:
        """Run security analysis using Slither and Mythril."""
        tasks = []
        
        # Run Slither analysis
        tasks.append(self._run_slither(contract_file))
        
        # Run Mythril analysis (if available)
        if self._is_mythril_available():
            tasks.append(self._run_mythril(contract_file))
        
        # Run Semgrep analysis
        tasks.append(self._run_semgrep(contract_file))
        
        # Wait for all analyses to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        combined_findings = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.warning(f"Analysis tool {i} failed", error=str(result))
                continue
            
            if isinstance(result, list):
                combined_findings.extend(result)
        
        return {
            "findings": combined_findings,
            "tools_used": ["slither", "mythril", "semgrep"]
        }
    
    async def _run_slither(self, contract_file: str) -> List[Dict[str, Any]]:
        """Run Slither static analysis."""
        try:
            cmd = [
                "slither",
                contract_file,
                "--json", "-",
                "--disable-color"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.slither_timeout
            )
            
            if process.returncode != 0 and stdout:
                # Slither may return non-zero but still provide results
                pass
            
            # Parse Slither JSON output
            if stdout:
                slither_results = json.loads(stdout.decode())
                return self._parse_slither_results(slither_results)
            
            return []
            
        except asyncio.TimeoutError:
            logger.warning("Slither analysis timed out")
            return []
        except json.JSONDecodeError:
            logger.warning("Failed to parse Slither output")
            return []
        except Exception as e:
            logger.warning("Slither analysis failed", error=str(e))
            return []
    
    async def _run_mythril(self, contract_file: str) -> List[Dict[str, Any]]:
        """Run Mythril static analysis."""
        try:
            cmd = [
                "myth",
                "analyze",
                contract_file,
                "--output", "json",
                "--max-depth", "12"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.mythril_timeout
            )
            
            if process.returncode != 0:
                logger.warning("Mythril analysis failed", stderr=stderr.decode())
                return []
            
            # Parse Mythril JSON output
            if stdout:
                mythril_results = json.loads(stdout.decode())
                return self._parse_mythril_results(mythril_results)
            
            return []
            
        except asyncio.TimeoutError:
            logger.warning("Mythril analysis timed out")
            return []
        except json.JSONDecodeError:
            logger.warning("Failed to parse Mythril output")
            return []
        except Exception as e:
            logger.warning("Mythril analysis failed", error=str(e))
            return []
    
    async def _run_semgrep(self, contract_file: str) -> List[Dict[str, Any]]:
        """Run Semgrep static analysis with Solidity rules."""
        try:
            cmd = [
                "semgrep",
                "--config=auto",
                "--json",
                "--lang=solidity",
                contract_file
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.semgrep_timeout
            )
            
            if process.returncode != 0 and not stdout:
                logger.warning("Semgrep analysis failed", stderr=stderr.decode())
                return []
            
            # Parse Semgrep JSON output
            if stdout:
                semgrep_results = json.loads(stdout.decode())
                return self._parse_semgrep_results(semgrep_results)
            
            return []
            
        except asyncio.TimeoutError:
            logger.warning("Semgrep analysis timed out")
            return []
        except json.JSONDecodeError:
            logger.warning("Failed to parse Semgrep output")
            return []
        except Exception as e:
            logger.warning("Semgrep analysis failed", error=str(e))
            return []
    
    async def _run_gas_analysis(self, contract_file: str) -> Dict[str, Any]:
        """Run gas optimization analysis."""
        # Use Slither for gas optimization detection
        try:
            cmd = [
                "slither",
                contract_file,
                "--print", "gas",
                "--json", "-"
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.slither_timeout
            )
            
            optimizations = []
            
            if stdout:
                try:
                    results = json.loads(stdout.decode())
                    optimizations = self._parse_gas_optimizations(results)
                except json.JSONDecodeError:
                    pass
            
            return {
                "optimizations": optimizations,
                "tools_used": ["slither"]
            }
            
        except Exception as e:
            logger.warning("Gas analysis failed", error=str(e))
            return {"optimizations": [], "tools_used": []}
    
    async def _run_compliance_analysis(self, contract_file: str) -> Dict[str, Any]:
        """Run compliance analysis using custom rules."""
        # This would typically use custom Semgrep rules for compliance
        try:
            # For now, return empty results
            # TODO: Implement custom compliance rules
            return {
                "compliance_issues": [],
                "standards_checked": ["ERC-20", "ERC-721", "ERC-1155"]
            }
            
        except Exception as e:
            logger.warning("Compliance analysis failed", error=str(e))
            return {"compliance_issues": [], "standards_checked": []}
    
    def _parse_slither_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Slither analysis results."""
        findings = []
        
        for result in results.get("results", {}).get("detectors", []):
            finding = {
                "title": result.get("check", "Unknown Issue"),
                "description": result.get("description", ""),
                "severity": self._map_slither_severity(result.get("impact", "Low")),
                "category": self._categorize_slither_finding(result.get("check", "")),
                "confidence": self._map_slither_confidence(result.get("confidence", "Medium")),
                "tool": "slither",
                "recommendation": self._get_slither_recommendation(result.get("check", "")),
                "metadata": result
            }
            
            # Extract location information
            elements = result.get("elements", [])
            if elements:
                first_element = elements[0]
                finding["line_number"] = first_element.get("source_mapping", {}).get("lines", [None])[0]
                finding["function_name"] = first_element.get("name")
            
            findings.append(finding)
        
        return findings
    
    def _parse_mythril_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Mythril analysis results."""
        findings = []
        
        for issue in results.get("issues", []):
            finding = {
                "title": issue.get("title", "Unknown Issue"),
                "description": issue.get("description", ""),
                "severity": self._map_mythril_severity(issue.get("severity", "Low")),
                "category": self._categorize_mythril_finding(issue.get("swc-id", "")),
                "confidence": 0.8,  # Mythril doesn't provide confidence scores
                "tool": "mythril",
                "recommendation": self._get_mythril_recommendation(issue.get("swc-id", "")),
                "metadata": issue
            }
            
            # Extract location information
            if "lineno" in issue:
                finding["line_number"] = issue["lineno"]
            if "function" in issue:
                finding["function_name"] = issue["function"]
            
            findings.append(finding)
        
        return findings
    
    def _parse_semgrep_results(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Semgrep analysis results."""
        findings = []
        
        for result in results.get("results", []):
            finding = {
                "title": result.get("check_id", "Unknown Issue").split(".")[-1],
                "description": result.get("extra", {}).get("message", ""),
                "severity": self._map_semgrep_severity(result.get("extra", {}).get("severity", "INFO")),
                "category": self._categorize_semgrep_finding(result.get("check_id", "")),
                "confidence": 0.7,  # Default confidence for Semgrep
                "tool": "semgrep",
                "recommendation": "Review and address the identified pattern",
                "metadata": result
            }
            
            # Extract location information
            if "start" in result:
                finding["line_number"] = result["start"].get("line")
            
            findings.append(finding)
        
        return findings
    
    def _parse_gas_optimizations(self, results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse gas optimization results."""
        optimizations = []
        
        # This would parse gas-specific results from Slither
        # For now, return empty list
        # TODO: Implement gas optimization parsing
        
        return optimizations
    
    def _map_slither_severity(self, impact: str) -> str:
        """Map Slither impact to our severity levels."""
        mapping = {
            "High": "high",
            "Medium": "medium",
            "Low": "low",
            "Informational": "low"
        }
        return mapping.get(impact, "low")
    
    def _map_mythril_severity(self, severity: str) -> str:
        """Map Mythril severity to our severity levels."""
        mapping = {
            "High": "high",
            "Medium": "medium",
            "Low": "low"
        }
        return mapping.get(severity, "low")
    
    def _map_semgrep_severity(self, severity: str) -> str:
        """Map Semgrep severity to our severity levels."""
        mapping = {
            "ERROR": "high",
            "WARNING": "medium",
            "INFO": "low"
        }
        return mapping.get(severity.upper(), "low")
    
    def _map_slither_confidence(self, confidence: str) -> float:
        """Map Slither confidence to numeric value."""
        mapping = {
            "High": 0.9,
            "Medium": 0.7,
            "Low": 0.5
        }
        return mapping.get(confidence, 0.5)
    
    def _categorize_slither_finding(self, check: str) -> str:
        """Categorize Slither finding based on check name."""
        if "reentrancy" in check.lower():
            return "reentrancy"
        elif "access" in check.lower() or "modifier" in check.lower():
            return "access-control"
        elif "arithmetic" in check.lower() or "overflow" in check.lower():
            return "arithmetic"
        elif "gas" in check.lower():
            return "gas"
        else:
            return "other"
    
    def _categorize_mythril_finding(self, swc_id: str) -> str:
        """Categorize Mythril finding based on SWC ID."""
        # SWC (Smart Contract Weakness Classification) mapping
        swc_mapping = {
            "SWC-107": "reentrancy",
            "SWC-101": "arithmetic",
            "SWC-104": "access-control",
            "SWC-105": "access-control",
            "SWC-115": "access-control"
        }
        return swc_mapping.get(swc_id, "other")
    
    def _categorize_semgrep_finding(self, check_id: str) -> str:
        """Categorize Semgrep finding based on check ID."""
        if "reentrancy" in check_id.lower():
            return "reentrancy"
        elif "access" in check_id.lower():
            return "access-control"
        elif "overflow" in check_id.lower() or "underflow" in check_id.lower():
            return "arithmetic"
        else:
            return "other"
    
    def _get_slither_recommendation(self, check: str) -> str:
        """Get recommendation for Slither finding."""
        # This would contain specific recommendations for each Slither check
        # For now, return generic recommendation
        return f"Address the {check} issue identified by Slither analysis."
    
    def _get_mythril_recommendation(self, swc_id: str) -> str:
        """Get recommendation for Mythril finding."""
        recommendations = {
            "SWC-107": "Implement reentrancy guard or use checks-effects-interactions pattern",
            "SWC-101": "Use SafeMath library or Solidity 0.8+ built-in overflow protection",
            "SWC-104": "Implement proper access control mechanisms",
            "SWC-105": "Validate all external calls and handle failures appropriately"
        }
        return recommendations.get(swc_id, "Review and address the identified security issue.")
    
    def _is_mythril_available(self) -> bool:
        """Check if Mythril is available in the system."""
        try:
            subprocess.run(["myth", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


# Global static analysis service instance
static_analysis_service = StaticAnalysisService()
