
## Check connection pressure
Run this from psql:

```sql
SELECT
    current_setting('max_connections')::int AS max_connections,
    count(*) FILTER (
        WHERE backend_type = 'client backend'
    ) AS client_connections,
    count(*) FILTER (
        WHERE state = 'active'
    ) AS active_sessions,
    count(*) FILTER (
        WHERE state = 'idle'
    ) AS idle_sessions
FROM pg_stat_activity;
```


## Find long-running queries and transactions

```sql
SELECT
    pid,
    state,
    now() - query_start AS query_duration,
    now() - xact_start AS transaction_duration,
    wait_event_type,
    wait_event,
    LEFT(query, 200) AS query_excerpt
FROM pg_stat_activity
WHERE datname = current_database()
  AND pid <> pg_backend_pid()
ORDER BY query_start NULLS LAST;
```


### Inspect statements with the highest cumulative execution time:
```sql
SELECT
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_ms,
    ROUND(mean_exec_time::numeric, 2) AS mean_ms,
    ROUND(max_exec_time::numeric, 2) AS max_ms,
    LEFT(query, 200) AS query_excerpt
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```
