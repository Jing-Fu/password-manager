import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_list = password_letters + password_symbols + password_numbers

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }}

    if not website or not password:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("save.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open("save.json", "w") as f:
                data = dict()
                json.dump(new_data, f, indent=4)
        else:
            data.update(new_data)
            with open("save.json", "w") as f:
                json.dump(data, f, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


def find_password():
    website = website_entry.get()
    try:
        with open("save.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No Data File Found")
    else:
        website_data = data.get(website)
        if website_data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Oops", message=f"email:{email}\n password:{password}")
        else:
            messagebox.showinfo(title="Oops", message="No details for the website exists")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)

logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

website_label = Label()
website_label.config(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label()
email_label.config(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label()
password_label.config(text="Password:")
password_label.grid(row=3, column=0)

website_entry = Entry()
website_entry.config(width=21)
website_entry.grid(row=1, column=1, columnspan=2, sticky="W")

email_entry = Entry()
email_entry.config(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="W")
email_entry.insert(0, "test@gmail.com")

password_entry = Entry()
password_entry.config(width=21)
password_entry.grid(row=3, column=1, sticky="W")

search_button = Button(command=find_password, width=13)
search_button.config(text="Search")
search_button.grid(row=1, column=2)

generate_password_button = Button(command=generate_password)
generate_password_button.config(text="Generate Password")
generate_password_button.grid(row=3, column=2, sticky="W")

add = Button(command=save_password)
add.config(text="Add", width=36)
add.grid(row=4, column=1, columnspan=2)

window.mainloop()
