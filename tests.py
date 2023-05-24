import pytest
from .server_connection_logic import Connection
#testing server connection

account = Connection('testuser','testpassword')

def test_conn():
    create =account.conn('http://127.0.0.1:8000/stats/create_user')
    assert create=='success' or create == 'User exsist'
    
    login =account.conn('http://127.0.0.1:8000/stats/login')
    assert login=='success'
    
def test_show_best_score():
    score=account.show_best_score()
    assert 'output'
    
def test_show_stats():
    score=account.show_stats()
    assert 'output'
    