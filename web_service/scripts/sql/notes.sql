 CREATE TABLE users
 (
    userid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);




CREATE TABLE foo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL
);


INSERT INTO foo (name) VALUES ('foo1'), ('foo2'), ('foo3');

select * from foo
