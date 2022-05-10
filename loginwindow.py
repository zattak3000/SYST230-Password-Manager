from string import ascii_letters, digits
from os.path import exists, abspath

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename


# TODO Truncate long paths
class VaultPicker(ttk.Labelframe):
    def __init__(self, master, *args, default="", **kwargs):
        super().__init__(master, *args, text="Vault File", **kwargs)

        self.__file = StringVar(self, "NO FILE SELECTED")
        self.__default_file = default

        if exists(default):
            self.__file.set(abspath(default))

        self.__makewidgets()


    def __select_file(self, new):
        if new:
            file = asksaveasfilename(filetypes=[("Vault Files", "*.bin")], initialfile=self.__default_file)
        else:
            file = askopenfilename(filetypes=[("Vault Files", "*.bin")])

        if file:
            self.__file.set(file)


    def __makewidgets(self):
        file_text = ttk.Label(self, textvariable=self.__file)
        file_text.pack(side=BOTTOM, pady=5)

        new_button = ttk.Button(self, text="New", command=lambda : self.__select_file(True))
        new_button.pack(side=LEFT, expand=True, fill=X, padx=5)

        open_button = ttk.Button(self, text="Open", command=lambda : self.__select_file(False))
        open_button.pack(side=LEFT, expand=True, fill=X, padx=5)

    
    def get(self):
        file = self.__file.get()
        return file if file != "NO FILE SELECTED" else False


class Login(Toplevel):
    def __init__(self, master, callback, *args, **kwargs):
        '''
        Login Window

        Parameters
        ----------
        master
            Parent tk instance
        callback
            login verification function that takes
            (username, password) as arguments,
            returns True upon successful login,
            False otherwise
        '''

        super().__init__(master, *args, **kwargs)

        self.resizable(False, False)

        self.__passwd = StringVar(self, "Password")
        self.__message = StringVar(self, "")
        self.__verify_cb = callback

        self.__makewidgets()


    def __makewidgets(self):
        self.columnconfigure(0, weight=1)

        self.title("Login")

        title = ttk.Label(self, text="🔒 Login", font=('Arial', 24))
        title.grid(row=0, sticky=N)

        vdt = (self.register(self.__validate_entry), '%d', '%S')

        self.__file = VaultPicker(self, default='vault.bin')
        self.__file.grid(row=1, ipadx=80, padx=10, pady=5)

        passwd_field = ttk.Entry(self, textvariable=self.__passwd, foreground="gray", show='*', validate='key', validatecommand=vdt)
        passwd_field.grid(row=2, sticky=EW, padx=10, pady=5)

        passwd_field.bind('<Return>', self.__callback)
        passwd_field.bind('<FocusIn>', lambda _ : self.__placeholder(passwd_field, True, "Password"))
        passwd_field.bind('<FocusOut>', lambda _ : self.__placeholder(passwd_field, False, "Password"))

        message_field = ttk.Label(self, textvariable=self.__message, font=('Arial', 14))
        message_field.grid(row=3, sticky=N, padx=10, pady=(0,5))


    def __placeholder(self, element, focus, default):
        if focus and element.get() == default:
            element['foreground'] = 'black'
            element.delete(0, END)

        elif element.get() == '':
            element['foreground'] = 'gray'
            element.insert(0, default)


    def __validate_entry(self, event, new_text):
        if event == '0':
            return True

        for i in new_text:
            if i not in (ascii_letters + digits):
                return False

        return True


    def __callback(self, _):
        if not self.__file.get():
            self.__login_fail("SELECT FILE")
            return

        result = self.__verify_cb(self.__file.get(), self.__passwd.get())

        if result:
            self.__login_success()
            
        else:
            self.__login_fail("LOGIN FAILED")


    def __login_fail(self, message):
        self.__message.set(message)
        self.after(2000, lambda : self.__message.set(""))


    def __login_success(self):
        # self.__message.set("LOGIN SUCCESS")
        # self.after(2000, lambda : self.destroy())
        self.destroy()


if __name__ == "__main__":
    # Create root tk instance
    root = Tk()

    svr = StringVar(root, "Not Logged In.")

    # Add label so it isn't blank
    lbl = Label(root, textvariable=svr)
    lbl.grid(ipadx=20, ipady=20)

    # Hide the root window
    root.iconify()

    # Define verification function for login popup
    def verify(user, passwd):
        print(f'Username: {user}')
        print(f'Password: {passwd}')
        
        # Example verifcation code
        if user == 'admin' and passwd == 'admin':
            svr.set("Logged In!")
            return True
        else:
            return False

    # Create login popup instance
    window = Login(root, verify)

    root.mainloop()