CREATE TABLE stocks(
    name VARCHAR(50) PRIMARY KEY COMMENT 'stock name',
    code VARCHAR(10) COMMENT 'stock code'
);

CREATE TABLE newsComments(
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
    date DATE COMMENT 'news date',
    name VARCHAR(50) COMMENT 'stock name',
    code VARCHAR(10) COMMENT 'stock code',
    title TEXT COMMENT 'news title',
    link TEXT COMMENT 'news link',
    up INT COMMENT 'like',
    down INT COMMENT 'dislike',
    comment TEXT COMMENT 'news comments',
    analysis VARCHAR(10) DEFAULT 'F' COMMENT 'whether analysis',
    sent_type VARCHAR(20) COMMENT 'positive or negative or neutral',
    sent_score FLOAT DEFAULT 0 COMMENT '0 ~ 100',
    FOREIGN KEY(name) REFERENCES stocks(name)
);

CREATE TABLE discussion(
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT 'id',
    date DATE COMMENT 'board date',
    name VARCHAR(50) COMMENT 'stock name',
    code VARCHAR(10) COMMENT 'stock code',
    title VARCHAR(255) COMMENT 'board title',
    link TEXT COMMENT 'board link',
    up INT COMMENT 'like',
    down INT COMMENT 'dislike',
    view INT COMMENT 'views',
    comment TEXT COMMENT 'news comments',
    analysis VARCHAR(10) DEFAULT 'F' COMMENT 'whether analysis',
    sent_type VARCHAR(20) COMMENT 'positive or negative or neutral',
    sent_score FLOAT DEFAULT 0 COMMENT '0 ~ 100',
    FOREIGN KEY(name) REFERENCES stocks(name),
    UNIQUE KEY unique_post (name, code, date, title, link)
);

CREATE TABLE date_table (
    date DATE PRIMARY KEY
);

WITH RECURSIVE date_series AS (
    SELECT DATE('2024-06-01') AS date
    UNION ALL
    SELECT DATE_ADD(date, INTERVAL 1 DAY)
    FROM date_series
    WHERE date < '2025-01-31'
)
SELECT date FROM date_series;

INSERT INTO date_table (date)
SELECT date FROM (
    WITH RECURSIVE date_series AS (
        SELECT DATE('2024-06-01') AS date
        UNION ALL
        SELECT DATE_ADD(date, INTERVAL 1 DAY)
        FROM date_series
        WHERE date < '2025-01-31'
    )
    SELECT date FROM date_series
) AS temp;
