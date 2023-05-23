import requests
from getpass import getpass
from bs4 import BeautifulSoup
import json

class Connection:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
    def conn(self,link):
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
        if link.endswith('login'):
            if self.response.status_code == 200 and self.response.url.endswith('login_success'):
                return 'success'
            else:
                if self.response.status_code == 200:
                    return 'Bad username or password'
                else:
                    return f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4'

                
        if link.endswith('create_user'):
            if self.response.status_code == 200 and self.response.url.endswith('register_success'):
                return 'success'
            else:
                if self.response.status_code == 200:
                    return 'User exsist'
                else:
                    return f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4'
    
    def update_best_score(self):
        link = 'http://127.0.0.1:8000/stats/modify_best_score'
        new_best_score=load_stats()
        self.data = {
        'username': self.username,
        'best_score': new_best_score['best_score'],
        }
        self.response = requests.post(link, data=self.data)
        if self.response.status_code == 200:
            pass
        else:
            print(f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4')
        
    def show_best_score(self):
        link='http://127.0.0.1:8000/stats/show_best_score'
        self.response = requests.get(link)
        if self.response.status_code == 200:
            self.stats = self.response.json()
            self.stats = json.loads(self.stats)
            output=''
            for i in self.stats:
                output+=(
                    f"{i['fields']['username']}: "
                    F"{i['fields']['best_score']}\n"
                )
            return output
        else:
            return f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4'
    
    def update_stats(self):
        link ='http://127.0.0.1:8000/stats/modify_stats'
        new_stats = load_stats()
        self.data = {
        'username': self.username,
        'all_levels': new_stats['all_levels'],
        'all_gold': new_stats['all_gold'],
        'enemies_killed': new_stats['enemies_killed'],
        'destroyed_obstacles': new_stats['destroyed_obstacles'],
        'bosses_killed': new_stats['bosses_killed'],
        'devils_killed': new_stats['devils_killed'],
        'fasts_killed': new_stats['fasts_killed'],
        'mutants_killed': new_stats['mutants_killed'],
        'ghosts_killed': new_stats['ghosts_killed'],
        }
        self.response = requests.post(link, data=self.data)
        if self.response.status_code == 200:
            pass
        else:
            return f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4'
        
    def show_stats(self):
        link='http://127.0.0.1:8000/stats/show_stats'
        self.response = requests.get(link)
        if self.response.status_code == 200:
            self.stats = self.response.json()
            self.stats = json.loads(self.stats)
            output = ''
            for i in self.stats:
                output += (
                            f"Username: {i['fields']['username']}\n"
                            f"Levels Compleat: {i['fields']['all_levels']}\n"
                            f"Golds Earned: {i['fields']['all_gold']}\n"
                            f"Enemies Killed: {i['fields']['enemies_killed']}\n"
                            f"Destroyed Obstacles: {i['fields']['destroyed_obstacles']}\n"
                            f"Bosses Killed: {i['fields']['bosses_killed']}\n"
                            f"Devils Killed: {i['fields']['devils_killed']}\n"
                            f"Fasts Killed: {i['fields']['fasts_killed']}\n"
                            f"Mutants Killed: {i['fields']['mutants_killed']}\n"
                            f"Ghosts Killed: {i['fields']['ghosts_killed']}\n\n"
                        )

            return output
        else:
            return f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4'

def load_stats():
    with open('game/stats.json','r') as f:
        new_stats = json.load(f)
    return new_stats

texts=[
    'Account created successfully',
    'You succesfully logged in',
    'Best score has been updated',
    'Stats has been updated',
]

links=[
    'http://127.0.0.1:8000/stats/create_user',
    'http://127.0.0.1:8000/stats/login',
]

def main():
    username = input('Type your username: ')
    password = getpass('Type your password: ')
    acc = Connection(username,password)
    #create user
    acc.conn(links[0])
    #login user
    #acc.conn(links[1],texts[1])
    #update user's best score
    #acc.update_best_score(links[2],texts[2])
    #show global best scores
    #acc.show_best_score(links[3])
    #update user's stats
    #acc.update_stats(links[4],texts[3])
    #show global stats
    #acc.show_stats(links[5])
    

if __name__ == '__main__':
    main()