-- Create databases
CREATE DATABASE metastore;
CREATE DATABASE shop;

-- Connect to shop and create initial data
\c shop;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    signup_date DATE
);

INSERT INTO customers (name, email, signup_date) VALUES
('Alice', 'alice@example.com', '2023-01-01'),
('Bob', 'bob@example.com', '2023-02-15'),
('Charlie', 'charlie@example.com', '2023-03-10');

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10, 2)
);

INSERT INTO products (name, price) VALUES
('Laptop', 999.99),
('Mouse', 29.99),
('Keyboard', 59.99);
