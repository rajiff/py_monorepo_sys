
3. Database Connectivity and the Request/Response Cycle

Understanding the strict chronology of database connectivity within a Python ASGI framework like FastAPI is essential for performance tuning and preventing database socket exhaustion.
The lifecycle splits cleanly into two distinct operational layers:

Phase A: Application Initialization Lifecycle (One-Time Event)

When you run uvicorn app.main:app, the statement create_async_engine(...) executes globally.
• No physical database connections are made yet.
• SQLAlchemy creates a logical configuration placeholder wrapper (the engine). The connection pool initializes at a size of zero by default until incoming traffic forces an initialization burst.

Phase B: The Request/Response Loop (Per HTTP Request)

When an HTTP request strikes an endpoint containing your Depends(get_db) hook, the lifecycle executes in this sequence:


```text
[ Client HTTP Request ]
         │
         ▼
 1. FastAPI maps route and executes Dependencies
         │
         ▼
 2. `get_db` generator starts: `async with AsyncSessionLocal()` is invoked
         │
         ▼
 3. Session contacts the Engine Pool -> Asks for an active socket
         │
   ┌─────┴────────────────────────────────────────┐
   │ Is an idle connection available in pool?    │
   ├──────────────────────┬───────────────────────┤
   │ YES                  │ NO                    │
   ▼                      ▼                       ▼
Pool hands connection  Pool spins up a new     If pool is full, waits
instantly (0ms cost).  TCP socket over wire    up to `POOL_TIMEOUT`
                       (adds slight overhead). before throwing 500 error.
   │                      │                       │
   └──────────────────────┼───────────────────────┘
                          ▼
 4. Active operational Context Session is injected into route
         │
         ▼
 5. Route logic processes data queries: `await session.execute(...)`
         │
         ▼
 6. Route finishes and compiles the outgoing Response dictionary
         │
         ▼
 7. `finally:` block executes in `get_db` -> `await session.close()`
         │
         ▼
 8. TCP Socket is NOT closed or destroyed!
    It is instantly dropped back into the engine connection pool queue.
         │
         ▼
[ Client HTTP Response Received ]

```
