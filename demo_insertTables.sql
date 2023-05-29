INSERT INTO Users (username, _password, _name, surname)
VALUES
('steven.jobs', 'apple123', 'Steven', 'Jobs'),
('minion.lover', 'bello387', 'Felonius', 'Gru'),
('steve.wozniak', 'pass4321', 'Ryan', 'Andrews'),
('he.gongmin', 'passwordpass', 'He', 'Gongmin'),
('carm.galian', 'madrid9897', 'Carmelita', 'Galiano'),
('kron.helene', 'helenepass', 'Helene', 'Kron'),
('arzucan.ozgur', 'deneme123', 'Arzucan', 'Ozgur'),
('egemen.isguder', 'deneme124', 'Egemen', 'Isguder'),
('busra.oguzoglu', 'deneme125', 'Busra', 'Oguzoglu'),
('peter.weir', 'peter weir879', 'Peter', 'Weir'),
('kyle.balda', 'mynameiskyle9', 'Kyle', 'Balda');

INSERT INTO audience (username)
VALUES 
('arzucan.ozgur'),
('egemen.isguder'),
('busra.oguzoglu'),
("steven.jobs"),
("steve.wozniak");


 
 
INSERT INTO Rating_Platform (platform_id, platform_name)
 VALUES 
('10130', 'IMDB'),
('10131', 'Letterboxd'),
('10132', 'FilmIzle'),
('10133', 'Filmora'),
('10134', 'BollywoodMDB');


INSERT INTO Subscribed_Platforms (username, platform_id)
VALUES 
("steven.jobs", "10130"),
("steven.jobs", "10131"),
("steve.wozniak", "10131"),
("arzucan.ozgur", "10130"),
("egemen.isguder", "10132"),
("busra.oguzoglu", "10131");


INSERT INTO Director (username, nationality, platform_id)
VALUES 
("he.gongmin", "Turkish", "10130"),
("carm.galian", "Turkish", "10131"),
("kron.helene", "French", "10130"),
("peter.weir", "Spanish", "10131"),
("kyle.balda", "German", "10132");


INSERT INTO movie (movie_id, movie_name, duration, username, platform_id)
VALUES
    (20001, 'Despicable Me', 2, 'kyle.balda', 10132),
    (20002, 'Catch Me If You Can', 2, 'he.gongmin', 10130),
    (20003, 'The Bone Collector', 2, 'carm.galian', 10131),
    (20004, 'Eagle Eye', 2, 'kron.helene', 10130),
    (20005, 'Minions: The Rise Of Gru', 1, 'kyle.balda', 10132),
    (20006, 'The Minions', 1, 'kyle.balda', 10132),
    (20007, 'The Truman Show', 3, 'peter.weir', 10131);


INSERT INTO Predecessors (predecessor_id, movie_id)
VALUES
(20001, 20006),
(20006, 20005);


INSERT INTO Genre_list (genre_id, genre_name)
VALUES
  (80001, 'Animation'),
  (80002, 'Comedy'),
  (80003, 'Adventure'),
  (80004, 'Real Story'),
  (80005, 'Thriller'),
  (80006, 'Drama');
  
  
INSERT INTO has_genre (movie_id, genre_id)
VALUES
    (20001, 80001),
    (20001, 80002),
    (20002, 80003),
    (20002, 80004),
    (20003, 80005),
    (20004, 80003),
    (20005, 80001),
    (20005, 80002),
    (20006, 80001),
    (20006, 80002),
    (20007, 80002),
    (20007, 80006);

INSERT INTO Theatre (theatre_id, theatre_district, theatre_name, theatre_capacity)
VALUES
    (40001, 'Sisli', 'Sisli_1', 300),
    (40002, 'Sisli', 'Sisli_2', 200),
    (40003, 'Besiktas', 'Besiktas1', 100),
    (40004, 'Besiktas', 'Besiktas2', 100),
    (40005, 'Besiktas', 'Besiktas3', 500);

INSERT INTO Movie_Sessions (session_id, time_slot, _date, theatre_id)
VALUES
    (50001, 1, STR_TO_DATE('3/15/2023', '%m/%d/%Y'), 40001),
    (50002, 3, STR_TO_DATE('3/15/2023', '%m/%d/%Y'), 40001),
    (50003, 1, STR_TO_DATE('3/15/2023', '%m/%d/%Y'), 40002),
    (50004, 3, STR_TO_DATE('3/15/2023', '%m/%d/%Y'), 40002),
    (50005, 1, STR_TO_DATE('3/16/2023', '%m/%d/%Y'), 40003),
    (50006, 3, STR_TO_DATE('3/16/2023', '%m/%d/%Y'), 40003),
    (50007, 1, STR_TO_DATE('3/16/2023', '%m/%d/%Y'), 40004),
    (50008, 3, STR_TO_DATE('3/16/2023', '%m/%d/%Y'), 40004),
    (50009, 1, STR_TO_DATE('3/16/2023', '%m/%d/%Y'), 40005);

INSERT INTO screens_as (movie_id, session_id)
VALUES
    (20001, 50001),
    (20001, 50002),
    (20001, 50003),
    (20002, 50004),
    (20003, 50005),
    (20004, 50006),
    (20005, 50007),
    (20006, 50008),
    (20007, 50009);

drop table bought_tickets;

INSERT INTO bought_tickets (username, session_id)
VALUES
    ('steven.jobs', 50001),
    ('steve.wozniak', 50004),
    ('steve.wozniak', 50005),
    ('arzucan.ozgur', 50006),
    ('egemen.isguder', 50001),
	('egemen.isguder', 50004),
    ('egemen.isguder', 50008),
	('egemen.isguder', 50007),
    ('busra.oguzoglu', 50009);

INSERT INTO ratings (username, movie_id, rating)
VALUES
    ('egemen.isguder', 20001, 5),
    ('egemen.isguder', 20005, 5),
    ('egemen.isguder', 20006, 5),
    ('arzucan.ozgur', 20004, 5),
    ('busra.oguzoglu', 20007, 5);
    
-- no need to insert values into average ratings table as it will be automatically created as values are inserted into Ratings
select * from Average_Ratings;

INSERT INTO database_managers (username, _password)
VALUES
    ('manager1', 'managerpass1'),
    ('manager2', 'managerpass2'),
    ('manager35', 'managerpass35');


INSERT INTO database_managers (username, _password)
VALUES
  ("m1", "p1"),	
  ('manager1', 'managerpass1'),
  ('manager2', 'managerpass2'),
  ('manager35', 'managerpass35');
  
