from typing import Any

from langchain_exa import ExaSearchResults
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

        # Only add Exa if API key is valid
        if settings.exa_api_key and settings.exa_api_key != "your_exa_key_here":
            try:
                tools.append(ExaSearchResults(
                    num_results=10,
                    api_key=settings.exa_api_key
                ))
            except Exception as e:
                print(f"Warning: Failed to initialize Exa: {e}")

        # If no real tools available, add a dummy tool for testing
        if not tools:
            from langchain_core.tools import tool

            @tool
            def dummy_search(query: str) -> str:
                """Dummy search tool for development/testing"""
                return f"Mock search results for: {query}"

            tools.append(dummy_search)

        return tools

    def create_agent(self):
        return create_react_agent(
            model=self.model,
            tools=self.tools,
            prompt="""You are a research specialist focused on gathering accurate information.

            Your responsibilities:
            1. Conduct thorough web research using available tools
            2. Verify information from multiple sources
            3. Extract structured data according to task schema
            4. Provide clear citations for all findings
            5. Focus on factual, verifiable information

            Always use multiple search tools to cross-verify findings.
            Prioritize recent, authoritative sources.
            Be thorough but concise in your research.
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
