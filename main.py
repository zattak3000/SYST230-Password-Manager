from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno

from loginwindow import Login
from securestorage import Vault, DecryptionError
from databasewindow import DetailsView, CredsWindow

root = Tk()

# TODO CLEAN UP EVERYTHING IN HERE SO IT ISNT LITERAL GARBAGE

# Grid Config
root.columnconfigure((0,2), weight=1)
root.rowconfigure(0, weight=1)

# Listbox Config
lbxvar = StringVar(root)

lbx = Listbox(root, listvariable=lbxvar)
lbx.grid(sticky=NSEW)

# Scrollbar Config
scr = ttk.Scrollbar(root, orient=VERTICAL, command=lbx.yview)
scr.grid(row=0, column=1, sticky=NS)

lbx['yscrollcommand'] = scr.set

# Right panel config
frm = Frame(root)
frm.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

frm.columnconfigure((0,1,2), weight=1)
frm.rowconfigure(0, weight=1)

dvw = DetailsView(frm)
dvw.grid(column=0, columnspan=3, row=0, sticky=NSEW)

def display_creds(_):
    # TODO I have no idea why the listbox randomly deselects this fixes it for now
    try:
        l = vlt.list_creds()[lbx.curselection()[0]]
        dvw.display(*vlt.get_creds(l))

    except IndexError:
        dvw.display("","")

lbx.bind("<<ListboxSelect>>", display_creds)
        
# Buttons on main screen config
def save(s, u, p):
        if s in vlt.list_creds():
            confirm = askyesno('Delete Credentials', f'Are you sure you want to overwrite "{s}"')
            if not confirm:
                return

        print('New/Updated Credentials:')
        print(f'Site: {s}')
        print(f'User: {u}')
        print(f'Pass: {p}')
        vlt.add_creds(s, u, p)
        vlt.write()
        lbxvar.set(vlt.list_creds())

def cred_add():
    window = CredsWindow(root, save)

def cred_modify():
    site = vlt.list_creds()[lbx.curselection()[0]]
    user, passwd = vlt.get_creds(site)
    window = CredsWindow(root, save, site, user, passwd)

def cred_delete():
    site = vlt.list_creds()[lbx.curselection()[0]]

    confirm = askyesno('Delete Credentials', f'Are you sure you want to delete "{site}"')

    if confirm:
        print("Site deleted!")
        vlt.del_creds(site)
        vlt.write()
        lbxvar.set(vlt.list_creds())
    else:
        print("Operation Cancelled")

buttons = zip(
    ["Add", "Modify", "Delete"],
    [cred_add, cred_modify, cred_delete]
)

for i, (label, cb) in enumerate(buttons):
    button = ttk.Button(frm, text=label, command=cb)
    button.grid(column=i, row=1, ipady=20, sticky=NSEW)


# Login config
def login_cb(file, passwd):
    try:
        global vlt
        vlt = Vault(passwd, file)
    
    except DecryptionError:
        return False

    lbxvar.set(vlt.list_creds())
    root.deiconify()
    return True


root.withdraw()
lgn = Login(root, login_cb)

root.mainloop()