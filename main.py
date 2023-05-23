import tkinter as tk
from tkinter import messagebox
import server_connection_logic
import subprocess
from tkinter import scrolledtext

links = [
    'http://127.0.0.1:8000/stats/create_user',
    'http://127.0.0.1:8000/stats/login',
]

def main_window(username, account):
    window = tk.Tk()
    window.title(f"Dark_forest_client - {username} Logged In")
    window.geometry("900x603")
    
    background_image = tk.PhotoImage(file="client_textures/background_client.png")

    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    best_scores_button = tk.Button(background_label, text="Global best Scores", command=lambda: show_best_scores_window(account))
    best_scores_button.pack()

    stats_button = tk.Button(background_label, text="Global stats", command=lambda: show_stats_window(account))
    stats_button.pack()

    play_button = tk.Button(background_label, text="Play Dark forest", command=lambda: play(username, account.password))
    play_button.pack()

    window.mainloop()

def show_stats_window(account):
    stats_window = tk.Toplevel()
    stats_window.title("Global Stats")

    stats_text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD)
    stats_text.pack(fill='both', expand=True)

    stats_data = account.show_stats()
    stats_text.insert(tk.END, stats_data)

    stats_window.mainloop()
    
def show_best_scores_window(account):
    best_scores_window = tk.Toplevel()
    best_scores_window.title("Global Best Scores")

    scores_text = scrolledtext.ScrolledText(best_scores_window, wrap=tk.WORD)
    scores_text.pack(fill='both', expand=True)

    best_scores_data = account.show_best_score()
    scores_text.insert(tk.END, best_scores_data)

    best_scores_window.mainloop()

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
        elif check == 'User exists':
            messagebox.showerror('Error', check)
        else:
            messagebox.showerror('Unexpected error', check)

    def login():
        username = username_entry.get()
        password = password_entry.get()
        account = server_connection_logic.Connection(username, password)
        check = account.conn(links[1])
        if check == 'success':
            entry.destroy()
            main_window(username, account)
        elif check == 'Bad username or password':
            messagebox.showerror('Error', check)
        else:
            messagebox.showerror('Unexpected error',check)
            

    label = tk.Label(entry, text="Enter your username:")
    label.pack()

    username_entry = tk.Entry(entry)
    username_entry.pack()

    label = tk.Label(entry, text="Enter your password:")
    label.pack()

    password_entry = tk.Entry(entry, show="*")
    password_entry.pack()

    login_button = tk.Button(entry, text="Login", command=login)
    login_button.pack()

    register_button = tk.Button(entry, text="Register", command=register)
    register_button.pack()

    entry.mainloop()


def play(username, password):
    subprocess.run(['python', 'game/gra.py', username, password])

if __name__ == '__main__':
    start()