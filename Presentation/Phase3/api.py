#use flask to create a web app for super smash bros ultimate tournament creation

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.secret_key = 'supersmashbros'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/roster', methods=['GET', 'POST'])
def roster_page():
    conn = openConnection("./ssb.db")
    cur = conn.cursor()
    

    # Get the search query from the request's args
    search_query = request.args.get('search')
    
    if search_query:
        # If there is a search query, filter the players based on the name (case-insensitive)
        cur.execute("""
            SELECT p_name, sponsor, ctrltype, c_name, character.ch_name
            FROM player
            JOIN country ON player.countryID = country.countryID
            JOIN character ON player.charID = character.charID
            WHERE LOWER(p_name) LIKE LOWER(?)
        """, ('%' + search_query + '%',))
    else:
        # If no search query, fetch all players
        cur.execute("""
            SELECT p_name, sponsor, ctrltype, c_name, character.ch_name
            FROM player
            JOIN country ON player.countryID = country.countryID
            JOIN character ON player.charID = character.charID
        """)

    players = cur.fetchall()
    conn.close()

    return render_template('roster.html', players=players, search_query=search_query)

@app.route('/character')
def character_page():
    conn = openConnection("./ssb.db")
    cur = conn.cursor()
    cur.execute("""
                SELECT ch_name, series, description

                FROM character
                
                """)
    characters = cur.fetchall()
    conn.close()

    for character in characters:
        print("Character: reg")
        image_url = url_for('static', filename='src/images/characters/' + str(character[1]).lower().replace(' ', '-') + '.png')
        print("Image URL:", image_url)
    
    print("Fetched characters:", characters)  # Add this line for debugging
    
    return render_template('character.html', characters=characters)

@app.route('/top_characters', methods=['GET'])
def top_characters():
    conn = openConnection("./ssb.db")
    cur = conn.cursor()

    # Get the selected value from the form
    top_value = request.args.get('top')

    # Use the selected value to determine the LIMIT in the SQL query
    if top_value == 'ALL':
        return redirect(url_for('character_page'))
    else:
        limit_clause = 'LIMIT ' + str(top_value)

    cur.execute(f"""
        SELECT character.ch_name, COUNT(*) AS count
        FROM player
        JOIN character ON player.charID = character.charID
        GROUP BY character.ch_name
        ORDER BY count DESC
        {limit_clause}
    """)

    characters = cur.fetchall()
    conn.close()

    for character in characters:
        print("Character: TOP")
        image_url = url_for('static', filename='src/images/characters/' + str(character[0]).lower().replace(' ', '-') + '.png')
        print("Image URL:", image_url)

    return render_template('character.html', characters=characters)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        name = request.form['name']
        sponsor = request.form['sponsor']
        country_name = request.form['country']
        controller = request.form['controller']
        main = request.form['main']

        conn = openConnection("./ssb.db")
        cur = conn.cursor()

        # Fetch the country ID based on the selected country name
        cur.execute("SELECT countryID FROM country WHERE c_name = ?", (country_name,))
        result = cur.fetchone()

        if result:
            country_id = result[0]

            # Fetch the character ID based on the selected main character name
            cur.execute("SELECT charID FROM character WHERE ch_name = ?", (main,))
            character_result = cur.fetchone()

            if character_result:
                character_id = character_result[0]

                # Insert data into the player table
                cur.execute("""
                    INSERT INTO player (p_name, sponsor, countryID, ctrltype, charID)
                    VALUES (?, ?, ?, ?, ?)
                """, (name, sponsor, country_id, controller, character_id))

                # Commit the changes to the database
                conn.commit()

                # Close the database connection
                conn.close()

                flash("You have been registered!")
                return redirect(url_for('register_page', name=name))
            else:
                flash("Invalid main character name. Please select a valid character.")
                return redirect(url_for('register_page'))
        else:
            flash("Invalid country name. Please select a valid country.")
            return redirect(url_for('register_page'))

    else:
        # Handle the GET request, render the registration form
        # Fetch the list of characters from the database
        conn = openConnection("./ssb.db")
        cur = conn.cursor()
        cur.execute("SELECT ch_name FROM character")
        characters = cur.fetchall()
        conn.close()

        return render_template('register.html', characters=characters)

    
@app.route('/tournament')
def tournament_page():
    conn = openConnection("./ssb.db")
    cur = conn.cursor()

    # Fetch tournament names and years
    cur.execute("""
        SELECT t_name, year, eventID
        FROM tournament
    """)
    tournaments = cur.fetchall()

    # Fetch match counts and player names for each tournament
    tournament_matches = {}
    match_counts = {}
    for tournament in tournaments:
        event_id = tournament[2]

        # Fetch match IDs and player names for each match in the tournament
        #cur.execute("""
        #    SELECT DISTINCT shoubu.matchID, GROUP_CONCAT(player.p_name, ', ')
        #    FROM shoubu
        #    JOIN playermatch ON shoubu.matchID = playermatch.matchID
        #    JOIN player ON playermatch.playerID = player.playerID
        #    WHERE shoubu.eventID = ?
        #    GROUP BY shoubu.matchID
        #""", (event_id,))

        cur.execute("""
            select s.matchID, P1.p_name, P2.p_name, s.result 
            from player P1, player P2, shoubu s, playerMatch pm1, playerMatch pm2 
            where P1.playerID = pm1.playerID 
            and P2.playerID = pm2.playerID 
            and pm1.matchID = pm2.matchID 
            and pm1.playerID <> pm2.playerID 
            and pm1.matchID = s.matchID 
            and P1.playerID < P2.playerID
            and s.eventID = ?
        """, (event_id,))
        
        matches = cur.fetchall()
        tournament_matches[event_id] = matches

        # Fetch match count for each tournament
        cur.execute("""
            SELECT COUNT(DISTINCT matchID) FROM shoubu
            WHERE eventID = ?
        """, (event_id,))
        match_count = cur.fetchone()[0]
        match_counts[event_id] = match_count

    conn.close()

    print("Fetched tournaments:", tournaments)
    print("Match counts:", match_counts)
    print("Tournament matches:", tournament_matches)

    return render_template('tournament.html', tournaments=tournaments, match_counts=match_counts, tournament_matches=tournament_matches)
@app.route('/match')
def match_page():
    conn = openConnection("./ssb.db")
    cur = conn.cursor()

    # Fetch tournaments with eventID
    cur.execute("""
        SELECT tournament.t_name, tournament.eventID
        FROM tournament
    """)
    tournaments = cur.fetchall()

    # Get the selected tournament's eventID from the URL parameter
    selected_event_id = request.args.get('event_id')

    # Fetch matches based on the selected tournament
    cur.execute("""
        SELECT shoubu.matchID, shoubu.eventID, stage.s_name, player.p_name
        FROM shoubu
        JOIN tournament ON shoubu.eventID = tournament.eventID
        JOIN stage ON shoubu.stageID = stage.stageID
        JOIN playerMatch ON shoubu.matchID = playerMatch.matchID
        JOIN player ON playerMatch.playerID = player.playerID
        WHERE shoubu.eventID = ?
    """, (selected_event_id,))

    matches = cur.fetchall()

    conn.close()

    return render_template('match.html', tournaments=tournaments, matches=matches)

@app.route('/tournament_matches/<int:event_id>')
def tournament_matches(event_id):
    conn = openConnection("./ssb.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT matchID, player1, player2, result
        FROM shoubu
        WHERE eventID = ?
    """, (event_id,))
    matches = cur.fetchall()
    conn.close()

    return render_template('matches_for_tournament.html', matches=matches)


@app.route('/delete_player', methods=['POST'])
def delete_player():
    if request.method == 'POST':
        player_id = request.form.get('player_id')  # Assuming you have a form field named 'player_id'
        if player_id:
            conn = openConnection("./ssb.db")
            cur = conn.cursor()

            try:
                # Print the SQL query to debug
                sql_query = "DELETE FROM player WHERE p_name = ?"
                print("SQL Query:", sql_query, "Parameters:", (player_id,))
                
                # Delete the player from the player table
                cur.execute(sql_query, (player_id,))

                # Commit the changes to the database
                conn.commit()

                # Close the database connection
                conn.close()
                print("Player deleted successfully!")
                flash("Player deleted successfully!")
            except Exception as e:
                print("Error:", str(e))
                flash("An error occurred while deleting the player.")
        else:
            flash("Invalid player ID. Please enter a valid player ID.")
    else:
        flash("Invalid request. Please enter a player ID.")

    return redirect(url_for('roster_page'))
    


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


if __name__ == '__main__':
    
    app.run(debug=True)