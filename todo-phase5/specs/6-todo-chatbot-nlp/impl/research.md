# Research Document: Todo Chatbot with NLP + NeonDB

## R1: NLP Implementation Strategy

### Decision: Use rule-based NLP with keyword matching
**Rationale**: For a todo application with predictable commands (add, complete, delete, list), rule-based parsing is more reliable than ML-based approaches. It's deterministic, debuggable, and sufficient for the limited command vocabulary.
**Alternatives considered**:
- OpenAI GPT-based parsing (more flexible but less predictable)
- spaCy/NLTK advanced NLP (overkill for simple commands)
- Simple regex matching (too limited)

### Decision: Predefined intent classification
**Rationale**: Define specific intents (ADD_TASK, COMPLETE_TASK, DELETE_TASK, LIST_TASKS, UPDATE_TASK) with keyword patterns for reliable command recognition.
**Alternatives considered**:
- Machine learning classification (requires training data)
- Semantic similarity matching (computationally heavy)

## R2: Chatbot Integration Pattern

### Decision: API Gateway approach
**Rationale**: Create a dedicated chat endpoint that processes natural language, determines intent, and calls existing API endpoints. This preserves existing API structure while adding NLP layer.
**Alternatives considered**:
- Direct service integration (tight coupling)
- Separate microservice (unnecessary complexity for this scale)

## R3: Error Handling Framework

### Decision: Structured error responses with user-friendly messages
**Rationale**: Map technical errors to user-friendly messages while maintaining debug information for developers. Use consistent error response format.
**Alternatives considered**:
- Generic error messages (poor UX)
- Technical error exposure (security risk)

## R4: Serial Number to UUID Mapping Strategy

### Decision: Database VIEW-based mapping
**Rationale**: Use the existing `tasks_with_serial` VIEW to map between serial numbers (for users) and UUIDs (for internal operations). This ensures consistency and leverages existing infrastructure.
**Alternatives considered**:
- Cache-based mapping (adds complexity)
- Application-level mapping (duplicate logic)

## R5: Verification Query Strategy

### Decision: Immediate SELECT verification after each operation
**Rationale**: Execute a SELECT query immediately after each CRUD operation to confirm the database state matches expectations. This ensures reliability.
**Alternatives considered**:
- Eventual consistency checking (less reliable)
- No verification (violates requirements)