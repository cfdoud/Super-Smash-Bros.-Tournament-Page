#use flask to create a web app for super smash bros ultimate tournament creation
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/character')
def character_page():
    return render_template('character.html')

@app.route('/register')
def register_page():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)