"""Small SQLite fixtures for runnable SQL examples in database articles.

Each article example gets an isolated in-memory database. These fixtures are
kept separate from the visualizer demos because their teaching queries often
use a simpler schema than the interactive demo above the article.
"""

SPECS = {
    "aggregate_functions_in_sql": {
        "seed": """CREATE TABLE payments (payment_id INTEGER PRIMARY KEY, amount REAL);
INSERT INTO payments (amount) VALUES (10), (NULL), (20);""",
    },
    "case_and_views_in_sql": {
        "seed": """CREATE TABLE orders (order_id INTEGER PRIMARY KEY, total REAL);
INSERT INTO orders VALUES (1, 125), (2, 65), (3, 18);
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT, status TEXT);
INSERT INTO customers VALUES (1, 'Ada', 'active'), (2, 'Grace', 'inactive');""",
    },
    "common_table_expressions_in_sql": {
        "seed": """CREATE TABLE orders (customer_id INTEGER, amount REAL);
INSERT INTO orders VALUES (1, 320), (1, 260), (2, 450), (3, 100);""",
    },
    "composite_and_covering_indexes": {
        "seed": """CREATE TABLE orders (order_id INTEGER PRIMARY KEY, created_at TEXT, customer_id INTEGER);
INSERT INTO orders VALUES (1, '2025-03-01', 42), (2, '2025-03-04', 42), (3, '2025-03-02', 7);""",
    },
    "constraints_in_sql": {
        "seed": """PRAGMA foreign_keys = ON;
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO customers VALUES (1, 'Ada'), (2, 'Grace');""",
    },
    "ddl_in_sql": {"seed": ""},
    "dml_in_sql": {
        "seed": """CREATE TABLE inventory (product_id INTEGER PRIMARY KEY, quantity INTEGER NOT NULL);
INSERT INTO inventory VALUES (17, 4), (18, 0);""",
    },
    "exists_vs_in_vs_join": {
        "seed": """CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO customers VALUES (1, 'Ada'), (2, 'Grace'), (3, 'Alan');
INSERT INTO orders VALUES (101, 1), (102, 1), (103, 3);""",
    },
    "groupby_in_sql": {
        "seed": """CREATE TABLE orders (customer_id INTEGER, total REAL, status TEXT);
INSERT INTO orders VALUES (1, 120, 'paid'), (1, 40, 'paid'), (2, 90, 'pending'), (3, 250, 'paid');""",
    },
    "having_in_sql": {
        "seed": """CREATE TABLE orders (customer_id INTEGER, status TEXT);
INSERT INTO orders VALUES (1, 'paid'), (1, 'paid'), (1, 'paid'), (1, 'pending'), (2, 'paid'), (2, 'paid'), (3, 'paid'), (3, 'paid'), (3, 'paid');""",
    },
    "indexes_in_sql": {
        "seed": """CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER);
INSERT INTO orders VALUES (1, 7), (2, 42), (3, 42);""",
    },
    "joins_in_sql": {
        "seed": """CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL, status TEXT);
INSERT INTO customers VALUES (1, 'Ada'), (2, 'Grace'), (3, 'Alan');
INSERT INTO orders VALUES (101, 1, 80, 'paid'), (102, 1, 20, 'pending'), (103, 2, 130, 'paid');""",
    },
    "limit_and_offset_in_sql": {
        "seed": """CREATE TABLE orders (order_id INTEGER PRIMARY KEY, created_at TEXT NOT NULL);
WITH RECURSIVE n(x) AS (SELECT 1 UNION ALL SELECT x + 1 FROM n WHERE x < 60)
INSERT INTO orders
SELECT x, '2025-01-' || printf('%03d', x) FROM n;""",
        "params": {":last_created_at": "2025-01-040", ":last_id": "40"},
    },
    "null_handling_in_sql": {
        "seed": """CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, email TEXT);
INSERT INTO customers VALUES (1, 'ada@example.com'), (2, NULL), (3, NULL);""",
    },
    "order_by_in_sql": {
        "seed": """CREATE TABLE orders (order_id INTEGER PRIMARY KEY, created_at TEXT);
INSERT INTO orders VALUES (1, '2025-02-01'), (2, '2025-02-03'), (3, '2025-02-02');""",
    },
    "primary_and_foreign_keys": {
        "seed": """PRAGMA foreign_keys = ON;
CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO customers VALUES (1, 'Ada'), (2, 'Grace');""",
    },
    "query_execution_order": {
        "seed": """CREATE TABLE orders (customer_id INTEGER, status TEXT);
INSERT INTO orders VALUES (1, 'paid'), (1, 'paid'), (1, 'paid'), (2, 'paid'), (2, 'pending'), (3, 'paid'), (3, 'paid'), (3, 'paid'), (3, 'paid');""",
    },
    "recursive_ctes_in_sql": {
        "seed": """CREATE TABLE employees (id INTEGER PRIMARY KEY, manager_id INTEGER);
INSERT INTO employees VALUES (1, NULL), (2, 1), (3, 1), (4, 2), (5, 4);""",
    },
    "self_joins_in_sql": {
        "seed": """CREATE TABLE employees (employee_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);
INSERT INTO employees VALUES (1, 'Mina', NULL), (2, 'Omar', 1), (3, 'Tess', 1), (4, 'Lee', 2);""",
    },
    "sql_injection_and_parameters": {
        "seed": """CREATE TABLE accounts (account_id INTEGER PRIMARY KEY, display_name TEXT, email TEXT);
INSERT INTO accounts VALUES (1, 'Ada', 'ada@example.com'), (2, 'Grace', 'grace@example.com');""",
        "params": {"?": ["ada@example.com"]},
    },
    "subqueries_in_sql": {
        "seed": """CREATE TABLE orders (customer_id INTEGER, amount REAL);
INSERT INTO orders VALUES (1, 320), (1, 260), (2, 300), (2, 250), (3, 40);""",
    },
    "transactions_and_acid": {
        "seed": """CREATE TABLE accounts (id INTEGER PRIMARY KEY, balance REAL NOT NULL);
INSERT INTO accounts VALUES (1, 100), (2, 40);""",
    },
    "union_intersect_except_in_sql": {
        "seed": """CREATE TABLE customers (email TEXT);
CREATE TABLE newsletter_signups (email TEXT);
INSERT INTO customers VALUES ('ada@example.com'), ('grace@example.com');
INSERT INTO newsletter_signups VALUES ('grace@example.com'), ('alan@example.com');""",
    },
    "where_clause_in_sql": {
        "seed": """CREATE TABLE orders (order_id INTEGER PRIMARY KEY, total REAL, status TEXT);
INSERT INTO orders VALUES (1, 80, 'paid'), (2, 40, 'paid'), (3, 130, 'pending');""",
    },
    "window_functions_in_sql": {
        "seed": """CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL, created_at TEXT);
INSERT INTO orders VALUES (1, 1, 40, '2025-01-01'), (2, 1, 25, '2025-01-02'), (3, 2, 90, '2025-01-01'), (4, 1, 10, '2025-01-03');""",
    },
}
