CREATE TABLE stocks(
    name VARCHAR(50) PRIMARY KEY,
    code VARCHAR(10)
);

CREATE TABLE news_comments(
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    name VARCHAR(50),
    code VARCHAR(10),
    title TEXT,
    link TEXT,
    up INT,
    down INT,
    comment TEXT,
    analysis VARCHAR(10) DEFAULT 'F',
    sent_type VARCHAR(20),
    sent_score FLOAT DEFAULT 0,
    FOREIGN KEY(name) REFERENCES stocks(name)
);

CREATE TABLE discussion(
    id INT PRIMARY KEY AUTO_INCREMENT,
    date DATE,
    name VARCHAR(50),
    code VARCHAR(10),
    title TEXT,
    link TEXT,
    up INT,
    down INT,
    view INT,
    comment TEXT,
    analysis VARCHAR(10) DEFAULT 'F',
    sent_type VARCHAR(20),
    sent_score FLOAT DEFAULT 0,
    FOREIGN KEY(name) REFERENCES stocks(name)
);