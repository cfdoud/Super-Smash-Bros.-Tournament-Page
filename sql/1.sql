SELECT stageID from stage 
WHERE stageID = 1; 

select country_name from player, country
where player_name = 'GamesDean';

Select countryID from player
where player_name = 'GamesDean';

select player_name as 'name', country_name as 'country'
from player, country
where player.countryID = country.countryID;

SELECT * from player, country
where player.countryID = country.countryID;

Select player_name as 'name', c_name as 'Character', country_name as 'country'
FROM player, character, country, playerCharacter
where player.playerID = character.charID
AND player_name = 'Jacky'
AND player.countryID = country.countryID
;

SELECT player_name, playerCharacter.charID ,c_name as 'Character' from player, playerCharacter, character
where player_name = 'Jacky'
AND player.playerID = playerCharacter.playerID
AND playerCharacter.charID = character.charID;

SELECT player_name, playerCharacter.charID ,c_name as 'Character', tournament_name as 'Tournament' 
from 
    player, 
    playerCharacter, 
    character,
    tournament,
    playerTournament,
    country
where player_name = 'Jacky'
AND player.playerID = playerCharacter.playerID
AND playerCharacter.charID = character.charID
AND playerTournament.playerID = player.playerID
AND playerTournament.eventID = tournament.eventID
AND player.countryID = country.countryID;

SELECT year, player_name, placement 
FROM 
    tournament, 
    player,
    playerTournament
WHERE tournament_name = 'RedBull'
AND player.playerID = playerTournament.playerID
AND playerTournament.eventID = tournament.eventID;

SELECT player_name, tournament_name, name as 'stage name'
FROM 
    tournament, 
    player,
    playerTournament,
    match,
    playerMatch,
    stage,
    round,
    roundStage
WHERE player.playerID = playerTournament.playerID
AND playerTournament.eventID = tournament.eventID
AND tournament_name = 'UCM'
AND playerMatch.playerID = player.playerID
AND playerMatch.matchID = match.matchID
AND match.matchID = round.roundID
AND round.roundID = roundStage.roundID
AND roundStage.stageID = stage.stageID;
