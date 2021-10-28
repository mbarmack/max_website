DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS paragraph;
DROP TABLE IF EXISTS comments;

CREATE TABLE posts (
  postid INTEGER PRIMARY KEY,
  author TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL
);

CREATE TABLE paragraphs (
  paragraphid INTEGER PRIMARY KEY,
  paragraph TEXT NOT NULL,
  postid INTEGER,
  FOREIGN KEY (postid) REFERENCES posts(postid)
);

CREATE TABLE users (
    username VARCHAR(20) NOT NULL,
    password VARCHAR(256) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE comments (
  commentid INTEGER PRIMARY KEY,
  owner VARCHAR(20) NOT NULL,
  author varchar(20) NOT NULL,
  text TEXT NOT NULL,
  postid INTEGER,
  FOREIGN KEY (postid) REFERENCES posts(postid),
  FOREIGN KEY (owner) REFERENCES users(username)
);