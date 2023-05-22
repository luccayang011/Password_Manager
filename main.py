from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pw():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers

    shuffle(password_list)

    password = "".join(password_list)
    pw_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = web_entry.get()
    username = username_entry.get()
    pw = pw_entry.get()
    new_data = {
        website: {
            "username": username,
            "password": pw,
        }
    }
    if len(website) == 0 or len(username) == 0 or len(pw) == 0:
        messagebox.showinfo(title='Oops...', message="Please make sure you don't leave any field empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f'These are the details entered: \nUsername:{username}'
                                                              f'\nPassword: {pw} \nIs this okay to save?')

        if is_ok:
            try:
                with open('data.json', 'r') as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:  # json read mode can't deal with nonexistent file
                with open('data.json', 'w') as data:
                    # using the new data to update the old data
                    json.dump(new_data, data, indent=4)
            else:
                data.update(new_data)
                with open('data.json', 'w') as data:
                    json.dump(new_data, data, indent=4)  # number of spaces to indent all the json data
                    messagebox.showinfo(title='Success', message='Password Saved!')
            finally:  # run it anyway
                web_entry.delete(0, END)
                pw_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = web_entry.get()
    try:
        with open('data.json', 'r') as data:
            d = json.load(data)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No Data File Found')
    else:
        if website in d:
            username = d[website]["username"]
            password = d[website]["password"]
            messagebox.showinfo(title=website, message=f"username: {username}\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showinfo(title='Error', message='No Details for the website exists')


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# create canvas widget
canvas = Canvas(width=200, height=200)
pw_image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=pw_image)  # create an image inside the canvas
canvas.grid(row=0, column=1)

# create labels
website = Label(text='Website:')
website.grid(row=1, column=0)

username = Label(text='Email/Username:')
username.grid(row=2, column=0)

password = Label(text='Password:')
password.grid(row=3, column=0)

# create buttons
generate_password = Button(text='Generate Password', command=generate_pw)
generate_password.grid(row=3, column=2)

add = Button(text='Add', width=44, command=save_password)
add.grid(row=4, column=1, columnspan=2)

search = Button(text='Search', width=15, command=find_password)
search.grid(row=1, column=2)

# create entries
web_entry = Entry(width=33)
web_entry.grid(row=1, column=1)
web_entry.focus()  # default the curser to the website entry

username_entry = Entry(width=52)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0, 'Your Email Address')  # pre populate the email

pw_entry = Entry(width=33)
pw_entry.grid(row=3, column=1)

window.mainloop()
