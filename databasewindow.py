from random import choice
from tkinter import *
from tkinter import ttk

from string import ascii_uppercase as uppercase
from string import ascii_lowercase as lowercase
from string import digits, punctuation


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

    # TODO fix trace loop with external and internal tkinter variables that this funciton avoids
    def set_text(self, text):
        self['foreground'] = self.__foreground
        self.__placeholder = False
        self.__internal_var.set(text)

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


class GeneratorOptions(ttk.LabelFrame):
    def __init__(self, master, *args, command=None, **kwargs):
        super().__init__(master, text='Password Generator', borderwidth=10, *args, **kwargs)

        self.__callback = command

        self.__makewidgets()

    def __generate(self, *_):
        
        self.__len_text.set(f"Length: {self.__len_var.get()}")

        characters = []

        if self.__upper_var.get():
            characters.append(uppercase)

        if self.__lower_var.get():
            characters.append(lowercase)

        if self.__number_var.get():
            characters.append(digits)

        if self.__symbol_var.get():
            characters.append(punctuation)

        password = []

        if characters:
            for i in range(self.__len_var.get()):
                password.append(choice(choice(characters)))

        self.__callback("".join(password))

    def __makewidgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.__len_text = StringVar(self, "Length: 12")
        self.__len_var = IntVar(self, 12)
        self.__upper_var = IntVar(self, 1)
        self.__lower_var = IntVar(self, 1)
        self.__number_var = IntVar(self)
        self.__symbol_var = IntVar(self)

        len_label = ttk.Label(self, textvariable=self.__len_text)
        len_label.pack(side=TOP)

        len_slider = ttk.Scale(self, from_=1, to=50, variable=self.__len_var, length=200, command=self.__generate)
        len_slider.pack(side=TOP)

        upper_check = ttk.Checkbutton(self, variable=self.__upper_var, text="Uppercase", command=self.__generate)
        upper_check.pack(side=TOP)

        lower_check = ttk.Checkbutton(self, variable=self.__lower_var, text="Lowercase", command=self.__generate)
        lower_check.pack(side=TOP)

        number_check = ttk.Checkbutton(self, variable=self.__number_var, text="Numbers", command=self.__generate)
        number_check.pack(side=TOP)

        symbol_check = ttk.Checkbutton(self, variable=self.__symbol_var, text="Symbols", command=self.__generate)
        symbol_check.pack(side=TOP)


# TODO change parent to frame?
# TODO change command to kwarg
# TODO apply/cancel button
class CredsWindow(Toplevel):
    def __init__(self, master, command, site="", user="", passwd=""):
        super().__init__(master)

        self.__site_var = StringVar(self, site)
        self.__user_var = StringVar(self, user)
        self.__passwd_var = StringVar(self, passwd)

        self.__callback = command
        self.__makewidgets()

    def __makewidgets(self):
        self.columnconfigure(0, weight=1)

        site_field = PlaceholderEntry(self, title='Site', textvariable=self.__site_var)
        site_field.grid(column=0, row=0, padx=10, pady=(10,5), sticky=NSEW)

        site_field.bind('<Return>', self.__apply)

        user_field = PlaceholderEntry(self, title='Username', textvariable=self.__user_var)
        user_field.grid(column=0, row=1, padx=10, pady=5, sticky=NSEW)

        user_field.bind('<Return>', self.__apply)

        passwd_field = PlaceholderEntry(self, title="Password", textvariable=self.__passwd_var)
        passwd_field.grid(column=0, row=2, padx=10, pady=5, sticky=NSEW)

        passwd_field.bind('<Return>', self.__apply)

        passwd_generator = GeneratorOptions(self, command=lambda passwd: passwd_field.set_text(passwd))
        passwd_generator.grid(column=0, row=3, padx=10, pady=10)

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


if __name__ == "__main__":
    tk = Tk()

    # def cb(pwd):
    #     print(f'Password: {pwd}')

    # test = GeneratorOptions(tk, cb)
    # tk.columnconfigure(0, weight=1)
    # tk.rowconfigure(0, weight=1)
    # test.grid(column=0, row=0, padx=5, pady=(0,5))

    def cb(*args):
        print(*args)

    test = CredsWindow(tk, cb)

    tk.mainloop()