import pytest
import requests
from .server_connection_logic import Connection
from .server_connection_logic import load_stats
#testing server connection

account = Connection('testuser','testpassword')

def test_register():
    create =account.register()
    assert create=='success' or create == 'User exists'
    
def test_login():
    login =account.login()
    assert login=='success'
    
def test_show_best_score():
    score=account.show_best_score()
    assert 'output'
    
def test_show_stats():
    score=account.show_stats()
    assert 'output'
    
#can t update stats other users
def test_unauthorized_update_stats():
    username='testuser'
    session = requests.session()
    
    link ='http://127.0.0.1:8000/stats/modify_stats'
    
    data = {
    'username': username,
    'all_levels': 1,
    'all_gold': 1,
    'enemies_killed': 1,
    'destroyed_obstacles': 1,
    'bosses_killed': 1,
    'devils_killed': 1,
    'fasts_killed': 1,
    'mutants_killed': 1,
    'ghosts_killed': 1,
    }
    csrftoken = session.cookies.get('csrftoken')
    session.headers.update({'X-CSRFToken': csrftoken})
    response = session.post(link, data=data)

    assert response.status_code ==403
    
#can t update best scores other users
def test_unauthorized_best_score_stats():
    username='testuser'
    session = requests.session()
     
    link = 'http://127.0.0.1:8000/stats/modify_best_score'
    
    data = {
    'username': username,
    'best_score': 1,
    }
    csrftoken = session.cookies.get('csrftoken')
    session.headers.update({'X-CSRFToken': csrftoken})
    response = session.post(link, data=data)
    
    assert response.status_code ==403



    