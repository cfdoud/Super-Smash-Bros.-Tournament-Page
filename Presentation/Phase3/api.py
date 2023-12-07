#use flask to create a web app for super smash bros ultimate tournament creation

from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
app.secret_key = 'supersmashbros'


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/roster')
def roster_page():
    conn = openConnection("./ssb.db")
    cur = conn.cursor()
    cur.execute("""
                SELECT p_name, sponsor, ctrltype, c_name
                FROM player
                JOIN country ON player.countryID = country.countryID
                """)
    players = cur.fetchall()
    conn.close()
    return render_template('roster.html', players=players)


@app.route('/character')
def character_page():
    conn = openConnection("./ssb.db")
    cur = conn.cursor()
    cur.execute("""
                SELECT * FROM character
                """)
    characters = cur.fetchall()
    conn.close()
    
    print("Fetched characters:", characters)  # Add this line for debugging
    
    return render_template('character.html', characters=characters)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        name = request.form['name']
        sponsor = request.form['sponsor']
        country_name = request.form['country']
        controller = request.form['controller']
        main = request.form['main']
        rank = request.form['rank']

        conn = openConnection("./ssb.db")
        cur = conn.cursor()

        # Fetch the country ID based on the selected country name
        cur.execute("SELECT countryID FROM country WHERE c_name = ?", (country_name,))
        result = cur.fetchone()

        if result:
            country_id = result[0]

            # Insert data into the player table
            cur.execute("""
                INSERT INTO player (p_name, sponsor, countryID, ctrltype, rank)
                VALUES (?, ?, ?, ?, ?)
            """, (name, sponsor, country_id, controller, rank))

            # Insert data into the playerCharacter table
            cur.execute("INSERT INTO playerCharacter (playerID, charID) VALUES (?, ?)", (name, main))

            # Commit the changes to the database
            conn.commit()

            # Close the database connection
            conn.close()

            flash("You have been registered!")
            return redirect(url_for('register_page', name=name))
        else:
            flash("Invalid country name. Please select a valid country.")
            return redirect(url_for('register_page'))

    else:
        # Handle the GET request, render the registration form
        return render_template('register.html')

    
@app.route('/tournament')
def tournament_page():
    conn = openConnection("./ssb.db")
    cur = conn.cursor()
    cur.execute("""
                SELECT t_name, year
                FROM tournament
                """)
    tournaments = cur.fetchall()
    conn.close()
    return render_template('tournament.html' , tournaments=tournaments)

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