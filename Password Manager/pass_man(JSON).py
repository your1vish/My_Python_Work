import tkinter as tk
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- SEARCH WEBSITE ------------------------------- #
def search_website():
    with open("data.json", "r")as data_file:
        file_load = json.load(data_file)
        web_search = website_entry.get()
        try:
            dats = file_load[web_search]
        except KeyError:
            messagebox.showinfo(title="Error", message="Website not found in databse.")
        else:
            messagebox.showinfo(title=web_search, message=f"Email: {dats['email']}\nPassword: {dats['password']}")
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
    json_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) != 0 and len(password) != 0:
        go_ahead = messagebox.askokcancel(title=website,
                                          message=f"Email : {email} \nPassword : {password}\nIs it ok to save?")
        if go_ahead:
            try:
                with open("data.json", "r") as data:
                    jdat = json.load(data)
                    jdat.update(json_data)
            except json.decoder.JSONDecodeError:
                with open("data.json", "w") as data:
                    json.dump(json_data, data, indent=2)

            else:
                with open("data.json", "w") as data:
                    json.dump(jdat, data, indent=2)
            finally:
                website_entry.delete(0, 'end')
                password_entry.delete(0, 'end')

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
