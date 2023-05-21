import requests
from getpass import getpass
from bs4 import BeautifulSoup

def create_user(username, password):
    session = requests.session()

    create_user_url = 'http://127.0.0.1:8000/stats/create_user'
    response = session.get(create_user_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']

    data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': username,
        'password': password,
    }

    response = session.post(create_user_url, data=data)

    if response.status_code == 200:
        print('Account created successfully')
    else:
        print(f'Error {response.status_code} pleas contact to administrator https://github.com/0lch4')
        
        
def login_user(username, password):
    session = requests.session()

    login_url = 'http://127.0.0.1:8000/stats/login'
    response = session.get(login_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']

    data = {
        'csrfmiddlewaretoken': csrf_token,
        'username': username,
        'password': password,
    }

    response = session.post(login_url, data=data)

    if response.status_code == 200:
        print('you successfully logged in')
    else:
        print(f'Error {response.status_code} pleas contact to administrator https://github.com/0lch4')
        
def update(username, new_score):
    update_stats_url = 'http://127.0.0.1:8000/stats/modify'
    data = {
        'username': username,
        'best_score': new_score,
    }

    response = requests.post(update_stats_url, data=data)
    if response.status_code == 200:
        print('Stats have been updated')
    else:
        print(f'Error {response.status_code} pleas contact to administrator https://github.com/0lch4')

def show():
    show_stats_url = 'http://127.0.0.1:8000/stats/show'
    response = requests.get(show_stats_url)
    if response.status_code == 200:
        serialized_stats = response.json()
        print(serialized_stats)
    else:
        print(f'Error {response.status_code} pleas contact to administrator https://github.com/0lch4')


def register():
    username = input('Type your username: ')
    password = getpass('Type your password: ')
    create_user(username, password)
    
def login():
    username = input('Type your username: ')
    password = getpass('Type your password: ')
    login_user(username, password)

def main():
    #register()
    #login()
    update('janek','5')
    show()
    

if __name__ == '__main__':
    main()