import os
import tkinter as tk
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import pymysql

# ---------------------------- INITIALIZE DATABASE ------------------------------- #
# Connection to databse
sql_server_address = os.environ.get("SERVER_IP")
sql_server_user = os.environ.get("SERVER_USER")
sql_server_pass = os.environ.get("SERVER_PASS")


connection = pymysql.connect(host=sql_server_address,
                             user=sql_server_user,
                             password=sql_server_pass,
                             database="YOUR DATABASE NAME",
                             cursorclass=pymysql.cursors.DictCursor)

##USE ONCE at first run ONLY!
# with connection:
#     with connection.cursor() as concur:
#         #Create a new database
#         sql_statement1 = "CREATE DATABASE db_pass"
#         concur.execute(sql_statement1)

# with connection:
#     with connection.cursor() as concur:
#         #Create a new Table
#         sql_statement2 = """CREATE TABLE Passwords(id int NOT NULL AUTO_INCREMENT,
#                                                     website varchar(255) NOT NULL,
#                                                      email varchar(255) NOT NULL,
#                                                       password varchar(255) NOT NULL,
#                                                       PRIMARY KEY (id))"""
#         concur.execute(sql_statement2)


# ---------------------------- SEARCH WEBSITE ------------------------------- #
def search_website():
    with connection:
        with connection.cursor() as concur:
            sql_fetch = """SELECT website,email,password FROM Passwords WHERE website = 'myweb'"""
            concur.execute(sql_fetch)
            dats = concur.fetchone()
        if not dats:
            messagebox.showinfo(title="Error", message="Website not found in databse.")
        else:
            messagebox.showinfo(title=dats["website"], message=f"Email: {dats['email']}\nPassword: {dats['password']}")
            password_entry.insert(0, dats["password"])
            email_entry.delete(0,"end")
            email_entry.insert(0, dats["email"])

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    password_entry.delete(0, 'end')

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letter = [choice(letters) for _ in range(randint(8, 10))]

    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letter + password_numbers + password_symbols

    shuffle(password_list)

    password_rand = "".join(password_list)

    password_entry.insert(0, password_rand)

    pyperclip.copy(password_rand)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    # json_data = {
    #     website: {
    #         "email": email,
    #         "password": password,
    #     }
    # }

    if len(website) != 0 and len(password) != 0:
        go_ahead = messagebox.askokcancel(title=website,
                                          message=f"Email : {email} \nPassword : {password}\nIs it ok to save?")
        if go_ahead:
            with connection:
                with connection.cursor() as concur:
                    #Provide SQL Statement
                    sql_insert = f"""INSERT INTO Passwords(website,email,password)
                                    VALUES({website},{email},{password})"""
                    #Execute SQL Statement
                    concur.execute(sql_insert)
                    # Commit to save changes made in table
                    connection.commit()
    else:
        messagebox.showinfo(title="Error", message="Don't leave any field empty.")


# ---------------------------- UI SETUP ------------------------------- #
# Window

window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# PhotoImage
logo = tk.PhotoImage(file="logo.png")

# Canvas
canvas = tk.Canvas(width=200, height=200, highlightthickness=0)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Label
website_label = tk.Label(text="Website")
email_label = tk.Label(text="Email/Username")
password_label = tk.Label(text="Password")
website_label.grid(column=0, row=1)
email_label.grid(column=0, row=2)
password_label.grid(column=0, row=3)

# Entries
website_entry = tk.Entry(width=33)
website_entry.focus()
email_entry = tk.Entry(width=50)
email_entry.insert(0, "@gmail.com")
password_entry = tk.Entry(width=18)
website_entry.grid(column=1, row=1)
email_entry.grid(column=1, row=2, columnspan=2)
password_entry.grid(column=1, row=3, sticky="nsew")

# Buttons
search_button = tk.Button(text="Search", width=13, command=search_website)
generate_button = tk.Button(text="Generate Password", width=13, command=gen_pass)
add_button = tk.Button(text="Add", width=40, command=add)
search_button.grid(column=2, row=1)
generate_button.grid(column=2, row=3, sticky="nsew")
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
