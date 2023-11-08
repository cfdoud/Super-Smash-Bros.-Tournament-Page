# Python script to execute sql queries on database
# original skeleton code provided by Professor Rusu
# modified by Tanner Jackson and Christian Doud

import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    """ close the connection to the database
        specified by the db_file"""
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def createTables(_conn):
    """ create all the tables for the database with
        their columns and corresponding datatypes"""
    print("++++++++++++++++++++++++++++++++++")
    print("Create tables")

    _conn.execute("BEGIN")
    try:
        sql = """CREATE TABLE character (
                    charID integer,
                    c_name text,
                    origin text,
                    description text)"""
        _conn.execute(sql)

        sql = """CREATE TABLE country (
                    countryID integer,
                    country_name text)"""
        _conn.execute(sql)

        sql = """CREATE TABLE player (
                playerID INTEGER,
                player_name text,
                rank INTEGER,
                sponsor text,
                controllertype text,
                countryID integer)"""
        _conn.execute(sql)

        sql = """CREATE TABLE playerCharacter (
                playerID integer,
                charID integer)"""
        _conn.execute(sql)

        sql = """CREATE TABLE playerMatch (
                playerID integer,
                matchID integer)"""
        _conn.execute(sql)

        sql = """CREATE TABLE playerTournament (
                playerID integer,
                eventID integer,
                winnings decimal,
                placement integer)"""
        _conn.execute(sql)

        sql = """CREATE TABLE round (
                roundID integer,
                matchID integer,
                result text)"""
        _conn.execute(sql)

        sql = """CREATE TABLE roundStage (
                stageID integer,
                roundID integer)"""
        _conn.execute(sql)

        sql = """CREATE TABLE shoubu (
                matchID integer,
                eventID integer,
                result text)"""
        _conn.execute(sql)

        sql = """CREATE TABLE stage (
                stageID integer,
                name text,
                origin text)"""
        _conn.execute(sql)

        sql = """CREATE TABLE tournament (
                eventID integer,
                tournament_name text,
                year integer)"""
        _conn.execute(sql)

        _conn.execute("COMMIT")
        print("success")
    except Error as e:
        _conn.execute("ROLLBACK")
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def dropTable(_conn, _table):
    """ drop a given table
    :param _table: table name"""
    print("++++++++++++++++++++++++++++++++++")
    print("Drop ", _table)

    try:
        sql = "DROP TABLE {}".format(_table)
        #args = [_table]
        _conn.execute(sql)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertChar(_conn, _cID, _name, _origin, _description):
    # insert given data into the character table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert character")

    try:
        sql = """INSERT INTO character(charID, c_name, origin, description)
            VALUES(?, ?, ?, ?)"""
        args = [_cID, _name, _origin, _description]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertCountry(_conn, _cID, _name):
    # insert given data into the country table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert country")

    try:
        sql = """INSERT INTO country(countryID, country_name)
            VALUES(?, ?)"""
        args = [_cID, _name]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertPlayer(_conn, _pID, _name, _rank, _sponsor, _ctrlr, _cID):
    # insert given data into the player table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert player")

    try:
        sql = """INSERT INTO player(playerID, player_name, rank, sponsor, controllertype, countryID)
            VALUES(?, ?, ?, ?, ?, ?)"""
        args = [_pID, _name, _rank, _sponsor, _ctrlr, _cID]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertPlayerChar(_conn, _pID, _cID):
    # insert given data into the playerCharacter table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert playerCharacter")

    try:
        sql = """INSERT INTO playerCharacter(playerID, charID)
            VALUES(?, ?)"""
        args = [_pID, _cID]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertPlayerMatch(_conn, _pID, _mID):
    # insert given data into the playerMatch table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert playerMatch")

    try:
        sql = """INSERT INTO playerMatch(playerID, matchID)
            VALUES(?, ?)"""
        args = [_pID, _mID]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertPlayerTournament(_conn, _pID, _eID, _winnings, _placement):
    # insert given data into the playerTournament table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert playerTournament")

    try:
        sql = """INSERT INTO playerTournament(playerID, eventID, winnings, placement)
            VALUES(?, ?, ?, ?)"""
        args = [_pID, _eID, _winnings, _placement]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertRound(_conn, _rID, _mID, _result):
    # insert given data into the round table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert round")

    try:
        sql = """INSERT INTO round(roundID, matchID, result)
            VALUES(?, ?, ?)"""
        args = [_rID, _mID, _result]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertRoundStage(_conn, _sID, _rID):
    # insert given data into the roundStage table
    # stageID and roundID will be swapped later
    print("++++++++++++++++++++++++++++++++++")
    print("Insert roundStage")

    try:
        sql = """INSERT INTO roundStage(stageID, roundID)
            VALUES(?, ?)"""
        args = [_sID, _rID]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertShoubu(_conn, _mID, _eID, _result):
    # insert given data into the shoubu table
    # match is a keyword, so need to change match to shoubu
    # shoubu is the Japanese word for match
    print("++++++++++++++++++++++++++++++++++")
    print("Insert shoubu")

    try:
        sql = """INSERT INTO shoubu(matchID, eventID, result)
            VALUES(?, ?, ?)"""
        args = [_mID, _eID, _result]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertStage(_conn, _sID, _name, _origin):
    # insert given data into the stage table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert stage")

    try:
        sql = """INSERT INTO stage(stageID, name, origin)
            VALUES(?, ?, ?)"""
        args = [_sID, _name, _origin]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def insertTournament(_conn, _eID, _name, _year):
    # insert given data into the tournament table
    print("++++++++++++++++++++++++++++++++++")
    print("Insert tournament")

    try:
        sql = """INSERT INTO tournament(eventID, tournament_name, year)
            VALUES(?, ?, ?)"""
        args = [_eID, _name, _year]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def updatePlayerRank(_conn, _rank, _pID):
    # update a player's rank when given their playerID
    print("++++++++++++++++++++++++++++++++++")
    print("Update player's rank")

    try:
        sql = """UPDATE player
            SET rank = ?
            WHERE playerID = ?"""
        args = [_rank, _pID]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def deletePlayer(_conn, _pID):
    # delete all records of a player when given their playerID
    print("++++++++++++++++++++++++++++++++++")
    print("Delete player")

    try:
        sql = """DELETE from player WHERE playerID = ?"""
        args = [_pID]
        _conn.execute(sql, args)
        sql = """DELETE from playerCharacter WHERE playerID = ?"""
        args = [_pID]
        _conn.execute(sql, args)
        sql = """DELETE from playerMatch WHERE playerID = ?"""
        args = [_pID]
        _conn.execute(sql, args)
        sql = """DELETE from playerTournament WHERE playerID = ?"""
        args = [_pID]
        _conn.execute(sql, args)

        _conn.commit()
        print("success")
    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def charsByPlayer(_conn, _player):
    # display all characters played by a given player
    print("++++++++++++++++++++++++++++++++++")
    print("Characters played by player: ", _player)

    try:
        sql = """select player.player_name, character.c_name 
            from player, character, playerCharacter
            where player.playerID = playerCharacter.playerID 
            and character.charID = playerCharacter.charID 
            and player.player_name = ?"""
        args = [_player]

        cur = _conn.cursor()
        cur.execute(sql, args)

        l = '{:>15} {:>15}'.format("player", "characters")
        print(l)
        print("-------------------------------")

        rows = cur.fetchall()
        for row in rows:
            l = '{:>15} {:>15}'.format(row[0], row[1])
            print(l)

    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def playersByChar(_conn, _char):
    # display all players that play a given character
    print("++++++++++++++++++++++++++++++++++")
    print("Players that play: ", _char)

    try:
        sql = """select character.c_name, player.player_name 
            from player, character, playerCharacter 
            where player.playerID = playerCharacter.playerID 
            and character.charID = playerCharacter.charID
            and character.c_name = ?"""
        args = [_char]

        cur = _conn.cursor()
        cur.execute(sql, args)

        l = '{:>15} {:>15}'.format("character", "players")
        print(l)
        print("-------------------------------")

        rows = cur.fetchall()
        for row in rows:
            l = '{:>15} {:>15}'.format(row[0], row[1])
            print(l)

    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def winningsByPlayer(_conn, _player):
    # display the winnings of a given player at each tournament they attended
    print("++++++++++++++++++++++++++++++++++")
    print("Winnings by player: ", _player)

    try:
        sql = """select player.player_name, tournament.tournament_name, playerTournament.winnings 
            from player, tournament, playerTournament 
            where player.playerID = playerTournament.playerID 
            and tournament.eventID = playerTournament.eventID
            and player.player_name = ?"""
        args = [_player]

        cur = _conn.cursor()
        cur.execute(sql, args)

        l = '{:>15} {:>15} {:>15}'.format("player", "tournament", "winnings")
        print(l)
        print("-------------------------------")

        rows = cur.fetchall()
        for row in rows:
            l = '{:>15} {:>15} {:>15}'.format(row[0], row[1], row[2])
            print(l)

    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def numOfEventsByPlayer(_conn, _player):
    # display the number of tournaments a given player has attended
    print("++++++++++++++++++++++++++++++++++")
    print("Number of tournaments attended by player: ", _player)

    try:
        sql = """select player.player_name, count(tournament.eventID) 
            from player, tournament, playerTournament 
            where player.playerID = playerTournament.playerID 
            and tournament.eventID = playerTournament.eventID 
            and player.player_name = ?
            group by player.player_name"""
        args = [_player]

        cur = _conn.cursor()
        cur.execute(sql, args)

        l = '{:>15} {:>15}'.format("player", "count")
        print(l)
        print("-------------------------------")

        rows = cur.fetchall()
        for row in rows:
            l = '{:>15} {:>15}'.format(row[0], row[1])
            print(l)

    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def playersByEvent(_conn, _event):
    # display all players that attended a given tournament
    print("++++++++++++++++++++++++++++++++++")
    print("Players that attended: ", _event)

    try:
        sql = """select tournament.tournament_name, player.player_name 
            from player, tournament, playerTournament 
            where player.playerID = playerTournament.playerID 
            and tournament.eventID = playerTournament.eventID 
            and tournament.tournament_name = ?"""
        args = [_event]

        cur = _conn.cursor()
        cur.execute(sql, args)

        l = '{:>15} {:>15}'.format("tournament", "players")
        print(l)
        print("-------------------------------")

        rows = cur.fetchall()
        for row in rows:
            l = '{:>15} {:>15}'.format(row[0], row[1])
            print(l)

    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def resultByMatch(_conn, _match):
    # display both players and the result of the given match
    print("++++++++++++++++++++++++++++++++++")
    print("Result of match: ", _match)

    try:
        sql = """select P1.player_name, P2.player_name, shoubu.result 
            from player P1, player P2, shoubu, playerMatch pm1, playerMatch pm2 
            where P1.playerID = pm1.playerID 
            and P2.playerID = pm2.playerID 
            and pm1.matchID = pm2.matchID 
            and pm1.playerID <> pm2.playerID 
            and pm1.matchID = shoubu.matchID 
            and P1.playerID < P2.playerID
            and shoubu.matchID = ?"""
        args = [_match]

        cur = _conn.cursor()
        cur.execute(sql, args)

        l = '{:>15} {:>15} {:>15}'.format("P1", "P2", "result")
        print(l)
        print("-------------------------------")

        rows = cur.fetchall()
        for row in rows:
            l = '{:>15} {:>15} {:>15}'.format(row[0], row[1], row[2])
            print(l)

    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def main():
    database = r"ssb.db"

    # create a database connection
    conn = openConnection(database)
    with conn:
        # createTables(conn)

        # dropTable(conn, 'country')

        # insertChar(conn, 1, 'Mario', 'Super Mario', 'The iconic plumber from the Mushroom Kingdom.')
        # insertCountry(conn, 1, 'US')
        # insertPlayer(conn, 1, 'Chip_Whitley', 100, 'Redbull', 'GameCube', 1)
        # insertPlayerChar(conn, 1, 3)
        # insertPlayerMatch(conn, 1, 2)
        # insertPlayerTournament(conn, 1, 2, 900, 2)
        # insertRound(conn, 1, 2, 'P1')
        # insertRoundStage(conn, 1, 1)
        # insertShoubu(conn, 2, 1, 'P1')
        # insertStage(conn, 1, '3D Land', 'Super Mario')
        # insertTournament(conn, 1, 'UCM', 2023)

        # updatePlayerRank(conn, 100, 1)

        # deletePlayer(conn, 3)

        charsByPlayer(conn, 'Chip_Whitley')

        playersByChar(conn, 'Link')

        winningsByPlayer(conn, 'Chip_Whitley')

        numOfEventsByPlayer(conn, 'Chip_Whitley')

        playersByEvent(conn, 'UCM')

        resultByMatch(conn, 2)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
