# PostgreSQL Remote Connection & CLI Cheatsheet

A comprehensive guide to connecting to a remote PostgreSQL database from the command line, initializing users, and running essential DDL/DML commands.

---

## 1. Connecting to a Remote PostgreSQL DB

To connect to a remote PostgreSQL instance from your local command line, use the `psql` client utility.

```bash
psql -h <remote_host_ip_or_domain> -p <port> -U <username> -d <database_name>
```

### Parameter Breakdown:
*   **`-h`**: The IP address or domain name of your remote server (e.g., `192.168.1.50` or `db.example.com`).
*   **`-p`**: The port number PostgreSQL is listening on (Default is **`5432`**).
*   **`-U`**: The database user account you are authenticating with (e.g., `postgres`).
*   **`-d`**: The specific database you want to connect to initially.

---

## 2. Database Administration (Users, Databases & Permissions)

Run these commands inside the `psql` interactive prompt. Ensure you are logged in as a superuser (like `postgres`) to execute administrative tasks.

### Create a New Database
```sql
CREATE DATABASE my_new_db;
```

### Create a New User with a Secure Password
```sql
CREATE USER new_admin_user WITH PASSWORD 'SecurePassword123!';
```

### Grant Permissions & Access Rights
```sql
-- Grant full administrative privileges over the new database
GRANT ALL PRIVILEGES ON DATABASE my_new_db TO new_admin_user;

-- Connect to the specific database to alter schema-level privileges
\c my_new_db

-- Grant schema privileges (Required for PostgreSQL 15+)
GRANT ALL ON SCHEMA public TO new_admin_user;
```

---

## 3. Data Definition Language (DDL) Commands

DDL commands are used to define, alter, or drop the physical structure of your database tables and schemas.

### Create a Table (with Constraints)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Modify a Table Structure (Alter)
```sql
-- Add a new column
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);

-- Drop an existing column
ALTER TABLE users DROP COLUMN phone_number;
```

### Drop a Table
```sql
DROP TABLE users;
```

---

## 4. Data Manipulation Language (DML) Commands

DML commands allow you to query, insert, update, and delete the actual records stored within your tables.

### Insert Data (Create)
```sql
INSERT INTO users (username, email)
VALUES ('johndoe', 'john@example.com');
```

### Query Data (Read)
```sql
-- Fetch all columns from a table
SELECT * FROM users;

-- Fetch specific columns with filters
SELECT id, username FROM users WHERE email = 'john@example.com';
```

### Update Data (Modify)
```sql
UPDATE users
SET email = 'newjohn@example.com'
WHERE username = 'johndoe';
```

### Delete Data (Remove)
```sql
DELETE FROM users
WHERE username = 'johndoe';
```

---

## 5. Essential `psql` Meta-Commands

These are built-in terminal shortcuts specific to the `psql` interface. They do not require a semicolon (`;`) at the end.

*   **`\l`** : List all databases on the server.
*   **`\c <database_name>`** : Connect or switch to a different database.
*   **`\dt`** : List all tables in the currently connected database.
*   **`\d <table_name>`** : Describe a specific table's schema (columns, types, indexes).
*   **`\d+ <table_name>`** : Shows detailed structural layouts, data types, indexes, constraints, and foreign keys of a target table.
*   **`\df`** : Lists all functions and stored procedures.
*   **`\dn`** : Lists all active database schemas.
*   **`\sf <function_name>`** : Outputs the complete raw source code of an existing function
*   **`\du`** : List all users/roles and their respective attributes.
*   **`\q`** : Exit the `psql` client interface and return to your terminal.
*   **`\x`** : Toggle Expanded Display.
*   **`\i <path/to/file.sql>`** : Reads, parses, and executes raw SQL scripts saved on your local Mac environment directly onto the remote server.

## 🛠️ Performance Diagnostic & Monitoring Suite

Use these essential `psql` queries to monitor connections, track active queries, and resolve lock contentions in your PostgreSQL database.

### 1. Connection & Pool Monitoring

Monitoring Active Connections & Pools

* **Count Connections by State:** Verify pool saturation using
Count Total Connections by Status.
See how many connections are active, idling, or waiting.
This helps you determine if your application or connection pooler (like PgBouncer) is saturating slots.

    ```sql
    SELECT state, count(*)
    FROM pg_stat_activity
    GROUP BY state;
    ```

* **Breakdown by User/App:** Identify resource consumption via
Count Connections by Application/User.
Identify exactly which app or developer is consuming the most connection slots.

    ```sql
    SELECT usename, application_name, client_addr, count(*)
    FROM pg_stat_activity
    GROUP BY usename, application_name, client_addr
    ORDER BY count(*) DESC;
    ```

### 2. Live Query Tracking & Execution Health
* **View Active Queries:** List running tasks sorted by duration using
View All Currently Running Queries.
This lists all active connections that are actively executing a query right now, sorted by how long they have been running.

    ```sql
    SELECT pid, age(clock_timestamp(), query_start) AS duration, usename, query, state
    FROM pg_stat_activity
    WHERE state != 'idle' AND query NOT LIKE '%pg_stat_activity%'
    ORDER BY duration DESC;
    ```

* **Kill a Query:** Terminate a Rogue or Stuck Query
Gracefully cancel using the `pg_cancel_backend` function.
This function can be used to cancel a query by its process ID
If you spot a bad query using the previous command, you can stop it safely using its process ID (pid).


    ```sql
    SELECT pg_cancel_backend(YOUR_PID_HERE);
    ```
    or terminate forcefully using

    ```sql
    SELECT pg_terminate_backend(YOUR_PID_HERE);
    ```

### 3. Locks, Blocks, & Conflict Resolution
* **Identify Lock Trees:** Expose blocked and blocking process IDs to resolve contention.
You can find the full diagnostic SQL query and instructions in the system documentation. Once a `blocking_pid` is identified, release the block with

    ```sql
    SELECT pg_terminate_backend(blocking_pid);
    ```
