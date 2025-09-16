# Implementation Plan: Due Diligence System v2.0

**Priority:** Strategic Tool Usage with Exa as Primary Engine
**Timeline:** 3 weeks
**Focus Areas:** Proper Tool Selection, Agent Specialization, System Operation

## Phase 1: Foundation Update (Week 1)

### 1.1 Python Runtime & Core Dependencies

- **Upgrade Python to 3.13.7** - Required for all other changes
- **Update LangGraph to 1.0+** - Zero breaking changes, just version bump
- **Update FastAPI to 0.116+** - Minor compatibility changes needed
- **Update Pydantic to 2.9+** - Enhanced typing, no breaking changes
- **Test all imports and basic functionality**

### 1.2 Exa API Integration & Tool Understanding

- **Update exa-py to 1.15.6** - Access to enhanced capabilities
- **Master Exa's four core tools:**
    - `search()` - Neural web search for discovery
    - `search_and_contents()` - Search with full content extraction
    - `find_similar()` - Find related content from URLs
    - `get_contents()` - Extract content from specific URLs
- **Understand autoprompt vs manual query construction**
- **Test each tool's strengths and appropriate use cases**

### 1.3 Tavily as Strategic Backup

- **Update tavily-python to 0.7.12** - Keep current for specific scenarios
- **Configure for specific use cases where Exa falls short:**
    - Real-time news and breaking information
    - Broad topic surveys when Exa is too focused
    - Specific database queries (court records, sanctions)
- **Test API connectivity and basic functionality**

### 1.4 CLI Framework Update

- **Update Rich to 14.0** - BREAKING CHANGE in color handling
- **Update Typer to 0.12+** - Enhanced CLI features
- **Test terminal output and fix display issues**

## Phase 2: Agent Specialization by Tool Strengths (Week 2)

### 2.1 Research Agent - Exa Neural Search Specialist

**Primary Exa Tools:** `search()` with autoprompt, `find_similar()`

- **Use Exa search() for initial entity discovery** - Neural search excels here
- **Leverage autoprompt for query optimization**
- **Use find_similar() to discover related entities and connections**
- **Tavily backup:** Only for real-time news about the entity
- **Focus:** Deep, intelligent entity discovery and relationship mapping

### 2.2 Financial Analysis Agent - Exa Content Extraction Master

**Primary Exa Tools:** `search_and_contents()`, `get_contents()`

- **Use Exa search_and_contents() for SEC filings and financial documents**
- **Use get_contents() to extract full text from financial reports**
- **Leverage Exa's ability to find high-quality financial sources**
- **Tavily backup:** Only for breaking financial news or market sentiment
- **Focus:** Deep financial document analysis and data extraction

### 2.3 Legal Compliance Agent - Strategic Tool Selection

**Primary Exa Tools:** `search()` for legal documents, `get_contents()` for extraction
**Strategic Tavily Use:** Court records, sanctions lists, regulatory databases

- **Use Exa for legal document discovery and case law research**
- **Use Tavily specifically for databases Exa doesn't index well**
- **Use Exa get_contents() for full legal document analysis**
- **Focus:** Comprehensive legal research with tool-specific strengths

### 2.4 OSINT Investigation Agent - Multi-Tool Strategy

**Primary Exa Tools:** `find_similar()` for relationship discovery, `search_and_contents()`
**Strategic Tavily Use:** Social media monitoring, domain-specific searches

- **Use Exa find_similar() to map entity relationships and connections**
- **Use Exa search_and_contents() for deep background research**
- **Use Tavily for specific OSINT databases and social platforms**
- **Focus:** Comprehensive background profiling using each tool's strengths

### 2.5 Verification Agent - Cross-Tool Validation

**Primary Exa Tools:** `find_similar()` for source verification
**Strategic Tavily Use:** Independent fact-checking

- **Use Exa find_similar() to find alternative sources for fact-checking**
- **Use Tavily for independent verification of Exa findings**
- **Compare results between tools to identify discrepancies**
- **Focus:** Quality assurance through strategic tool comparison

## Phase 3: System Integration (Week 3)

### 3.1 Intelligent Workflow Orchestration

- **Build agent routing based on optimal tool usage patterns**
- **Implement tool selection logic based on query type and data needs**
- **Create parallel execution where tools complement each other**
- **Add tool performance monitoring and optimization**

### 3.2 Session Management

- **Update session storage to track which tools were used for which insights**
- **Implement session resumability that preserves tool-specific context**
- **Add tool usage analytics and optimization suggestions**

### 3.3 Report Generation Engine

- **Design reports that show methodology and tool usage**
- **Create source attribution that identifies which tool found each insight**
- **Implement quality indicators based on tool strengths**
- **Add tool performance metrics to reports**

### 3.4 CLI Interface Updates

- **Add tool-specific status and performance indicators**
- **Show which agent is using which tool for what purpose**
- **Display tool usage optimization suggestions**
- **Add tool-specific diagnostics and health checks**

## Strategic Tool Usage Framework

### Exa Excels At:

- **Neural search for entity discovery** - Use `search()` with autoprompt
- **Deep content analysis** - Use `search_and_contents()` or `get_contents()`
- **Relationship mapping** - Use `find_similar()` for connections
- **High-quality source discovery** - Neural ranking finds better sources
- **Academic and professional content** - Better at authoritative sources

### Tavily Excels At:

- **Real-time information** - Breaking news and current events
- **Broad topic surveys** - When you need comprehensive coverage
- **Specific databases** - Court records, government databases
- **Social media and public sentiment** - Current discourse monitoring

### Agent Tool Strategy:

**Research Agent:** Exa `search()` + `find_similar()` for discovery, Tavily for news
**Financial Agent:** Exa `search_and_contents()` + `get_contents()` for documents, Tavily for market news
**Legal Agent:** Exa `search()` + `get_contents()` for legal docs, Tavily for court/regulatory databases
**OSINT Agent:** Exa `find_similar()` for relationships, Tavily for social/domain monitoring
**Verification Agent:** Exa `find_similar()` for source verification, Tavily for independent validation

## Critical Success Factors

### 1. Tool-Specific Optimization

- Each agent must use the optimal Exa tool for its specific task
- Understand when to use autoprompt vs manual queries
- Know when Tavily provides better data than Exa

### 2. Strategic Tool Selection

- Use Exa for deep, analytical research tasks
- Use Tavily for real-time, broad, or database-specific queries
- Never use tools redundantly - each should add unique value

### 3. Quality Through Specialization

- Agents produce better results by using tools strategically
- System demonstrates clear understanding of tool strengths
- Results show why each tool was chosen for each task

## Testing Strategy per Phase

### Phase 1 Testing

- Test each Exa tool individually with various query types
- Validate autoprompt effectiveness vs manual queries
- Test Tavily for specific backup scenarios
- Ensure all APIs work with new versions

### Phase 2 Testing

- Test each agent with its optimized tool selection strategy
- Validate that agents produce better results with specialized tools
- Test fallback scenarios and tool failure handling
- Compare results quality between strategic vs random tool usage

### Phase 3 Testing

- End-to-end workflows with intelligent tool routing
- Validate that system uses tools strategically across agents
- Test reporting shows clear tool usage methodology
- Performance testing with optimized tool usage patterns

## Success Criteria

1. **Each agent uses Exa tools strategically for maximum effectiveness**
2. **Tavily is used only where it provides superior data to Exa**
3. **System demonstrates clear understanding of tool strengths and weaknesses**
4. **Research quality improves through strategic tool selection**
5. **Reports show methodology and justify tool usage choices**

This plan focuses on using each tool for what it does best rather than defaulting everything to one tool.
