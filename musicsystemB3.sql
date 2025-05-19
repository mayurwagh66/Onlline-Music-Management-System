-- Drop all tables if they exist
DROP TABLE IF EXISTS User_History;
DROP TABLE IF EXISTS Favorites;
DROP TABLE IF EXISTS Playlist_Songs;
DROP TABLE IF EXISTS Playlists;
DROP TABLE IF EXISTS Song_Moods;
DROP TABLE IF EXISTS Songs;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS Artists;
DROP TABLE IF EXISTS Moods;
DROP TABLE IF EXISTS Users;

CREATE DATABASE musicsystemB43;
USE musicsystemB43

CREATE TABLE Users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    user_type VARCHAR(10) NOT NULL DEFAULT 'user' CHECK (user_type IN ('user', 'admin'))
);

CREATE TABLE Artists (
    artist_id INT PRIMARY KEY IDENTITY(1,1),
    artist_name VARCHAR(100) NOT NULL,
    genre VARCHAR(50)
);

CREATE TABLE Albums (
    album_id INT PRIMARY KEY IDENTITY(1,1),
    album_name VARCHAR(100) NOT NULL,
    artist_id INT NOT NULL,
    release_year INT,
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id)
);

CREATE TABLE Songs (
    song_id INT PRIMARY KEY IDENTITY(1,1),
    song_name VARCHAR(100) NOT NULL,
    artist_id INT NOT NULL,
    album_id INT NOT NULL,
    release_year INT,
    file_path VARCHAR(200),
    FOREIGN KEY (artist_id) REFERENCES Artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES Albums(album_id)
);

CREATE TABLE Moods (
    mood_id INT PRIMARY KEY IDENTITY(1,1),
    mood_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Song_Moods (
    song_id INT NOT NULL,
    mood_id INT NOT NULL,
    PRIMARY KEY (song_id, mood_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id),
    FOREIGN KEY (mood_id) REFERENCES Moods(mood_id)
);

CREATE TABLE Playlists (
    playlist_id INT PRIMARY KEY IDENTITY(1,1),
    user_id INT NOT NULL,
    playlist_name VARCHAR(100) NOT NULL,
    is_default BIT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Playlist_Songs (
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES Playlists(playlist_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

CREATE TABLE User_History (
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    played_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);

CREATE TABLE Favorites (
    user_id INT NOT NULL,
    song_id INT NOT NULL,
    PRIMARY KEY (user_id, song_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (song_id) REFERENCES Songs(song_id)
);



-- Insert sample users (30 users)
INSERT INTO Users (username, password, email, user_type) VALUES
('admin', 'mpstme@123', 'admin@musicmail.com', 'admin'),
('user1', 'pass1', 'user1@musicmail.com', 'user'),
('user2', 'pass2', 'user2@musicmail.com', 'user'),
('user3', 'pass3', 'user3@musicmail.com', 'user'),
('user4', 'pass4', 'user4@musicmail.com', 'user'),
('user5', 'pass5', 'user5@musicmail.com', 'user'),
('user6', 'pass6', 'user6@musicmail.com', 'user'),
('user7', 'pass7', 'user7@musicmail.com', 'user'),
('user8', 'pass8', 'user8@musicmail.com', 'user'),
('user9', 'pass9', 'user9@musicmail.com', 'user'),
('user10', 'pass10', 'user10@musicmail.com', 'user'),
('user11', 'pass11', 'user11@musicmail.com', 'user'),
('user12', 'pass12', 'user12@musicmail.com', 'user'),
('user13', 'pass13', 'user13@musicmail.com', 'user'),
('user14', 'pass14', 'user14@musicmail.com', 'user'),
('user15', 'pass15', 'user15@musicmail.com', 'user'),
('user16', 'pass16', 'user16@musicmail.com', 'user'),
('user17', 'pass17', 'user17@musicmail.com', 'user'),
('user18', 'pass18', 'user18@musicmail.com', 'user'),
('user19', 'pass19', 'user19@musicmail.com', 'user'),
('user20', 'pass20', 'user20@musicmail.com', 'user'),
('user21', 'pass21', 'user21@musicmail.com', 'user'),
('user22', 'pass22', 'user22@musicmail.com', 'user'),
('user23', 'pass23', 'user23@musicmail.com', 'user'),
('user24', 'pass24', 'user24@musicmail.com', 'user'),
('user25', 'pass25', 'user25@musicmail.com', 'user'),
('user26', 'pass26', 'user26@musicmail.com', 'user'),
('user27', 'pass27', 'user27@musicmail.com', 'user'),
('user28', 'pass28', 'user28@musicmail.com', 'user'),
('user29', 'pass29', 'user29@musicmail.com', 'user');

-- Insert sample artists (30 artists)
INSERT INTO Artists (artist_name, genre) VALUES
('Arijit Singh', 'Bollywood'),
('Shreya Ghoshal', 'Bollywood'),
('A.R. Rahman', 'Bollywood'),
('Sonu Nigam', 'Bollywood'),
('Neha Kakkar', 'Bollywood'),
('Atif Aslam', 'Bollywood'),
('Jubin Nautiyal', 'Bollywood'),
('Armaan Malik', 'Bollywood'),
('Darshan Raval', 'Bollywood'),
('Amit Trivedi', 'Bollywood'),
('Vishal Bhardwaj', 'Bollywood'),
('Pritam', 'Bollywood'),
('Ankit Tiwari', 'Bollywood'),
('Mithoon', 'Bollywood'),
('Vishal-Shekhar', 'Bollywood'),
('KK', 'Bollywood'),
('Sunidhi Chauhan', 'Bollywood'),
('Mohit Chauhan', 'Bollywood'),
('Palak Muchhal', 'Bollywood'),
('Jonita Gandhi', 'Bollywood'),
('Asees Kaur', 'Bollywood'),
('Javed Ali', 'Bollywood'),
('Shilpa Rao', 'Bollywood'),
('Sachet Tandon', 'Bollywood'),
('Parampara Thakur', 'Bollywood'),
('Rochak Kohli', 'Bollywood'),
('Tanishk Bagchi', 'Bollywood'),
('Guru Randhawa', 'Bollywood'),
('Badshah', 'Bollywood'),
('Diljit Dosanjh', 'Bollywood');

-- Insert sample albums (30 albums)
INSERT INTO Albums (album_name, artist_id, release_year) VALUES
('Aashiqui 2', 1, 2021),
('Raabta', 1, 2021),
('Khamoshiyan', 1, 2021),
('Aashiqui', 2, 2021),
('Jab Tak Hai Jaan', 2, 2021),
('Rockstar', 3, 2021),
('Dil Se', 3, 2021),
('Kal Ho Naa Ho', 4, 2021),
('Main Hoon Na', 4, 2021),
('Cocktail', 5, 2021),
('Ae Dil Hai Mushkil', 6, 2021),
('Tere Naal Love Ho Gaya', 6, 2021),
('Tum Bin 2', 7, 2021),
('Baaghi 2', 7, 2021),
('Dhadak', 8, 2021),
('Main Tera Hero', 8, 2021),
('Ek Villain', 9, 2021),
('Luka Chuppi', 9, 2021),
('Dev D', 10, 2021),
('Queen', 10, 2021),
('Haider', 11, 2021),
('Kaminey', 11, 2021),
('Yeh Jawaani Hai Deewani', 12, 2021),
('Barfi', 12, 2021),
('Aashiqui 2 (OST)', 13, 2021),
('Ek Villain (OST)', 13, 2021),
('Aashiqui 2 (OST) Vol 2', 14, 2021),
('Ek Villain (OST) Vol 2', 14, 2021),
('Student of the Year', 15, 2021),
('Bang Bang', 15, 2021);

-- Insert sample songs (30 songs)
INSERT INTO Songs (song_name, artist_id, album_id, release_year, file_path) VALUES
('Tum Hi Ho', 1, 1, 2021, 'songs/tum_hi_ho.mp3'),
('Raabta', 1, 1, 2021, 'songs/raabta.mp3'),
('Khamoshiyan', 1, 1, 2021, 'songs/khamoshiyan.mp3'),
('Sun Raha Hai', 2, 2, 2021, 'songs/sun_raha_hai.mp3'),
('Saans', 2, 2, 2021, 'songs/saans.mp3'),
('Tum Se Hi', 3, 3, 2021, 'songs/tum_se_hi.mp3'),
('Kun Faya Kun', 3, 3, 2021, 'songs/kun_faya_kun.mp3'),
('Dil Se Re', 3, 4, 2021, 'songs/dil_se_re.mp3'),
('Kal Ho Naa Ho', 4, 5, 2021, 'songs/kal_ho_naa_ho.mp3'),
('Main Hoon Na', 4, 5, 2021, 'songs/main_hoon_na.mp3'),
('Tum Hi Ho Bandhu', 5, 6, 2021, 'songs/tum_hi_ho_bandhu.mp3'),
('Tum Hi Ho (Reprise)', 6, 7, 2021, 'songs/tum_hi_ho_reprise.mp3'),
('Tere Naal Love Ho Gaya', 6, 7, 2021, 'songs/tere_naal.mp3'),
('Tum Bin', 7, 8, 2021, 'songs/tum_bin.mp3'),
('Baaghi', 7, 8, 2021, 'songs/baaghi.mp3'),
('Dhadak', 8, 9, 2021, 'songs/dhadak.mp3'),
('Main Tera Hero', 8, 9, 2021, 'songs/main_tera_hero.mp3'),
('Banjaara', 9, 10, 2021, 'songs/banjaara.mp3'),
('Luka Chuppi', 9, 10, 2021, 'songs/luka_chuppi.mp3'),
('Emotional Atyachar', 10, 11, 2021, 'songs/emotional_atyachar.mp3'),
('London Thumakda', 10, 11, 2021, 'songs/london_thumakda.mp3'),
('Bismil', 11, 12, 2021, 'songs/bismil.mp3'),
('Dhan Te Nan', 11, 12, 2021, 'songs/dhan_te_nan.mp3'),
('Badtameez Dil', 12, 13, 2021, 'songs/badtameez_dil.mp3'),
('Phir Le Aya Dil', 12, 13, 2021, 'songs/phir_le_aya_dil.mp3'),
('Sunn Raha Hai', 13, 14, 2021, 'songs/sunn_raha_hai.mp3'),
('Galliyan', 13, 14, 2021, 'songs/galliyan.mp3'),
('Banjaara (Reprise)', 14, 15, 2021, 'songs/banjaara_reprise.mp3'),
('Tu Hi Mera', 14, 15, 2021, 'songs/tu_hi_mera.mp3'),
('Ishq Wala Love', 15, 16, 2021, 'songs/ishq_wala_love.mp3');

-- Insert sample moods (10 moods)
INSERT INTO Moods (mood_name) VALUES
('Happy'),
('Sad'),
('Romantic'),
('Chill'),
('Energetic'),
('Melancholic'),
('Peaceful'),
('Party'),
('Workout'),
('Travel');

-- Insert sample song-mood relationships
INSERT INTO Song_Moods (song_id, mood_id) VALUES
(1, 2),  -- Tum Hi Ho - Sad
(2, 3),  -- Raabta - Romantic
(3, 4),  -- Khamoshiyan - Chill
(4, 1),  -- Sun Raha Hai - Happy
(5, 3),  -- Saans - Romantic
(6, 3),  -- Tum Se Hi - Romantic
(7, 7),  -- Kun Faya Kun - Peaceful
(8, 5),  -- Dil Se Re - Energetic
(9, 2),  -- Kal Ho Naa Ho - Sad
(10, 1), -- Main Hoon Na - Happy
(11, 3), -- Tum Hi Ho Bandhu - Romantic
(12, 2), -- Tum Hi Ho (Reprise) - Sad
(13, 1), -- Tere Naal Love Ho Gaya - Happy
(14, 2), -- Tum Bin - Sad
(15, 5), -- Baaghi - Energetic
(16, 3), -- Dhadak - Romantic
(17, 1), -- Main Tera Hero - Happy
(18, 3), -- Banjaara - Romantic
(19, 1), -- Luka Chuppi - Happy
(20, 8), -- Emotional Atyachar - Party
(21, 1), -- London Thumakda - Happy
(22, 6), -- Bismil - Melancholic
(23, 5), -- Dhan Te Nan - Energetic
(24, 1), -- Badtameez Dil - Happy
(25, 2), -- Phir Le Aya Dil - Sad
(26, 2), -- Sunn Raha Hai - Sad
(27, 3), -- Galliyan - Romantic
(28, 3), -- Banjaara (Reprise) - Romantic
(29, 3), -- Tu Hi Mera - Romantic
(30, 1); -- Ishq Wala Love - Happy

select * from users


-- SQL Query Types with Examples
-- ===========================

-- 1. Basic SELECT Operations
-- --------------------------

-- Simple SELECT
SELECT * FROM Users;
SELECT * FROM Songs;
SELECT * FROM Artists;

-- SELECT with specific columns
SELECT username, email FROM Users;
SELECT song_name, release_year FROM Songs;

-- SELECT with WHERE
SELECT * FROM Songs WHERE release_year = 2021;
SELECT * FROM Users WHERE user_type = 'admin';

-- ORDER BY
SELECT * FROM Songs ORDER BY song_name ASC;
SELECT * FROM Songs ORDER BY release_year DESC;
SELECT * FROM Songs ORDER BY song_name ASC, release_year DESC;

-- SELECT TOP/LIMIT
SELECT TOP 5 * FROM Songs ORDER BY release_year DESC;
SELECT TOP 10 * FROM Users ORDER BY user_id;

-- SELECT DISTINCT
SELECT DISTINCT genre FROM Artists;
SELECT DISTINCT release_year FROM Songs;

-- 2. Multiple Conditions
-- ---------------------

-- NULL checks
SELECT * FROM Songs WHERE file_path IS NULL;
SELECT * FROM Songs WHERE file_path IS NOT NULL;

-- AND conditions
SELECT * FROM Songs 
WHERE release_year = 2021 
AND artist_id = 1;

SELECT * FROM Users 
WHERE user_type = 'user' 
AND email LIKE '%@musicmail.com';

-- OR conditions
SELECT * FROM Songs 
WHERE artist_id = 1 
OR artist_id = 2;

SELECT * FROM Users 
WHERE username LIKE 'user%' 
OR email LIKE '%@gmail.com';

-- IN clauses
SELECT * FROM Songs 
WHERE artist_id IN (1, 2, 3);

SELECT * FROM Users 
WHERE user_type IN ('admin', 'user');

-- BETWEEN ranges
SELECT * FROM Songs 
WHERE release_year BETWEEN 2020 AND 2022;

SELECT * FROM Users 
WHERE user_id BETWEEN 1 AND 10;

-- 3. Pattern Matching (LIKE)
-- -------------------------

-- Start with pattern
SELECT * FROM Songs 
WHERE song_name LIKE 'Tum%';

SELECT * FROM Users 
WHERE username LIKE 'user%';

-- Contains pattern
SELECT * FROM Songs 
WHERE song_name LIKE '%Hi%';

SELECT * FROM Users 
WHERE email LIKE '%@%';

-- Ends with pattern
SELECT * FROM Songs 
WHERE song_name LIKE '%Ho';

SELECT * FROM Users 
WHERE email LIKE '%.com';

-- Single character match
SELECT * FROM Songs 
WHERE song_name LIKE 'T_m%';

SELECT * FROM Users 
WHERE username LIKE 'user_';

-- Complex patterns
SELECT * FROM Songs 
WHERE song_name LIKE '[T-S]%' 
AND song_name LIKE '%[a-z]';

SELECT * FROM Users 
WHERE username LIKE '[a-z]%[0-9]';

-- 4. Joins
-- --------

-- INNER JOIN
SELECT s.song_name, a.artist_name, al.album_name
FROM Songs s
INNER JOIN Artists a ON s.artist_id = a.artist_id
INNER JOIN Albums al ON s.album_id = al.album_id;

-- LEFT JOIN
SELECT u.username, p.playlist_name
FROM Users u
LEFT JOIN Playlists p ON u.user_id = p.user_id;

-- RIGHT JOIN
SELECT a.artist_name, s.song_name
FROM Artists a
RIGHT JOIN Songs s ON a.artist_id = s.artist_id;

-- FULL OUTER JOIN
SELECT u.username, p.playlist_name
FROM Users u
FULL OUTER JOIN Playlists p ON u.user_id = p.user_id;

-- Self Join
SELECT a1.artist_name AS Artist1, a2.artist_name AS Artist2
FROM Artists a1
JOIN Artists a2 ON a1.genre = a2.genre
WHERE a1.artist_id < a2.artist_id;

-- 5. Aggregation and Grouping
-- --------------------------

-- Basic GROUP BY
SELECT artist_id, COUNT(*) as song_count
FROM Songs
GROUP BY artist_id;

-- GROUP BY with HAVING
SELECT artist_id, COUNT(*) as song_count
FROM Songs
GROUP BY artist_id
HAVING COUNT(*) > 2;

-- Multiple aggregates
SELECT 
    artist_id,
    COUNT(*) as song_count,
    AVG(release_year) as avg_year,
    MIN(release_year) as earliest_year,
    MAX(release_year) as latest_year
FROM Songs
GROUP BY artist_id;

-- String aggregation
SELECT 
    artist_id,
    STRING_AGG(song_name, ', ') as all_songs
FROM Songs
GROUP BY artist_id;

-- 6. Set Operations
-- ----------------

-- UNION
SELECT song_name FROM Songs WHERE artist_id = 1
UNION
SELECT song_name FROM Songs WHERE artist_id = 2;

-- INTERSECT
SELECT song_name FROM Songs WHERE release_year = 2021
INTERSECT
SELECT song_name FROM Songs WHERE artist_id = 1;

-- EXCEPT
SELECT song_name FROM Songs
EXCEPT
SELECT song_name FROM Songs WHERE artist_id = 1;

-- UNION ALL
SELECT song_name FROM Songs WHERE artist_id = 1
UNION ALL
SELECT song_name FROM Songs WHERE artist_id = 2;

-- 7. Data Modification
-- -------------------

-- Basic INSERT
INSERT INTO Users (username, password, email, user_type)
VALUES ('newuser', 'password123', 'newuser@email.com', 'user');

-- Multiple row INSERT
INSERT INTO Moods (mood_name)
VALUES ('Excited'), ('Relaxed'), ('Nostalgic');

-- INSERT INTO SELECT
INSERT INTO Favorites (user_id, song_id)
SELECT user_id, song_id 
FROM Users, Songs 
WHERE username = 'user1' AND song_name = 'Tum Hi Ho';

-- UPDATE
UPDATE Songs
SET release_year = 2022
WHERE song_id = 1;

-- DELETE
DELETE FROM Favorites
WHERE user_id = 1 AND song_id = 1;

-- 8. Schema Modification
-- ---------------------

-- Add Column
ALTER TABLE Users
ADD last_login DATETIME;

-- Modify Column
ALTER TABLE Songs
ALTER COLUMN file_path VARCHAR(300);

-- Drop Column
ALTER TABLE Users
DROP COLUMN last_login;

-- Add Constraints
ALTER TABLE Songs
ADD CONSTRAINT chk_release_year CHECK (release_year > 1900);

-- Add Foreign Keys
ALTER TABLE User_History
ADD CONSTRAINT fk_user_history_user
FOREIGN KEY (user_id) REFERENCES Users(user_id);

-- 9. Views
-- --------

-- Simple View
CREATE VIEW vw_artist_songs AS
SELECT a.artist_name, s.song_name, s.release_year
FROM Artists a
JOIN Songs s ON a.artist_id = s.artist_id;

-- Aggregation View
CREATE VIEW vw_artist_stats AS
SELECT 
    a.artist_name,
    COUNT(s.song_id) as total_songs,
    AVG(s.release_year) as avg_release_year
FROM Artists a
JOIN Songs s ON a.artist_id = s.artist_id
GROUP BY a.artist_name;

-- Multiple Join View
CREATE VIEW vw_song_details AS
SELECT 
    s.song_name,
    a.artist_name,
    al.album_name,
    m.mood_name
FROM Songs s
JOIN Artists a ON s.artist_id = a.artist_id
JOIN Albums al ON s.album_id = al.album_id
JOIN Song_Moods sm ON s.song_id = sm.song_id
JOIN Moods m ON sm.mood_id = m.mood_id;

-- 10. Advanced Queries
-- -------------------

-- EXISTS
SELECT a.artist_name
FROM Artists a
WHERE EXISTS (
    SELECT 1 
    FROM Songs s 
    WHERE s.artist_id = a.artist_id 
    AND s.release_year = 2021
);

-- ALL operator
SELECT song_name
FROM Songs
WHERE release_year >= ALL (
    SELECT release_year 
    FROM Songs 
    WHERE artist_id = 1
);

-- Complex nested queries
SELECT song_name
FROM Songs
WHERE artist_id IN (
    SELECT artist_id
    FROM Artists
    WHERE genre = 'Bollywood'
    AND artist_id IN (
        SELECT artist_id
        FROM Songs
        GROUP BY artist_id
        HAVING COUNT(*) > 2
    )
);

-- CASE expressions
SELECT 
    song_name,
    CASE 
        WHEN release_year < 2020 THEN 'Old'
        WHEN release_year = 2020 THEN 'Recent'
        ELSE 'New'
    END as song_age
FROM Songs;

-- NULLIF
SELECT 
    song_name,
    NULLIF(release_year, 2021) as non_2021_year
FROM Songs;

-- 11. Subqueries
-- -------------

-- Subquery in WHERE
SELECT song_name
FROM Songs
WHERE artist_id IN (
    SELECT artist_id 
    FROM Artists 
    WHERE genre = 'Bollywood'
);

-- Correlated subquery
SELECT a.artist_name
FROM Artists a
WHERE EXISTS (
    SELECT 1 
    FROM Songs s 
    WHERE s.artist_id = a.artist_id
);

-- 12. Window Functions
-- -------------------

-- ROW_NUMBER
SELECT 
    song_name,
    release_year,
    ROW_NUMBER() OVER (ORDER BY release_year) as row_num
FROM Songs;

-- RANK
SELECT 
    song_name,
    release_year,
    RANK() OVER (ORDER BY release_year) as rank
FROM Songs;

-- DENSE_RANK
SELECT 
    song_name,
    release_year,
    DENSE_RANK() OVER (ORDER BY release_year) as dense_rank
FROM Songs;

-- 13. Common Table Expressions (CTEs)
-- ---------------------------------

-- Simple CTE
WITH ArtistSongs AS (
    SELECT artist_id, COUNT(*) as song_count
    FROM Songs
    GROUP BY artist_id
)
SELECT a.artist_name, as.song_count
FROM Artists a
JOIN ArtistSongs as ON a.artist_id = as.artist_id;

-- Recursive CTE
WITH RecursiveCTE AS (
    -- Base case
    SELECT artist_id, artist_name, 0 as level
    FROM Artists
    WHERE artist_id = 1
    
    UNION ALL
    
    -- Recursive case
    SELECT a.artist_id, a.artist_name, r.level + 1
    FROM Artists a
    JOIN RecursiveCTE r ON a.artist_id = r.artist_id + 1
    WHERE r.level < 5
)
SELECT * FROM RecursiveCTE; 