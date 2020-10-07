#!/usr/bin/python3

"""tksudo.pyw: visual sudo application, similar to gksudo"""

__author__ = 'Timothy Welborn'
__copyright__ = 'Copyright 2020, Timothy Welborn'
__credits__ = 'Timothy Welborn'
__license__ = 'GPL v3'
__version__ = '0.8.0'
__maintainer__ = 'Timothy Welborn'
__status__ = 'Prototype'

import sys
from os import devnull
from subprocess import Popen, PIPE
from tkinter import *
from tkinter.ttk import *


def RunCommand(sender):
    """execute command with sudo; pass entered password via subprocess.PIPE"""
    # redirect stdout and stderr to /dev/null
    if sender.nopipe:
        with open(devnull, 'w') as null:
            proc = Popen(['sudo', '-Sb'] + sender.command.split(' '), text=True, stdin=PIPE, stdout=null, stderr=null)
    else:
        proc = Popen(['sudo', '-Sb'] + sender.command.split(' '), stdin=PIPE, text=True)
    proc.communicate(input=sender.PasswordEntry.get() + '\n')
    exit()


class TkSudo(Tk):
    """visual sudo app, similar to gksudo"""

    def __init__(self, command, message='Authentication is required to run command', nopipe=False):
        super().__init__()

        self.nopipe = nopipe
        self.command = command
        self.message = message

        # gui dimensions percentages of display
        gui_x = 0.15
        gui_y = 0.175

        # set the gui dimensions and display position
        self.title('TkSudo')
        self.geometry('{0}x{1}+{2}+{3}'.format(
            int(self.winfo_screenwidth() * gui_x),
            int(self.winfo_screenheight() * gui_y),
            int(self.winfo_screenwidth() / 2 - self.winfo_screenwidth() * gui_x / 2),
            int(self.winfo_screenheight() / 2 - self.winfo_screenheight() * gui_y / 2)))

        self.resizable(0, 0)

        # configure widgets
        self.TitleLabel = Label(self, text='Authentication required')
        self.TitleLabel.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        self.MessageLabel = Label(self, text=self.message)
        self.MessageLabel.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.PasswordEntry = Entry(self, show='*')
        self.PasswordEntry.grid(row=3, column=0, columnspan=2, sticky='EW', padx=10, pady=10)

        self.CancelButton = Button(self, text='Cancel', command=exit)
        self.CancelButton.grid(row=4, column=0, sticky='NESW', padx=10, pady=10)
        self.AuthButton = Button(self, text='Authenticate', command=lambda: RunCommand(self))
        self.AuthButton.grid(row=4, column=1, sticky='NESW', padx=10, pady=10)

        for i in range(5):
            self.rowconfigure(i, weight=1)
        for i in range(2):
            self.columnconfigure(i, weight=1)

        self.bind('<Return>', lambda event: RunCommand(self))
        self.bind('<Escape>', exit)

        # set window to top level and set focus on password entry
        self.lift()
        self.PasswordEntry.focus()


# entry point
if __name__ == '__main__':
    # evaluate arguments
    if len(sys.argv) == 0:
        print('No command given.', file=sys.stderr)
    args = ' '.join(sys.argv[1:])
    TkSudo(args, 'Command: "{0}"'.format(args)).mainloop()
