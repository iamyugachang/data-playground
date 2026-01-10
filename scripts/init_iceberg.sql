CREATE SCHEMA IF NOT EXISTS iceberg.data;

CREATE TABLE IF NOT EXISTS iceberg.data.events (
    event_id VARCHAR,
    user_id INTEGER,
    event_type VARCHAR,
    event_time TIMESTAMP
);

INSERT INTO iceberg.data.events VALUES
('e1', 1, 'login', TIMESTAMP '2023-01-01 10:00:00'),
('e2', 1, 'view_product', TIMESTAMP '2023-01-01 10:05:00'),
('e3', 2, 'login', TIMESTAMP '2023-02-15 09:00:00'),
('e4', 3, 'purchase', TIMESTAMP '2023-03-10 12:00:00');
