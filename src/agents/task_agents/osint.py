from typing import Any

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_exa import ExaFindSimilarResults, ExaSearchResults
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config.settings import settings
from src.state.definitions import ResearchTask


class OSINTAgent:
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

        # Add comprehensive Exa tools for OSINT investigation
        if settings.has_exa_key:
            try:
                # Comprehensive OSINT neural search across all digital platforms
                tools.append(ExaSearchResults(
                    name="exa_osint_comprehensive",
                    description="Large-scale OSINT investigation with full content across social media, forums, and digital platforms. For thorough digital footprint analysis.",
                    num_results=40,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "linkedin.com", "twitter.com", "facebook.com", "instagram.com",
                        "youtube.com", "tiktok.com", "reddit.com", "github.com",
                        "stackoverflow.com", "medium.com", "crunchbase.com",
                        "angellist.com", "producthunt.com", "hackernews.com"
                    ],
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))

                # Public records and directories with full content
                tools.append(ExaSearchResults(
                    name="exa_public_records",
                    description="Deep search of public records, business directories, and government databases with full content extraction",
                    num_results=25,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "whitepages.com", "spokeo.com", "sec.gov", "irs.gov",
                        "census.gov", "usa.gov", "corporationwiki.com", "bizapedia.com",
                        "manta.com", "opencorporates.com", "fec.gov"
                    ],
                    type="auto",
                    text_contents_options=True,
                    highlights=True
                ))

                # Reputation and news monitoring with sentiment analysis
                tools.append(ExaSearchResults(
                    name="exa_reputation_monitoring",
                    description="Comprehensive reputation monitoring with full article content and sentiment analysis",
                    num_results=30,
                    api_key=settings.exa_api_key,
                    include_domains=[
                        "reuters.com", "bloomberg.com", "wsj.com", "forbes.com",
                        "techcrunch.com", "businesswire.com", "prnewswire.com",
                        "glassdoor.com", "trustpilot.com", "bbb.org", "yelp.com",
                        "ripoffreport.com", "complaintsboard.com"
                    ],
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))

                # OSINT keyword search for precise terms
                tools.append(ExaSearchResults(
                    name="exa_osint_keyword",
                    description="Precise keyword search for specific names, usernames, emails, or identifiers in OSINT investigation",
                    num_results=15,
                    api_key=settings.exa_api_key,
                    type="keyword",
                    text_contents_options=True
                ))

                # Find similar digital assets and related entities
                tools.append(ExaFindSimilarResults(
                    name="exa_find_similar_digital_assets",
                    description="Find similar digital assets, related entities, and connected online presence for expanded OSINT investigation",
                    num_results=12,
                    api_key=settings.exa_api_key,
                    text_contents_options=True,
                    highlights=True
                ))

                print("✅ Advanced Exa OSINT tool suite initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize Exa OSINT tools: {e}")

        # Add minimal Tavily for urgent OSINT updates only
        if settings.has_tavily_key:
            try:
                tools.append(TavilySearchResults(
                    name="tavily_urgent_osint",
                    description="ONLY for urgent real-time OSINT updates and breaking developments within hours. Use minimally - Exa is primary source.",
                    max_results=3,
                    api_wrapper_kwargs={"api_key": settings.tavily_api_key}
                ))
                print("✅ Tavily auxiliary OSINT tool initialized")
            except Exception as e:
                print(f"Warning: Failed to initialize Tavily OSINT tool: {e}")

        # Add specialized OSINT tools that require custom integrations (mock implementations)
        @tool
        def domain_technical_analysis(domain: str) -> str:
            """Analyze domain registration, DNS records, hosting details, and technical infrastructure"""
            # Mock implementation - would integrate with WHOIS, DNS lookup, and hosting analysis tools
            return f"Mock domain technical analysis for: {domain} - Registrar: GoDaddy, Hosting: AWS, SSL: Valid"

        @tool
        def breach_security_monitoring(entity_identifier: str, search_type: str = "email") -> str:
            """Check for data breaches, exposed credentials, and security incidents"""
            # Mock implementation - would integrate with HaveIBeenPwned, breach databases
            return f"Mock breach monitoring for {entity_identifier} ({search_type}) - Status: No breaches found"

        @tool
        def dark_web_threat_monitoring(entity_name: str, monitoring_scope: str = "standard") -> str:
            """Monitor dark web forums, markets, and underground sources for entity mentions and threats"""
            # Mock implementation - would integrate with dark web monitoring services
            return f"Mock dark web monitoring for {entity_name} (scope: {monitoring_scope}) - No threats detected"

        @tool
        def digital_forensics_analysis(target_identifier: str, analysis_type: str = "passive") -> str:
            """Perform digital forensics analysis on digital assets and online presence"""
            # Mock implementation - would integrate with forensics tools and metadata analysis
            return f"Mock digital forensics analysis for {target_identifier} (type: {analysis_type}) - Clean profile"

        tools.extend([
            domain_technical_analysis,
            breach_security_monitoring,
            dark_web_threat_monitoring,
            digital_forensics_analysis
        ])

        # Add fallback tools if no APIs available
        if not any(tool.name in ['social_media_osint', 'public_records_osint'] for tool in tools):
            @tool
            def dummy_osint_search(query: str, osint_type: str = "general") -> str:
                """Dummy OSINT search tool for development/testing"""
                return f"Mock OSINT search results for: {query} | Type: {osint_type}"

            tools.append(dummy_osint_search)
            print("⚠️ Using dummy OSINT tools - configure API keys for real functionality")

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are an Open Source Intelligence (OSINT) specialist focused on comprehensive digital investigations using publicly available information.

            AVAILABLE TOOLS:
            - exa_osint_comprehensive: Large-scale OSINT investigation (40+ results) with full content across all digital platforms
            - exa_public_records: Deep public records search with full content from directories and government databases
            - exa_reputation_monitoring: Comprehensive reputation monitoring (30+ results) with full content and sentiment analysis
            - exa_osint_keyword: Precise keyword search for specific names, usernames, emails, or identifiers
            - exa_find_similar_digital_assets: Similar digital assets and related entities for expanded investigation
            - tavily_urgent_osint: ONLY for urgent real-time OSINT updates (use minimally)
            - domain_technical_analysis: Analyze domain registration, DNS records, and hosting infrastructure
            - breach_security_monitoring: Check for data breaches, exposed credentials, and security incidents
            - dark_web_threat_monitoring: Monitor underground sources for entity mentions and potential threats
            - digital_forensics_analysis: Perform passive digital forensics analysis on online presence

            OSINT INVESTIGATION STRATEGY (EXA-DOMINATED):
            1. Start with exa_osint_comprehensive for broad digital footprint analysis with full content
            2. Use exa_public_records for deep dive into official records and business information
            3. Use exa_reputation_monitoring for comprehensive reputation analysis with full articles
            4. Use exa_osint_keyword for precise searches of specific identifiers or terms
            5. Use exa_find_similar_digital_assets to expand investigation to related entities
            6. Use domain_technical_analysis for technical infrastructure assessment
            7. Use breach_security_monitoring to identify security incidents and data exposure
            8. Use dark_web_threat_monitoring for threat intelligence and underground mentions
            9. Use digital_forensics_analysis for detailed technical assessment when needed
            10. ONLY use tavily_urgent_osint for immediate breaking developments (last resort)
            11. Always leverage full content extraction and highlights for comprehensive OSINT analysis

            KEY INVESTIGATION AREAS:
            - Digital Presence: Social media profiles, professional networks, online activity patterns
            - Public Records: Business registrations, government filings, directory listings
            - Reputation Intelligence: News coverage, reviews, sentiment analysis, controversy assessment
            - Technical Infrastructure: Domain analysis, hosting providers, SSL certificates, DNS records
            - Security Posture: Data breaches, exposed information, credential leaks, security incidents
            - Threat Intelligence: Dark web mentions, threat actor discussions, potential risks

            OPERATIONAL SECURITY & ETHICS:
            - Use only publicly available information - no unauthorized access or illegal methods
            - Maintain operational security to avoid attribution or detection
            - Verify findings across multiple independent sources before reporting
            - Document methodology and assess source reliability for each finding
            - Respect privacy laws and ethical boundaries in all investigations
            - Flag any suspicious or concerning activity patterns discovered
            """,
            name="osint_agent"
        )

    async def execute_task(self, task: ResearchTask, context: str = "") -> dict[str, Any]:
        """Execute OSINT investigation task with structured approach"""

        # Step 1: Extract OSINT investigation requirements
        osint_focus = self._extract_osint_focus(task.description, context)

        # Step 2: Gather OSINT data from multiple sources
        osint_data = await self._gather_osint_data(osint_focus)

        # Step 3: Perform digital investigation analysis
        osint_analysis = await self._perform_osint_analysis(osint_data, osint_focus)

        # Step 4: Structure results according to schema
        structured_results = await self._structure_osint_results(
            analysis=osint_analysis,
            schema=task.output_schema,
            task_description=task.description
        )

        return {
            "task_id": task.id,
            "results": structured_results,
            "citations": self._extract_citations(osint_data),
            "confidence": self._calculate_confidence(structured_results, osint_data)
        }

    def _extract_osint_focus(self, description: str, context: str) -> dict[str, Any]:
        """Extract what type of OSINT investigation is needed"""
        # Determine focus areas based on task description
        focus_areas = {
            "social_media": "social" in description.lower() or "media" in description.lower(),
            "digital_footprint": "digital" in description.lower() or "footprint" in description.lower(),
            "domain_analysis": "domain" in description.lower() or "website" in description.lower(),
            "public_records": "records" in description.lower() or "background" in description.lower(),
            "reputation": "reputation" in description.lower() or "sentiment" in description.lower(),
            "security": "security" in description.lower() or "breach" in description.lower(),
            "dark_web": "dark web" in description.lower() or "threat" in description.lower()
        }

        return {
            "entity_name": self._extract_entity_name(description, context),
            "entity_type": self._extract_entity_type(description, context),
            "focus_areas": [area for area, needed in focus_areas.items() if needed],
            "investigation_scope": "comprehensive" if len([a for a in focus_areas.values() if a]) > 3 else "targeted"
        }

    def _extract_entity_name(self, description: str, context: str) -> str:
        """Extract entity name from description or context"""
        # Simple extraction - in real implementation would use NLP
        words = description.split()
        for i, word in enumerate(words):
            if word.lower() in ["corp", "inc", "llc", "ltd", "company"]:
                if i > 0:
                    return f"{words[i-1]} {word}"

        # Look for person names (very basic)
        if any(keyword in description.lower() for keyword in ["person", "individual", "ceo", "founder"]):
            # Extract potential name
            for word in words:
                if word[0].isupper() and len(word) > 2:
                    return word

        return "Unknown Entity"

    def _extract_entity_type(self, description: str, context: str) -> str:
        """Extract entity type from description or context"""
        if any(keyword in description.lower() for keyword in ["corp", "company", "inc", "llc"]):
            return "company"
        elif any(keyword in description.lower() for keyword in ["person", "individual", "ceo", "founder"]):
            return "person"
        elif any(keyword in description.lower() for keyword in ["website", "domain", "platform"]):
            return "digital_asset"
        else:
            return "unknown"

    async def _gather_osint_data(self, osint_focus: dict[str, Any]) -> dict[str, Any]:
        """Gather OSINT data from multiple sources"""
        entity_name = osint_focus["entity_name"]
        osint_focus["entity_type"]
        focus_areas = osint_focus["focus_areas"]

        osint_data = {
            "social_media_profiles": [],
            "digital_footprint": {},
            "domain_information": {},
            "public_records": [],
            "reputation_data": {},
            "security_findings": {},
            "sources": []
        }

        # Gather data based on focus areas
        if "social_media" in focus_areas:
            # Mock social media data
            osint_data["social_media_profiles"] = [
                {
                    "platform": "LinkedIn",
                    "profile_url": f"linkedin.com/company/{entity_name.lower().replace(' ', '-')}",
                    "followers": 15420,
                    "activity_level": "Moderate",
                    "last_post": "2024-09-10"
                },
                {
                    "platform": "Twitter",
                    "profile_url": f"twitter.com/{entity_name.lower().replace(' ', '')}",
                    "followers": 8950,
                    "activity_level": "High",
                    "last_post": "2024-09-14"
                }
            ]

        if "digital_footprint" in focus_areas:
            # Mock digital footprint data
            osint_data["digital_footprint"] = {
                "websites": [f"{entity_name.lower().replace(' ', '')}.com"],
                "subdomains": 15,
                "email_patterns": [f"contact@{entity_name.lower().replace(' ', '')}.com"],
                "technologies": ["React", "AWS", "Cloudflare"],
                "ssl_status": "Valid",
                "hosting_provider": "AWS"
            }

        if "domain_analysis" in focus_areas:
            # Mock domain information
            osint_data["domain_information"] = {
                "registration_date": "2018-03-15",
                "expiration_date": "2025-03-15",
                "registrar": "GoDaddy",
                "privacy_protection": True,
                "dns_records": ["A", "MX", "TXT", "CNAME"]
            }

        if "public_records" in focus_areas:
            # Mock public records
            osint_data["public_records"] = [
                {
                    "type": "Business Registration",
                    "source": "Secretary of State",
                    "status": "Active",
                    "registration_date": "2018-03-15"
                },
                {
                    "type": "Tax Records",
                    "source": "IRS",
                    "status": "Current",
                    "last_filing": "2024-04-15"
                }
            ]

        if "reputation" in focus_areas:
            # Mock reputation data
            osint_data["reputation_data"] = {
                "overall_sentiment": "Positive",
                "news_mentions": 145,
                "positive_reviews": 78,
                "negative_reviews": 12,
                "neutral_coverage": 55
            }

        if "security" in focus_areas:
            # Mock security findings
            osint_data["security_findings"] = {
                "data_breaches": 0,
                "exposed_credentials": 0,
                "security_rating": "A-",
                "vulnerabilities": ["None detected"],
                "dark_web_mentions": 0
            }

        osint_data["sources"].extend([
            "Social Media Platforms",
            "Domain Registration Databases",
            "Public Records Repositories",
            "Security Intelligence Feeds"
        ])

        return osint_data

    async def _perform_osint_analysis(self, osint_data: dict, osint_focus: dict) -> dict[str, Any]:
        """Perform comprehensive OSINT analysis"""
        analysis = {
            "digital_presence": {},
            "security_posture": {},
            "reputation_assessment": {},
            "risk_indicators": {},
            "operational_security": {},
            "red_flags": [],
            "recommendations": []
        }

        # Analyze digital presence
        social_profiles = len(osint_data.get("social_media_profiles", []))
        analysis["digital_presence"] = {
            "social_media_coverage": "Comprehensive" if social_profiles >= 3 else "Limited",
            "website_presence": "Active" if osint_data.get("digital_footprint", {}).get("websites") else "Minimal",
            "brand_consistency": "Good",
            "online_activity": "Regular"
        }

        # Security posture assessment
        security_findings = osint_data.get("security_findings", {})
        analysis["security_posture"] = {
            "breach_history": "Clean" if security_findings.get("data_breaches", 0) == 0 else "Concerning",
            "exposed_data": "None" if security_findings.get("exposed_credentials", 0) == 0 else "Present",
            "security_rating": security_findings.get("security_rating", "Unknown"),
            "dark_web_presence": "None" if security_findings.get("dark_web_mentions", 0) == 0 else "Detected"
        }

        # Reputation assessment
        reputation = osint_data.get("reputation_data", {})
        analysis["reputation_assessment"] = {
            "overall_sentiment": reputation.get("overall_sentiment", "Unknown"),
            "media_coverage": "Positive" if reputation.get("positive_reviews", 0) > reputation.get("negative_reviews", 0) else "Mixed",
            "public_perception": "Favorable",
            "controversy_level": "Low"
        }

        # Risk indicators
        analysis["risk_indicators"] = {
            "privacy_protection": "Enabled" if osint_data.get("domain_information", {}).get("privacy_protection") else "Disabled",
            "information_exposure": "Minimal",
            "attack_surface": "Moderate",
            "opsec_practices": "Good"
        }

        # Identify red flags
        if security_findings.get("data_breaches", 0) > 0:
            analysis["red_flags"].append("Historical data breaches detected")

        if security_findings.get("dark_web_mentions", 0) > 0:
            analysis["red_flags"].append("Dark web mentions found")

        if reputation.get("negative_reviews", 0) > reputation.get("positive_reviews", 0):
            analysis["red_flags"].append("Predominantly negative online sentiment")

        # Recommendations
        analysis["recommendations"].extend([
            "Continue monitoring digital footprint regularly",
            "Implement comprehensive security awareness training",
            "Monitor brand mentions and sentiment trends"
        ])

        if not osint_data.get("domain_information", {}).get("privacy_protection"):
            analysis["recommendations"].append("Enable domain privacy protection")

        return analysis

    async def _structure_osint_results(self, analysis: dict, schema: dict, task_description: str) -> dict:
        """Structure OSINT analysis results according to task schema"""
        # Use LLM to structure results if schema is provided
        if schema:
            # Mock structured output - would use LLM in real implementation
            return {
                "osint_summary": analysis,
                "key_findings": [
                    "Strong digital presence across major platforms",
                    "Good security posture with no known breaches",
                    "Positive online reputation and sentiment"
                ],
                "risk_factors": [
                    "Moderate attack surface from digital presence",
                    "Potential for social engineering attacks"
                ],
                "recommendations": [
                    "Implement comprehensive digital monitoring",
                    "Regular security awareness training",
                    "Monitor brand reputation continuously"
                ]
            }
        else:
            return analysis

    def _extract_citations(self, osint_data: dict) -> list[str]:
        """Extract citations from OSINT data sources"""
        citations = []

        if osint_data.get("sources"):
            citations.extend(osint_data["sources"])

        if osint_data.get("social_media_profiles"):
            for profile in osint_data["social_media_profiles"]:
                citations.append(f"{profile['platform']} - {profile['profile_url']}")

        return citations

    def _calculate_confidence(self, results: dict, osint_data: dict) -> float:
        """Calculate confidence score based on data quality and source diversity"""
        confidence_factors = []

        # Data completeness
        if osint_data.get("social_media_profiles"):
            confidence_factors.append(0.25)
        if osint_data.get("digital_footprint"):
            confidence_factors.append(0.2)
        if osint_data.get("domain_information"):
            confidence_factors.append(0.15)
        if osint_data.get("public_records"):
            confidence_factors.append(0.2)
        if osint_data.get("security_findings"):
            confidence_factors.append(0.2)

        # Source diversity
        source_count = len(osint_data.get("sources", []))
        confidence_factors.append(min(source_count * 0.02, 0.1))

        return min(sum(confidence_factors), 1.0)
