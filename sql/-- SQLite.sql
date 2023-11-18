-- SQLite chaanged up
INSERT INTO player (playerID, player_name, rank, sponsor, controllertype, countryID) 
VALUES (NULL, 'GamesDean', 88, 'VGHS', 'WiiMote', NULL);

INSERT INTO country (countryID, name)
VALUES 
    (1, 'US'),
    (2, 'Canada'),
    (3, 'Mexico'),
    (4, 'Japan')
    ;

INSERT INTO character (charID, name, origin, description)
VALUES
    (1, 'Mario', 'Super Mario', 'The iconic plumber from the Mushroom Kingdom.'),
    (2, 'Donkey Kong', 'Donkey Kong', 'The original gorilla with a tie and a penchant for barrels.'),
    (3, 'Link', 'The Legend of Zelda', 'The hero of Hyrule and the wielder of the Master Sword.'),
    (4, 'Samus', 'Metroid', 'The intergalactic bounty hunter in a powered suit.'),
    (5, 'Yoshi', 'Super Mario', 'A friendly dinosaur who serves as Mario''s trusty steed.'),
    (6, 'Kirby', 'Kirby', 'A pink, round, and adorable hero with the ability to copy powers.');
