# ---------------------------------------------- EL PYTHONCITO XD 🔒🐍🐍🐍🐍!!!!!
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
import sys, os

FONT_NAME = "Courier"


# *************************************************************************** FUNCTIONS
def resource_path(relative_path):
    """Devuelve la ruta absoluta, incluso cuando se empaqueta en un .exe"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def create_password():
    """This function create a random password 🔒."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '+']

    nr_letters = randint(8, 10)
    nr_symbols = randint(2, 4)
    nr_numbers = randint(2, 4)

    password_list = [choice(letters) for letter in range(nr_letters)]
    password_list += [choice(symbols) for symbol in range(nr_symbols)]
    password_list += [choice(numbers) for number in range(nr_numbers)]

    shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)
    copied_label = Label(window, text="Copied to clipboard ✅", fg="green", font=(FONT_NAME, 10))
    copied_label.config(pady=5)
    copied_label.grid(column=0, row=6, columnspan=3)
    window.after(1500, copied_label.destroy)


def save_password():
    """This function save the password in data.txt"""
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Sorry!!!", message="Please don't forget any field.")
    else:
        try:
            with open(DATA_PATH, "r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open(DATA_PATH, "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Update old data with new data
            data.update(new_data)

            with open(DATA_PATH, "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

    website_entry.focus()


# ⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️
def find_password():
    """This function searches the web page in data.json"""
    website = website_entry.get()

    try:
        with open(DATA_PATH, mode="r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Warning!!!", message="You have not registered any data yet.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            show_popup(website, email, password)
        else:
            messagebox.showinfo(title="Warning!!!", message="No details for the website.")
    website_entry.focus()


def combobox_click(event=None):
    """This function updates the combobox."""
    websites = []
    try:
        with open(DATA_PATH, "r") as file:
            data = json.load(file)
            for web in data:
                websites.append(web)
    except FileNotFoundError:
        pass
    combo["values"] = websites  # Update values


def show_selection(event):
    """This function displays the combobox selection in the website entry."""
    user_choose = combo.get()
    website_entry.delete(0, END)
    website_entry.insert(0, user_choose)
    combo.set("")


def show_popup(title, email, password):
    """This function displays a window where you can copy the email and password."""
    popup = Toplevel(window)
    popup.title(title)
    popup.config(padx=20, pady=20, bg="white")
    popup.resizable(False, False)
    popup.grab_set()

    # ------------- Title Label
    title_label = Label(
        popup,
        text=f"{title}",
        font=(FONT_NAME, 14, "bold"),
        fg="lime",
        bg="white"
    )
    title_label.pack(pady=(0, 10))

    # ------------- Textbox
    text_box = Text(
        popup,
        wrap="word",
        width=45,
        height=6,
        font=(FONT_NAME, 11),
        bg="white",
        fg="black",
        insertbackground="black"
    )

    text_box.insert(END, f"Email: {email}\nPassword: {password}")
    text_box.config(state="disabled")
    text_box.pack(padx=5, pady=5)

    btn_frame = Frame(popup, bg="white")
    btn_frame.pack(pady=10)

    # ----------------- Button to copy email
    copy_email_btn = ttk.Button(
        btn_frame,
        text="Copy Email 📝",
        command=lambda: (pyperclip.copy(email), copied_feedback(popup, "Email copied ✅"))
    )
    copy_email_btn.pack(side=LEFT, padx=5)

    # --------------- Button to copy the password
    copy_pass_btn = ttk.Button(
        btn_frame,
        text="Copy Password 🔑",
        command=lambda: (pyperclip.copy(password), copied_feedback(popup, "Password copied ✅"))
    )
    copy_pass_btn.pack(side=LEFT, padx=5)

    # -------------- Button to close
    close_btn = ttk.Button(btn_frame, text="Close ❌", command=popup.destroy)
    close_btn.pack(side=LEFT, padx=5)

    # ------------- Center the window on the screen
    popup.update_idletasks()
    width = popup.winfo_width()
    height = popup.winfo_height()
    x = (popup.winfo_screenwidth() // 2) - (width // 2)
    y = (popup.winfo_screenheight() // 2) - (height // 2)
    popup.geometry(f"+{x}+{y}")

    website_entry.delete(0, END)


def copied_feedback(parent, message):
    """Displays a temporary message when copying something."""
    feedback = Label(parent, text=message, fg="green", bg="white", font=(FONT_NAME, 10))
    feedback.pack()
    parent.after(1200, feedback.destroy)


def delete_website():
    """This function deletes a website that you no longer need."""
    website = website_entry.get().strip()
    if len(website) == 0:
        messagebox.showinfo(title="Warning!!!", message="Please enter a website to delete.")
        return

    try:
        with open(DATA_PATH, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Warning!!!", message="No data file found.")
        return

    if website in data:
        confirm = messagebox.askyesno(title="Confirm Delete", message=f"Do you really want to delete '{website}'")
        if confirm:
            del data[website]
            with open(DATA_PATH, "w") as file:
                json.dump(data, file, indent=4)
            website_entry.delete(0, END)
            combo.set("")
            combobox_click()
            messagebox.showinfo(title="Deleted!!!", message=f"{website} has been deleted successfully.")
        else:
            messagebox.showinfo(title="Warning!!!", message=f"No entry found for {website}")


# ---------------
LOGO_PATH = resource_path("logo.png")
DATA_PATH = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "data.json")

# ******************************************************************* GUI
window = Tk()
window.title("Password manager 2.0")
window.config(padx=40, pady=40)
window.geometry("+500+150")

# ----------------- Canvas
canvas = Canvas(width=256, height=256)
logo_img = PhotoImage(file=LOGO_PATH)
canvas.create_image(135, 130, image=logo_img)
canvas.grid(column=0, row=1, sticky="n", columnspan=3)

# ----------------- Labels
website_label = Label(text="Website:")
website_label.config(font=(FONT_NAME, 12))
website_label.grid(column=0, row=2, sticky="e")

email_username_label = Label(text="Email/Username:")
email_username_label.config(font=(FONT_NAME, 12))
email_username_label.grid(column=0, row=3, sticky="e")

password_label = Label(text="Password:")
password_label.config(font=(FONT_NAME, 12))
password_label.grid(column=0, row=4, sticky="e")

name = Label(text="EL PYTHONCITO XD 🐍!!!!")
name.config(font=(FONT_NAME, 15, "bold"), fg="lime")
name.grid(column=0, row=0, sticky="n", columnspan=3)

# ------------------ Entries
website_entry = Entry()
website_entry.config(width=12, font=(FONT_NAME, 12))
website_entry.grid(column=1, row=2, sticky="w", columnspan=2)
website_entry.focus()

email_username_entry = Entry()
email_username_entry.config(width=20, font=(FONT_NAME, 12))
email_username_entry.grid(column=1, row=3, sticky="w", columnspan=2)
email_username_entry.insert(0, "example@gmail.com")

password_entry = Entry()
password_entry.config(width=20, font=(FONT_NAME, 12))
password_entry.grid(column=1, row=4, sticky="w")

# ------------------- Buttons
g_password_button = ttk.Button(text="Generate Password", command=create_password)
g_password_button.config(width=18)
g_password_button.grid(column=2, row=4, sticky="e")

add_button = ttk.Button(text="Add", command=save_password)
add_button.config(width=53)
add_button.grid(column=1, row=5, columnspan=2, sticky="w")

search_button = ttk.Button(text="Search", command=find_password)
search_button.config(width=18)
search_button.grid(column=2, row=2, sticky="e")

delete_button = ttk.Button(text="Delete", command=delete_website, width=18)
delete_button.grid(column=2, row=3, sticky="e")

combo = ttk.Combobox(values=[], state="readonly", width=8)
combo.grid(column=1, row=2, sticky="e")

combo.bind("<Button-1>", combobox_click)
combo.bind("<<ComboboxSelected>>", show_selection)

# ---------------------------
window.mainloop()
