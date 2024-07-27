from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, messagebox
import sqlite3
import main
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\python\bot\BOT_12H_update\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Connect to SQLite database
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute('''
    SELECT * FROM users WHERE username = ? AND password = ?
    ''', (username, password))

    user = cursor.fetchone()

    if user:
        window.destroy()
        main.main(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

    conn.close()

window = Tk()
window.geometry("800x450")
window.title("Đăng nhập")
window.configure(bg="#FFFFFF")

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=450,
    width=800,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)
canvas.create_rectangle(
    44.0,
    27.0,
    764.0,
    432.0,
    fill="#FFFFFF",
    outline=""
)

username_entry_image = PhotoImage(
    file=relative_to_assets("username_entry.png"))
username_entry_bg = canvas.create_image(
    389.0,
    144.5,
    image=username_entry_image
)
username_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0
)
username_entry.place(
    x=176.0,
    y=120.0,
    width=426.0,
    height=47.0
)

canvas.create_text(
    179.0,
    94.0,
    anchor="nw",
    text="Tên đăng nhập:",
    fill="#000000",
    font=("Marmelad Regular", 15 * -1)
)

password_entry_image = PhotoImage(
    file=relative_to_assets("password_entry.png"))
password_entry_bg = canvas.create_image(
    389.0,
    233.5,
    image=password_entry_image
)
password_entry = Entry(
    bd=0,
    bg="#D9D9D9",
    fg="#000716",
    highlightthickness=0,
    show="*"
)
password_entry.place(
    x=176.0,
    y=210.0,
    width=426.0,
    height=45.0
)

canvas.create_text(
    179.0,
    183.0,
    anchor="nw",
    text="Mật khẩu:\n\n",
    fill="#000000",
    font=("Marmelad Regular", 15 * -1)
)

login_button_image = PhotoImage(
    file=relative_to_assets("login_button.png"))
login_button = Button(
    image=login_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=login,
    relief="flat"
)
login_button.place(
    x=587.0,
    y=317.0,
    width=50.0,
    height=50.0
)

window.resizable(False, False)
window.mainloop()
