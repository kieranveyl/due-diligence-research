from typing import Any

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config.settings import settings
from src.state.definitions import ResearchTask


class LegalAgent:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.default_model
        self.model = ChatOpenAI(
            model=self.model_name,
            temperature=settings.default_temperature,
            api_key=settings.openai_api_key
        )
        self.tools = self._initialize_tools()

    def _initialize_tools(self):
        tools = []

        # Add legal research tools
        @tool
        def legal_database_search(query: str, jurisdiction: str = "US") -> str:
            """Search legal databases for case law, statutes, and regulatory information"""
            # Mock implementation - would integrate with legal databases like Westlaw, LexisNexis
            return f"Legal database search for: {query} in jurisdiction: {jurisdiction}"

        @tool
        def compliance_check(entity_name: str, industry: str = "", regulations: str = "") -> str:
            """Check regulatory compliance status and potential violations"""
            # Mock implementation - would integrate with regulatory databases
            return f"Compliance check for {entity_name} in {industry}, regulations: {regulations}"

        @tool
        def litigation_search(entity_name: str, court_level: str = "all") -> str:
            """Search for active and historical litigation involving the entity"""
            # Mock implementation - would integrate with court record systems
            return f"Litigation search for {entity_name}, court level: {court_level}"

        @tool
        def regulatory_filing_search(entity_name: str, filing_type: str = "all") -> str:
            """Search regulatory filings and compliance documents"""
            # Mock implementation - would integrate with regulatory filing systems
            return f"Regulatory filing search for {entity_name}, type: {filing_type}"

        @tool
        def sanctions_screening(entity_name: str, lists: str = "OFAC,EU,UN") -> str:
            """Screen entity against sanctions lists and watch lists"""
            # Mock implementation - would integrate with sanctions screening services
            return f"Sanctions screening for {entity_name} against lists: {lists}"

        @tool
        def intellectual_property_search(entity_name: str, ip_type: str = "all") -> str:
            """Search for patents, trademarks, and other intellectual property"""
            # Mock implementation - would integrate with IP databases
            return f"IP search for {entity_name}, type: {ip_type}"

        tools.extend([
            legal_database_search,
            compliance_check,
            litigation_search,
            regulatory_filing_search,
            sanctions_screening,
            intellectual_property_search
        ])

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are a legal research and compliance specialist focused on comprehensive legal due diligence.

            Your responsibilities:
            1. Research legal history, litigation, and regulatory compliance
            2. Analyze regulatory filings and compliance status
            3. Identify legal risks, sanctions, and regulatory violations
            4. Review corporate governance and legal structure
            5. Assess intellectual property portfolios and disputes
            6. Evaluate contract disputes and legal obligations
            7. Screen against sanctions lists and watch lists

            Use multiple legal databases and regulatory sources for comprehensive coverage.
            Focus on material legal risks and compliance issues.
            Provide clear risk assessments with regulatory citations.
            Always verify information across multiple authoritative sources.
            Pay special attention to sanctions, AML, and regulatory violations.
            """,
            name="legal_agent"
        )

    async def execute_task(self, task: ResearchTask, context: str = "") -> dict[str, Any]:
        """Execute legal analysis task with structured approach"""

        # Step 1: Extract legal research requirements
        legal_focus = self._extract_legal_focus(task.description, context)

        # Step 2: Gather legal data from multiple sources
        legal_data = await self._gather_legal_data(legal_focus)

        # Step 3: Perform legal risk analysis
        legal_analysis = await self._perform_legal_analysis(legal_data, legal_focus)

        # Step 4: Structure results according to schema
        structured_results = await self._structure_legal_results(
            analysis=legal_analysis,
            schema=task.output_schema,
            task_description=task.description
        )

        return {
            "task_id": task.id,
            "results": structured_results,
            "citations": self._extract_citations(legal_data),
            "confidence": self._calculate_confidence(structured_results, legal_data)
        }

    def _extract_legal_focus(self, description: str, context: str) -> dict[str, Any]:
        """Extract what type of legal analysis is needed"""
        # Determine focus areas based on task description
        focus_areas = {
            "litigation": "litigation" in description.lower() or "lawsuit" in description.lower(),
            "compliance": "compliance" in description.lower() or "regulation" in description.lower(),
            "sanctions": "sanctions" in description.lower() or "aml" in description.lower(),
            "intellectual_property": "patent" in description.lower() or "trademark" in description.lower(),
            "corporate_governance": "governance" in description.lower() or "board" in description.lower(),
            "regulatory": "regulatory" in description.lower() or "sec" in description.lower()
        }

        return {
            "entity_name": self._extract_entity_name(description, context),
            "focus_areas": [area for area, needed in focus_areas.items() if needed],
            "jurisdiction": self._extract_jurisdiction(description, context),
            "analysis_type": "comprehensive" if len([a for a in focus_areas.values() if a]) > 2 else "focused"
        }

    def _extract_entity_name(self, description: str, context: str) -> str:
        """Extract entity name from description or context"""
        # Simple extraction - in real implementation would use NLP
        words = description.split()
        for i, word in enumerate(words):
            if word.lower() in ["corp", "inc", "llc", "ltd", "company"]:
                if i > 0:
                    return f"{words[i-1]} {word}"
        return "Unknown Entity"

    def _extract_jurisdiction(self, description: str, context: str) -> str:
        """Extract jurisdiction from description or context"""
        # Simple extraction - would use more sophisticated parsing in real implementation
        if "eu" in description.lower() or "europe" in description.lower():
            return "EU"
        elif "uk" in description.lower() or "britain" in description.lower():
            return "UK"
        else:
            return "US"  # Default

    async def _gather_legal_data(self, legal_focus: dict[str, Any]) -> dict[str, Any]:
        """Gather legal data from multiple sources"""
        legal_focus["entity_name"]
        focus_areas = legal_focus["focus_areas"]
        legal_focus["jurisdiction"]

        legal_data = {
            "litigation_records": [],
            "compliance_status": {},
            "sanctions_screening": {},
            "regulatory_filings": [],
            "ip_portfolio": {},
            "sources": []
        }

        # Gather data based on focus areas
        if "litigation" in focus_areas:
            # Mock litigation data
            legal_data["litigation_records"] = [
                {
                    "case_id": "2023-CV-001234",
                    "court": "Superior Court",
                    "status": "Active",
                    "filed_date": "2023-01-15",
                    "case_type": "Contract Dispute",
                    "amount": "$2.5M"
                },
                {
                    "case_id": "2022-CV-005678",
                    "court": "Federal District Court",
                    "status": "Settled",
                    "filed_date": "2022-06-30",
                    "case_type": "Employment Law",
                    "amount": "$850K"
                }
            ]

        if "compliance" in focus_areas:
            # Mock compliance data
            legal_data["compliance_status"] = {
                "regulatory_standing": "Good Standing",
                "last_inspection": "2024-01-15",
                "violations": 0,
                "pending_matters": 1
            }

        if "sanctions" in focus_areas:
            # Mock sanctions screening
            legal_data["sanctions_screening"] = {
                "ofac_status": "Clear",
                "eu_sanctions": "Clear",
                "un_sanctions": "Clear",
                "screening_date": "2024-09-15"
            }

        if "intellectual_property" in focus_areas:
            # Mock IP data
            legal_data["ip_portfolio"] = {
                "patents": 45,
                "trademarks": 12,
                "pending_applications": 8,
                "disputes": 2
            }

        legal_data["sources"].extend([
            "Legal Database Search Results",
            "Court Records",
            "Regulatory Filing Systems",
            "Sanctions Screening Services"
        ])

        return legal_data

    async def _perform_legal_analysis(self, legal_data: dict, legal_focus: dict) -> dict[str, Any]:
        """Perform comprehensive legal risk analysis"""
        analysis = {
            "legal_standing": {},
            "risk_assessment": {},
            "compliance_status": {},
            "litigation_exposure": {},
            "regulatory_risks": {},
            "red_flags": [],
            "recommendations": []
        }

        # Analyze legal standing
        analysis["legal_standing"] = {
            "sanctions_status": legal_data.get("sanctions_screening", {}).get("ofac_status", "Unknown"),
            "regulatory_compliance": legal_data.get("compliance_status", {}).get("regulatory_standing", "Unknown"),
            "active_litigation": len(legal_data.get("litigation_records", []))
        }

        # Risk assessment
        active_cases = [case for case in legal_data.get("litigation_records", []) if case.get("status") == "Active"]
        analysis["risk_assessment"] = {
            "litigation_risk": "High" if len(active_cases) > 3 else "Moderate" if len(active_cases) > 0 else "Low",
            "compliance_risk": "Low" if legal_data.get("compliance_status", {}).get("violations", 0) == 0 else "High",
            "sanctions_risk": "Low" if legal_data.get("sanctions_screening", {}).get("ofac_status") == "Clear" else "High"
        }

        # Compliance status
        analysis["compliance_status"] = legal_data.get("compliance_status", {})

        # Litigation exposure
        total_exposure = sum(
            float(case.get("amount", "$0").replace("$", "").replace("M", "000000").replace("K", "000"))
            for case in legal_data.get("litigation_records", [])
            if case.get("status") == "Active"
        )
        analysis["litigation_exposure"] = {
            "active_cases": len(active_cases),
            "total_exposure": f"${total_exposure:,.0f}",
            "material_cases": len([case for case in active_cases if "M" in case.get("amount", "")])
        }

        # Identify red flags
        if legal_data.get("sanctions_screening", {}).get("ofac_status") != "Clear":
            analysis["red_flags"].append("Entity appears on sanctions list")

        if len(active_cases) > 5:
            analysis["red_flags"].append("High volume of active litigation")

        if legal_data.get("compliance_status", {}).get("violations", 0) > 0:
            analysis["red_flags"].append("Recent regulatory violations")

        # Recommendations
        if len(active_cases) > 0:
            analysis["recommendations"].append("Monitor active litigation for material developments")

        analysis["recommendations"].append("Maintain regular sanctions screening")
        analysis["recommendations"].append("Review compliance status quarterly")

        return analysis

    async def _structure_legal_results(self, analysis: dict, schema: dict, task_description: str) -> dict:
        """Structure legal analysis results according to task schema"""
        # Use LLM to structure results if schema is provided
        if schema:
            # Mock structured output - would use LLM in real implementation
            return {
                "legal_summary": analysis,
                "key_findings": [
                    "Entity has clear sanctions screening status",
                    "Moderate litigation exposure from active cases",
                    "Compliance status is in good standing"
                ],
                "risk_factors": [
                    "Active litigation cases requiring monitoring",
                    "Potential regulatory changes impact"
                ],
                "recommendations": [
                    "Implement regular legal risk monitoring",
                    "Update sanctions screening quarterly",
                    "Review litigation strategy for active cases"
                ]
            }
        else:
            return analysis

    def _extract_citations(self, legal_data: dict) -> list[str]:
        """Extract citations from legal data sources"""
        citations = []

        if legal_data.get("sources"):
            citations.extend(legal_data["sources"])

        if legal_data.get("litigation_records"):
            for case in legal_data["litigation_records"]:
                citations.append(f"Case {case['case_id']} - {case['court']}")

        return citations

    def _calculate_confidence(self, results: dict, legal_data: dict) -> float:
        """Calculate confidence score based on data quality and completeness"""
        confidence_factors = []

        # Data completeness
        if legal_data.get("litigation_records"):
            confidence_factors.append(0.25)
        if legal_data.get("compliance_status"):
            confidence_factors.append(0.25)
        if legal_data.get("sanctions_screening"):
            confidence_factors.append(0.3)
        if legal_data.get("regulatory_filings"):
            confidence_factors.append(0.2)

        # Source reliability
        reliable_sources = len(legal_data.get("sources", []))
        confidence_factors.append(min(reliable_sources * 0.03, 0.15))

        return min(sum(confidence_factors), 1.0)
