from tkinter import *
from random import randint, choice, shuffle
from tkinter import messagebox
import json


from docutils.nodes import title


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbol
    shuffle(password_list)

    password = "".join(password_list)

    password_input.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_creds():
    website = website_input.get()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email" : email,
            "password" : password
        }
    }

# checks if the email is a valid one

    def is_password_valid():
        if email.count("@") == 1 and len(email) >= 5 and email.endswith(".com"):
            return True
        else:
            return False

#This checks if there is any empty field
    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")

# this get triggered only when there is no empty field
    else:
        if is_password_valid():
                is_ok = messagebox.askokcancel(title=website, message=f"These are the details you entered: \nEmail: {email}" f"\nPassword: {password}")
                if is_ok:
                    try:
                        with open("data.json","r") as data_file:
                           # Reading old data
                           data = json.load(data_file)

                    except FileNotFoundError as e:
                        with open("data.json", "w") as data_file:
                            json.dump(new_data, data_file, indent=4)

                    except json.JSONDecodeError:
                        # If the file exists but contains invalid JSON, overwrite it with new data
                        with open("data.json", "w") as data_file:
                            json.dump(new_data, data_file, indent=4)

                    else:
                        # Updating old data with new Data
                        data.update(new_data)

                        # Saving updated data
                        with open("data.json", "w") as data_file:
                            json.dump(data, data_file, indent=4)

                    finally:
                        clear()
        else:
            messagebox.askokcancel(title="Opps", message=f"Email is invalid")

def clear():
    website_input.delete(0, END)
    email_input.delete(0, END)
    password_input.delete(0, END)
    email_input.insert(0, "isrealurephu@gmail.com")
#----------------------------------SEARCH FUNCTION------------------------#

def search():
    website = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except json.decoder.JSONDecodeError:
        messagebox.showinfo(title="Opps", message=f"Website {website} not found. List is empty")
        clear()

    except FileNotFoundError:
        messagebox.showinfo(title="Opps", message=f"file not found")
        clear()

    else:
        if website in data:
            email = data[website]["email"]
            passcode = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {passcode}")
            clear()
        else:
            messagebox.showinfo(title="Opps", message=f"Website {website} not found")
            clear()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("My Password Manager")
window.config(padx=50, pady=50)


canvas = Canvas(width=200, height=200)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image )
canvas.grid(row=0, column=1)

# website details
web_site_label = Label(text="Website:")
web_site_label.grid(row=1, column=0)

website_input =  Entry(width=17)
website_input.grid(row=1, column=1)
website_input.focus()

website_search_button = Button(text="search", command=search, width=12)
website_search_button.grid(row=1, column=2)


# email and username details
email_username_label = Label(text="Email/Username:")
email_username_label.grid(row=2, column=0)

email_input =  Entry(width=35)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "isrealurephu@gmail.com")


# password details
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

password_input =  Entry(width=16)
password_input.grid(row=3, column=1)

password_generator_button = Button(text="Generate Password", command=generate_password)
password_generator_button.grid(row=3, column=2)

# add button
add_button = Button(text="Add", width=33, command=save_creds)
add_button.grid(row=4, column=1, columnspan=2)





window.mainloop()