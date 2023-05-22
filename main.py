import requests
from getpass import getpass
from bs4 import BeautifulSoup
import json


class Connection:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
    def conn(self,link,text):
        self.session = requests.session()
        self.response=self.session.get(link)
        soup = BeautifulSoup(self.response.content, 'html.parser')
        self.csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.data = {
        'csrfmiddlewaretoken': self.csrf_token,
        'username': self.username,
        'password': self.password,
        }
        self.response = self.session.post(link, data=self.data)
        if self.response.status_code == 200:
            print(text)
        else:
            print(f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4')
        
    def update(self,new_score,link,text):
        self.data = {
        'username': self.username,
        'best_score': new_score,
        }
        self.response = requests.post(link, data=self.data)
        if self.response.status_code == 200:
            print(text)
        else:
            print(f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4')
        
    def show(self,link):
        self.response = requests.get(link)
        if self.response.status_code == 200:
            self.stats = self.response.json()
            self.stats = json.loads(self.stats)
            for i in self.stats:
                print(i['fields']['username'],i['fields']['best_score'])
        else:
            print(f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4')

texts=[
    'Account created successfully',
    'You succesfully logged in',
    'Stats has been updated',
]

links=[
    'http://127.0.0.1:8000/stats/create_user',
    'http://127.0.0.1:8000/stats/login',
    'http://127.0.0.1:8000/stats/modify',
    'http://127.0.0.1:8000/stats/show',
]

def main():
    username = input('Type your username: ')
    password = getpass('Type your password: ')
    acc = Connection(username,password)
    #create user
    acc.conn(links[0],texts[0])
    #login user
    acc.conn(links[1],texts[1])
    #update user's stats
    acc.update(12,links[2],texts[2])
    #show global stats
    acc.show(links[3])
    

if __name__ == '__main__':
    main()