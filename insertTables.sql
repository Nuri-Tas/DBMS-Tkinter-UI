INSERT INTO User (username, password, name, surname)
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


INSERT INTO Rating_Platform (platform_id, platform_name)
VALUES
('10130', 'IMDB'),
('10131', 'Letterboxd'),
('10132', 'FilmIzle'),
('10133', 'Filmora'),
('10134', 'BollywoodMDB');


insert into directors(username)
values 
('peter.weir'),
('kyle.balda');


insert into nations(nation)
values 
("english"),
("america");


insert into audience(username)
values 
('arzucan.ozgur'),
('egemen.isguder'),
('busra.oguzoglu');

  
insert into Movies(movie_id, duration, movie_name)
values 
('20001',  2, 'Despicable Me'),
('20002',  2, 'Catch Me If You Can'),
('20003',  2, 'Despicable Me 2'),
('20004',  2, 'Catch Me If You Can 2');

insert into ratings(username, movie_id, rating)
values 
('arzucan.ozgur', '20001',  3),
('arzucan.ozgur', '20002', 4),
('arzucan.ozgur', '20003',  5),
('arzucan.ozgur', '20004', 4),
('egemen.isguder', '20001', 5),
('egemen.isguder', '20002', 5),
('egemen.isguder', '20003', 5),
('egemen.isguder', '20004', 5);

INSERT INTO Rate (username, movie_id, ratings)
VALUES
  ('arzucan.ozgur', '20002', 3),
  ('arzucan.ozgur', '20004', 5),
  ('egemen.isguder', '20001', 4),
  ('egemen.isguder', '20003', 5);


insert into Predecessors(movie_id, predecessor_id)
values 
('20001', '20003'),
('20002', '20004');



INSERT INTO genres (genre_id, genre_name)
VALUES
  (80001, 'Animation'),
  (80002, 'Comedy'),
  (80003, 'Adventure'),
  (80004, 'Real Story'),
  (80005, 'Thriller'),
  (80006, 'Drama');
  
  
INSERT INTO Theatre_Location (theatre_id, theatre_name, theatre_district, theatre_capacity)
VALUES
  ('10132', 'Sisli_1', 'Sisli',  300),
  ('10130', 'Sisli_2', 'Sisli', 200),
  ('10131', 'Besiktas_1', 'Besiktas',  100);
  
  
INSERT INTO Movie_Sessions (session_id, date, theatre_id)
VALUES
  ('50001', STR_TO_DATE('3/15/23', '%m/%d/%y'), '10130'),
  ('50002', STR_TO_DATE('3/15/23', '%m/%d/%y'), '10131'),
  ('50003', STR_TO_DATE('3/15/23', '%m/%d/%y'), '10132'),
  ('50004', STR_TO_DATE('3/15/23', '%m/%d/%y'), '10131'),
  ('50005', STR_TO_DATE('3/16/23', '%m/%d/%y'), '10132');
  
  
INSERT INTO database_managers (username, password)
VALUES
  ("m1", "p1"),	
  ('manager1', 'managerpass1'),
  ('manager2', 'managerpass2'),
  ('manager35', 'managerpass35');
  
  
  INSERT INTO Nationality (username, nation)
  VALUES
   ('peter.weir', 'english'),
   ('kyle.balda', 'america');


INSERT INTO Rate (username, movie_id, ratings)
VALUES
  ('arzucan.ozgur', '20001', 3),
  ('arzucan.ozgur', '20003', 5),
  ('egemen.isguder', '20002', 4),
  ('egemen.isguder', '20004', 5);
  

  
INSERT INTO Genre (movie_id, genre_id)
VALUES
  ('20001', '80002'),
  ('20002', '80003'),
  ('20003', '80002'),
  ('20004', '80003');
  
  
  INSERT INTO Subscription (username, platform_id, movie_id)
VALUES
  ('arzucan.ozgur', '10130', '20001'),
  ('arzucan.ozgur', '10130', '20003'),
  ('egemen.isguder', '10131', '20002'),
  ('egemen.isguder', '10131', '20004');


  INSERT INTO Bought (username, session_id, movie_id)
VALUES
  ('arzucan.ozgur', '50001', '20001'),
  ('arzucan.ozgur', '50003', '20003'),
  ('egemen.isguder', '50002', '20002'),
  ('egemen.isguder', '50004', '20004');
  
  
  INSERT INTO Filmed (session_id, movie_id, theatre_id, time_slot)
VALUES
  ('50001', '20001', '10130', 1),
  ('50002', '20002', '10131', 3),
  ('50003', '20003', '10132', 3),
  ('50004', '20004', '10132', 1);
  
INSERT INTO Directed_By(movie_id, username)
values
 ('20001', 'peter.weir'),
 ('20003', 'peter.weir'),
 ('20002', 'kyle.balda'),
 ('20004', 'kyle.balda');

INSERT INTO Agreement(username, platform_id)
VALUES
 ('peter.weir', '10130'),
('kyle.balda', '10131');
