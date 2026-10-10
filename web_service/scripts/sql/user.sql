-- PostgreSQL v18 Setup

CREATE TABLE IF NOT EXISTS public.users (
    -- Modern built-in v18 UUID generator
    user_id UUID PRIMARY KEY DEFAULT uuidv4(),

    -- tenant_id UUID NOT NULL, -- Added for multi-tenancy

    -- Standard TEXT fields
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    name TEXT,
    phone VARCHAR(20),
    city VARCHAR(255),
    pincode VARCHAR(10),

    -- Metadata for auditing (Python ORM will update 'updated_at' on saves)
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Basic sanity check for email format
    CONSTRAINT email_must_contain_at CHECK (email LIKE '%@%')

     -- Add a foreign key constraint (Assuming you have a tenants table)
    -- CONSTRAINT fk_tenant
    --   FOREIGN KEY(tenant_id) REFERENCES public.tenants(id)
    --   ON DELETE CASCADE,
);

-- Case-insensitive enforcement indexes
CREATE UNIQUE INDEX idx_users_lowercase_username ON public.users (LOWER(username));
CREATE UNIQUE INDEX idx_users_lowercase_email ON public.users (LOWER(email));
CREATE UNIQUE INDEX idx_users_lowercase_city  ON public.users (LOWER(city));
CREATE UNIQUE INDEX idx_users_lowercase_pincode  ON public.users (LOWER(pincode));

-- CREATE INDEX idx_users_tenant_id ON public.users(tenant_id);
-- CREATE INDEX idx_users_tenant_username ON public.users(tenant_id, LOWER(username));

-- Optional search index for names
CREATE INDEX IF NOT EXISTS idx_users_name ON public.users(name);
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);


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
