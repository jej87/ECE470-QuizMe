DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS questions;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  upassword TEXT NOT NULL,
  alias TEXT NOT NULL,
  score INT 
);

CREATE TABLE questions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT NOT NULL,
  a TEXT NOT NULL,
  b TEXT NOT NULL,
  c TEXT NOT NULL,
  d TEXT NOT NULL,
  answer TEXT NOT NULL
);

INSERT INTO users (email, upassword, alias, score) VALUES("student1@miami.edu", "pass1", "student1", 0);
INSERT INTO users (email, upassword, alias, score) VALUES("student2@miami.edu", "pass2", "student2", 0);
INSERT INTO questions (question, a, b, c, d, answer) VALUES("Which is a school color of UM?", "green", "blue", "red", "yellow", "green");
INSERT INTO questions (question, a, b, c, d, answer) VALUES("What is the name of the school mascot?", "Steve", "Simon", "Sebastian", "Stella", "Sebastian");
INSERT INTO questions (question, a, b, c, d, answer) VALUES("What celebrity recently visited the UM campus?", "Shakira", "Beyonce", "Pitbull", "JayZ", "Pitbull");
INSERT INTO questions (question, a, b, c, d, answer) VALUES("Who is the President of UM?", "Patricia Whitely", "Julio Frenk", "Jose Freud", "Marc Delgado", "Julio Frenk");

