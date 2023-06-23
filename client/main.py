import tkinter as tk
from tkinter import messagebox
import client.connection.server_connection_logic as connection
import subprocess
from tkinter import ttk, font
import pygame
from typing import Any
import platform

width = 1920
height = 1080
bright = 0

# playin background music
def play_background_music() -> None:
    pygame.mixer.music.load("client/client_sounds/darkforest_client.mp3")
    pygame.mixer.music.play(-1)


# stop music
def stop_background_music() -> None:
    pygame.mixer.music.stop()


# initialize mixer
pygame.mixer.init()


# main window for client
def main_window(username: str, account: Any) -> None:
    global width  # noqa: PLW0602
    global height  # noqa: PLW0602
    window = tk.Tk()
    # inscription at the top of the window
    window.title(f"Dark_forest_client - {username} Logged In")
    # static window size
    window.geometry("900x600")
    window.resizable(False, False)  # noqa: FBT003
    # font, if you have error here pleas install font from game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    # client image
    background_image = tk.PhotoImage(
        file="client/client_textures/background_client.png"
    )
    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # global scores button with some style, forwarding to best scores
    best_scores_button = tk.Button(
        background_label,
        text="Global Best Scores",
        command=lambda: show_best_scores_window(account, window),
        bg="black",
        fg="red",
        width=14,
        height=2,
        font=dark_forest_font,
    )
    best_scores_button.pack()

    # global stats button with some style, forwarding to stats
    stats_button = tk.Button(
        background_label,
        text="Global Stats",
        command=lambda: show_stats_window(account, window),
        bg="black",
        fg="red",
        width=14,
        height=2,
        font=dark_forest_font,
    )
    stats_button.pack(pady=16)

    settings_button = tk.Button(
        background_label,
        text="Settings",
        command=lambda: settings(window),
        bg="black",
        fg="red",
        width=14,
        height=2,
        font=dark_forest_font,
    )
    settings_button.pack(pady=10)

    # game starting button with some style, launching the game
    play_button = tk.Button(
        background_label,
        text="Play Dark Forest",
        command=lambda: play(username, account.password, width, height),
        bg="black",
        fg="red",
        width=14,
        height=2,
        font=dark_forest_font,
    )
    play_button.pack(pady=70)

    # main loop from main window
    window.mainloop()


# show global stast
def show_stats_window(account: Any, window: Any) -> None:
    # ussing server connection logic method to connect to server
    stats_data = account.show_stats()
    # font, if you have error here pleas install font from client/game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    # create new view in main window
    stats_pane = ttk.PanedWindow(window, orient=tk.VERTICAL)
    stats_pane.pack(fill="both", expand=True)
    # load background image into paned window
    background_image = tk.PhotoImage(file="client/client_textures/menu.png")
    background_label = tk.Label(stats_pane, image=background_image)
    background_label.image = background_image  # type: ignore
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # inscription at the top of window
    stats_label = tk.Label(
        stats_pane, text="Global Stats", bg="black", fg="red", font=dark_forest_font
    )
    stats_label.grid(row=0, column=0, padx=10, pady=10)
    # scrolled area for players stats
    scrollbar = tk.Scrollbar(stats_pane)
    scrollbar.grid(row=1, column=1, sticky=tk.NS)
    stats_text = tk.Text(
        stats_pane,
        wrap=tk.WORD,
        font=dark_forest_font,
        bg="black",
        fg="red",
        yscrollcommand=scrollbar.set,
    )
    stats_text.insert(tk.END, stats_data)
    stats_text.grid(row=1, column=0, padx=10, pady=(0, 10))
    scrollbar.config(command=stats_text.yview)
    # back to the main view in main window
    back_button = tk.Button(
        stats_pane,
        text="Back",
        command=stats_pane.destroy,
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    back_button.grid(row=2, column=0, pady=10)
    # size
    stats_pane.grid_rowconfigure(1, weight=1)
    stats_pane.grid_columnconfigure(0, weight=1)


def show_best_scores_window(account: Any, window: Any) -> None:
    # ussing server connection logic method to connect to server
    best_scores_data = account.show_best_score()
    # font, if you have error here pleas install font from client/game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    # create new view in main window
    scores_pane = ttk.PanedWindow(window, orient=tk.VERTICAL)
    scores_pane.pack(fill="both", expand=True)
    # load background image into paned window
    background_image = tk.PhotoImage(file="client/client_textures/menu.png")
    background_label = tk.Label(scores_pane, image=background_image)
    background_label.image = background_image  # type: ignore
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # inscription at the top of window
    scores_label = tk.Label(
        scores_pane,
        text="Global Best Scores",
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    scores_label.grid(row=0, column=0, padx=10, pady=10)
    # scrolled area for bestscores
    scrollbar = tk.Scrollbar(scores_pane)
    scrollbar.grid(row=1, column=1, sticky=tk.NS)
    scores_text = tk.Text(
        scores_pane,
        wrap=tk.WORD,
        font=dark_forest_font,
        bg="black",
        fg="red",
        yscrollcommand=scrollbar.set,
    )
    scores_text.insert(tk.END, best_scores_data)
    scores_text.grid(row=1, column=0, padx=10, pady=(0, 10))
    scrollbar.config(command=scores_text.yview)
    # back to the main view in main window
    back_button = tk.Button(
        scores_pane,
        text="Back",
        command=scores_pane.destroy,
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    back_button.grid(row=2, column=0, pady=10)
    # size
    scores_pane.grid_rowconfigure(1, weight=1)
    scores_pane.grid_columnconfigure(0, weight=1)


def settings(window: Any) -> None:  # noqa: PLR0915
    global width_game  # noqa: PLW0603
    global height_game  # noqa: PLW0603
    # font, if you have error here pleas install font from client/game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    # create new view in main window
    settings_pane = ttk.PanedWindow(window, orient=tk.VERTICAL)
    settings_pane.pack(fill="both", expand=True)
    # load background image into paned window
    background_image = tk.PhotoImage(file="client/client_textures/menu.png")
    background_label = tk.Label(settings_pane, image=background_image)
    background_label.image = background_image  # type: ignore
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    # inscription about resolution
    settings_label = tk.Label(
        settings_pane,
        text="Enter your screen resolution",
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    settings_label.pack(pady=5)
    screen_label = tk.Label(
        settings_pane,
        text="Default is 1920x1080",
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    screen_label.pack(pady=5)
    # place to enter your width
    width_label = tk.Label(
        settings_pane, text="width", bg="black", fg="red", font=dark_forest_font
    )
    width_label.pack(pady=5)
    width_game = tk.Entry(settings_pane, bg="black", fg="red", font=dark_forest_font)
    width_game.pack(pady=5)
    # place to enter your height
    height_label = tk.Label(
        settings_pane, text="height", bg="black", fg="red", font=dark_forest_font
    )
    height_label.pack(pady=5)
    height_game = tk.Entry(settings_pane, bg="black", fg="red", font=dark_forest_font)
    height_game.pack(pady=5)
    # button to confirm your resolution
    confirm_resolution_button = tk.Button(
        settings_pane,
        text="Confirm new resolution",
        command=lambda: change_resolution(),
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    confirm_resolution_button.pack(pady=5)
    # inscription about brightness
    brightness_label = tk.Label(
        settings_pane,
        text="Enter brightness level what you prefer",
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    brightness_label.pack(pady=5)
    brightness_label = tk.Label(
        settings_pane, text="Default is 0", bg="black", fg="red", font=dark_forest_font
    )
    brightness_label.pack(pady=5)
    # place to enter your height
    brightness = tk.Entry(settings_pane, bg="black", fg="red", font=dark_forest_font)
    brightness.pack(pady=5)
    # button to confirm your brighntess
    confirm_brightness_button = tk.Button(
        settings_pane,
        text="Confirm new brightness",
        command=lambda: change_brightness(),
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    confirm_brightness_button.pack(pady=5)
    # back to the main view in main window
    back_button = tk.Button(
        settings_pane,
        text="Back",
        command=settings_pane.destroy,
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    back_button.pack(pady=5)
    # size
    settings_pane.grid_rowconfigure(1, weight=1)
    settings_pane.grid_columnconfigure(0, weight=1)

    def change_resolution() -> tuple[str, str] | str:
        global width  # noqa: PLW0603
        global height  # noqa: PLW0603
        new_width = width_game.get()
        new_height = height_game.get()
        try:
            if int(new_width) >= 800 and int(new_height) >= 600:
                width = new_width
                height = new_height
                return width, height
            return messagebox.showerror("Error", "Minimal resolution is 800x600")

        except ValueError:
            return messagebox.showerror("Error", "Enter correct resolution")

    def change_brightness() -> str:
        global bright  # noqa: PLW0603
        new_bright = brightness.get()
        try:
            if int(new_bright) <= 50 and int(new_bright) >= 0:
                bright = new_bright
                return bright
            return messagebox.showerror("Error", "Ener a value beetween 0 and 50")

        except ValueError:
            return messagebox.showerror("Error", "Enter correct values")


def start() -> None:  # noqa: PLR0915
    # login/register window, closing after login/register, static window size
    entry = tk.Tk()
    entry.title("Dark_forest_client")
    entry.geometry("400x400")
    entry.resizable(False, False)  # noqa: FBT003
    # background music
    play_background_music()
    # font, if you have error here pleas install font from game/font/Snap.ttf
    dark_forest_font = font.Font(family="Snap ITC", size=18)
    # load background image into window
    background_image = tk.PhotoImage(file="client/client_textures/menu.png")
    background_label = tk.Label(entry, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # register function using method from server connection logic
    def register() -> None:
        username = username_entry.get()
        password = password_entry.get()
        account = connection.Connection(username, password)
        check = account.register()
        # verify response and inform user in case he cant register
        if check == "success":
            entry.destroy()
            main_window(username, account)
        elif check == "User exists":  # noqa: SIM114
            messagebox.showerror("Error", check)
        elif check == "Enter username and password in text area":
            messagebox.showerror("Error", check)
        else:
            messagebox.showerror("Unexpected error", check)

    # login function using method from server connection logic
    def login() -> None:
        username = username_entry.get()
        password = password_entry.get()
        account = connection.Connection(username, password)
        check = account.login()
        # verify response and inform user in case he cant login
        if check == "success":
            entry.destroy()
            main_window(username, account)
        elif check == "Bad username or password":  # noqa: SIM114
            messagebox.showerror("Error", check)
        elif check == "Enter username and password in text area":
            messagebox.showerror("Error", check)
        else:
            messagebox.showerror("Unexpected error", check)

    # inscription about user required data
    label = tk.Label(
        entry, text="Enter your username", bg="black", fg="red", font=dark_forest_font
    )
    label.pack(pady=10)
    # username text area
    username_entry = tk.Entry(entry, bg="black", fg="red", font=dark_forest_font)
    username_entry.pack()

    # inscription about user required data
    label = tk.Label(
        entry, text="Enter your password", bg="black", fg="red", font=dark_forest_font
    )
    label.pack(pady=10)
    # password text area
    password_entry = tk.Entry(
        entry, show="*", bg="black", fg="red", font=dark_forest_font
    )
    password_entry.pack()
    # login button
    login_button = tk.Button(
        entry, text="Login", command=login, bg="black", fg="red", font=dark_forest_font
    )
    login_button.pack(pady=10)
    # register button
    register_button = tk.Button(
        entry,
        text="Register",
        command=register,
        bg="black",
        fg="red",
        font=dark_forest_font,
    )
    register_button.pack()
    # start entry loop
    entry.mainloop()


# launch the game
def play(username: str, password: str, width_game: int, height_game: int) -> None:
    if platform.system() == "Windows":
        noconsole = subprocess.CREATE_NO_WINDOW
    if platform.system() == "Linux":
        noconsole = 0

    stop_background_music()

    creationflags = noconsole if platform.system() == "Windows" else 0

    subprocess.run(
        [  # noqa: S603, S607
            "python",
            "-m",
            "client.game.game",
            username,
            password,
            str(width_game),
            str(height_game),
            str(bright),
        ],
        creationflags=creationflags,
    )


if __name__ == "__main__":
    start()
