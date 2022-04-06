from tkinter import *
from tkinter import ttk


class DetailsView(ttk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Details", labelanchor=NW)

        self.__user_var = StringVar(self)
        self.__passwd_var = StringVar(self)

        self.__makewidgets()


    def __makewidgets(self):

        def clipboard_set(text):
            self.clipboard_clear()
            self.clipboard_append(text)

        font = ("Arial", 14)

        self.columnconfigure(1, weight=1)

        user_label = ttk.Label(self, text="Username: ", font=font)
        user_label.grid(column=0, row=0, sticky=E)

        user_field = ttk.Label(self, textvariable=self.__user_var, font=font)
        user_field.grid(column=1, row=0, sticky=W)

        passwd_label = ttk.Label(self, text="Password: ", font=font)
        passwd_label.grid(column=0, row=1, sticky=E)
        
        passwd_field = ttk.Label(self, textvariable=self.__passwd_var, font=font)
        passwd_field.grid(column=1, row=1, sticky=W)

        user_copy = ttk.Button(self, text="Copy",
            command=lambda : self.__copy(user_copy, self.__user_var)
        )

        user_copy.grid(column=2, row=0)

        passwd_copy = ttk.Button(self, text="Copy",
            command=lambda : self.__copy(passwd_copy, self.__passwd_var)
        )
        
        passwd_copy.grid(column=2, row=1)

    def __copy(self, element, var):
        self.clipboard_clear()
        self.clipboard_append(var.get())

        element.config(text="Copied!")

        if hasattr(element, "msgclr"):
            self.after_cancel(element.msgclr)

        element.msgclr = self.after(500, lambda : element.config(text="Copy"))

    def display(self, username, password):
        self.__user_var.set(username)
        self.__passwd_var.set(password)

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master, *args, title='', textvariable=None, foreground='black', **kwargs):

        self.__foreground = foreground
        self.__title = title

        if textvariable:

            self.__external_var = textvariable
            
            if textvariable.get() == '':
                self.__internal_var = StringVar(master)
                self.__placeholder = True

            else:
                self.__internal_var = StringVar(master, textvariable.get())
                self.__placeholder = False

            self.__internal_var.trace_add('write', self.__update_external)
        
        else:
            self.__internal_var = StringVar(master)
            self.__placeholder = True

        super().__init__(master, *args, textvariable=self.__internal_var, foreground=foreground, **kwargs)

        self.__placeholder_update(False)

        self.bind('<FocusIn>', lambda _ : self.__placeholder_update(True))
        self.bind('<FocusOut>', lambda _ : self.__placeholder_update(False))

    def __update_external(self, *_):
        if self.__placeholder:
            self.__external_var.set('')

        else:
            self.__external_var.set(self.__internal_var.get())

    def __placeholder_update(self, focus):
        if focus and self.__placeholder:
            self.__placeholder = False
            self['foreground'] = self.__foreground
            self.delete(0, END)

        elif self.get() == '':
            self.__placeholder = True
            self['foreground'] = 'gray'
            self.insert(0, self.__title)

class CredsWindow(Toplevel):
    def __init__(self, master, command, site="", user="", passwd=""):
        super().__init__(master)

        self.__site_var = StringVar(self, site)
        self.__user_var = StringVar(self, user)
        self.__passwd_var = StringVar(self, passwd)

        self.__callback = command
        self.__makewidgets()

    # TODO Refactor placeholder entry into own class
    def __makewidgets(self):
        self.columnconfigure(0, weight=1)

        site_field = PlaceholderEntry(self, title='Site', textvariable=self.__site_var)
        site_field.grid(column=0, row=0, padx=10, pady=(10,5))

        site_field.bind('<Return>', self.__apply)

        user_field = PlaceholderEntry(self, title='Username', textvariable=self.__user_var)
        user_field.grid(column=0, row=1, padx=10, pady=5)

        user_field.bind('<Return>', self.__apply)

        passwd_field = PlaceholderEntry(self, title="Password", textvariable=self.__passwd_var)
        passwd_field.grid(column=0, row=2, padx=10, pady=(5,10))

        passwd_field.bind('<Return>', self.__apply)

    # TODO HORRIBLE
    def __apply(self, _):
        if (self.__site_var.get() == "" or
            self.__user_var.get() == "" or
            self.__passwd_var.get() == ""):
            # Do something
            return

        self.__callback(
            self.__site_var.get(),
            self.__user_var.get(),
            self.__passwd_var.get()
        )

        self.destroy()



