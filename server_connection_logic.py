import requests
from bs4 import BeautifulSoup
import json

#user have to be always log in if he want connecct to the server
class Connection:
    def __init__(self,username,password):
        self.username = username
        self.password = password
    #login or register in server, only links was changed    
    def conn(self,link):
        self.session = requests.session()
        self.response=self.session.get(link)
        soup = BeautifulSoup(self.response.content, 'html.parser')
        #additional security when logging in
        self.csrf_token = soup.find('input', attrs={'name': 'csrfmiddlewaretoken'})['value']
        self.data = {
        'csrfmiddlewaretoken': self.csrf_token,
        'username': self.username,
        'password': self.password,
        }
        #send data to server
        self.response = self.session.post(link, data=self.data)
        
        #i excpect some login errors and return values for them
        if link.endswith('login'):
            if self.response.status_code == 200 and self.response.url.endswith('login_success'):
                return 'success'
            else:
                if self.response.status_code == 200:
                    return 'Bad username or password'
                else:
                    #for unexpected errors
                    return f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4'

        #i excpect some register errors and return values for them        
        if link.endswith('create_user'):
            if self.response.status_code == 200 and self.response.url.endswith('register_success'):
                return 'success'
            else:
                if self.response.status_code == 200:
                    return 'User exsist'
                else:
                    #for unexpected errors
                    return f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4'
                
    #send new player best score to server
    def update_best_score(self,username):
        link = 'http://127.0.0.1:8000/stats/modify_best_score'
        #score was reading from json file
        new_best_score=load_stats(username)
        self.data = {
        'username': self.username,
        'best_score': new_best_score['best_score'],
        }
        self.response = requests.post(link, data=self.data)
        if self.response.status_code == 200:
            pass
        else:
            print(f'Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4')
    
    #show global best scores    
    def show_best_score(self):
        link = 'http://127.0.0.1:8000/stats/show_best_score'
        self.response = requests.get(link)
        
        if self.response.status_code == 200:
            self.stats = self.response.json()
            self.stats = json.loads(self.stats)
            #Sort by best score
            sorted_stats = sorted(self.stats, key=lambda x: x['fields']['best_score'], reverse=True)
            output = ''
            #return data to main app
            for i in sorted_stats:
                output += f"{i['fields']['username']}: {i['fields']['best_score']}\n"
            
            return output
        else:
            return f'Error {self.response.status_code}, please contact the administrator at https://github.com/0lch4'
        
    #send new player statse to server 
    def update_stats(self,username):
        link ='http://127.0.0.1:8000/stats/modify_stats'
        #stats was reading from json file
        new_stats = load_stats(username)
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
        
    #show global stats            
    def show_stats(self):
        link='http://127.0.0.1:8000/stats/show_stats'
        self.response = requests.get(link)
        if self.response.status_code == 200:
            self.stats = self.response.json()
            self.stats = json.loads(self.stats)
            output = ''
            #return data to main app
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
    
    #load user data from server to local    
    def load_data_to_local(self):
        #links with user stats and best score
        score_link = 'http://127.0.0.1:8000/stats/show_best_score'
        stats_link = 'http://127.0.0.1:8000/stats/show_stats'
        self.response_score = requests.get(score_link)
        self.response_stats = requests.get(stats_link)

        data_stats = {}
        data_score = {}

        if self.response_stats.status_code == 200:
            self.stats = self.response_stats.json()
            self.stats = json.loads(self.stats)
            #import stats data from server
            for entry in self.stats:
                if entry['fields']['username'] == self.username:
                    data_stats = {
                        'all_levels': entry['fields']['all_levels'],
                        'all_gold': entry['fields']['all_gold'],
                        'enemies_killed': entry['fields']['enemies_killed'],
                        'destroyed_obstacles': entry['fields']['destroyed_obstacles'],
                        'bosses_killed': entry['fields']['bosses_killed'],
                        'devils_killed': entry['fields']['devils_killed'],
                        'fasts_killed': entry['fields']['fasts_killed'],
                        'mutants_killed': entry['fields']['mutants_killed'],
                        'ghosts_killed': entry['fields']['ghosts_killed'],
                    }
                    break
                else:
                    #if user was created program use this 
                    data_stats = {
                        'all_levels': 0,
                        'all_gold': 0,
                        'enemies_killed': 0,
                        'destroyed_obstacles': 0,
                        'bosses_killed': 0,
                        'devils_killed': 0,
                        'fasts_killed': 0,
                        'mutants_killed': 0,
                        'ghosts_killed': 0,
                    }
        #same to best score
        if self.response_score.status_code == 200:
            self.score = self.response_score.json()
            self.score = json.loads(self.score)

            for entry in self.score:
                if entry['fields']['username'] == self.username:
                    data_score = {
                        'best_score': entry['fields']['best_score'],
                    }
                    break
                else:
                    data_score={
                        'best_score':0,
                    }
        #join two dicts
        data_combined = { **data_score,**data_stats}
        #save it
        with open(f'game/stats/{self.username}/stats.json','w') as f:
            json.dump(data_combined,f,indent=4)

#load data from json file
def load_stats(username):
    with open(f'game/stats/{username}/stats.json','r') as f:
        new_stats = json.load(f)
    return new_stats
