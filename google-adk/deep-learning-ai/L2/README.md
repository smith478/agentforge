## ADK Primitives

ADK hides much of the complexity, but we often need lower level access for customization.

### Session
This is the current conversation thread. Here's a simple example of how this is managed:
```python
from google.adk.sessions import InMemorySessionService

# The runner is configured with a service to manage sessions
session_service = InMemorySessionService()
session = await session_service.create_session(
    app_name="my_app", user_id="user_123"
)
```

### State
The session's short term scratchpad. It is stored as a set of key-value pairs that captures key parts of the context. You can write any info to the state and it will be accessible to your tools.

### Memory
Long-term memory for your agent