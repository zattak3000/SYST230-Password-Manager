from tkinter import *
from tkinter import ttk

from loginwindow import Login
from securestorage import Vault, DecryptionError
from databasewindow import DetailsView, PlaceholderEntry, CredsWindow

root = Tk()

root.columnconfigure(tuple(range(3)), weight=1)
root.rowconfigure(0, weight=1)

root.columnconfigure(1, weight=0)

lbxvar = StringVar(root)
lbxvar.set(list(f'Site {i}' for i in range(200)))

lbx = Listbox(root, listvariable=lbxvar)

lbx.grid(sticky=NSEW)

scr = ttk.Scrollbar(root, orient=VERTICAL, command=lbx.yview)
scr.grid(row=0, column=1, sticky=NS)

lbx['yscrollcommand'] = scr.set

frm = Frame(root)
frm.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

frm.columnconfigure((0,1,2), weight=1)
frm.rowconfigure(0, weight=1)

dvw = DetailsView(frm)
dvw.grid(column=0, columnspan=3, row=0, sticky=NSEW)
# dvw.display("User", "passwd123")

for i, label in enumerate(["Add", "Modify", "Delete"]):
    button = ttk.Button(frm, text=label)
    button.grid(column=i, row=1, ipady=20, sticky=NSEW)

def cb(s,u,p):
    print(f'Site: {s}')
    print(f'User: {u}')
    print(f'Pass: {p}')

# crd = CredsWindow(root, cb, 'asdf', 'asdf', 'asdf')
# crd.grab_set()

def login_cb(user, passwd):
    try:
        global vlt
        vlt = Vault(passwd, "testvault.bin")
    
    except DecryptionError:
        return False

    lbxvar.set(vlt.list_creds())
    root.deiconify()
    return True

def display_creds(_):
    l = vlt.list_creds()[lbx.curselection()[0]]
    dvw.display(*vlt.get_creds(l))

lbx.bind("<<ListboxSelect>>", display_creds)

root.withdraw()
lgn = Login(root, login_cb)

root.mainloop()