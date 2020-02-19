DROP TABLE IF EXISTS musicals;
DROP TABLE IF EXISTS songs;
DROP SEQUENCE  IF EXISTS musicals_id_seq;
DROP SEQUENCE IF EXISTS songs_id_seq;


CREATE TABLE musicals (
                        id serial PRIMARY KEY,
                        title varchar(200) UNIQUE NOT NULL,
                        year int CHECK (year BETWEEN 1900 AND 2020),
                        book varchar(200),
                        music varchar(200),
                        genre varchar(200));

CREATE SEQUENCE musicals_id_seq
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE ONLY musicals ALTER COLUMN id SET DEFAULT nextval('musicals_id_seq'::regclass);

INSERT INTO musicals VALUES (1, 'Wicked', 2004, 'Winnie Holzman','Stephen Schwartz', 'book musical');
INSERT INTO musicals VALUES (2, 'Once on this island', 1990, 'Lynn Ahrens', 'Stephen Flaherty', 'book musical');
INSERT INTO musicals VALUES (3, 'Hamilton', 2015 , 'Lin-Manuel Miranda', 'Lin-Manuel Miranda', 'pop/rock musical');

SELECT pg_catalog.setval('musicals_id_seq', 3, true);

CREATE TABLE songs (
                     id serial PRIMARY KEY,
                     title varchar(250) NOT NULL,
                     length float,
                     performer varchar(250),
                     show varchar(250)REFERENCES musicals(title) ON DELETE CASCADE

);

CREATE SEQUENCE songs_id_seq
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;

ALTER TABLE ONLY songs ALTER COLUMN id SET DEFAULT nextval('songs_id_seq'::regclass);

INSERT INTO songs VALUES (1,'Overture / No One Mourns the Wicked', 6.40,'Ensemble', 'Wicked' );
INSERT INTO songs VALUES (2,'Dear Old Shiz', 1.26, 'Ensemble', 'Wicked');
INSERT INTO songs VALUES (3,'The Wizard and I', 5.09, 'Elphaba', 'Wicked');
INSERT INTO songs VALUES (4,'What is this feeling', 3.32, 'Glinda, Elphaba, Ensemble','Wicked');
INSERT INTO songs VALUES (5,'Something bad',1.39, 'Dr.Dillamond, Elphaba', 'Wicked');
INSERT INTO songs VALUES (6, 'Dancing through life', 7.37, 'Fiyero, Ensemble', 'Wicked');
INSERT INTO songs VALUES (7, 'Popular', 3.44, 'Glinda', 'Wicked');
INSERT INTO songs VALUES (8, 'I''m not that girl', 2.58, 'Elphaba', 'Wicked');
INSERT INTO songs VALUES (9, 'One short day', 3.03, 'Elphaba, Glinda, Ensemble', 'Wicked');
INSERT INTO songs VALUES (10, 'A sentimental man', 1.51, 'The Wizard', 'Wicked');
INSERT INTO songs VALUES (11, 'Defying gravity', 5.53, 'Elphaba, Glinda');
INSERT INTO songs VALUES (12, 'No One Mourns the Wicked (Reprise) / Thank Goodness', 6.22, 'Glinda, Ensemble', 'Wicked');
INSERT INTO songs VALUES (13, 'Wonderful', 4.57, 'The Wizard, Elphaba', 'Wicked');
INSERT INTO songs VALUES (14, 'I''m not that girl (reprise)', 0.49, 'Glinda', 'Wicked');
INSERT INTO songs VALUES (15, 'As long as you''re mine', 3.45, 'Elphaba, Fiyero', 'Wicked');
INSERT INTO songs VALUES (16, 'No good deed', 3.31, 'Elphaba', 'Wicked');
INSERT INTO songs VALUES (17, 'March of the Witch Hunters', 1.30, 'Ensemble', 'Wicked');
INSERT INTO songs VALUES (18, 'For good', 5.06, 'Elphaba, Glinda', 'Wicked');
INSERT INTO songs VALUES (19, 'Finale: For Good (reprise)', 1.41, 'Ensemble', 'Wicked');
INSERT INTO songs VALUES (20, 'We dance', 5.32, 'Ensemble', 'Once on this island');
INSERT INTO songs VALUES (21, 'One small girl', 6.22, 'Ensemble', 'Once on this island');
INSERT INTO songs VALUES (22, 'Waiting for life', 3.25, 'Ti Moune', 'Once on this island');
SELECT pg_catalog.setval('songs_id_seq', 22, true);

CREATE TABLE users (
                     id serial PRIMARY KEY,
                     creation_date date NOT NULL ,
                     username varchar(250) UNIQUE NOT NULL,
                     password varchar(250) NOT NULL ,
                     list_no numeric

);

CREATE TABLE tags (
                    id serial PRIMARY KEY,
                    creation_date date NOT NULL ,
                    creator_id int REFERENCES users(id),
                    tag varchar(250) NOT NULL UNIQUE,
                    song_id int REFERENCES songs(id)


);

INSERT INTO tags VALUES (2,NOW(),1,'solo',8);
INSERT INTO tags VALUES (3,NOW(),1,'sad',8);
INSERT INTO tags VALUES (4,NOW(),1,'soprano',8);
INSERT INTO tags VALUES (5, NOW(),1, 'ballad',29);
INSERT INTO tags VALUES (6, NOW(),1, 'sad',29);
INSERT INTO tags VALUES (7, NOW(),1, 'emotional',29);
INSERT INTO tags VALUES (8, NOW(),1,'teen',8);
INSERT INTO tags VALUES (9, NOW(),1,'20s',8);
INSERT INTO tags VALUES (10, NOW(),1,'30s',8);
INSERT INTO tags VALUES (11, NOW(),1,'white skin',8);
INSERT INTO tags VALUES (12, NOW(),1,'dark skin',8);
INSERT INTO tags VALUES (13, NOW(),1,'female',8);

ALTER TABLE songs ADD COLUMN lyrics varchar(250);
ALTER TABLE songs ADD COLUMN sheet_music varchar(250);
ALTER TABLE songs ADD COLUMN video varchar(250);

SELECT pg_catalog.setval('tags_id_seq', 13, true);

ALTER TABLE songs ADD COLUMN creator_id int REFERENCES users(id);
ALTER TABLE musicals ADD COLUMN creator_id int REFERENCES users(id);