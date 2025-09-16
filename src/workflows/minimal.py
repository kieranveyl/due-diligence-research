"""
Minimal Due Diligence Workflow

A simplified workflow implementation that works without external APIs for demo mode.
Provides realistic sample analysis while the full system is being built.
"""

import asyncio
import random
from collections.abc import AsyncGenerator
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DemoAgent:
    """Simple demo agent that generates realistic sample data"""
    name: str
    emoji: str

    async def analyze(self, entity_name: str, entity_type: str) -> dict[str, Any]:
        """Generate sample analysis for this agent"""
        # Simulate processing time
        await asyncio.sleep(random.uniform(0.5, 2.0))

        if self.name == "financial":
            return await self._financial_analysis(entity_name, entity_type)
        elif self.name == "legal":
            return await self._legal_analysis(entity_name, entity_type)
        elif self.name == "osint":
            return await self._osint_analysis(entity_name, entity_type)
        elif self.name == "verification":
            return await self._verification_analysis(entity_name, entity_type)
        else:
            return await self._general_analysis(entity_name, entity_type)

    async def _financial_analysis(self, entity_name: str, entity_type: str) -> dict[str, Any]:
        """Generate financial analysis sample data"""
        if entity_type == "company":
            return {
                "summary": f"Financial analysis completed for {entity_name}",
                "key_findings": [
                    f"{entity_name} shows stable revenue growth patterns",
                    "Market capitalization within industry averages",
                    "Debt-to-equity ratio appears manageable",
                    "Cash flow analysis indicates operational efficiency"
                ],
                "financial_health": "Good",
                "risk_level": "Medium",
                "confidence": random.uniform(0.75, 0.95),
                "metrics": {
                    "revenue_growth": "8.5% YoY",
                    "profit_margin": "12.3%",
                    "debt_ratio": "0.35",
                    "current_ratio": "1.8"
                },
                "red_flags": [],
                "recommendations": [
                    "Monitor quarterly earnings reports",
                    "Track industry performance comparisons"
                ]
            }
        else:
            return {
                "summary": f"Personal financial background check for {entity_name}",
                "key_findings": [
                    "No significant financial irregularities detected",
                    "Professional compensation appears consistent with role"
                ],
                "confidence": random.uniform(0.6, 0.8),
                "recommendations": ["Standard financial monitoring procedures"]
            }

    async def _legal_analysis(self, entity_name: str, entity_type: str) -> dict[str, Any]:
        """Generate legal analysis sample data"""
        return {
            "summary": f"Legal compliance review completed for {entity_name}",
            "key_findings": [
                "No major litigation currently pending",
                "Regulatory compliance status appears satisfactory",
                f"{entity_name} maintains good legal standing",
                "No sanctions or watch list matches found"
            ],
            "compliance_status": "Compliant",
            "litigation_risk": "Low",
            "confidence": random.uniform(0.8, 0.95),
            "active_cases": 0,
            "regulatory_issues": [],
            "sanctions_status": "Clear",
            "recommendations": [
                "Continue monitoring regulatory changes",
                "Maintain compliance documentation"
            ]
        }

    async def _osint_analysis(self, entity_name: str, entity_type: str) -> dict[str, Any]:
        """Generate OSINT analysis sample data"""
        return {
            "summary": f"Digital footprint analysis for {entity_name}",
            "key_findings": [
                f"{entity_name} maintains professional online presence",
                "Social media activity appears consistent and appropriate",
                "No concerning digital security issues identified",
                "Online reputation is generally positive"
            ],
            "digital_presence": "Professional",
            "reputation_score": "Positive",
            "confidence": random.uniform(0.7, 0.9),
            "social_platforms": ["LinkedIn", "Twitter", "Company Website"],
            "security_indicators": {
                "data_breaches": 0,
                "exposed_credentials": 0,
                "security_rating": "Good"
            },
            "recommendations": [
                "Regular digital presence monitoring",
                "Maintain professional online standards"
            ]
        }

    async def _verification_analysis(self, entity_name: str, entity_type: str) -> dict[str, Any]:
        """Generate verification analysis sample data"""
        return {
            "summary": f"Information verification completed for {entity_name}",
            "key_findings": [
                "Core business information verified through multiple sources",
                "Registration and incorporation details confirmed",
                f"{entity_name} identity and credentials validated",
                "No significant discrepancies found in public records"
            ],
            "verification_rate": "95%",
            "source_reliability": "High",
            "confidence": random.uniform(0.85, 0.98),
            "verified_facts": [
                "Business registration status",
                "Corporate address verification",
                "Key personnel identification",
                "Industry classification"
            ],
            "unverified_items": [],
            "recommendations": [
                "Periodic re-verification of key facts",
                "Monitor for any material changes"
            ]
        }

    async def _general_analysis(self, entity_name: str, entity_type: str) -> dict[str, Any]:
        """Generate general analysis sample data"""
        return {
            "summary": f"General research analysis for {entity_name}",
            "key_findings": [
                f"{entity_name} appears to be a legitimate {entity_type}",
                "Background research completed successfully",
                "No immediate red flags identified"
            ],
            "confidence": random.uniform(0.7, 0.85),
            "recommendations": ["Continue standard due diligence procedures"]
        }


class MinimalWorkflow:
    """Minimal workflow implementation for demo mode"""

    def __init__(self):
        self.agents = {
            "financial": DemoAgent("financial", "💰"),
            "legal": DemoAgent("legal", "⚖️"),
            "osint": DemoAgent("osint", "🔍"),
            "verification": DemoAgent("verification", "✅"),
            "research": DemoAgent("research", "📊")
        }

    async def run(self, entity_name: str, entity_type: str, scopes: list[str],
                  session_id: str = None) -> AsyncGenerator[dict[str, Any], None]:
        """Run the minimal workflow and yield progress events"""

        start_time = datetime.now()

        # Initialization event
        yield {
            "type": "initialization",
            "message": f"Starting due diligence research for {entity_name}",
            "entity_name": entity_name,
            "entity_type": entity_type,
            "scopes": scopes,
            "session_id": session_id,
            "timestamp": start_time.isoformat()
        }

        # Planning phase
        yield {
            "type": "planning",
            "message": f"Planning research strategy for {len(scopes)} analysis areas",
            "scopes": scopes,
            "estimated_duration": len(scopes) * 30,  # 30 seconds per scope
            "timestamp": datetime.now().isoformat()
        }

        # Execute analysis for each scope
        results = {}
        citations = []

        for i, scope in enumerate(scopes):
            if scope in self.agents:
                agent = self.agents[scope]

                # Start agent event
                yield {
                    "type": "agent_start",
                    "agent": scope,
                    "emoji": agent.emoji,
                    "message": f"Starting {scope} analysis...",
                    "progress": (i / len(scopes)) * 100,
                    "timestamp": datetime.now().isoformat()
                }

                # Run analysis
                try:
                    analysis_result = await agent.analyze(entity_name, entity_type)
                    results[scope] = analysis_result

                    # Add sample citations
                    citations.extend([
                        f"Sample source {j+1} for {scope} analysis"
                        for j in range(random.randint(2, 5))
                    ])

                    # Complete agent event
                    yield {
                        "type": "agent_complete",
                        "agent": scope,
                        "emoji": agent.emoji,
                        "message": f"Completed {scope} analysis",
                        "confidence": analysis_result.get("confidence", 0.8),
                        "key_findings": analysis_result.get("key_findings", [])[:2],  # First 2 findings
                        "progress": ((i + 1) / len(scopes)) * 100,
                        "timestamp": datetime.now().isoformat()
                    }

                except Exception as e:
                    # Error event
                    yield {
                        "type": "agent_error",
                        "agent": scope,
                        "error": str(e),
                        "message": f"Error in {scope} analysis: {e}",
                        "timestamp": datetime.now().isoformat()
                    }

        # Synthesis phase
        yield {
            "type": "synthesis",
            "message": "Synthesizing research findings...",
            "progress": 95,
            "timestamp": datetime.now().isoformat()
        }

        # Calculate overall metrics
        all_confidences = [
            result.get("confidence", 0.8)
            for result in results.values()
            if result.get("confidence")
        ]
        overall_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.8

        duration = (datetime.now() - start_time).total_seconds()

        # Generate executive summary
        executive_summary = self._generate_executive_summary(entity_name, entity_type, results, overall_confidence)

        # Final completion event
        yield {
            "type": "completion",
            "message": f"Due diligence research completed for {entity_name}",
            "entity_name": entity_name,
            "entity_type": entity_type,
            "scopes": scopes,
            "results": results,
            "executive_summary": executive_summary,
            "overall_confidence": overall_confidence,
            "total_sources": len(citations),
            "duration": duration,
            "citations": citations[:10],  # First 10 citations
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "progress": 100
        }

    def _generate_executive_summary(self, entity_name: str, entity_type: str,
                                  results: dict[str, Any], confidence: float) -> str:
        """Generate executive summary based on analysis results"""

        summary_parts = [
            f"DEMO MODE: Comprehensive due diligence analysis completed for {entity_name}.",
            f"This {entity_type} was evaluated across {len(results)} key areas."
        ]

        # Add key insights
        if "financial" in results:
            financial = results["financial"]
            if financial.get("financial_health") == "Good":
                summary_parts.append("Financial position appears stable with manageable risk levels.")
            else:
                summary_parts.append("Financial analysis indicates areas requiring attention.")

        if "legal" in results:
            legal = results["legal"]
            if legal.get("compliance_status") == "Compliant":
                summary_parts.append("Legal compliance status is satisfactory with no major red flags.")
            else:
                summary_parts.append("Legal review identified items requiring further investigation.")

        if "osint" in results:
            osint = results["osint"]
            if osint.get("reputation_score") == "Positive":
                summary_parts.append("Digital presence and online reputation are professional and positive.")

        if "verification" in results:
            verification = results["verification"]
            if verification.get("verification_rate", "0%").replace("%", "").replace(".", "").isdigit():
                rate = verification.get("verification_rate", "95%")
                summary_parts.append(f"Information verification achieved {rate} accuracy across key data points.")

        # Overall assessment
        if confidence > 0.85:
            summary_parts.append("Overall assessment: LOW RISK - Proceed with standard protocols.")
        elif confidence > 0.70:
            summary_parts.append("Overall assessment: MEDIUM RISK - Some areas warrant closer attention.")
        else:
            summary_parts.append("Overall assessment: HIGH RISK - Significant concerns identified requiring investigation.")

        summary_parts.append("\nNote: This is demonstration data for system testing purposes. Real API integration required for actual due diligence research.")

        return " ".join(summary_parts)


# Export the minimal workflow for use in the CLI
async def run_demo_workflow(entity_name: str, entity_type: str, scopes: list[str],
                           session_id: str = None) -> dict[str, Any]:
    """Convenience function to run the demo workflow and return final results"""

    workflow = MinimalWorkflow()
    final_result = None

    async for event in workflow.run(entity_name, entity_type, scopes, session_id):
        if event["type"] == "completion":
            final_result = event
            break

    if final_result:
        # Format for CLI consumption
        return {
            "entity_name": final_result["entity_name"],
            "entity_type": final_result["entity_type"],
            "scopes": final_result["scopes"],
            "findings": final_result["results"],
            "citations": final_result["citations"],
            "confidence_scores": {
                scope: result.get("confidence", 0.8)
                for scope, result in final_result["results"].items()
            },
            "overall_confidence": final_result["overall_confidence"],
            "duration": final_result["duration"],
            "session_id": final_result["session_id"],
            "sources_count": final_result["total_sources"],
            "executive_summary": final_result["executive_summary"]
        }

    # Fallback if workflow fails
    return {
        "entity_name": entity_name,
        "entity_type": entity_type,
        "scopes": scopes,
        "findings": {"demo": {"summary": "Demo workflow completed"}},
        "citations": ["Demo source 1", "Demo source 2"],
        "confidence_scores": {"demo": 0.8},
        "overall_confidence": 0.8,
        "duration": 10,
        "session_id": session_id,
        "sources_count": 2,
        "executive_summary": f"DEMO: Basic analysis completed for {entity_name}."
    }
