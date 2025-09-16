from typing import Any

from langchain_exa import ExaSearchResults, ExaSearchRetriever, ExaFindSimilarResults
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.config.settings import settings
from src.state.definitions import ResearchTask


class ResearchAgent:
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

        # Add comprehensive Exa tools if API key is valid
        if settings.has_exa_key:
            try:
                # Neural search for comprehensive, semantic research
                tools.append(ExaSearchResults(
                    name="exa_neural_search",
                    description="Perform deep neural search for comprehensive research using semantic understanding. Best for exploratory research and finding conceptually related content.",
                    num_results=15,
                    api_key=settings.exa_api_key,
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Auto search for optimal results without manual type selection
                tools.append(ExaSearchResults(
                    name="exa_auto_search",
                    description="Intelligent search that automatically chooses optimal search strategy (neural vs keyword). Use when unsure of best search approach.",
                    num_results=12,
                    api_key=settings.exa_api_key,
                    type="auto",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Keyword search for precise term matching
                tools.append(ExaSearchResults(
                    name="exa_keyword_search",
                    description="Traditional keyword search for exact term matching. Best for proper nouns, specific company names, or technical terms.",
                    num_results=10,
                    api_key=settings.exa_api_key,
                    type="keyword",
                    text_contents_options=True
                ))
                
                # Large-scale comprehensive search for due diligence
                tools.append(ExaSearchResults(
                    name="exa_comprehensive_search",
                    description="Large-scale search returning many results for comprehensive due diligence research. Use for thorough investigation.",
                    num_results=50,
                    api_key=settings.exa_api_key,
                    type="neural",
                    text_contents_options=True,
                    highlights=True
                ))
                
                # Find similar content for verification and expansion
                tools.append(ExaFindSimilarResults(
                    name="exa_find_similar",
                    description="Find content similar to a given URL for cross-verification and expanding research scope",
                    num_results=8,
                    api_key=settings.exa_api_key,
                    text_contents_options=True
                ))
                
                print("✅ Advanced Exa tool suite initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize Exa tools: {e}")

        # Add minimal Tavily for breaking news only
        if settings.has_tavily_key:
            try:
                tools.append(TavilySearchResults(
                    name="tavily_breaking_news",
                    description="ONLY for breaking news and real-time updates within last 24 hours. Use sparingly as auxiliary to main Exa research.",
                    max_results=3,
                    api_wrapper_kwargs={"api_key": settings.tavily_api_key}
                ))
                print("✅ Tavily auxiliary tool initialized")
            except Exception as e:
                print(f"Warning: Failed to initialize Tavily: {e}")

        # If no real tools available, add a dummy tool for testing
        if not tools:
            from langchain_core.tools import tool

            @tool
            def dummy_search(query: str) -> str:
                """Dummy search tool for development/testing"""
                return f"Mock search results for: {query}"

            tools.append(dummy_search)
            print("⚠️ Using dummy search tool - configure API keys for real functionality")

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are a research specialist focused on gathering accurate, comprehensive information for due diligence investigations.

            AVAILABLE TOOLS:
            - exa_neural_search: Primary tool for deep, semantic research with full content and highlights
            - exa_auto_search: Intelligent search that automatically optimizes search strategy
            - exa_keyword_search: For exact term matching (company names, technical terms, proper nouns)
            - exa_comprehensive_search: Large-scale search for thorough due diligence (50+ results)
            - exa_find_similar: Find similar content for verification and research expansion
            - tavily_breaking_news: ONLY for breaking news within 24 hours (use minimally)

            RESEARCH STRATEGY (EXA-FIRST APPROACH):
            1. Start with exa_auto_search for initial comprehensive research
            2. Use exa_neural_search for deeper semantic exploration of complex topics
            3. Use exa_keyword_search for specific entities, names, or technical terms
            4. Use exa_comprehensive_search for thorough due diligence requiring many sources
            5. Use exa_find_similar to expand research scope from high-quality sources found
            6. ONLY use tavily_breaking_news for immediate news updates (last resort)
            7. Always leverage full content and highlights from Exa results for detailed analysis

            FOCUS AREAS:
            - Corporate information: SEC filings, financial reports, business profiles
            - Legal matters: Court records, regulatory actions, compliance status  
            - Recent developments: News, press releases, market updates
            - Background verification: Company history, leadership, operations

            QUALITY STANDARDS:
            - Prioritize authoritative sources (government, regulatory, established media)
            - Provide specific citations with URLs
            - Note confidence levels and source reliability
            - Flag any contradictory information found between sources
            """,
            name="research_agent"
        )

    async def execute_task(self, task: ResearchTask, context: str = "") -> dict[str, Any]:
        """Execute research task with two-tier retrieval strategy"""

        # Step 1: Initial search and snippet analysis
        search_query = self._build_search_query(task.description, context)
        snippets = await self._search_snippets(search_query)

        # Step 2: Analyze snippets for relevance
        relevant_sources = await self._analyze_snippets(snippets, task)

        # Step 3: Deep content extraction from relevant sources
        detailed_content = await self._extract_detailed_content(relevant_sources)

        # Step 4: Structure results according to schema
        structured_results = await self._structure_results(
            content=detailed_content,
            schema=task.output_schema,
            task_description=task.description
        )

        return {
            "task_id": task.id,
            "results": structured_results,
            "citations": [source["url"] for source in relevant_sources],
            "confidence": self._calculate_confidence(structured_results, relevant_sources)
        }

    def _build_search_query(self, description: str, context: str) -> str:
        """Build optimized search query"""
        # Extract key terms and create focused query
        base_query = description
        if context:
            base_query += f" {context}"
        return base_query

    async def _search_snippets(self, query: str) -> list[dict]:
        """Search multiple sources for initial snippets"""
        # This would use the actual tools in practice
        # For now, return placeholder
        return [
            {"title": "Sample Result", "snippet": "Sample content", "url": "https://example.com"}
        ]

    async def _analyze_snippets(self, snippets: list[dict], task: ResearchTask) -> list[dict]:
        """Analyze snippets for relevance to task"""
        # Implement relevance scoring logic
        return snippets[:3]  # Return top 3 for now

    async def _extract_detailed_content(self, sources: list[dict]) -> str:
        """Extract detailed content from relevant sources"""
        # Implement content extraction
        return "Detailed research findings..."

    async def _structure_results(self, content: str, schema: dict, task_description: str) -> dict:
        """Structure results according to task schema"""
        # Use LLM to structure content according to schema
        return {"findings": content, "summary": "Research summary"}

    def _calculate_confidence(self, results: dict, sources: list[dict]) -> float:
        """Calculate confidence score based on source quality and consistency"""
        # Implement confidence calculation
        return 0.8
