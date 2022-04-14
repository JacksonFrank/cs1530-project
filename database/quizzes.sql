-- Table to manage information needed to create quizzes

DROP TABLE IF EXISTS QUIZ;

CREATE TABLE QUIZ (
    english_tr TEXT NOT NULL,
    mandarin_tr TEXT NOT NULL,
    level int NOT NULL
);