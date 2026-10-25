import sys
import os
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.pool import QueuePool

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.db_config import DatabaseConfig

def check_database():
    """
    Checks the database connection and prints the current migration version.
    """
    print("Checking database connection...")
    try:
        # Use the app's DatabaseConfig instead of alembic.ini
        settings = DatabaseConfig()
        # Alembic/SQLAlchemy connection for checking needs the synchronous driver
        url = settings.DB_URL.replace("+asyncpg", "+psycopg2")

        print(f"Connecting to: {url}")

        engine = create_engine(
            url,
            poolclass=QueuePool,
            pool_pre_ping=True
        )

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            print("✅ Database connection successful.")

        # 2. Get current version
        print("\nCurrent migration history:")
        result_history = subprocess.run(
            ["alembic", "history"],
            capture_output=True,
            text=True,
            check=False
        )
        print(result_history.stdout if result_history.returncode == 0 else result_history.stderr)

        print("\nCurrent heads:")
        result_heads = subprocess.run(
            ["alembic", "heads"],
            capture_output=True,
            text=True,
            check=False
        )
        print(result_heads.stdout if result_heads.returncode == 0 else result_heads.stderr)

    except Exception as e:
        print(f"❌ Database connection or check failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_database()
