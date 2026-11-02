# Database Migrations with Alembic

This project uses **Alembic** to manage database schema migrations. It is configured to work with the application's existing `DatabaseConfig` and `SQLModel` definitions.

## Configuration

The migration system is integrated with the application's core:
- **Database Configuration:** Alembic dynamically fetches the connection string from `DatabaseConfig`.
- **Sync vs Async:** While the application runs asynchronously using `asyncpg`, Alembic uses `psycopg2` for performing migrations.
- **Autogeneration:** The system supports `alembic revision --autogenerate` to detect schema changes automatically.

## Usage

### Migration Commands

Run these commands from the root directory:

| Action | Command | Description |
| :--- | :--- | :--- |
| **Upgrade** | `uv run alembic upgrade head` | Apply all pending migrations. |
| **Downgrade** | `uv run alembic downgrade -1` | Revert the last migration. |
| **History** | `uv run alembic history` | View all migration versions. |
| **Check** | `uv run alembic heads` | View the current head version. |

### Dry Run & Verification

To verify your connection and see the current migration state without applying any changes, use the helper script:

```bash
uv run python scripts/check_db_connection.py
```

This script confirms the connection to the database and prints the migration history and current head.

## Development Workflow

1.  **Update Model:** Modify the `User` model in `app/models/user.py`.
2.  **Generate Migration:** Run `uv run alembic revision --autogenerate -m "description"` to create a migration file.
3.  **Apply Migration:** Run `uv run alembic upgrade head` to update the database schema.
4.  **Verify:** Use the dry-run script to ensure the database is in the expected state.


## Testing
| Command | Purpose |
| :--- | :--- |
|`alembic heads` | Check the Alembic configuration and migration files |
|`alembic history` |  Check the Alembic configuration and migration files|
|`alembic current` | Verify Alembic can connect to the database|
|`alembic upgrade head --sql` | Generate SQL without executing it|
|`uv run python scripts/check_db_connection.py` | Check the connection to the database and print the migration history and current head |
