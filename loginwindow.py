from string import ascii_letters, digits
from tkinter import *
from tkinter import ttk

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

        self.__user = StringVar(self, "Username")
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

        self.__user_field = ttk.Entry(self, textvariable=self.__user, foreground="gray", width=40, validate='key', validatecommand=vdt)
        self.__user_field.grid(row=1, sticky=EW, padx=10, pady=5)

        self.__user_field.bind('<Return>', self.__callback)
        self.__user_field.bind('<FocusIn>', lambda _ : self.__placeholder(self.__user_field, True, "Username"))
        self.__user_field.bind('<FocusOut>', lambda _ : self.__placeholder(self.__user_field, False, "Username"))

        self.__passwd_field = ttk.Entry(self, textvariable=self.__passwd, foreground="gray", show='*', validate='key', validatecommand=vdt)
        self.__passwd_field.grid(row=2, sticky=EW, padx=10, pady=5)

        self.__passwd_field.bind('<Return>', self.__callback)
        self.__passwd_field.bind('<FocusIn>', lambda _ : self.__placeholder(self.__passwd_field, True, "Password"))
        self.__passwd_field.bind('<FocusOut>', lambda _ : self.__placeholder(self.__passwd_field, False, "Password"))

        self.__message_field = ttk.Label(self, textvariable=self.__message, font=('Arial', 14))
        self.__message_field.grid(row=3, sticky=N, padx=10, pady=(0,5))


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

        result = self.__verify_cb(self.__user.get(), self.__passwd.get())

        if result:
            self.__login_success()
            
        else:
            self.__login_fail()


    def __login_fail(self):
        self.__message.set("LOGIN FAILED")
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