-- PostgreSQL v18 Setup

CREATE TABLE IF NOT EXISTS public.users (
    user_id UUID PRIMARY KEY DEFAULT uuidv4(),

    username TEXT NOT NULL,
    email TEXT NOT NULL,

    name TEXT,
    phone VARCHAR(20),
    city VARCHAR(255),
    pincode VARCHAR(10),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT email_must_contain_at
        CHECK (email LIKE '%@%')
);

-- Case-insensitive uniqueness.
CREATE UNIQUE INDEX uq_users_username_ci
    ON public.users (LOWER(username));

CREATE UNIQUE INDEX uq_users_email_ci
    ON public.users (LOWER(email));

-- Optional: retain only if query patterns justify this index.
CREATE INDEX IF NOT EXISTS idx_users_name
    ON public.users (name);

-- ALTER TABLE users DROP CONSTRAINT email_must_contain_at;

SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM
    information_schema.columns
WHERE
    table_name = 'users';

select * from users

-- insert a mock user to users table using insert script
INSERT INTO users (username, email,
    city, pincode, name)
    VALUES ('testuser', 'testuser@example.com',
    'New York', '10001,
    12345', 'Test User');


DROP TABLE IF EXISTS public.users;
