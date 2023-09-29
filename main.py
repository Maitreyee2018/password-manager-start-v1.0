from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# Write -> json.dump()  #Read ->  json.load() #Update -> json.update()

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_gen():
    password_entry.delete(0, END)
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

    print(f"Your password is: {password}")
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_to_file():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    # contents = website + " | " + email + " | " + password + "\n"
    new_data = {website: {email: password}}

    if website == "" or password == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Read old data in the file
                data = json.load(data_file)
        except FileNotFoundError:
            # if file not found then create a file and dump new data
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # if file is found, update new data into old data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    email = email_entry.get()

    if website == "":
        messagebox.showinfo(title="Oops", message="Please enter a website to search")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.")
        else:
            try:
                searched_password = data[website][email]
            except KeyError:
                messagebox.showinfo(title="Error", message="No details for the website exists.")
            else:
                messagebox.showinfo(title=website,
                                    message=f"Email: {email}\n Password:{searched_password}")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)
website_entry = Entry(width=32)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=52)
email_entry.insert(0, "mailtome.dearfriends@gmail.com")
email_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=32)
password_entry.grid(column=1, row=3)

gen_pass_button = Button(text="Generate Password", command=password_gen)
gen_pass_button.grid(column=2, row=3)
add_button = Button(text="Add", width=45, command=add_to_file)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
