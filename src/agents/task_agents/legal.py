from typing import Any

from langchain_core.tools import tool
from langchain_exa import ExaSearchResults, ExaFindSimilarResults
from langchain_community.tools.tavily_search import TavilySearchResults
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

        # Add comprehensive Exa tools for legal research
        if settings.has_exa_key:
            try:
                # Comprehensive legal document neural search
                tools.append(ExaSearchResults(
                    name="exa_legal_comprehensive",
                    description="Large-scale legal research with full content from courts, regulators, and legal sources. For thorough legal due diligence.",
                    num_results=35,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "courtlistener.com", "justia.com", "findlaw.com", 
                        "sec.gov", "ftc.gov", "justice.gov", "uscourts.gov",
                        "supremecourt.gov", "law.cornell.edu", "caselaw.findlaw.com"
                    ],
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Court records and case law search
                tools.append(ExaSearchResults(
                    name="exa_court_records",
                    description="Deep search for court records, case law, and judicial decisions with full content",
                    num_results=20,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "courtlistener.com", "justia.com", "uscourts.gov",
                        "supremecourt.gov", "pacer.gov", "ca9.uscourts.gov"
                    ],
                    type="auto",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Regulatory and compliance search
                tools.append(ExaSearchResults(
                    name="exa_regulatory_compliance",
                    description="Search regulatory filings, compliance updates, and enforcement actions with full content",
                    num_results=18,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "sec.gov", "ftc.gov", "justice.gov", "cftc.gov",
                        "occ.gov", "federalregister.gov", "regulations.gov"
                    ],
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Legal keyword search for precise terms
                tools.append(ExaSearchResults(
                    name="exa_legal_keyword",
                    description="Precise keyword search for specific legal terms, case citations, or statute numbers",
                    num_results=12,
                    api_key=settings.exa_api_key,
                    type="keyword",
                    text_contents_options=True
                ))
                
                # Find similar legal documents for precedent research
                tools.append(ExaFindSimilarResults(
                    name="exa_find_similar_legal",
                    description="Find similar legal documents, cases, and precedents for expanded legal analysis",
                    num_results=10,
                    api_key=settings.exa_api_key,
                    text_contents_options=True,
                    highlights=True
                ))
                
                print("✅ Advanced Exa legal tool suite initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize Exa legal tools: {e}")

        # Add minimal Tavily for urgent legal breaking news only
        if settings.has_tavily_key:
            try:
                tools.append(TavilySearchResults(
                    name="tavily_urgent_legal_news",
                    description="ONLY for urgent legal breaking news and immediate court decisions within hours. Use minimally - Exa is primary source.",
                    max_results=3,
                    api_wrapper_kwargs={"api_key": settings.tavily_api_key}
                ))
                print("✅ Tavily auxiliary legal tool initialized")
            except Exception as e:
                print(f"Warning: Failed to initialize Tavily legal tool: {e}")

        # Add specialized legal tools that don't have public APIs as mock implementations
        @tool
        def sanctions_screening(entity_name: str, lists: str = "OFAC,EU,UN") -> str:
            """Screen entity against sanctions lists and watch lists"""
            # Mock implementation - would integrate with sanctions screening services
            return f"Mock sanctions screening for {entity_name} against lists: {lists} - Status: Clear"

        @tool  
        def litigation_database_search(entity_name: str, court_level: str = "all") -> str:
            """Search specialized litigation databases for case records"""
            # Mock implementation - would integrate with Westlaw, LexisNexis, etc.
            return f"Mock litigation database search for {entity_name}, court level: {court_level}"

        @tool
        def compliance_regulatory_check(entity_name: str, industry: str = "", regulations: str = "") -> str:
            """Check regulatory compliance status across multiple agencies"""  
            # Mock implementation - would integrate with regulatory databases
            return f"Mock compliance check for {entity_name} in {industry}, regulations: {regulations}"

        tools.extend([sanctions_screening, litigation_database_search, compliance_regulatory_check])

        # Add fallback tools if no APIs available
        if not any(tool.name in ['legal_documents_search', 'legal_news_search'] for tool in tools):
            @tool
            def dummy_legal_search(query: str, legal_area: str = "") -> str:
                """Dummy legal search tool for development/testing"""
                return f"Mock legal search results for: {query} | Legal area: {legal_area}"

            tools.append(dummy_legal_search)
            print("⚠️ Using dummy legal tools - configure API keys for real functionality")

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are a legal research and compliance specialist focused on comprehensive legal due diligence.

            AVAILABLE TOOLS:
            - exa_legal_comprehensive: Large-scale legal research (35+ results) with full content from courts and regulators
            - exa_court_records: Deep court records and case law search with full content
            - exa_regulatory_compliance: Regulatory filings and enforcement actions with full content
            - exa_legal_keyword: Precise search for legal terms, case citations, statute numbers
            - exa_find_similar_legal: Similar legal documents and precedents for expanded analysis
            - tavily_urgent_legal_news: ONLY for urgent legal breaking news (use minimally)
            - sanctions_screening: Screen entities against OFAC, EU, and UN sanctions lists
            - litigation_database_search: Search specialized litigation databases for case records
            - compliance_regulatory_check: Check regulatory compliance across multiple agencies

            LEGAL RESEARCH STRATEGY (EXA-DOMINATED):
            1. Start with exa_legal_comprehensive for broad legal landscape analysis with full content
            2. Use exa_court_records for deep dive into case law and judicial decisions
            3. Use exa_regulatory_compliance for enforcement actions and regulatory compliance
            4. Use exa_legal_keyword for specific legal terms, citations, or statute numbers
            5. Use exa_find_similar_legal to expand research through similar cases and precedents
            6. Always run sanctions_screening for compliance due diligence
            7. Use litigation_database_search for specialized case history
            8. Use compliance_regulatory_check for multi-agency compliance status
            9. ONLY use tavily_urgent_legal_news for immediate legal breaking news (last resort)
            10. Always leverage full content extraction and highlights for comprehensive legal analysis

            KEY FOCUS AREAS:
            - Litigation: Active cases, settlements, judgments, class actions
            - Regulatory Compliance: SEC violations, FTC actions, industry-specific compliance
            - Sanctions & AML: OFAC screening, EU sanctions, UN sanctions, PEP lists
            - Corporate Governance: Board issues, executive misconduct, governance failures
            - Intellectual Property: Patent disputes, trademark conflicts, IP litigation
            - Employment Law: Labor violations, discrimination cases, workplace safety

            QUALITY STANDARDS:
            - Prioritize official government sources (courts, regulators, agencies)
            - Always verify sanctions screening results across multiple lists
            - Note case status (active, settled, dismissed) and materiality
            - Extract specific citation numbers, filing dates, and court jurisdictions
            - Flag any patterns of recurring legal issues or compliance failures
            - Cross-verify legal findings from multiple authoritative sources
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
