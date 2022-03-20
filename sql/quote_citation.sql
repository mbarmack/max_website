DROP TABLE IF EXISTS quotes;
DROP TABLE IF EXISTS citations;

CREATE TABLE quotes (
  quoteid INTEGER PRIMARY KEY,
  quote TEXT NOT NULL,
  postid INTEGER,
  FOREIGN KEY (postid) REFERENCES posts(postid)
);

CREATE TABLE citations (
  citid INTEGER PRIMARY KEY,
  cit TEXT NOT NULL,
  postid INTEGER,
  FOREIGN KEY (postid) REFERENCES posts(postid)
);