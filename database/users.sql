-- Defines table that stores user credentials and the amount of quizzes they've completed

DROP EXTENSION IF EXISTS pgcrypto;
CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS LCTUSER CASCADE;

CREATE TABLE LCTUSER (
    username varchar(20),
    password TEXT NOT NULL,
    quizzes_completed int DEFAULT 0,
    CONSTRAINT USERNAME_PK PRIMARY KEY (username)
);

CREATE OR REPLACE PROCEDURE register_user(_username varchar(20), _password TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO LCTUSER (username, password) VALUES (_username, crypt(_password, gen_salt('bf')));
    END;
$$;


CREATE OR REPLACE FUNCTION authenticate_user(_username varchar(20), _password TEXT) RETURNS BOOLEAN AS $$
BEGIN
    IF (SELECT COUNT(*) FROM LCTUSER WHERE LCTUSER.username = _username AND LCTUSER.password = crypt(_password, LCTUSER.password)) = 1 THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
    RETURN FALSE;
    END;
$$ LANGUAGE plpgsql;

        
