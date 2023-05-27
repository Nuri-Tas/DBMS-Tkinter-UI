-- I used underscores since mysql has built in features of password and user
CREATE TABLE Users(
	username VARCHAR(20),
    _password VARCHAR(20) NOT NULL,
    -- since passwords cant be null in real life
	_name VARCHAR(20),
    surname VARCHAR(20),
    PRIMARY KEY (username)
);

CREATE TABLE Audience(
	username VARCHAR(20),
	PRIMARY KEY (username),
	FOREIGN KEY (username) 
		REFERENCES users(username)
        ON DELETE CASCADE
	-- i assumed if someone deletes their account as a user then they wont be an audience because of the isa hierarchy
);

CREATE TABLE Rating_Platform (
	platform_id INTEGER(20),
    platform_name VARCHAR(20) NOT NULL,
    UNIQUE (platform_name),
    -- I assumed there wont be any platforms with the same name
    PRIMARY KEY (platform_id)
);



CREATE TABLE Subscribed_Platforms(
	username VARCHAR(20),
    platform_id INTEGER(20),
    FOREIGN KEY (username)
		REFERENCES Audience(username)
        ON DELETE CASCADE,
	FOREIGN KEY (platform_id) REFERENCES Rating_platform(platform_id) ON DELETE CASCADE,
    PRIMARY KEY (username, platform_id)
);


CREATE TABLE Director(
	username VARCHAR(20),
    nationality VARCHAR(20) NOT NULL,
    platform_id INTEGER(20),
	UNIQUE (username, platform_id),
    FOREIGN KEY (username)
		REFERENCES users(username)
        ON DELETE CASCADE,
	-- same assumption as before
    FOREIGN KEY (platform_id) REFERENCES Rating_Platform(platform_id)
    -- didnt put on delete here because in the assignment the director can have at most only one platform but doesnt say must
);




CREATE TABLE Movie(
	movie_id INTEGER(20),
    movie_name VARCHAR(50) NOT NULL,
    -- because movie name cant be blank in real life
    duration INTEGER(20) NOT NULL,
    -- because movie has to last some time to be booked
    username VARCHAR(20) NOT NULL,
    platform_id INTEGER(20),
	-- every movie must have exactly one director so if the director is deleted movie should be as well  
    FOREIGN KEY (username, platform_id) REFERENCES Director(username, platform_id) ON UPDATE CASCADE,
	-- the platform id of the movie should be the same as the director's platform id 
    -- movies platform is the same as the directors
	PRIMARY KEY (movie_id, username)
);



CREATE TABLE Predecessors(
	predecessor_id INTEGER(20),
    movie_id INTEGER(20),
    FOREIGN KEY (movie_id)
		REFERENCES Movie(movie_id)
        ON DELETE CASCADE,
	-- I figured if the movie gets deleted then everything related to it should be as well
    PRIMARY KEY(predecessor_id, movie_id)
);

CREATE TABLE Genre_list(
	genre_id INTEGER(20),
    genre_name VARCHAR(20),
    UNIQUE (genre_name),
    PRIMARY KEY (genre_id)
);


CREATE TABLE has_genre(
	movie_id INT,
    genre_id INT NOT NULL,
    FOREIGN KEY (movie_id)
		REFERENCES Movie(movie_id)
		ON DELETE CASCADE,
	-- if a movie no longer exists in the platform we shouldnt keep the genre information
    FOREIGN KEY (genre_id) REFERENCES Genre_list(genre_id),
    PRIMARY KEY (movie_id, genre_id)
);


-- create a trigger for has genre to ensure all movies have at least one genre
DELIMITER $$
CREATE TRIGGER check_movie_count AFTER INSERT
ON has_genre FOR EACH ROW

BEGIN
  DECLARE movie_count INT;
  DECLARE has_genre_count INT;
  DECLARE msg VARCHAR(128);
  
  SELECT COUNT(DISTINCT movie_id) INTO movie_count FROM Movie;
  SELECT COUNT(DISTINCT movie_id) INTO has_genre_count FROM has_genre;
  
  IF has_genre_count > movie_count THEN
		set msg = 'has genre must include all movie ids in the Movie table';
        signal sqlstate '45000' set message_text = msg;
  end IF;
end $$

delimiter ;


CREATE TABLE Ratings(
	username VARCHAR(20),
    movie_id INT,
    rating FLOAT,
	PRIMARY KEY (username, movie_id),
    FOREIGN KEY (movie_id)
		REFERENCES Movie(movie_id)
        ON DELETE CASCADE,
	-- If a movie is deleted no longer need to keep ratings
    -- however if a user is deleted we dont need to delete the rating as it is stated in the discussion forum
	CONSTRAINT rating_check CHECK (rating >= 0 AND rating <= 5)
);


-- trigger to ensure only audiences who are subscribed to the platform of the movie and bought ticket for the movie can rate the movie

drop trigger if exists can_rate;

DELIMITER $$
CREATE TRIGGER can_rate  
BEFORE INSERT ON Ratings
FOR EACH ROW
BEGIN 
	DECLARE platform_of_new_movie INT;
    DECLARE msg VARCHAR(128);
	
	SELECT platform_id INTO platform_of_new_movie FROM Movie
    WHERE Movie.movie_id = NEW.movie_id;
	
    IF NOT EXISTS (Select username from audience where username = NEW.username) THEN
		set msg = 'Only audience can rate a movie!';
        signal sqlstate '45000' set message_text = msg;
	ELSEIF NOT EXISTS (select username from subscribed_platforms where username = New.username AND platform_id = platform_of_new_movie) THEN 
		set msg = "The audience isn't subscribed to the platform of the movie!";
        signal sqlstate '45000' set message_text = msg;
	ELSEIF NOT EXISTS (select username from bought_tickets where session_id in (SELECT session_id from screens_as where screens_as.movie_id = NEW.movie_id) 
						and username = NEW.username) THEN
		set msg = "The audience didn't buy a ticket for the movie!";
        signal sqlstate '45000' set message_text = msg;
  end IF;
end $$
delimiter ;
		

CREATE TABLE Average_Ratings(
	movie_id INT,
    average_rating FLOAT,
    PRIMARY KEY (movie_id),
    FOREIGN KEY (movie_id) REFERENCES Ratings (movie_id) ON DELETE CASCADE,
	CONSTRAINT avg_rating_check CHECK(average_rating >= 0 AND average_rating <= 5));


-- create a trigger to automatically update the average rating for each movie 
DELIMITER //
CREATE TRIGGER update_average_rating AFTER INSERT
ON Ratings FOR EACH ROW
BEGIN
  REPLACE INTO Average_Ratings (movie_id, average_rating)
  SELECT movie_id, AVG(rating) AS average_rating
  FROM Ratings
  WHERE movie_id = NEW.movie_id
  GROUP BY movie_id;
END //
delimiter ;
    
    
CREATE TABLE Theatre(
	theatre_id INTEGER(20),
    theatre_district VARCHAR(20),
    theatre_name VARCHAR(20),
    theatre_capacity INTEGER(20),
    PRIMARY KEY (theatre_id)
);


CREATE TABLE Movie_Sessions(
	session_id INTEGER(20),
    time_slot INTEGER(20) NOT NULL,
    -- session needs to be at a time slot, date and place to be screened
    _date date NOT NULL,
    theatre_id INTEGER (20) NOT NULL,
    FOREIGN KEY (theatre_id) REFERENCES Theatre(theatre_id) ON DELETE CASCADE,
    UNIQUE (time_slot, _date, theatre_id),
    PRIMARY KEY (session_id),
    -- since there cant be more than one session at the same time at the same place I imposed unique, but i wanted pk to be sessionid
	CONSTRAINT CHK_TimeSlot CHECK (time_slot between 1 and 4)
);


CREATE TABLE Screens_as(
	movie_id INTEGER(20),
	session_id INTEGER(20),
    FOREIGN KEY (movie_id) 
		REFERENCES Movie(movie_id)
        ON DELETE CASCADE,
	-- Since if a movie is deleted from the database we cant book it anymore
    FOREIGN KEY (session_id) REFERENCES Movie_Sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,
	PRIMARY KEY (session_id)
    -- one movie cant have the same session id since both session id and movie id is unique
);


drop view if exists sessions_view;

-- create a view to that will be convenient inside the following trigger
create view sessions_view as 
select m.movie_id, m.duration, s.time_slot, s._date, s.theatre_id, s.session_id from movie m
join screens_as sa on sa.movie_id = m.movie_id
join movie_sessions s on s.session_id = sa.session_id; 


-- create a trigger to avoid overlapped sessions for a given date and theatre
drop trigger if exists check_overlapping;

delimiter $$
create trigger check_overlapping
before insert on Screens_as 
for each row
begin
    declare new_time_slot INT;
    declare new_movie_duration INT;
    declare new_date date;
    declare new_theatre_id INT;
    declare previous_slot INT;
    declare previous_duration INT;
	declare proceeding_slot INT;
    declare msg varchar(128);
        
    select duration into new_movie_duration from sessions_view s
    where s.session_id = new.session_id;
    
    select _date into new_date from sessions_view s 
    where s.session_id = new.session_id;
    
    select theatre_id into new_theatre_id from sessions_view s 
    where s.session_id = new.session_id;
    
	select time_slot into new_time_slot from sessions_view s 
    where s.session_id = new.session_id;
    
    select max(time_slot) into previous_slot from sessions_view s
    where s.theatre_id = new_theatre_id and s._date = new_date and time_slot < new_time_slot;
    
    select duration into previous_duration from sessions_view s
    where s.theatre_id = new_theatre_id and s._date = new_date and time_slot = previous_slot;
    
	select min(time_slot)
	into proceeding_slot from sessions_view s
    where s.theatre_id = new_theatre_id and s._date = new_date and time_slot > new_time_slot;
    
    IF  new_time_slot < (previous_slot + previous_duration) then
		set msg = "The theatre has another film sessioned in the given date and slot!";
        signal sqlstate '45000' set message_text = msg;	
	ELSEIF  (new_time_slot + new_movie_duration) > proceeding_slot then
		set msg = "The theatre has another film sessioned in the given date and slot!";
        signal sqlstate '45000' set message_text = msg;	
  end IF;
end $$
delimiter ;
 
CREATE TABLE Bought_tickets(
	username VARCHAR(20),
    session_id INTEGER(20),
    FOREIGN KEY (username) REFERENCES Audience(username) ON DELETE CASCADE,
    -- I wasnt sure whether or not to on delete cascade this since we dont have clear instructions, I kept it
    FOREIGN KEY (session_id) REFERENCES Movie_Sessions(session_id),
    PRIMARY KEY (username, session_id)
    -- cant have the same person book the same session twice so I made this constraint
);


-- trigger to check if a theatre has available seating capacity for a given session
DELIMITER $$
CREATE TRIGGER check_available_seats
BEFORE INSERT ON Bought_tickets
FOR EACH ROW
BEGIN
    DECLARE available_seats INT;
    DECLARE msg VARCHAR(128);
    
    SELECT (theatre_capacity - COUNT(*))
    INTO available_seats
    FROM Bought_tickets
    INNER JOIN Movie_Sessions ON Bought_tickets.session_id = Movie_Sessions.session_id
    INNER JOIN Theatre ON Movie_Sessions.theatre_id = Theatre.theatre_id
    WHERE Bought_tickets.session_id = NEW.session_id
    GROUP BY Theatre.theatre_capacity;

    IF available_seats <= 0 THEN
		set MSG = 'There are no available seats in the theatre!';
        signal sqlstate '45000' set message_text = msg;
    END IF;
END $$
DELIMITER ;



drop trigger if exists check_predecessors;

-- trigger to check if the given audience has watched all the predecessors of a movie she wants to buy a ticket for
DELIMITER $$
CREATE TRIGGER check_predecessors
BEFORE INSERT ON Bought_tickets
FOR EACH ROW
BEGIN
	DECLARE new_movie_id INT;
    DECLARE predecessor_movie_id INT;
    DECLARE count_watched INT;
	DECLARE MSG VARCHAR(128);
    
    SELECT movie_id INTO new_movie_id  FROM screens_as
    WHERE screens_as.session_id = NEW.session_id;
    
    SELECT predecessor_id INTO predecessor_movie_id FROM predecessors
    WHERE predecessors.movie_id = new_movie_id;
    
    IF (predecessor_movie_id IS NOT NULL) AND NOT EXISTS (select username from bought_tickets 
			   where bought_tickets.username = NEW.username and bought_tickets.session_id 
               in ( SELECT session_id FROM screens_as
					WHERE screens_as.movie_id = predecessor_movie_id)) 
		THEN
		set MSG = 'All predecessors, if any, of a movie must be watched before buying a new ticket for the new movie!';
		signal sqlstate '45000' set message_text = msg;
    END IF;
END $$
DELIMITER ;
    
   

CREATE TABLE Database_Managers(
	username VARCHAR(20),
    _password VARCHAR(20),
    PRIMARY KEY (username)
);

