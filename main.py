import tkinter as tk
from tkinter import messagebox
import server_connection_logic
import subprocess


texts = [
    'Account created successfully',
    'You successfully logged in',
    'Best score has been updated',
    'Stats has been updated',
]

links = [
    'http://127.0.0.1:8000/stats/create_user',
    'http://127.0.0.1:8000/stats/login',
]


def main_window(username, account):
    window = tk.Tk()
    window.title(f"Dark_forest_client - {username} Logged In")
    window.geometry("600x400")
    
    label = tk.Label(window, text=f"Welcome, {username}")
    label.pack()
    
    best_scores_button = tk.Button(window, text="Global best Scores", command=account.show_best_score)
    best_scores_button.pack()
    
    stats_button = tk.Button(window, text="Global stats", command=account.show_stats)
    stats_button.pack()
    
    play_button = tk.Button(window, text="Play Dark forest", command=play)
    play_button.pack()
    
    window.mainloop()


def start():
    entry = tk.Tk()
    entry.title("Dark_forest_client")
    entry.geometry("600x400")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        account = server_connection_logic.Connection(username, password)
        check = account.conn(links[0])
        if check == 'success':
            entry.destroy()
            main_window(username, account)
        elif check =='User exsist':
            messagebox.showerror('Error',check)
        else:
            messagebox.showerror('Unexpected error',check)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        account = server_connection_logic.Connection(username, password)
        check = account.conn(links[1])
        if check == 'success':
            entry.destroy()
            main_window(username, account)
        elif check == 'Bad username or password':
            messagebox.showerror('Error',check)
        else:
            messagebox.showerror('Unexpected error',check)
            

    label = tk.Label(entry, text="Enter your username:")
    label.pack()

    username_entry = tk.Entry(entry)
    username_entry.pack()

    label = tk.Label(entry, text="Enter your password:")
    label.pack()

    password_entry = tk.Entry(entry)
    password_entry.pack()

    login_button = tk.Button(entry, text="Login", command=login)
    login_button.pack()

    register_button = tk.Button(entry, text="Register", command=register)
    register_button.pack()

    entry.mainloop()
    
def play():
    subprocess.run(['python', 'game/gra.py'])

if __name__=='__main__':
    start()