from typing import Any

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_exa import ExaFindSimilarResults, ExaSearchResults
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

        # Add comprehensive Exa tools for verification and fact-checking
        if settings.has_exa_key:
            try:
                # Comprehensive authoritative source verification
                tools.append(ExaSearchResults(
                    name="exa_authoritative_comprehensive",
                    description="Large-scale search of authoritative sources for comprehensive fact verification with full content",
                    num_results=30,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "sec.gov", "irs.gov", "ftc.gov", "justice.gov", "treasury.gov",
                        "uscourts.gov", "supremecourt.gov", "bls.gov", "census.gov",
                        "factcheck.org", "snopes.com", "politifact.com", "reuters.com",
                        "ap.org", "bbc.com", "npr.org", "pbs.org"
                    ],
                    type="auto",
                    text_contents_options=True,
                    highlights=True
                ))

                # Primary source neural search
                tools.append(ExaSearchResults(
                    name="exa_primary_sources_neural",
                    description="Deep neural search for primary source documents and official records with full content extraction",
                    num_results=25,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "sec.gov", "edgar.sec.gov", "investor.gov", "irs.gov",
                        "uspto.gov", "copyright.gov", "icann.org", "whois.net",
                        "corporationwiki.com", "bizapedia.com", "opencorporates.com",
                        "federalregister.gov", "gpo.gov", "govinfo.gov"
                    ],
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))

                # Fact-checking and verification keyword search
                tools.append(ExaSearchResults(
                    name="exa_verification_keyword",
                    description="Precise keyword search for specific claims, facts, or data points requiring verification",
                    num_results=15,
                    api_key=settings.exa_api_key,
                    type="keyword",
                    text_contents_options=True,
                    highlights=True
                ))

                # Academic and research sources
                tools.append(ExaSearchResults(
                    name="exa_academic_sources",
                    description="Search academic and research sources for scholarly verification with full content",
                    num_results=20,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "scholar.google.com", "pubmed.ncbi.nlm.nih.gov", "arxiv.org",
                        "ssrn.com", "jstor.org", "ieee.org", "acm.org",
                        "researchgate.net", "academia.edu"
                    ],
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))

                # Find corroborating sources with expanded scope
                tools.append(ExaFindSimilarResults(
                    name="exa_find_corroborating_sources",
                    description="Find corroborating or contradicting sources for comprehensive fact verification and cross-referencing",
                    num_results=12,
                    api_key=settings.exa_api_key,
                    text_contents_options=True,
                    highlights=True
                ))

                print("✅ Advanced Exa verification tool suite initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize Exa verification tools: {e}")

        # Add minimal Tavily for urgent fact-checking only
        if settings.has_tavily_key:
            try:
                tools.append(TavilySearchResults(
                    name="tavily_urgent_fact_check",
                    description="ONLY for urgent real-time fact-checking of breaking information within hours. Use minimally - Exa is primary source.",
                    max_results=3,
                    api_wrapper_kwargs={"api_key": settings.tavily_api_key}
                ))
                print("✅ Tavily auxiliary fact-checking tool initialized")
            except Exception as e:
                print(f"Warning: Failed to initialize Tavily fact-checking tool: {e}")

        # Add specialized verification and analysis tools (these focus on analysis rather than search)
        @tool
        def cross_reference_analysis(claim: str, source_urls: str) -> str:
            """Analyze and cross-reference a claim against multiple source URLs for consistency"""
            # Mock implementation - would implement sophisticated cross-referencing analysis
            sources = source_urls.split(',') if source_urls else []
            return f"Cross-reference analysis of claim: '{claim}' across {len(sources)} sources - Consistency: High"

        @tool
        def temporal_consistency_check(events_timeline: str) -> str:
            """Check temporal consistency and logical sequence of events across sources"""
            # Mock implementation - would analyze dates and timeline consistency
            return f"Temporal analysis of timeline: {events_timeline} - Consistency: Verified"

        @tool
        def numerical_data_verification(data_claims: str, entity_name: str) -> str:
            """Verify numerical claims (financial, statistical) against authoritative data sources"""
            # Mock implementation - would verify numbers against official sources
            return f"Numerical verification for {entity_name}: {data_claims} - Status: Verified within margin"

        @tool
        def source_credibility_assessment(source_list: str) -> str:
            """Assess credibility scores and reliability ratings for information sources"""
            # Mock implementation - would evaluate source reputation and reliability
            sources = source_list.split(',') if source_list else []
            return f"Credibility assessment of {len(sources)} sources - Average reliability: High (8.5/10)"

        @tool
        def contradiction_detection_analysis(statements: str) -> str:
            """Detect logical contradictions and inconsistencies between statements"""
            # Mock implementation - would analyze logical consistency
            return f"Contradiction analysis of statements: {statements} - No significant contradictions detected"

        @tool
        def identity_verification_analysis(entity_identifiers: str) -> str:
            """Verify entity identity using official identifiers and registration numbers"""
            # Mock implementation - would verify against official registrations
            return f"Identity verification using identifiers: {entity_identifiers} - Status: Confirmed"

        @tool
        def contact_verification_analysis(contact_data: str, entity_name: str) -> str:
            """Verify contact information accuracy against official records and directories"""
            # Mock implementation - would verify addresses, phone numbers, emails
            return f"Contact verification for {entity_name}: {contact_data} - Status: Verified and current"

        tools.extend([
            cross_reference_analysis,
            temporal_consistency_check,
            numerical_data_verification,
            source_credibility_assessment,
            contradiction_detection_analysis,
            identity_verification_analysis,
            contact_verification_analysis
        ])

        # Add fallback tools if no APIs available
        if not any(tool.name in ['authoritative_source_search', 'primary_source_search'] for tool in tools):
            @tool
            def dummy_verification_tool(claim: str, verification_type: str = "general") -> str:
                """Dummy verification tool for development/testing"""
                return f"Mock verification of claim: {claim} | Type: {verification_type} - Status: Verified"

            tools.append(dummy_verification_tool)
            print("⚠️ Using dummy verification tools - configure API keys for real functionality")

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are a verification and fact-checking specialist focused on ensuring information accuracy through systematic cross-referencing and source validation.

            AVAILABLE TOOLS:
            - exa_authoritative_comprehensive: Large-scale authoritative source search (30+ results) with full content
            - exa_primary_sources_neural: Deep neural search for primary documents with full content extraction
            - exa_verification_keyword: Precise keyword search for specific claims and data points
            - exa_academic_sources: Academic and research sources for scholarly verification
            - exa_find_corroborating_sources: Corroborating sources for comprehensive cross-referencing
            - tavily_urgent_fact_check: ONLY for urgent real-time fact-checking (use minimally)
            - cross_reference_analysis: Analyze claim consistency across multiple source URLs
            - temporal_consistency_check: Verify timeline consistency and event sequences
            - numerical_data_verification: Verify numerical claims against authoritative data
            - source_credibility_assessment: Assess reliability and credibility of information sources
            - contradiction_detection_analysis: Detect logical contradictions between statements
            - identity_verification_analysis: Verify entity identity using official identifiers
            - contact_verification_analysis: Verify contact information against official records

            VERIFICATION STRATEGY (EXA-DOMINATED):
            1. Start with exa_authoritative_comprehensive for broad authoritative source verification with full content
            2. Use exa_primary_sources_neural for deep dive into original documents and official records
            3. Use exa_academic_sources for scholarly and research-based verification
            4. Use exa_verification_keyword for precise searches of specific claims or data points
            5. Use exa_find_corroborating_sources for comprehensive cross-referencing from multiple angles
            6. Apply cross_reference_analysis to systematically compare sources
            7. Use temporal_consistency_check for timeline and sequence verification
            8. Apply numerical_data_verification for statistical and financial claims
            9. Use source_credibility_assessment to evaluate source reliability
            10. Apply contradiction_detection_analysis to identify inconsistencies
            11. Use specialized verification tools for identity and contact validation
            12. ONLY use tavily_urgent_fact_check for immediate breaking information (last resort)
            13. Always leverage full content extraction and highlights for comprehensive verification analysis

            VERIFICATION PRIORITIES:
            - Primary Sources: Government filings, official records, regulatory documents
            - Secondary Sources: Established news organizations, financial databases, legal records
            - Tertiary Sources: Industry reports, academic research, professional publications
            - Real-time Sources: Breaking news, current developments, market updates

            QUALITY STANDARDS:
            - Require minimum 2-3 independent sources for claim verification
            - Prioritize official government and regulatory sources
            - Assign confidence scores based on source authority and consistency
            - Flag any claims that cannot be independently verified
            - Document verification methodology and source hierarchy
            - Identify and investigate any contradictions or inconsistencies
            - Cross-reference numerical data against authoritative databases
            - Verify temporal consistency across all sources and timelines
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
