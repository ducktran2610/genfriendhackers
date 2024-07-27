import tkinter as tk
from tkinter import messagebox
import sqlite3

def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    finally:
        conn.close()

def login_user():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful")
    else:
        messagebox.showerror("Error", "Invalid username or password")
    
    conn.close()

app = tk.Tk()
app.title("Login and Register")

frame = tk.Frame(app)
frame.pack(pady=20, padx=20)

label_username = tk.Label(frame, text="Username")
label_username.grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(frame)
entry_username.grid(row=0, column=1, padx=10, pady=10)

label_password = tk.Label(frame, text="Password")
label_password.grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(frame, show='*')
entry_password.grid(row=1, column=1, padx=10, pady=10)

button_register = tk.Button(frame, text="Register", command=register_user)
button_register.grid(row=2, column=0, padx=10, pady=10)

button_login = tk.Button(frame, text="Login", command=login_user)
button_login.grid(row=2, column=1, padx=10, pady=10)

app.mainloop()
