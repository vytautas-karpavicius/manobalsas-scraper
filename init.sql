CREATE TABLE politicians (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    party TEXT NOT NULL,
    link TEXT NOT NULL
);

CREATE TABLE questions (
    tst_id INTEGER,
    q_id INTEGER,
    area TEXT,
    question TEXT,
    modifier INTEGER,
    PRIMARY KEY(tst_id, q_id)
);

CREATE TABLE answers (
    pol_id INTEGER,
    tst_id INTEGER,
    q_id INTEGER,
    answer INTEGER,
    comment TEXT,
    PRIMARY KEY(pol_id, tst_id, q_id)
);

--
.separator ,
.import questions.csv questions