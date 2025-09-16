from typing import Any

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config.settings import settings
from src.state.definitions import ResearchTask


class VerificationAgent:
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

        # Add verification and fact-checking tools
        @tool
        def cross_reference_sources(claim: str, sources: str) -> str:
            """Cross-reference claims against multiple independent sources"""
            # Mock implementation - would implement sophisticated fact-checking
            return f"Cross-referencing claim: '{claim}' across sources: {sources}"

        @tool
        def verify_financial_data(data_point: str, entity: str) -> str:
            """Verify financial data against authoritative sources"""
            # Mock implementation - would verify against SEC, financial databases
            return f"Verifying financial data: {data_point} for {entity}"

        @tool
        def validate_legal_information(legal_claim: str, jurisdiction: str = "US") -> str:
            """Validate legal information against legal databases"""
            # Mock implementation - would verify against legal databases
            return f"Validating legal claim: {legal_claim} in {jurisdiction}"

        @tool
        def check_date_consistency(events: str) -> str:
            """Check consistency of dates and timelines across sources"""
            # Mock implementation - would analyze temporal consistency
            return f"Checking date consistency for events: {events}"

        @tool
        def verify_entity_identity(entity_name: str, identifiers: str = "") -> str:
            """Verify entity identity using multiple identifiers"""
            # Mock implementation - would verify using tax IDs, registration numbers
            return f"Verifying identity of {entity_name} using identifiers: {identifiers}"

        @tool
        def assess_source_credibility(source: str) -> str:
            """Assess the credibility and reliability of information sources"""
            # Mock implementation - would evaluate source reputation
            return f"Assessing credibility of source: {source}"

        @tool
        def detect_contradictions(statements: str) -> str:
            """Detect contradictions or inconsistencies in statements"""
            # Mock implementation - would analyze logical consistency
            return f"Analyzing statements for contradictions: {statements}"

        @tool
        def verify_contact_information(contact_info: str, entity: str) -> str:
            """Verify contact information accuracy"""
            # Mock implementation - would verify addresses, phone numbers
            return f"Verifying contact info: {contact_info} for {entity}"

        tools.extend([
            cross_reference_sources,
            verify_financial_data,
            validate_legal_information,
            check_date_consistency,
            verify_entity_identity,
            assess_source_credibility,
            detect_contradictions,
            verify_contact_information
        ])

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are a verification and fact-checking specialist focused on ensuring information accuracy and reliability.

            Your responsibilities:
            1. Cross-reference claims against multiple independent authoritative sources
            2. Verify financial data accuracy using official filings and databases
            3. Validate legal information against legal databases and court records
            4. Check temporal consistency of events and timelines
            5. Verify entity identity using official identifiers and registrations
            6. Assess source credibility and reliability scores
            7. Detect contradictions or inconsistencies in gathered information
            8. Verify contact information and physical addresses

            Use rigorous fact-checking methodology and source triangulation.
            Prioritize primary sources over secondary and tertiary sources.
            Flag any information that cannot be independently verified.
            Assign confidence scores based on source quality and verification status.
            Document verification methodology and sources used.
            Identify areas requiring additional verification or clarification.
            """,
            name="verification_agent"
        )

    async def execute_task(self, task: ResearchTask, context: str = "") -> dict[str, Any]:
        """Execute verification task with systematic fact-checking approach"""

        # Step 1: Extract verification requirements
        verification_focus = self._extract_verification_focus(task.description, context)

        # Step 2: Gather verification data and sources
        verification_data = await self._gather_verification_data(verification_focus)

        # Step 3: Perform comprehensive verification analysis
        verification_analysis = await self._perform_verification_analysis(verification_data, verification_focus)

        # Step 4: Structure results according to schema
        structured_results = await self._structure_verification_results(
            analysis=verification_analysis,
            schema=task.output_schema,
            task_description=task.description
        )

        return {
            "task_id": task.id,
            "results": structured_results,
            "citations": self._extract_citations(verification_data),
            "confidence": self._calculate_confidence(structured_results, verification_data)
        }

    def _extract_verification_focus(self, description: str, context: str) -> dict[str, Any]:
        """Extract what type of verification is needed"""
        # Determine focus areas based on task description
        focus_areas = {
            "financial_data": "financial" in description.lower() or "revenue" in description.lower(),
            "legal_claims": "legal" in description.lower() or "lawsuit" in description.lower(),
            "entity_identity": "identity" in description.lower() or "registration" in description.lower(),
            "contact_verification": "contact" in description.lower() or "address" in description.lower(),
            "timeline_consistency": "timeline" in description.lower() or "date" in description.lower(),
            "source_credibility": "source" in description.lower() or "credibility" in description.lower(),
            "cross_reference": "verify" in description.lower() or "fact" in description.lower()
        }

        return {
            "entity_name": self._extract_entity_name(description, context),
            "focus_areas": [area for area, needed in focus_areas.items() if needed],
            "verification_scope": "comprehensive" if len([a for a in focus_areas.values() if a]) > 3 else "targeted",
            "claims_to_verify": self._extract_claims(description, context)
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

    def _extract_claims(self, description: str, context: str) -> list[str]:
        """Extract specific claims that need verification"""
        # Mock implementation - would use NLP to extract factual claims
        claims = []

        if "revenue" in description.lower():
            claims.append("Revenue figures and financial performance")
        if "founded" in description.lower():
            claims.append("Company founding date and history")
        if "employees" in description.lower():
            claims.append("Employee count and organizational size")
        if "lawsuit" in description.lower():
            claims.append("Legal proceedings and litigation status")

        return claims if claims else ["General entity information"]

    async def _gather_verification_data(self, verification_focus: dict[str, Any]) -> dict[str, Any]:
        """Gather data for verification from authoritative sources"""
        verification_focus["entity_name"]
        focus_areas = verification_focus["focus_areas"]
        claims = verification_focus["claims_to_verify"]

        verification_data = {
            "primary_sources": [],
            "secondary_sources": [],
            "official_records": [],
            "cross_references": [],
            "contradictions": [],
            "verification_status": {},
            "sources": []
        }

        # Gather data based on focus areas
        if "financial_data" in focus_areas:
            # Mock financial verification data
            verification_data["primary_sources"].extend([
                {
                    "type": "SEC Filing",
                    "source": "SEC EDGAR Database",
                    "document": "10-K Annual Report",
                    "date": "2024-03-15",
                    "verified": True
                },
                {
                    "type": "Audited Financial Statement",
                    "source": "Independent Auditor",
                    "auditor": "PwC",
                    "date": "2024-03-15",
                    "verified": True
                }
            ])

        if "legal_claims" in focus_areas:
            # Mock legal verification data
            verification_data["official_records"].extend([
                {
                    "type": "Court Records",
                    "source": "PACER Database",
                    "case_number": "2023-CV-001234",
                    "status": "Active",
                    "verified": True
                }
            ])

        if "entity_identity" in focus_areas:
            # Mock identity verification data
            verification_data["official_records"].extend([
                {
                    "type": "Business Registration",
                    "source": "Secretary of State",
                    "registration_number": "C1234567",
                    "status": "Active",
                    "verified": True
                }
            ])

        # Cross-reference verification
        for claim in claims:
            verification_data["cross_references"].append({
                "claim": claim,
                "sources_checked": 3,
                "sources_confirmed": 3,
                "confidence": 1.0,
                "verified": True
            })

        verification_data["sources"].extend([
            "SEC EDGAR Database",
            "Business Registration Records",
            "Court Filing Systems",
            "Independent Financial Audits"
        ])

        return verification_data

    async def _perform_verification_analysis(self, verification_data: dict, verification_focus: dict) -> dict[str, Any]:
        """Perform comprehensive verification analysis"""
        analysis = {
            "verification_summary": {},
            "source_assessment": {},
            "claim_verification": {},
            "contradictions_found": [],
            "confidence_scores": {},
            "verification_gaps": [],
            "recommendations": []
        }

        # Verification summary
        primary_sources = len(verification_data.get("primary_sources", []))
        official_records = len(verification_data.get("official_records", []))
        cross_refs = len(verification_data.get("cross_references", []))

        analysis["verification_summary"] = {
            "primary_sources_verified": primary_sources,
            "official_records_checked": official_records,
            "cross_references_completed": cross_refs,
            "overall_verification_rate": 0.95 if primary_sources > 0 else 0.5
        }

        # Source assessment
        analysis["source_assessment"] = {
            "primary_source_quality": "High" if primary_sources >= 2 else "Moderate",
            "official_record_availability": "Good" if official_records >= 1 else "Limited",
            "source_diversity": "Comprehensive" if len(verification_data.get("sources", [])) >= 3 else "Limited"
        }

        # Claim verification
        for claim_data in verification_data.get("cross_references", []):
            claim = claim_data["claim"]
            analysis["claim_verification"][claim] = {
                "verification_status": "Verified" if claim_data["verified"] else "Unverified",
                "sources_confirmed": f"{claim_data['sources_confirmed']}/{claim_data['sources_checked']}",
                "confidence": claim_data["confidence"]
            }

        # Confidence scores for different categories
        analysis["confidence_scores"] = {
            "financial_data": 0.95 if "financial_data" in verification_focus["focus_areas"] else 0.0,
            "legal_information": 0.90 if "legal_claims" in verification_focus["focus_areas"] else 0.0,
            "entity_identity": 0.98 if "entity_identity" in verification_focus["focus_areas"] else 0.0,
            "contact_information": 0.85 if "contact_verification" in verification_focus["focus_areas"] else 0.0
        }

        # Identify verification gaps
        if primary_sources == 0:
            analysis["verification_gaps"].append("Lack of primary source verification")
        if official_records == 0:
            analysis["verification_gaps"].append("No official records verified")

        # Recommendations
        analysis["recommendations"].extend([
            "Continue monitoring for information updates",
            "Re-verify critical claims annually",
            "Maintain source diversity for ongoing verification"
        ])

        if analysis["verification_gaps"]:
            analysis["recommendations"].append("Address identified verification gaps")

        return analysis

    async def _structure_verification_results(self, analysis: dict, schema: dict, task_description: str) -> dict:
        """Structure verification analysis results according to task schema"""
        # Use LLM to structure results if schema is provided
        if schema:
            # Mock structured output - would use LLM in real implementation
            return {
                "verification_summary": analysis,
                "key_findings": [
                    "High verification rate achieved across primary sources",
                    "Claims successfully cross-referenced against authoritative databases",
                    "No significant contradictions identified in verified information"
                ],
                "verified_claims": [
                    "Entity registration and legal status confirmed",
                    "Financial data verified against official filings",
                    "Contact information validated through multiple sources"
                ],
                "verification_gaps": analysis.get("verification_gaps", []),
                "recommendations": [
                    "Implement continuous monitoring for information updates",
                    "Schedule periodic re-verification of critical claims",
                    "Maintain documentation of verification methodology"
                ]
            }
        else:
            return analysis

    def _extract_citations(self, verification_data: dict) -> list[str]:
        """Extract citations from verification data sources"""
        citations = []

        if verification_data.get("sources"):
            citations.extend(verification_data["sources"])

        if verification_data.get("primary_sources"):
            for source in verification_data["primary_sources"]:
                citations.append(f"{source['type']} - {source['source']}")

        if verification_data.get("official_records"):
            for record in verification_data["official_records"]:
                citations.append(f"{record['type']} - {record['source']}")

        return citations

    def _calculate_confidence(self, results: dict, verification_data: dict) -> float:
        """Calculate confidence score based on verification completeness and source quality"""
        confidence_factors = []

        # Primary source verification
        primary_sources = len(verification_data.get("primary_sources", []))
        confidence_factors.append(min(primary_sources * 0.25, 0.4))

        # Official record verification
        official_records = len(verification_data.get("official_records", []))
        confidence_factors.append(min(official_records * 0.2, 0.3))

        # Cross-reference verification
        cross_refs = len(verification_data.get("cross_references", []))
        confidence_factors.append(min(cross_refs * 0.1, 0.2))

        # Source diversity
        source_count = len(verification_data.get("sources", []))
        confidence_factors.append(min(source_count * 0.02, 0.1))

        return min(sum(confidence_factors), 1.0)
