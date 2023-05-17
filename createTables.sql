-- I will first create tables for entities and then proceed to create the relations


create table User
(username varchar(200), password varchar(20), name varchar(50), surname varchar(50),
primary key (username));


-- Both name and id must be unique for rating platforms
create table Rating_Platform
(platform_id varchar(20), platform_name varchar(200),
primary key (platform_id, platform_name));

-- Although Directors entity has only one attribute, I show its corresponding 
-- relations later on including the nationality, platform_id, etc.
create table Directors
(username varchar(200), 
primary key (username),
foreign key (username) references User(username));

create table Nations
(nation varchar(20) not null,
unique (nation));


-- Similarly, I show the corresponding relations for Audience later on 
-- including the sessions bought, platforms subscribed, etc.
-- Audience and Directors COVER Users
create table Audience
(username varchar(20), 
primary key (username),
foreign key (username) references User(username) on delete cascade);




create table Movies
(movie_id varchar(20), duration decimal(4,2), movie_name varchar(200),
 primary key (movie_id));


-- Note, a username can rate different movies. We will show the Rate relation later 
-- on to make sure a user can rate a movie only once.
-- Additionally, we ensure that a rating score is a float number between 0 and 5
-- Also, a user may choose to not rate a movie at all. 
create table Ratings
(username varchar(200),  movie_id varchar(20), rating decimal(2,1), check (rating <= 5 and rating >= 0),
foreign key (username) references Audience(username) on delete cascade,
foreign key (movie_id) references Movies(movie_id) on delete cascade
);


create table Predecessors
(movie_id varchar(20), predecessor_id varchar(200),
primary key (movie_id, predecessor_id),
foreign key (movie_id) references Movies(movie_id),
foreign key (predecessor_id) references Movies(movie_id)
);

create table Genres
(genre_id varchar(20), genre_name varchar(20),
primary key (genre_id, genre_name));


-- a theatre id determines the corresponding theatre district and capacity
create table Theatre_Location
(theatre_id varchar(20),  theatre_name varchar(50), theatre_district varchar(20), theatre_capacity int, 
primary key (theatre_id));


create table Movie_Sessions
(session_id varchar(20), date date, theatre_id varchar(20),
primary key (session_id),
foreign key (theatre_id) references Theatre_Location(theatre_id) on delete cascade);


-- I couldn't create a table such that at most 4 database managers can be 
-- registered to the system
create table Database_Managers
(username varchar(50), password varchar(20) not null,
primary key (username));



-- RELATIONS 
-- We will now show the relations between entities


-- Each director must have only one nation 
-- we satisfy the participation constraint by setting nation not null and 
-- having the director's username as the primary key. Note, we don't even 
-- need to unique constraint since primary key will ensure
-- there are no duplicate directors and not null constraint for nation 
-- will assign only one nation per director. 
create table Nationality 
(username varchar(200), nation varchar(20) not null,
primary key (username),
foreign key (username) references Directors (username) on delete cascade,
foreign key (nation) references Nations (nation) on delete cascade);


-- Rate is a weak entity set where an user can rate a movie only once 
create table Rate
(username varchar(200), movie_id varchar(20), ratings float check (ratings <= 5 and ratings >= 0),
primary key (username, movie_id),
foreign key (username) references Ratings (username) on delete cascade); 


-- Genre relation ensures the participation constraint - that is each movie has 
-- at least one genre
create table Genre
(movie_id varchar(20), genre_id varchar(20) not null,
primary key (movie_id),
foreign key (movie_id) references Movies (movie_id) on delete cascade,
foreign key (genre_id) references Genres (genre_id) on delete cascade);


-- shows the Subscription relation between Audiences and Rating platforms. 
-- An audience can subscribe to different platforms
-- Moreover, Subscription relation has an aggregation relation with 
-- the Rates relation where Rates has a total participation to the Subscription 
create table Subscription
(username varchar(200), platform_id varchar(20), movie_id varchar(20),
primary key (username, platform_id, movie_id),
foreign key (movie_id) references Movies (movie_id) on delete cascade,
foreign key (username) references Audience (username) on delete cascade,
foreign key (platform_id) references 
Rating_Platform (platform_id) on delete cascade);

-- shows the Bought sessions relation between Audiences and Movie Sessions. 
-- An audience can buy tickets to different sessions
-- Similary, Bought has an aggregation relation to the Rates, and Rates must have
-- total participation to the Bought sessions as well. Overall, Subscription and Bought 
-- relations will ensure a user can rate a movie if s/he is subscribed to the movie's
-- platform and bought a ticket to the movie
create table Bought
(username varchar(200), session_id varchar(20), movie_id varchar(20),
primary key (username, session_id, movie_id),
foreign key (username) references Audience (username) on delete cascade,
foreign key (session_id) references Movie_Sessions (session_id) on delete cascade,
foreign key (movie_id) references Movies (movie_id) on delete cascade);



-- Filmed relation will make sure there will be no overlap of two films at the 
-- same date and theatre Filmed has a total participation constraint with 
-- both Theatre location and movies. 
-- Note, I wasn't able to create 4 different time slots for each day
create table Filmed
(session_id varchar(20), movie_id varchar(20) not null, 
theatre_id varchar(20) not null,
 time_slot int, 
primary key (session_id, movie_id, theatre_id), 
foreign key (movie_id) references
 Movies (movie_id) on delete cascade,
foreign key (theatre_id) references 
Theatre_Location (theatre_id) on delete cascade);


-- Directed By relation will ensure a movie will have only one director
--  and has the same platform with the director.
-- Directed By has a total participation constraint where each movie needs
--  to have exactly one director 
create table Directed_By
(movie_id varchar(20), username varchar(200) not null,
primary key (movie_id),
foreign key (username) references Directors (username) on delete cascade);


-- Agreement relation will ensure the key constraint between directors and rating platforms.
-- That is each director can have an agreement with at most one platform
create table Agreement
(username varchar(200), platform_id varchar(20), 
primary key (username),
unique (username, platform_id),
foreign key (platform_id) references
 Rating_Platform (platform_id) on delete cascade);




-- END