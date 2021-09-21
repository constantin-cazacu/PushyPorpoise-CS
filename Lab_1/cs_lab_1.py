from tkinter import *
from tkinter import filedialog
from tkinter import font
import json
from os import listdir
from os.path import isfile, join

root = Tk()
root.title('Lab Work No. 1 - Constantin Cazacu')
root.geometry('1200x660')

global selected
selected = False


# new file function
def new_file():
    # clear previous text
    my_text.delete('1.0', END)

    # update status bars
    root.title('New File - Constantin Cazacu')
    status_bar.config(text='New File       ')


# cut text
def cut_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    elif my_text.selection_get():
        # grab selected text from textbox
        selected = my_text.selection_get()
        # delete selected text from textbox
        my_text.delete("sel.first", "sel.last")
        # clear clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# copy text
def copy_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        # grab selected text from textbox
        selected = my_text.selection_get()
        # clear clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# paste text
def paste_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    elif selected:
        position = my_text.index(INSERT)
        my_text.insert(position, selected)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)
        # use start += 1 to find overlapping matches


# open file function
def open_file():
    # clear previous text
    my_text.delete('1.0', END)

    # get file name
    text_file = filedialog.askopenfilename(
        initialdir='Lab_1/Policies',
        title='Open File', filetypes=(('All Files', '*.*'),))

    # update status bars
    name = text_file
    status_bar.config(text=f'{name}       ')
    name = name.replace('Lab_1/', '')
    root.title(f'{name} - Constantin Cazacu')

    # open file
    text_file = open(text_file, 'r')
    contents = text_file.read()

    contents = contents.replace('            :', ':')
    contents = contents.replace('           :', ':')
    contents = contents.replace('          :', ':')
    contents = contents.replace('         :', ':')
    contents = contents.replace('        :', ':')
    contents = contents.replace('       :', ':')
    contents = contents.replace('      :', ':')
    contents = contents.replace('     :', ':')
    contents = contents.replace('    :', ':')
    contents = contents.replace('   :', ':')
    contents = contents.replace('  :', ':')
    contents = contents.replace(' :', ':')

    start = list(find_all(contents, '<custom_item>'))
    ending = list(find_all(contents, '</custom_item>'))

    custom_item = {}

    custom_item['PASSWORD_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'password_policy': []}
    custom_item['LOCKOUT_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'lockout_policy': []}
    custom_item['KERBEROS_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'kerberos_policy': []}
    custom_item['AUDIT_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'audit_policy': []}
    custom_item['AUDIT_POLICY_SUBCATEGORY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'audit_policy_policy': []}
    custom_item['AUDIT_POWERSHELL'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'powershell_args:': [], 'only_show_cmd_output:': [], 'check_type': [], 'severity:': [], 'powershell_option': [], 'powershell_console_file:': []}
    custom_item['AUDIT_FILEHASH_POWERSHELL'] = {'type': [], 'description': [], 'value_type': [], 'file': [], 'value_data': []}
    custom_item['AUDIT_IIS_APPCMD'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'appcmd_args': [], 'only_show_cmd_output': [], 'check_type': [], 'severity': [], 'appcmd_list': [], 'appcmd_filter': [], 'appcmd_filler_value': []}
    custom_item['AUDIT_ALLOWED_OPEN_PORTS'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'port_type': []}
    custom_item['AUDIT_DENIED_OPEN_PORTS'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'port_type': []}
    custom_item['AUDIT_PROCESS_ON_PORT'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'port_type': [], 'port_no': [], 'port_option': [], 'check_type': []}
    custom_item['AUDIT_USER_TIMESTAMPS'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'timestamp': [], 'ignore_users': [], 'check_type': []}
    custom_item['BANNER_CHECK'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'reg_key': [], 'reg_item': [], 'is_substring': []}
    custom_item['CHECK_ACCOUNT'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'account_type': [], 'check_type': []}
    custom_item['CHECK_LOCAL_GROUP'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'group_type': [], 'check_type': []}
    custom_item['ANONYMOUS_SID_SETTING'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': []}
    custom_item['SERVICE_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'service_name': []}
    custom_item['GROUP_MEMBERS_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'group_name': []}
    custom_item['USER_GROUPS_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'user_name': []}
    custom_item['USER_RIGHTS_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'right_type': [], 'use_domain': []}
    custom_item['FILE_CHECK'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'file_option': []}
    custom_item['FILE_VERSION'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'file': [], 'file_option': [], 'check_type': []}
    custom_item['FILE_PERMISSIONS'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'file': [], 'acl_option': []}
    custom_item['FILE_AUDIT'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'file': [], 'acl_option': []}
    custom_item['FILE_CONTENT_CHECK'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'regex': [], 'expect': [], 'file_option': [], 'avoid_floppy_access': []}
    custom_item['FILE_CONTENT_CHECK_NOT'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'regex': [], 'expect': [], 'file_option': []}
    custom_item['REG_CHECK'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'reg_key': [], 'reg_item': [], 'key_item': []}
    custom_item['REGISTRY_SETTING'] = {'type': [], 'description': [], 'info': [], 'value_type': [], 'value_data': [], 'reg_key': [], 'reg_item': [], 'reg_enum': [], 'reg_option': []}
    custom_item['REGISTRY_PERMISSIONS'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'reg_key': [], 'acl_option': []}
    custom_item['REGISTRY_AUDIT'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'reg_key': [], 'acl_option': []}
    custom_item['REGISTRY_TYPE'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'reg_key': [], 'reg_item': [], 'reg_option': []}
    custom_item['SERVICE_PERMISSIONS'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'service': [], 'acl_option': []}
    custom_item['SERVICE_AUDIT'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'service': [], 'acl_option': []}
    custom_item['WMI_POLICY'] = {'type': [], 'description': [], 'value_type': [], 'value_data': [], 'check_type': [], 'wmi_namespace': [], 'wmi_request': [], 'wmi_attribute': [], 'wmi_key': []}

    general_custom_item = {}
    general_custom_item_keys = []

    for key in custom_item:
        keys_list = list(custom_item[key])
        for key_x in keys_list:
            if key_x not in general_custom_item_keys:
                general_custom_item_keys.append(key_x)
    for key in general_custom_item_keys:
        general_custom_item[key] = []

    for i in range(len(start)):
        content_type_block = contents[start[i] + 13: ending[i]]
        for element in list(general_custom_item.keys()):
            element_length = len(element) + 1
            if content_type_block.find(element) != -1:
                general_custom_item[element].append(content_type_block[content_type_block.find(element + ':') + element_length: content_type_block[content_type_block.find(element + ':') + element_length:].find('\n') + content_type_block.find(element + ':') + element_length].strip())
            else:
                general_custom_item[element].append('')

    to_json = []
    for i in range(len(general_custom_item['type'])):
        to_print = {}
        for element in list(general_custom_item.keys()):
            if general_custom_item[element][i] != '':
                to_print[element] = general_custom_item[element][i]
        to_json.append(to_print)

    my_text.insert(END, json.dumps(to_json, indent=4))

    # close file
    text_file.close()


# save as file function
def save_as_file():
    text_file = filedialog.asksaveasfilename(
        defaultextension='.*',
        initialdir='Lab_1/Policies/',
        title='Save File', filetypes=(('All Files', '*.*'),))
    if text_file:
        # update status bars
        name = text_file
        status_bar.config(text=f'{name}       ')
        name = name.replace('Lab_1/Policies/', '')
        root.title(f'{name} - Constantin Cazacu')

        # save file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

        # close file
        text_file.close()


def export():
    text_file = filedialog.askopenfilename(
        defaultextension='.*',
        initialdir='Lab_1/Policies/',
        title='Save File', filetypes=(('All Files', '*.*'),))

    if text_file:
        # update status bars
        name = text_file
        status_bar.config(text=f'{name}      ')
        name = name.replace('Lab_1/Policies/', '')
        root.title(f'{name} - Constantin Cazacu')

        # save file
        text_file = open(text_file, 'w')
        text_file.write(my_text.get(1.0, END))

        # close file
        text_file.close()


# main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# text box scrollbar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# horizontal scrollbar
hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16),
               selectbackground="yellow", selectforeground="black",
               undo=True, yscrollcommand=text_scroll.set, wrap="none",
               xscrollcommand=hor_scroll.set)
my_text.pack()

# configure scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)

# menu
my_menu = Menu(root)
root.config(menu=my_menu)

# file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save')
file_menu.add_command(label='Save As', command=save_as_file)
file_menu.add_command(label='Export', command=export)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

# edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Cut', command=lambda: cut_text(False), accelerator="(Ctrl+X)")
edit_menu.add_command(label='Copy', command=lambda: copy_text(False), accelerator="(Ctrl+C)")
edit_menu.add_command(label='Paste', command=lambda: paste_text(False), accelerator="(Ctrl+V)")
edit_menu.add_separator()
edit_menu.add_command(label='Undo', command=my_text.edit_undo, accelerator="(Ctrl+Z)")
edit_menu.add_command(label='Redo', command=my_text.edit_redo, accelerator="(Ctrl+Y)")

# bottom status bar
status_bar = Label(root, text='Ready     ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# edit bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

root.mainloop()