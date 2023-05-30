import tkinter as tk
from tkinter import messagebox
import server_connection_logic
import subprocess
from tkinter import ttk, font
import pygame

#playin background music
def play_background_music():
    pygame.mixer.music.load("client_sounds/darkforest_client.mp3")
    pygame.mixer.music.play(-1)
#stop music    
def stop_background_music():
    pygame.mixer.music.stop()
#initialize mixer
pygame.mixer.init()

#main window for client
def main_window(username, account):
    window = tk.Tk()
    #inscription at the top of the window
    window.title(f"Dark_forest_client - {username} Logged In")
    #static window size
    window.geometry("900x600")
    window.resizable(False, False)
    #font, if you have error here pleas install font from game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    #client image    
    background_image = tk.PhotoImage(file="client_textures/background_client.png")
    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #global scores button with some style, forwarding to best scores
    best_scores_button = tk.Button(background_label, text="Global Best Scores",
                                   command=lambda: show_best_scores_window(account, window),
                                   bg="black", fg="red",width=14,height=2,font=dark_forest_font)
    best_scores_button.pack()

    #global stats button with some style, forwarding to stats
    stats_button = tk.Button(background_label, text="Global Stats",
                             command=lambda: show_stats_window(account, window),
                             bg="black", fg="red",width=14,height=2,font=dark_forest_font)
    stats_button.pack(pady=16)

    #game starting button with some style, launching the game
    play_button = tk.Button(background_label, text="Play Dark Forest",
                            command=lambda: play(username, account.password),
                            bg="black", fg="red",width=14,height=2,font=dark_forest_font)
    play_button.pack()
    
    #main loop from main window
    window.mainloop()

#show global stast 
def show_stats_window(account, window):
    #ussing server connection logic method to connect to server
    stats_data = account.show_stats()
    #font, if you have error here pleas install font from game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    #create new view in main window
    stats_pane = ttk.PanedWindow(window, orient=tk.VERTICAL)
    stats_pane.pack(fill='both', expand=True)
    #load background image into paned window
    background_image = tk.PhotoImage(file="client_textures/menu.png")
    background_label = tk.Label(stats_pane, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #inscription at the top of window
    stats_label = tk.Label(stats_pane, text="Global Stats", bg='black', fg="red", font=dark_forest_font)
    stats_label.grid(row=0, column=0, padx=10, pady=10)
    #scrolled area for players stats
    scrollbar = tk.Scrollbar(stats_pane)
    scrollbar.grid(row=1, column=1, sticky=tk.NS)
    stats_text = tk.Text(stats_pane, wrap=tk.WORD, font=dark_forest_font, bg='black', fg="red", yscrollcommand=scrollbar.set)
    stats_text.insert(tk.END, stats_data)
    stats_text.grid(row=1, column=0, padx=10, pady=(0, 10))
    scrollbar.config(command=stats_text.yview)
    #back to the main view in main window
    back_button = tk.Button(stats_pane, text="Back", command=stats_pane.destroy, bg='black', fg="red",
                            font=dark_forest_font)
    back_button.grid(row=2, column=0, pady=10)
    #size
    stats_pane.grid_rowconfigure(1, weight=1)
    stats_pane.grid_columnconfigure(0, weight=1)

def show_best_scores_window(account, window):
    #ussing server connection logic method to connect to server
    best_scores_data = account.show_best_score()
    #font, if you have error here pleas install font from game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    #create new view in main window
    scores_pane = ttk.PanedWindow(window, orient=tk.VERTICAL)
    scores_pane.pack(fill='both', expand=True)
    #load background image into paned window
    background_image = tk.PhotoImage(file="client_textures/menu.png")
    background_label = tk.Label(scores_pane, image=background_image)
    background_label.image = background_image
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #inscription at the top of window
    scores_label = tk.Label(scores_pane, text="Global Best Scores", bg='black', fg="red", font=dark_forest_font)
    scores_label.grid(row=0, column=0, padx=10, pady=10)
    #scrolled area for bestscores
    scrollbar = tk.Scrollbar(scores_pane)
    scrollbar.grid(row=1, column=1, sticky=tk.NS)
    scores_text = tk.Text(scores_pane, wrap=tk.WORD, font=dark_forest_font, bg='black', fg="red", yscrollcommand=scrollbar.set)
    scores_text.insert(tk.END, best_scores_data)
    scores_text.grid(row=1, column=0, padx=10, pady=(0, 10))
    scrollbar.config(command=scores_text.yview)
    #back to the main view in main window
    back_button = tk.Button(scores_pane, text="Back", command=scores_pane.destroy, bg='black', fg="red",
                            font=dark_forest_font)
    back_button.grid(row=2, column=0, pady=10)
    #size
    scores_pane.grid_rowconfigure(1, weight=1)
    scores_pane.grid_columnconfigure(0, weight=1)

def start(): 
    #login/register window, closing after login/register, static window size
    entry = tk.Tk()
    entry.title("Dark_forest_client")
    entry.geometry("400x400")
    entry.resizable(False, False)
    #background music
    play_background_music()
    #font, if you have error here pleas install font from game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    #load background image into window
    background_image = tk.PhotoImage(file="client_textures/menu.png")
    background_label = tk.Label(entry, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    #register function using method from server connection logic
    def register():
        username = username_entry.get()
        password = password_entry.get()
        account = server_connection_logic.Connection(username, password)
        check = account.register()
        #verify response and inform user in case he cant register
        if check == 'success':
            entry.destroy()
            main_window(username, account)
        elif check == 'User exists':
            messagebox.showerror('Error', check)
        else:
            messagebox.showerror('Unexpected error', check)
            
    #login function using method from server connection logic
    def login():
        username = username_entry.get()
        password = password_entry.get()
        account = server_connection_logic.Connection(username, password)
        check = account.login()
        #verify response and inform user in case he cant login
        if check == 'success':
            entry.destroy()
            main_window(username, account)
        elif check == 'Bad username or password':
            messagebox.showerror('Error', check)
        else:
            messagebox.showerror('Unexpected error', check)
            
    #inscription about user required data
    label = tk.Label(entry, text="Enter your username",
                     bg='black', fg="red",font=dark_forest_font)
    label.pack(pady=10)
    #username text area
    username_entry = tk.Entry(entry,bg='black', fg="red",
                              font=dark_forest_font)
    username_entry.pack()
    
    #inscription about user required data
    label = tk.Label(entry, text="Enter your password",
                     bg='black', fg="red",font=dark_forest_font)
    label.pack(pady=10)
    #password text area
    password_entry = tk.Entry(entry, show="*",bg='black', 
                              fg="red",font=dark_forest_font)
    password_entry.pack()
    #login button
    login_button = tk.Button(entry, text="Login", command=login,
                             bg="black", fg="red",font=dark_forest_font)
    login_button.pack(pady=10)
    #register button
    register_button = tk.Button(entry, text="Register", command=register,
                                bg="black", fg="red",font=dark_forest_font)
    register_button.pack()
    #start entry loop
    entry.mainloop()

#launch the game
def play(username, password):
    stop_background_music()
    subprocess.run(['python', 'game/gra.py', username, password], creationflags=subprocess.CREATE_NO_WINDOW)

if __name__ == '__main__':
    start()