

## Scaling: calculate pool capacity across the deployment
The total application-side connection budget is approximately:
$$C_{\max} = R \times W \times (P + O)$$

To calculate the maximum value ($C_{\max}$), you must define the following variables:

*   **$C_{\max}$**: Maximum overall capacity.
*   **$R$**: Total rate of data flow per second.
*   **$W$**: Window sizing metric.
*   **$P$**: Processing time constants.
*   **$O$**: Overhead margin allocations.


## Reference Reading for maintaing better database infrastructure

1. FastAPI: Lifespan events
    - Understand startup and shutdown, and how to manage resources shared across requests.
    - [Read FastAPI lifespan documentation](https://fastapi.tiangolo.com/advanced/events/)

2. SQLAlchemy: Asyncio extension
    - Study create_async_engine, async_sessionmaker, session cleanup, transaction usage, and await engine.dispose().
    - [Read SQLAlchemy asyncio documentation](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

3. SQLAlchemy: Connection pooling
    - Understand pool sizing, overflow, acquisition timeouts, pre-ping, recycling, and disconnection handling.
    - [Read SQLAlchemy pooling documentation](https://docs.sqlalchemy.org/en/20/core/pooling.html)

4. SQLAlchemy: Session basics
    - Understand transaction scope, the session's mutable state, and why one session cannot be shared across concurrent tasks.
    - [Read SQLAlchemy session documentation](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)

5. PostgreSQL: Connection and resource settings
    - Learn how the server manages connections, statement timeouts, lock timeouts, and connection limits.
    - [Connection settings](https://www.postgresql.org/docs/current/runtime-config-connection.html)
    - [Client connection defaults and statement timeouts](https://www.postgresql.org/docs/current/runtime-config-client.html)
