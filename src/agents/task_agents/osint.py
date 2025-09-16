from typing import Any

from langchain_core.tools import tool
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

        # Add OSINT research tools
        @tool
        def social_media_search(entity_name: str, platforms: str = "linkedin,twitter,facebook") -> str:
            """Search social media platforms for entity presence and activity"""
            # Mock implementation - would integrate with social media APIs
            return f"Social media search for {entity_name} on platforms: {platforms}"

        @tool
        def domain_analysis(domain: str) -> str:
            """Analyze domain registration, hosting, and technical details"""
            # Mock implementation - would integrate with WHOIS and domain analysis tools
            return f"Domain analysis for: {domain}"

        @tool
        def public_records_search(entity_name: str, location: str = "") -> str:
            """Search public records, directories, and government databases"""
            # Mock implementation - would integrate with public records APIs
            return f"Public records search for {entity_name} in {location}"

        @tool
        def breach_database_search(email_domain: str) -> str:
            """Check for data breaches and exposed information"""
            # Mock implementation - would integrate with breach monitoring services
            return f"Breach database search for domain: {email_domain}"

        @tool
        def news_sentiment_analysis(entity_name: str, timeframe: str = "1year") -> str:
            """Analyze news sentiment and media coverage"""
            # Mock implementation - would integrate with news analysis APIs
            return f"News sentiment analysis for {entity_name} over {timeframe}"

        @tool
        def digital_footprint_mapping(entity_name: str) -> str:
            """Map digital presence across websites, forums, and platforms"""
            # Mock implementation - would integrate with web crawling and analysis tools
            return f"Digital footprint mapping for: {entity_name}"

        @tool
        def reputation_monitoring(entity_name: str, sources: str = "all") -> str:
            """Monitor online reputation across review sites and forums"""
            # Mock implementation - would integrate with reputation monitoring services
            return f"Reputation monitoring for {entity_name} across {sources}"

        @tool
        def dark_web_monitoring(entity_name: str) -> str:
            """Monitor dark web mentions and potential threats"""
            # Mock implementation - would integrate with dark web monitoring services
            return f"Dark web monitoring for: {entity_name}"

        tools.extend([
            social_media_search,
            domain_analysis,
            public_records_search,
            breach_database_search,
            news_sentiment_analysis,
            digital_footprint_mapping,
            reputation_monitoring,
            dark_web_monitoring
        ])

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are an Open Source Intelligence (OSINT) specialist focused on comprehensive digital investigations.

            Your responsibilities:
            1. Conduct thorough social media and digital presence analysis
            2. Map digital footprints across platforms and websites
            3. Analyze domain ownership, hosting, and technical infrastructure
            4. Search public records, directories, and government databases
            5. Monitor online reputation and sentiment analysis
            6. Identify data breaches and exposed information
            7. Investigate dark web mentions and potential threats
            8. Assess cybersecurity posture and digital risks

            Use multiple OSINT sources and techniques for comprehensive coverage.
            Focus on publicly available information only - no illegal access.
            Verify information across multiple independent sources.
            Pay attention to operational security and attribution.
            Document methodology and source reliability.
            Identify potential security risks and digital threats.
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
