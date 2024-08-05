from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ----------------------------FINDING PASSWORD  ------------------------------- #
def find_password():
    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        for key in data:
            if website == key:
                web_info = data[website]
                messagebox.showinfo(title=website, message=f"Email: {web_info['email']} "
                                                           f"\nPassword: {web_info['password']}")
            else:
                messagebox.showinfo(title="Error", message="No details for the website exists.")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for char in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website:
            {
                "email": email,
                "password": password
            }
    }

    if website == "" or password == "" or email == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        is_okay = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}"
                                                                f"\nPassword: {password} \nIs it okay?")
        if is_okay:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                # Updating old data with new data
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    # Saving old data
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200)
img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=img)
canvas.grid(row=0, column=1)

website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

email_entry = Entry(width=35)
email_entry.insert(0, "trisha@gmail.com")
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

generate_pass_button = Button(text="Generate Password", command=generate)
generate_pass_button.grid(row=3, column=2, sticky="EW")

search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
#  the "sticky" parameter, the EW part is the compass directions (E)ast and (W)est and the sticky basically "sticks" the widget to the edges
#  of the column. So this instruction spans the widget to fill the whole width of the grid column/s.
#  This means we don't need to experiment with absolute pixel values for the widgets except for the longest one (add),
#  which determines the size of the last column.
