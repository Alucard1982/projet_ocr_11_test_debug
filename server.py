import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/club', methods=['POST'])
def club():
    for club in clubs:
        if club['email'] == request.form['email']:
            return render_template('clubs.html', clubs=clubs, club=club)
    if club['email'] != request.form['email']:
        flash("sorry this email doesn't exist")
        return render_template('index.html')


@app.route('/showSummary/<club>')
def showSummary(club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    return render_template('welcome.html', club=foundClub, competitions=competitions,
                           datetime=datetime)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    CONST_MAX_PLACES = 12
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if int(club['points']) < placesRequired or CONST_MAX_PLACES < placesRequired:
        flash("Vous avez plus assez de points ou vous avez dépasser"
              " le nombre maximum de places à louer qui est de 12")
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions, datetime=datetime)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
