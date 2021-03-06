import pytest
import json

from flask import template_rendered, url_for
from server import loadClubs, loadCompetitions, app
from datetime import datetime


@pytest.fixture(scope='module')
def test_client():
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    yield testing_client  # this is where the testing happens!
    ctx.pop()


@pytest.fixture
def captured_templates():
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


def test_loadClubs_ok():
    result = loadClubs()
    with open('tests/test_clubs.json') as c:
        assert result == json.load(c)['clubs']


def test_loadCompetitions_ok():
    result = loadCompetitions()
    with open('tests/test_competitions.json') as c:
        assert result == json.load(c)['competitions']


def test_view_index_ok(test_client, captured_templates):
    response = test_client.get('/')
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'index.html'


def test_view_showSummary_ok(test_client, captured_templates):
    with open('tests/test_clubs.json') as c:
        clubs = json.load(c)['clubs']
    with open('tests/test_competitions.json') as c:
        competitions = json.load(c)['competitions']
    response = test_client.get('/showSummary/Iron_Temple')
    club = clubs[1]
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'welcome.html'
    assert context["club"] == club
    assert context["competitions"] == competitions
    assert context["datetime"] == datetime


def test_view_club_good_email(test_client, captured_templates):
    with open('tests/test_clubs.json') as c:
        clubs = json.load(c)['clubs']
    data = {'email': "john@simplylift.co"}
    response = test_client.post('/club', data=data)
    club = clubs[0]
    assert response.status_code == 200
    assert clubs[0]['email'] == "john@simplylift.co"
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'clubs.html'
    assert context["clubs"] == clubs
    assert context["club"] == club


def test_view_club_bad_email(test_client, captured_templates):
    with open('tests/test_clubs.json') as c:
        clubs = json.load(c)['clubs']
    data = {'email': "n@simplylift.co"}
    response = test_client.post('/club', data=data)
    assert response.status_code == 200
    assert clubs[0]['email'] != "n@simplylift.co"
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'index.html'


def test_view_book_ok(test_client, captured_templates):
    with open('tests/test_clubs.json') as c:
        clubs = json.load(c)['clubs']
    with open('tests/test_competitions.json') as c:
        competitions = json.load(c)['competitions']
    response = test_client.get('/book/Fall_Classic/Iron_Temple')
    club = clubs[1]
    competition = competitions[1]
    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'booking.html'
    assert context["club"] == club
    assert context["competition"] == competition


def test_view_purchasePlace_nbPoint_inferieur_a_NbPLace_demande(test_client, captured_templates):
    with open('tests/test_clubs.json') as c:
        clubs = json.load(c)['clubs']
    with open('tests/test_competitions.json') as c:
        competitions = json.load(c)['competitions']
    data = {"club": "Iron_Temple", "competition": "Fall_Classic", "places": 5}
    response = test_client.post('/purchasePlaces', data=data)
    club = clubs[1]
    assert response.status_code == 200
    assert int(clubs[1]['points']) < data['places']
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'welcome.html'
    assert context["club"] == club
    assert context["competitions"] == competitions
    assert context["datetime"] == datetime


def test_view_purchasePlace_NbPlace_demande_superieur_a_douze(test_client, captured_templates):
    CONST_MAX_PLACE = 12
    with open('tests/test_clubs.json') as c:
        clubs = json.load(c)['clubs']
    with open('tests/test_competitions.json') as c:
        competitions = json.load(c)['competitions']
    data = {"club": "Iron_Temple", "competition": "Fall_Classic", "places": 13}
    response = test_client.post('/purchasePlaces', data=data)
    club = clubs[1]
    assert response.status_code == 200
    assert CONST_MAX_PLACE < data['places']
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'welcome.html'
    assert context["club"] == club
    assert context["competitions"] == competitions
    assert context["datetime"] == datetime


def test_view_purchasePlace_nbPoint_superieur_a_NbPLace_demande(test_client, captured_templates):
    CONST_MAX_PLACE = 12
    with open('tests/test_clubs.json') as c:
        clubs = json.load(c)['clubs']
    with open('tests/test_competitions.json') as c:
        competitions = json.load(c)['competitions']
    data = {"club": "Iron_Temple", "competition": "Fall_Classic", "places": 3}
    response = test_client.post('/purchasePlaces', data=data)
    assert response.status_code == 200
    assert int(clubs[1]['points']) > data['places']
    assert CONST_MAX_PLACE > data['places']
    assert int(clubs[1]['points']) - data['places']
    assert int(competitions[1]["numberOfPlaces"]) - data['places']
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == 'welcome.html'
    clubs[1]['points'] = 1
    club = clubs[1]
    competitions[1]["numberOfPlaces"] = 10
    assert context["club"] == club
    assert context["competitions"] == competitions
    assert context["datetime"] == datetime


def test_logout_ok(test_client):
    response = test_client.get('/logout')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost/'
