#pip install mysql-connector-python
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import os
# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    port=3308,
    user='root',
    password='root',
    database='age_gender_emotion',
    charset='utf8'
)
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(255) PRIMARY KEY,
                    password VARCHAR(255) NOT NULL
                )''')
conn.commit()


root = tk.Tk()
root.configure(bg='cyan4')
root.title("Login and Registration")
root.geometry("600x400")

# Function to center the window
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def register():
    register_screen = tk.Toplevel(root)
    register_screen.configure(bg='cyan4')
    register_screen.title("Register")
    register_screen.geometry("300x250")
    center_window(register_screen)

    username_label = tk.Label(register_screen, text="Username")
    username_label.pack()
    username_entry = tk.Entry(register_screen)
    username_entry.pack()

    password_label = tk.Label(register_screen, text="Password")
    password_label.pack()
    password_entry = tk.Entry(register_screen, show="*")
    password_entry.pack()

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Username already exists")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                conn.commit()
                messagebox.showinfo("Success", "Registration successful")
                register_screen.destroy()
        else:
            messagebox.showerror("Error", "All fields are required")

    register_button = tk.Button(register_screen, text="Register", command=register_user)
    register_button.place(relx=0.45,rely=0.45)

register_button = tk.Button(root,  command=register)
register_button.configure(text='Register', bg='cyan3', font=('Areal',15), bd=10)
register_button.place(relx=0.5,rely=0.6)


def login():
    login_screen = tk.Toplevel(root)
    login_screen.configure(bg='cyan4')
    login_screen.title("Login")
    login_screen.geometry("300x250")
    center_window(login_screen)

    username_label = tk.Label(login_screen, text="Username")
    username_label.pack()
    username_entry = tk.Entry(login_screen)
    username_entry.pack()



    password_label = tk.Label(login_screen, text="Password")
    password_label.pack()
    password_entry = tk.Entry(login_screen, show="*")
    password_entry.pack()

    def login_user():
        username = username_entry.get()
        password = password_entry.get()
        if username and password:
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
            if cursor.fetchone():
                messagebox.showinfo("Success", "Login successful")
                login_screen.destroy()
                root.withdraw()  # Hide the login window
                os.system("python gad2.py")
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            messagebox.showerror("Error", "All fields are required")

    login_button = tk.Button(login_screen, text="Login", command=login_user)
    login_button.place(relx=0.45,rely=0.45)

    def open_user_page():
        # Execute another Python file
        os.system("python gad2.py")

login_button = tk.Button(root, text="Login", command=login)
login_button.configure(text='Login', bg='cyan3', font=('Areal',15), bd=10)
login_button.place(relx=0.5,rely=0.3)



center_window(root)
root.mainloop()

# Close the database connection when the application is closed
conn.close()
