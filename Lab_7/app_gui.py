from tkinter import *
import json
from functools import partial
from read_db import is_correct_log_in
from read_db import read_data

root = Tk()
root.title('Laboratory 7 - Constantin Cazacu')
root.geometry('1200x660')

is_logged_in = False

USERNAME = StringVar()
PASSWORD = StringVar()


# Create New File Function
def new_file():
    # Delete previous text
    my_text.delete('1.0', END)

    # Update status bars
    root.title('New File - Constantin Cazacu')
    status_bar.config(text='New File       ')


def exit_db():
    global USERNAME
    global PASSWORD
    global is_logged_in

    USERNAME = ''
    PASSWORD = ''
    is_logged_in = False

    my_text.delete('1.0', END)


def connect():
    global USERNAME
    global PASSWORD
    global is_logged_in

    def validate_login(username, password):
        global USERNAME
        global PASSWORD
        global is_logged_in

        USERNAME = username.get()
        PASSWORD = password.get()

        is_logged_in = is_correct_log_in(USERNAME, PASSWORD)

        connect_window.destroy()
        return

    def logout():
        global USERNAME
        global PASSWORD
        global is_logged_in

        USERNAME = ''
        PASSWORD = ''

        is_logged_in = False

        my_text.delete('1.0', END)

        connect_window.destroy()
        return

    def okay():
        connect_window.destroy()

        return

    if is_logged_in == False:

        connect_window = Tk()
        connect_window.title('Signing in to database...')

        username_label = Label(connect_window, text='Username:').grid(row=0, column=0)
        username = StringVar(connect_window)
        username_entry = Entry(connect_window, textvariable=username, width=50).grid(row=0, column=1)

        password_label = Label(connect_window, text='Password:').grid(row=1, column=0)
        password = StringVar(connect_window)
        password_entry = Entry(connect_window, textvariable=password, width=50, show='*').grid(row=1, column=1)

        validate_login = partial(validate_login, username, password)

        submit = Button(connect_window, text='Submit', command=validate_login).grid(row=4, column=0)

        connect_window.mainloop()

    else:
        connect_window = Tk()
        connect_window.title('Signing in to database...')
        no_label = Label(connect_window, text='You are logged in!').grid(row=0, column=0)
        okay = partial(okay)
        ok = Button(connect_window, text='Ok', command=okay).grid(row=1, column=0)
        logout = partial(logout)
        log_out = Button(connect_window, text='Log out', command=logout).grid(row=1, column=1)
        connect_window.mainloop()


def view_data():
    global USERNAME
    global PASSWORD
    global is_logged_in

    if is_logged_in:
        nr_agents, list_of_agents = read_data(USERNAME, PASSWORD)
        my_text.delete('1.0', END)
        for agent in list_of_agents:
            my_text.insert(END, json.dumps(agent, indent=4))

    else:
        connect()


# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create out Scrollbar For the Text Box
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Create Text Box
my_text = Text(my_frame, width=97, height=25,
               font=('Helvetica', 16), selectbackground='yellow',
               selectforeground='black', undo=True,
               yscrollcommand=text_scroll.set)
my_text.pack()

# Configure out Scrollbar
text_scroll.config(command=my_text.yview)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Add File Menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Connect to Database', command=connect)
file_menu.add_command(label='View data', command=view_data)
file_menu.add_command(label='Log out', command=exit_db)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

# Add Status Bar to Bottom
status_bar = Label(root, text='Ready     ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=5)
root.mainloop()
