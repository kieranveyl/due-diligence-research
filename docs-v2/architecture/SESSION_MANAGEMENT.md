# Session Management & Persistence Layer

## Overview

This document defines the comprehensive session management and persistence architecture for the Due Diligence system, enabling resumable research sessions, state management, and long-term data retention across user interactions.

## Core Session Architecture

### 1. Session Lifecycle Management

```python
class SessionManager:
    """Manages complete lifecycle of research sessions"""
    
    def __init__(self):
        self.session_store = SessionStore()
        self.state_manager = StateManager()
        self.persistence_manager = PersistenceManager()
        self.session_cache = SessionCache()
    
    async def create_session(
        self, 
        query: str, 
        user_preferences: UserPreferences
    ) -> ResearchSession:
        """Create new research session"""
        
        session_id = self._generate_session_id(query)
        
        session = ResearchSession(
            session_id=session_id,
            query=query,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            phase=ResearchPhase.INITIALIZING,
            user_preferences=user_preferences,
            status=SessionStatus.ACTIVE
        )
        
        # Persist initial session state
        await self.session_store.save_session(session)
        
        # Initialize real-time state tracking
        await self.state_manager.initialize_session_state(session_id)
        
        return session
    
    async def resume_session(self, session_id: str) -> ResearchSession:
        """Resume existing research session"""
        
        # Load session from persistent storage
        session = await self.session_store.load_session(session_id)
        
        if not session:
            raise SessionNotFoundError(f"Session {session_id} not found")
        
        if session.status == SessionStatus.COMPLETED:
            raise SessionError("Cannot resume completed session")
        
        # Restore session state
        await self.state_manager.restore_session_state(session)
        
        # Update session timestamp
        session.updated_at = datetime.utcnow()
        session.status = SessionStatus.ACTIVE
        
        await self.session_store.save_session(session)
        
        return session
    
    async def pause_session(self, session_id: str) -> None:
        """Pause active research session"""
        
        session = await self.session_store.load_session(session_id)
        session.status = SessionStatus.PAUSED
        session.updated_at = datetime.utcnow()
        
        # Save current state snapshot
        await self.state_manager.create_checkpoint(session_id)
        
        # Persist session
        await self.session_store.save_session(session)
    
    async def complete_session(
        self, 
        session_id: str, 
        final_report: Report
    ) -> None:
        """Mark session as completed with final results"""
        
        session = await self.session_store.load_session(session_id)
        session.status = SessionStatus.COMPLETED
        session.completed_at = datetime.utcnow()
        session.updated_at = datetime.utcnow()
        session.final_report = final_report
        
        # Create final checkpoint
        await self.state_manager.create_checkpoint(session_id, is_final=True)
        
        # Archive session data
        await self.persistence_manager.archive_session(session)
        
        # Clean up real-time state
        await self.state_manager.cleanup_session_state(session_id)

class SessionStatus(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"

@dataclass
class ResearchSession:
    """Complete research session state"""
    session_id: str
    query: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    
    # Session state
    phase: ResearchPhase
    status: SessionStatus
    
    # Research plan and execution
    research_plan: Optional[TaskDependencyGraph] = None
    execution_graph: Optional[ExecutionGraph] = None
    
    # Agent states and results
    agent_states: Dict[str, AgentState] = field(default_factory=dict)
    agent_results: Dict[str, AgentResult] = field(default_factory=dict)
    
    # Progress tracking
    overall_progress: float = 0.0
    current_phase_progress: float = 0.0
    estimated_completion: Optional[datetime] = None
    
    # User interaction
    user_preferences: UserPreferences
    plan_approved: bool = False
    plan_modifications: List[PlanModification] = field(default_factory=list)
    
    # Results and conflicts
    partial_results: Dict[str, Any] = field(default_factory=dict)
    conflicts: List[Conflict] = field(default_factory=list)
    final_report: Optional[Report] = None
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    file_paths: Dict[str, str] = field(default_factory=dict)  # report files, etc.
```

### 2. Multi-Layer Persistence Architecture

```python
class PersistenceManager:
    """Manages data persistence across multiple storage layers"""
    
    def __init__(self):
        # Hot storage - Redis for active sessions
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db
        )
        
        # Warm storage - SQLite for session metadata and history
        self.db_manager = DatabaseManager()
        
        # Cold storage - File system for large data and reports
        self.file_manager = FileManager()
        
        # Cache layer - In-memory for frequently accessed data
        self.cache = SessionCache()
    
    async def save_session_state(
        self, 
        session_id: str, 
        state_data: Dict[str, Any]
    ) -> None:
        """Save session state to appropriate storage layer"""
        
        # Real-time state to Redis
        await self.redis_client.hset(
            f"session:{session_id}:state",
            mapping=state_data
        )
        
        # Set expiration for active session cleanup
        await self.redis_client.expire(
            f"session:{session_id}:state",
            timedelta(hours=24)  # Active session TTL
        )
    
    async def save_session_metadata(self, session: ResearchSession) -> None:
        """Save session metadata to database"""
        
        session_data = {
            'session_id': session.session_id,
            'query': session.query,
            'created_at': session.created_at,
            'updated_at': session.updated_at,
            'completed_at': session.completed_at,
            'phase': session.phase.value,
            'status': session.status.value,
            'overall_progress': session.overall_progress,
            'user_preferences': session.user_preferences.model_dump_json(),
            'tags': json.dumps(session.tags),
            'notes': session.notes
        }
        
        await self.db_manager.upsert_session(session_data)
    
    async def save_agent_results(
        self, 
        session_id: str, 
        agent_id: str, 
        results: AgentResult
    ) -> None:
        """Save agent results to appropriate storage"""
        
        # Large result data to file storage
        if results.data_size > 1024 * 1024:  # > 1MB
            file_path = await self.file_manager.save_agent_data(
                session_id, agent_id, results.data
            )
            
            # Store file reference in database
            await self.db_manager.save_agent_result_reference(
                session_id, agent_id, file_path, results.metadata
            )
        else:
            # Small results directly to database
            await self.db_manager.save_agent_result(
                session_id, agent_id, results
            )
    
    async def archive_session(self, session: ResearchSession) -> None:
        """Archive completed session to long-term storage"""
        
        # Create archive package
        archive_data = {
            'session_metadata': session,
            'agent_results': session.agent_results,
            'final_report': session.final_report,
            'conflicts': session.conflicts,
            'execution_history': await self._get_execution_history(session.session_id)
        }
        
        # Save to archive storage
        archive_path = await self.file_manager.create_session_archive(
            session.session_id, archive_data
        )
        
        # Update database with archive location
        await self.db_manager.update_session_archive_path(
            session.session_id, archive_path
        )
        
        # Clean up active storage
        await self._cleanup_active_session_data(session.session_id)
```

### 3. Real-Time State Management

```python
class StateManager:
    """Manages real-time session state and agent coordination"""
    
    def __init__(self):
        self.redis_client = redis.Redis()
        self.state_cache = {}
        self.state_locks = {}
    
    async def update_agent_state(
        self, 
        session_id: str, 
        agent_id: str, 
        state_update: AgentStateUpdate
    ) -> None:
        """Update agent state with coordination locking"""
        
        # Acquire lock for state consistency
        async with self._get_state_lock(session_id):
            
            # Get current session state
            session_state = await self.get_session_state(session_id)
            
            # Update agent state
            session_state.agent_states[agent_id] = AgentState(
                agent_id=agent_id,
                status=state_update.status,
                progress=state_update.progress,
                current_task=state_update.current_task,
                last_updated=datetime.utcnow(),
                error_info=state_update.error_info
            )
            
            # Recalculate overall progress
            session_state.overall_progress = self._calculate_overall_progress(
                session_state.agent_states
            )
            
            # Persist updated state
            await self._persist_session_state(session_id, session_state)
            
            # Broadcast state update
            await self._broadcast_state_update(session_id, state_update)
    
    async def add_partial_result(
        self, 
        session_id: str, 
        agent_id: str, 
        result_data: Dict[str, Any]
    ) -> None:
        """Add partial result from agent"""
        
        result_key = f"session:{session_id}:results:{agent_id}"
        
        # Append to agent's result stream
        await self.redis_client.lpush(
            f"{result_key}:stream",
            json.dumps({
                'timestamp': datetime.utcnow().isoformat(),
                'data': result_data
            })
        )
        
        # Update consolidated results
        await self.redis_client.hset(
            f"{result_key}:consolidated",
            mapping=result_data
        )
        
        # Notify UI of new results
        await self._notify_partial_results(session_id, agent_id, result_data)
    
    async def detect_conflicts(self, session_id: str) -> List[Conflict]:
        """Detect conflicts in real-time as results come in"""
        
        # Get all agent results so far
        all_results = await self.get_all_agent_results(session_id)
        
        # Run conflict detection
        conflict_detector = ConflictDetector()
        conflicts = conflict_detector.detect_conflicts(all_results)
        
        # Store new conflicts
        if conflicts:
            await self.redis_client.lpush(
                f"session:{session_id}:conflicts",
                *[json.dumps(conflict.model_dump()) for conflict in conflicts]
            )
            
            # Notify UI of conflicts
            await self._notify_conflicts(session_id, conflicts)
        
        return conflicts
    
    async def create_checkpoint(
        self, 
        session_id: str, 
        is_final: bool = False
    ) -> str:
        """Create state checkpoint for recovery"""
        
        checkpoint_id = f"{session_id}_{datetime.utcnow().isoformat()}"
        
        # Capture complete session state
        session_state = await self.get_session_state(session_id)
        agent_states = await self.get_all_agent_states(session_id)
        partial_results = await self.get_all_partial_results(session_id)
        
        checkpoint_data = {
            'checkpoint_id': checkpoint_id,
            'session_state': session_state.model_dump(),
            'agent_states': {k: v.model_dump() for k, v in agent_states.items()},
            'partial_results': partial_results,
            'created_at': datetime.utcnow().isoformat(),
            'is_final': is_final
        }
        
        # Save checkpoint
        await self.redis_client.hset(
            f"session:{session_id}:checkpoints",
            checkpoint_id,
            json.dumps(checkpoint_data)
        )
        
        # Keep only last 10 checkpoints for space efficiency
        await self._cleanup_old_checkpoints(session_id)
        
        return checkpoint_id
    
    async def restore_from_checkpoint(
        self, 
        session_id: str, 
        checkpoint_id: str
    ) -> None:
        """Restore session state from checkpoint"""
        
        # Load checkpoint data
        checkpoint_data = await self.redis_client.hget(
            f"session:{session_id}:checkpoints",
            checkpoint_id
        )
        
        if not checkpoint_data:
            raise CheckpointNotFoundError(f"Checkpoint {checkpoint_id} not found")
        
        checkpoint = json.loads(checkpoint_data)
        
        # Restore session state
        session_state = SessionState.model_validate(checkpoint['session_state'])
        await self._persist_session_state(session_id, session_state)
        
        # Restore agent states
        for agent_id, agent_state_data in checkpoint['agent_states'].items():
            agent_state = AgentState.model_validate(agent_state_data)
            await self._persist_agent_state(session_id, agent_id, agent_state)
        
        # Restore partial results
        for agent_id, results in checkpoint['partial_results'].items():
            await self._restore_partial_results(session_id, agent_id, results)
```

### 4. Database Schema & Management

```python
class DatabaseManager:
    """Manages SQLite database for session metadata and history"""
    
    def __init__(self):
        self.db_path = settings.database_path
        self.connection_pool = sqlite3.ConnectionPool(self.db_path)
    
    async def initialize_database(self):
        """Initialize database schema"""
        
        schema_sql = """
        -- Sessions table
        CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            query TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            completed_at TIMESTAMP,
            phase TEXT NOT NULL,
            status TEXT NOT NULL,
            overall_progress REAL DEFAULT 0.0,
            user_preferences TEXT,
            tags TEXT,
            notes TEXT,
            archive_path TEXT,
            
            -- Indexing for fast lookups
            INDEX idx_sessions_created_at ON sessions(created_at),
            INDEX idx_sessions_status ON sessions(status),
            INDEX idx_sessions_query_text ON sessions(query)
        );
        
        -- Agent results table
        CREATE TABLE IF NOT EXISTS agent_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            result_type TEXT NOT NULL,
            file_path TEXT,
            metadata TEXT,
            confidence_score REAL,
            created_at TIMESTAMP NOT NULL,
            
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            INDEX idx_agent_results_session ON agent_results(session_id),
            INDEX idx_agent_results_agent ON agent_results(agent_id)
        );
        
        -- Conflicts table
        CREATE TABLE IF NOT EXISTS conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            conflict_type TEXT NOT NULL,
            entity TEXT NOT NULL,
            finding1_agent TEXT NOT NULL,
            finding2_agent TEXT NOT NULL,
            severity TEXT NOT NULL,
            resolution_strategy TEXT,
            resolved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP NOT NULL,
            
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            INDEX idx_conflicts_session ON conflicts(session_id),
            INDEX idx_conflicts_resolved ON conflicts(resolved)
        );
        
        -- Execution history table
        CREATE TABLE IF NOT EXISTS execution_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            agent_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_data TEXT,
            timestamp TIMESTAMP NOT NULL,
            
            FOREIGN KEY (session_id) REFERENCES sessions(session_id),
            INDEX idx_execution_history_session ON execution_history(session_id),
            INDEX idx_execution_history_timestamp ON execution_history(timestamp)
        );
        """
        
        async with self.connection_pool.acquire() as conn:
            await conn.executescript(schema_sql)
    
    async def get_session_history(
        self, 
        limit: int = 50, 
        status_filter: Optional[SessionStatus] = None
    ) -> List[SessionSummary]:
        """Get session history with optional filtering"""
        
        query = """
        SELECT session_id, query, created_at, completed_at, status, 
               overall_progress, tags
        FROM sessions
        """
        
        params = []
        if status_filter:
            query += " WHERE status = ?"
            params.append(status_filter.value)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        async with self.connection_pool.acquire() as conn:
            cursor = await conn.execute(query, params)
            rows = await cursor.fetchall()
            
            return [
                SessionSummary(
                    session_id=row[0],
                    query=row[1],
                    created_at=datetime.fromisoformat(row[2]),
                    completed_at=datetime.fromisoformat(row[3]) if row[3] else None,
                    status=SessionStatus(row[4]),
                    overall_progress=row[5],
                    tags=json.loads(row[6]) if row[6] else []
                )
                for row in rows
            ]
    
    async def search_sessions(
        self, 
        search_query: str, 
        limit: int = 20
    ) -> List[SessionSummary]:
        """Search sessions by query text"""
        
        query = """
        SELECT session_id, query, created_at, completed_at, status, 
               overall_progress, tags
        FROM sessions
        WHERE query LIKE ? OR notes LIKE ?
        ORDER BY created_at DESC
        LIMIT ?
        """
        
        search_pattern = f"%{search_query}%"
        
        async with self.connection_pool.acquire() as conn:
            cursor = await conn.execute(
                query, [search_pattern, search_pattern, limit]
            )
            rows = await cursor.fetchall()
            
            return [
                SessionSummary(
                    session_id=row[0],
                    query=row[1],
                    created_at=datetime.fromisoformat(row[2]),
                    completed_at=datetime.fromisoformat(row[3]) if row[3] else None,
                    status=SessionStatus(row[4]),
                    overall_progress=row[5],
                    tags=json.loads(row[6]) if row[6] else []
                )
                for row in rows
            ]
```

### 5. File Storage Management

```python
class FileManager:
    """Manages file storage for reports, large data, and archives"""
    
    def __init__(self):
        self.base_path = Path(settings.data_directory)
        self.reports_path = self.base_path / "reports"
        self.agent_data_path = self.base_path / "agent_data"
        self.archives_path = self.base_path / "archives"
        self.temp_path = self.base_path / "temp"
        
        # Ensure directories exist
        for path in [self.reports_path, self.agent_data_path, 
                     self.archives_path, self.temp_path]:
            path.mkdir(parents=True, exist_ok=True)
    
    async def save_report(
        self, 
        session_id: str, 
        report: Report, 
        format: ReportFormat
    ) -> str:
        """Save research report to file system"""
        
        # Generate filename based on session and entity
        entity_name = self._extract_entity_name(report.title)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == ReportFormat.MARKDOWN:
            filename = f"{entity_name}_{timestamp}.md"
            file_path = self.reports_path / filename
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(report.content)
        
        elif format == ReportFormat.PDF:
            filename = f"{entity_name}_{timestamp}.pdf"
            file_path = self.reports_path / filename
            
            # Convert markdown to PDF using WeasyPrint
            from weasyprint import HTML, CSS
            
            html_content = self._markdown_to_html(report.content)
            HTML(string=html_content).write_pdf(file_path)
        
        return str(file_path)
    
    async def save_agent_data(
        self, 
        session_id: str, 
        agent_id: str, 
        data: Dict[str, Any]
    ) -> str:
        """Save large agent data to file storage"""
        
        # Create directory for session if it doesn't exist
        session_dir = self.agent_data_path / session_id
        session_dir.mkdir(exist_ok=True)
        
        # Save data as compressed JSON
        filename = f"{agent_id}_{datetime.now().isoformat()}.json.gz"
        file_path = session_dir / filename
        
        with gzip.open(file_path, 'wt', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        return str(file_path)
    
    async def create_session_archive(
        self, 
        session_id: str, 
        archive_data: Dict[str, Any]
    ) -> str:
        """Create compressed archive of complete session"""
        
        archive_filename = f"session_{session_id}_{datetime.now().strftime('%Y%m%d')}.tar.gz"
        archive_path = self.archives_path / archive_filename
        
        # Create temporary directory for archive contents
        temp_dir = self.temp_path / f"archive_{session_id}"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # Save all archive data to temp directory
            metadata_file = temp_dir / "session_metadata.json"
            with open(metadata_file, 'w') as f:
                json.dump(archive_data, f, indent=2, default=str)
            
            # Copy report files if they exist
            if 'final_report' in archive_data and archive_data['final_report']:
                report_files = archive_data['final_report'].get('file_paths', {})
                for format_type, file_path in report_files.items():
                    if os.path.exists(file_path):
                        shutil.copy2(file_path, temp_dir / f"report.{format_type}")
            
            # Create compressed archive
            with tarfile.open(archive_path, 'w:gz') as tar:
                tar.add(temp_dir, arcname=session_id)
            
        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir, ignore_errors=True)
        
        return str(archive_path)
    
    async def cleanup_old_files(self, retention_days: int = 90) -> None:
        """Clean up old temporary files and archives"""
        
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        # Clean up temp files
        for file_path in self.temp_path.glob("*"):
            if file_path.stat().st_mtime < cutoff_date.timestamp():
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    shutil.rmtree(file_path, ignore_errors=True)
        
        # Archive old agent data
        for session_dir in self.agent_data_path.iterdir():
            if session_dir.is_dir():
                # Check if session is completed and old enough
                session_id = session_dir.name
                session_metadata = await self._get_session_metadata(session_id)
                
                if (session_metadata and 
                    session_metadata.status == SessionStatus.COMPLETED and
                    session_metadata.completed_at < cutoff_date):
                    
                    # Move to archives if not already archived
                    if not session_metadata.archive_path:
                        await self._archive_old_session_data(session_id, session_dir)
```

### 6. Cache Management

```python
class SessionCache:
    """In-memory cache for frequently accessed session data"""
    
    def __init__(self):
        self.cache = {}
        self.cache_stats = CacheStats()
        self.max_size = 1000  # Maximum sessions to cache
        self.ttl = timedelta(minutes=30)  # Cache TTL
    
    def get_session(self, session_id: str) -> Optional[ResearchSession]:
        """Get session from cache"""
        
        if session_id in self.cache:
            cached_item = self.cache[session_id]
            
            # Check if cache entry is still valid
            if datetime.utcnow() - cached_item.cached_at < self.ttl:
                self.cache_stats.hits += 1
                return cached_item.session
            else:
                # Remove expired entry
                del self.cache[session_id]
        
        self.cache_stats.misses += 1
        return None
    
    def put_session(self, session: ResearchSession) -> None:
        """Put session in cache"""
        
        # Remove oldest entries if cache is full
        if len(self.cache) >= self.max_size:
            self._evict_oldest()
        
        self.cache[session.session_id] = CachedSession(
            session=session,
            cached_at=datetime.utcnow()
        )
    
    def invalidate_session(self, session_id: str) -> None:
        """Remove session from cache"""
        self.cache.pop(session_id, None)
    
    def _evict_oldest(self) -> None:
        """Evict oldest cache entries"""
        if not self.cache:
            return
        
        # Sort by cache time and remove oldest 10%
        sorted_items = sorted(
            self.cache.items(),
            key=lambda x: x[1].cached_at
        )
        
        evict_count = max(1, len(sorted_items) // 10)
        for session_id, _ in sorted_items[:evict_count]:
            del self.cache[session_id]

@dataclass
class CachedSession:
    session: ResearchSession
    cached_at: datetime

@dataclass
class CacheStats:
    hits: int = 0
    misses: int = 0
    
    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
```

## Integration with CLI Commands

### Session Management Commands

```python
# CLI command implementations using the session management system

@click.group()
def sessions():
    """Session management commands"""
    pass

@sessions.command()
@click.option('--limit', default=20, help='Number of sessions to show')
@click.option('--status', type=click.Choice(['active', 'paused', 'completed', 'failed']), 
              help='Filter by status')
def list(limit: int, status: Optional[str]):
    """List previous research sessions"""
    
    session_manager = SessionManager()
    status_filter = SessionStatus(status) if status else None
    
    session_history = await session_manager.get_session_history(
        limit=limit, 
        status_filter=status_filter
    )
    
    # Display using Rich tables
    display_session_list(session_history)

@sessions.command()
@click.argument('session_id')
def status(session_id: str):
    """Show detailed status of a research session"""
    
    session_manager = SessionManager()
    session = await session_manager.load_session(session_id)
    
    if not session:
        click.echo(f"Session {session_id} not found")
        return
    
    # Display detailed session status
    display_session_status(session)

@sessions.command()
@click.argument('session_id')
def resume(session_id: str):
    """Resume a paused research session"""
    
    session_manager = SessionManager()
    orchestration_engine = OrchestrationEngine()
    
    try:
        session = await session_manager.resume_session(session_id)
        
        # Continue execution from where it left off
        await orchestration_engine.resume_execution(session)
        
    except SessionNotFoundError:
        click.echo(f"Session {session_id} not found")
    except SessionError as e:
        click.echo(f"Cannot resume session: {e}")
```

This comprehensive session management system provides robust state persistence, efficient caching, and seamless resume functionality that enables users to work with long-running research tasks across multiple CLI sessions.