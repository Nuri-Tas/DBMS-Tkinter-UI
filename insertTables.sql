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
('busra.oguzoglu');
 
 
INSERT INTO Rating_Platform (platform_id, platform_name)
 VALUES 
('10130', 'IMDB'),
('10131', 'Letterboxd'),
('10132', 'FilmIzle'),
('10133', 'Filmora'),
('10134', 'BollywoodMDB');


INSERT INTO Subscribed_Platforms (username, platform_id)
VALUES 
("arzucan.ozgur", "10130"),
("arzucan.ozgur", "10131"),
("arzucan.ozgur", "10133"),
("arzucan.ozgur", "10134"),
("egemen.isguder", "10130"),
("egemen.isguder", "10131"),
("egemen.isguder", "10133"),
("busra.oguzoglu", "10132"),
("busra.oguzoglu", "10133"),
("busra.oguzoglu", "10134");


INSERT INTO Subscribed_Platforms (username, platform_id)
VALUES 
("busra.oguzoglu", "10131");

INSERT INTO Director (username, nationality, platform_id)
VALUES 
("he.gongmin", "korean", "10133"),
("peter.weir", "english", "10130"),
("kyle.balda", "american", "10131"),
("carm.galian", "italian", "10133"),
("kron.helene", "greek", NULL);


INSERT INTO Movie (movie_id, movie_name, duration, username, platform_id)
VALUES
(20001, "Despicable Me", 2, "peter.weir", "10130"),
(20002, "Despicable Me 2", 2, "peter.weir", "10130"),
(20003, "Despicable Me 3", 1, "peter.weir", "10130"),
(20004, "Catch Me If You Can", 1, "kyle.balda", "10131"),
(20005, "Catch Me If You Can 2", 1, "kyle.balda", "10131"),
(20006, "Eagle Eye", 1, "kyle.balda", "10131");


INSERT INTO Predecessors (predecessor_id, movie_id)
VALUES
(20001, 20002),
(20002, 20003),
(20004, 20005);

INSERT INTO Genre_list (genre_id, genre_name)
VALUES
  (80001, 'Animation'),
  (80002, 'Comedy'),
  (80003, 'Adventure'),
  (80004, 'Real Story'),
  (80005, 'Thriller'),
  (80006, 'Drama');
  
  
INSERT INTO has_genre(movie_id, genre_id)
VALUES
(20001, 80001),
(20001, 80003),
(20002, 80002),
(20003, 80006),
(20004, 80001),
(20004, 80002),
(20004, 80003),
(20005, 80002),
(20006, 80006);


INSERT INTO Theatre (theatre_id, theatre_district, theatre_name, theatre_capacity)
VALUES
(40001, "Sisli", "Sisli_1", 300),
(40002, "Sisli", "Sisli_2", 600),
(40003, "Besiktas", "Besiktas_1", 500),
(40004, "Besiktas", "Besiktas_2", 800),
(40005, "Besiktas", "Besiktas_3", 900),
(40006, "Besiktas", "Besiktas_4", 1);


INSERT INTO Movie_Sessions (session_id, time_slot, _date, theatre_id)
VALUES
(50001, 1, STR_TO_DATE('3/15/23', '%m/%d/%y') , 40001), 
(50002, 3, STR_TO_DATE('3/15/23', '%m/%d/%y') , 40001), 
(50003, 1, STR_TO_DATE('3/15/23', '%m/%d/%y') , 40002), 
(50004, 3, STR_TO_DATE('3/15/23', '%m/%d/%y') , 40002), 
(50005, 1, STR_TO_DATE('3/16/23', '%m/%d/%y') , 40001), 
(50006, 3, STR_TO_DATE('3/16/23', '%m/%d/%y') , 40001), 
(50007, 1, STR_TO_DATE('3/16/23', '%m/%d/%y') , 40002), 
(50008, 3, STR_TO_DATE('3/16/23', '%m/%d/%y') , 40002),  
(50009, 1, STR_TO_DATE('3/17/23', '%m/%d/%y') , 40001), 
(50010, 3, STR_TO_DATE('3/17/23', '%m/%d/%y') , 40001), 
(50011, 3, STR_TO_DATE('3/17/23', '%m/%d/%y') , 40002), 
(50012, 1, STR_TO_DATE('3/17/23', '%m/%d/%y') , 40006);


INSERT INTO screens_as (movie_id, session_id)
VALUES
(20001, 50001);

INSERT INTO screens_as (movie_id, session_id)
VALUES
(20002, 50002);

INSERT INTO screens_as (movie_id, session_id)
VALUES
(20003, 50003);

INSERT INTO screens_as (movie_id, session_id)
VALUES
(20004, 50004),
(20005, 50005),
(20006, 50006),
(20001, 50007),
(20002, 50008),
(20002, 50009),
(20003, 50010),
(20004, 50011),
(20005, 50012);


INSERT INTO bought_tickets (username, session_id)
VALUES 
("arzucan.ozgur", 50001),
("arzucan.ozgur", 50002),
("arzucan.ozgur", 50003),
("arzucan.ozgur", 50004),
("egemen.isguder", 50004),
("egemen.isguder", 50005),
("busra.oguzoglu", 50004),
("busra.oguzoglu", 50006);


select * from predecessors;

INSERT INTO Ratings (username, movie_id, rating)
VALUES 
("arzucan.ozgur", 20001, 4.5),
("arzucan.ozgur", 20002, 5),
("arzucan.ozgur", 20003, 4),
("egemen.isguder", 20004, 5),
("egemen.isguder", 20005, 4);

INSERT INTO Ratings (username, movie_id, rating)
VALUES 
("busra.oguzoglu", 20004, 4.5);

-- no need to insert values into average ratings table as it will be automatically created as values are inserted into Ratings
select * from Average_Ratings;


INSERT INTO database_managers (username, _password)
VALUES
  ("m1", "p1"),	
  ('manager1', 'managerpass1'),
  ('manager2', 'managerpass2'),
  ('manager35', 'managerpass35');
  
