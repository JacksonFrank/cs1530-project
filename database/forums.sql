-- Tables that stores forum posts and forum comments
-- FORUM_POST table relies on existance of USER table
-- FORUM_COMMENT table relies on existance of USER and FORUM_POST tables

DROP TABLE IF EXISTS FORUM_POST CASCADE;
DROP TABLE IF EXISTS FORUM_COMMENT CASCADE;

CREATE TABLE FORUM_POST (
    title varchar(140) NOT NULL,
    author varchar(20) NOT NULL,
    time_posted timestamp NOT NULL,
    content TEXT,
    CONSTRAINT FORUM_PK PRIMARY KEY (title, author, time_posted),
    CONSTRAINT FORUM_FK FOREIGN KEY (author) REFERENCES LCTUSER(username)
);

CREATE TABLE FORUM_COMMENT (
    author varchar(20) NOT NULL,
    time_commented timestamp NOT NULL,
    content TEXT,
    post_title varchar(140) NOT NULL,
    post_author varchar(20) NOT NULL,
    post_time timestamp NOT NULL,
    CONSTRAINT COMMENT_PK PRIMARY KEY (author, time_commented),
    CONSTRAINT COMMENT_FK FOREIGN KEY (post_title, post_author, post_time) REFERENCES FORUM_POST(title, author, time_posted),
    CONSTRAINT AUTHOR_FK FOREIGN KEY (author) REFERENCES LCTUSER(username),
    CONSTRAINT POST_AUTHOR_FK FOREIGN KEY (post_author) REFERENCES LCTUSER(username)
);