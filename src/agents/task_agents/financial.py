from typing import Any

from langchain_core.tools import tool
from langchain_exa import ExaSearchResults, ExaFindSimilarResults
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config.settings import settings
from src.state.definitions import ResearchTask


class FinancialAgent:
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

        # Add comprehensive Exa tools for financial analysis
        if settings.has_exa_key:
            try:
                # SEC filings neural search with full content
                tools.append(ExaSearchResults(
                    name="exa_sec_filings_neural",
                    description="Deep neural search for SEC filings with full content extraction. Best for comprehensive financial document analysis.",
                    num_results=20,
                    api_key=settings.exa_api_key,
                    include_domains=["sec.gov", "investor.gov", "edgar.sec.gov"],
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Financial data comprehensive search
                tools.append(ExaSearchResults(
                    name="exa_financial_comprehensive",
                    description="Large-scale financial research with full content from authoritative sources. For thorough financial due diligence.",
                    num_results=40,
                    api_key=settings.exa_api_key,
                    include_domains=["sec.gov", "finance.yahoo.com", "bloomberg.com", "marketwatch.com", "morningstar.com", "fool.com", "seekingalpha.com"],
                    type="auto",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Earnings and quarterly reports search
                tools.append(ExaSearchResults(
                    name="exa_earnings_reports",
                    description="Search for earnings calls, quarterly reports, and earnings analysis with full content",
                    num_results=15,
                    api_key=settings.exa_api_key,
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Financial keyword search for specific metrics/ratios
                tools.append(ExaSearchResults(
                    name="exa_financial_keyword",
                    description="Precise keyword search for specific financial metrics, ratios, or technical terms",
                    num_results=12,
                    api_key=settings.exa_api_key,
                    type="keyword",
                    text_contents_options=True
                ))
                
                # Find similar financial documents for verification
                tools.append(ExaFindSimilarResults(
                    name="exa_find_similar_financial",
                    description="Find similar financial documents for cross-verification and expanded analysis",
                    num_results=10,
                    api_key=settings.exa_api_key,
                    text_contents_options=True,
                    highlights=True
                ))
                
                print("✅ Advanced Exa financial tool suite initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize Exa financial tools: {e}")

        # Add minimal Tavily for immediate market updates only
        if settings.has_tavily_key:
            try:
                tools.append(TavilySearchResults(
                    name="tavily_urgent_market_updates",
                    description="ONLY for urgent market news and immediate financial updates within hours. Use minimally - Exa is primary source.",
                    max_results=3,
                    api_wrapper_kwargs={"api_key": settings.tavily_api_key}
                ))
                print("✅ Tavily auxiliary market tool initialized")
            except Exception as e:
                print(f"Warning: Failed to initialize Tavily market tool: {e}")

        # Add fallback tools if no APIs available
        if not tools:
            @tool
            def dummy_financial_search(query: str, entity_name: str = "") -> str:
                """Dummy financial search tool for development/testing"""
                return f"Mock financial search results for: {query} | Entity: {entity_name}"

            tools.append(dummy_financial_search)
            print("⚠️ Using dummy financial tools - configure API keys for real functionality")

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are a financial analysis specialist focused on comprehensive financial due diligence.

            AVAILABLE TOOLS:
            - exa_sec_filings_neural: Deep SEC filings search with full content extraction
            - exa_financial_comprehensive: Large-scale financial research (40+ results) with full content
            - exa_earnings_reports: Earnings calls and quarterly reports with full analysis
            - exa_financial_keyword: Precise search for specific financial metrics and ratios
            - exa_find_similar_financial: Cross-verification through similar financial documents
            - tavily_urgent_market_updates: ONLY for urgent market news (use minimally)

            FINANCIAL ANALYSIS STRATEGY (EXA-DOMINATED):
            1. Start with exa_financial_comprehensive for broad financial landscape analysis
            2. Use exa_sec_filings_neural for deep dive into official SEC documents with full content
            3. Use exa_earnings_reports for detailed earnings analysis and management commentary
            4. Use exa_financial_keyword for specific metrics, ratios, or technical financial terms
            5. Use exa_find_similar_financial to expand analysis through similar company comparisons
            6. ONLY use tavily_urgent_market_updates for breaking market news (last resort)
            7. Always leverage full content extraction and highlights for comprehensive financial analysis

            KEY FOCUS AREAS:
            - Financial Statements: Revenue, profit margins, cash flow, debt levels
            - SEC Filings: Material agreements, risk factors, management discussion
            - Market Performance: Stock performance, valuation metrics, analyst ratings
            - Financial Health: Liquidity ratios, debt-to-equity, working capital
            - Red Flags: Audit issues, restatements, regulatory actions, covenant violations

            QUALITY STANDARDS:
            - Prioritize official SEC filings over secondary sources
            - Extract specific financial metrics and ratios when available
            - Note filing dates and ensure data recency
            - Cross-verify key financial data from multiple sources
            - Flag any inconsistencies or concerning trends
            """,
            name="financial_agent"
        )

    async def execute_task(self, task: ResearchTask, context: str = "") -> dict[str, Any]:
        """Execute financial analysis task with structured approach"""

        # Step 1: Extract financial analysis requirements
        financial_focus = self._extract_financial_focus(task.description, context)

        # Step 2: Gather financial data from multiple sources
        financial_data = await self._gather_financial_data(financial_focus)

        # Step 3: Perform financial analysis
        analysis_results = await self._perform_financial_analysis(financial_data, financial_focus)

        # Step 4: Structure results according to schema
        structured_results = await self._structure_financial_results(
            analysis=analysis_results,
            schema=task.output_schema,
            task_description=task.description
        )

        return {
            "task_id": task.id,
            "results": structured_results,
            "citations": self._extract_citations(financial_data),
            "confidence": self._calculate_confidence(structured_results, financial_data)
        }

    def _extract_financial_focus(self, description: str, context: str) -> dict[str, Any]:
        """Extract what type of financial analysis is needed"""
        # Determine focus areas based on task description
        focus_areas = {
            "financial_statements": "financial statements" in description.lower() or "income statement" in description.lower(),
            "market_performance": "market" in description.lower() or "stock" in description.lower(),
            "credit_analysis": "credit" in description.lower() or "debt" in description.lower(),
            "valuation": "valuation" in description.lower() or "value" in description.lower(),
            "compliance": "compliance" in description.lower() or "sec" in description.lower()
        }

        return {
            "entity_name": self._extract_entity_name(description, context),
            "focus_areas": [area for area, needed in focus_areas.items() if needed],
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

    async def _gather_financial_data(self, financial_focus: dict[str, Any]) -> dict[str, Any]:
        """Gather financial data from multiple sources"""
        financial_focus["entity_name"]
        focus_areas = financial_focus["focus_areas"]

        financial_data = {
            "sec_filings": [],
            "market_data": {},
            "credit_info": {},
            "financial_statements": {},
            "sources": []
        }

        # Gather data based on focus areas
        if "financial_statements" in focus_areas:
            # Mock SEC filings data
            financial_data["sec_filings"] = [
                {"type": "10-K", "date": "2024-03-15", "summary": "Annual report"},
                {"type": "10-Q", "date": "2024-06-15", "summary": "Quarterly report"}
            ]

        if "market_performance" in focus_areas:
            # Mock market data
            financial_data["market_data"] = {
                "stock_price": 150.25,
                "market_cap": "50.2B",
                "pe_ratio": 18.5,
                "revenue_ttm": "12.5B"
            }

        if "credit_analysis" in focus_areas:
            # Mock credit information
            financial_data["credit_info"] = {
                "credit_rating": "A-",
                "debt_to_equity": 0.45,
                "current_ratio": 1.8
            }

        financial_data["sources"].extend([
            "SEC EDGAR Database",
            "Financial Markets Data",
            "Credit Rating Agencies"
        ])

        return financial_data

    async def _perform_financial_analysis(self, financial_data: dict, financial_focus: dict) -> dict[str, Any]:
        """Perform comprehensive financial analysis"""
        analysis = {
            "financial_health": {},
            "market_position": {},
            "risk_assessment": {},
            "key_metrics": {},
            "red_flags": [],
            "opportunities": []
        }

        # Analyze financial health
        if financial_data.get("credit_info"):
            credit_info = financial_data["credit_info"]
            analysis["financial_health"] = {
                "credit_rating": credit_info.get("credit_rating", "Not Available"),
                "liquidity": "Good" if credit_info.get("current_ratio", 0) > 1.5 else "Concerning",
                "leverage": "Moderate" if credit_info.get("debt_to_equity", 0) < 0.5 else "High"
            }

        # Analyze market position
        if financial_data.get("market_data"):
            market_data = financial_data["market_data"]
            analysis["market_position"] = {
                "market_cap": market_data.get("market_cap", "Unknown"),
                "valuation": "Reasonable" if market_data.get("pe_ratio", 0) < 25 else "High",
                "size": "Large Cap" if "B" in str(market_data.get("market_cap", "")) else "Small/Mid Cap"
            }

        # Risk assessment
        analysis["risk_assessment"] = {
            "financial_risk": "Low to Moderate",
            "market_risk": "Moderate",
            "regulatory_risk": "Low"
        }

        # Key financial metrics
        analysis["key_metrics"] = {
            "revenue_growth": "Stable",
            "profitability": "Profitable",
            "debt_levels": "Manageable"
        }

        return analysis

    async def _structure_financial_results(self, analysis: dict, schema: dict, task_description: str) -> dict:
        """Structure financial analysis results according to task schema"""
        # Use LLM to structure results if schema is provided
        if schema:
            # Mock structured output - would use LLM in real implementation
            return {
                "financial_summary": analysis,
                "key_findings": [
                    "Company shows stable financial performance",
                    "Credit rating indicates good financial health",
                    "Market position is strong in sector"
                ],
                "risk_factors": [
                    "Market volatility exposure",
                    "Regulatory changes impact"
                ],
                "recommendations": [
                    "Monitor debt levels quarterly",
                    "Track market performance trends"
                ]
            }
        else:
            return analysis

    def _extract_citations(self, financial_data: dict) -> list[str]:
        """Extract citations from financial data sources"""
        citations = []

        if financial_data.get("sources"):
            citations.extend(financial_data["sources"])

        if financial_data.get("sec_filings"):
            for filing in financial_data["sec_filings"]:
                citations.append(f"SEC Filing {filing['type']} - {filing['date']}")

        return citations

    def _calculate_confidence(self, results: dict, financial_data: dict) -> float:
        """Calculate confidence score based on data quality and completeness"""
        confidence_factors = []

        # Data completeness
        if financial_data.get("sec_filings"):
            confidence_factors.append(0.3)
        if financial_data.get("market_data"):
            confidence_factors.append(0.25)
        if financial_data.get("credit_info"):
            confidence_factors.append(0.25)

        # Source reliability
        reliable_sources = len(financial_data.get("sources", []))
        confidence_factors.append(min(reliable_sources * 0.05, 0.2))

        return min(sum(confidence_factors), 1.0)
