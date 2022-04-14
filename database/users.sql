-- Defines table that stores user credentials and the amount of quizzes they've completed

DROP EXTENSION IF EXISTS pgcrypto;
CREATE EXTENSION pgcrypto;

DROP TABLE IF EXISTS LCTUSER CASCADE;

CREATE TABLE LCTUSER (
    username varchar(20),
    password TEXT NOT NULL,
    quizes_completed int DEFAULT 0,
    CONSTRAINT USERNAME_PK PRIMARY KEY (username)
);

DROP TRIGGER IF EXISTS hash_password_tr ON LCTUSER;
CREATE TRIGGER hash_password_tr
    BEFORE INSERT ON LCTUSER
    EXECUTE PROCEDURE hash_password();
    

CREATE OR REPLACE FUNCTION hash_password() RETURNS TRIGGER AS $$
BEGIN
    NEW.password = crypt(NEW.password, gen_salt('bf'));
    RETURN NEW;
    END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION authenticate_user(username varchar(20), password TEXT) RETURNS BOOLEAN AS $$
BEGIN
    IF (SELECT COUNT(*) FROM LCTUSER WHERE LCTUSER.username = username AND LCTUSER.password = crypt(password, LCTUSER.password)) = 1 THEN
        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
    RETURN FALSE;
    END;
$$ LANGUAGE plpgsql;

        
