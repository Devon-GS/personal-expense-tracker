import tkinter as tk
import tkinter.ttk as ttk
from turtle import width
from options import Options
from categories import Categories
from category_rules import CategoryRules
from bank_statement_recon import BankStatementRecon
import bank_statement_recon as bsr
from accounts import Accounts
import sqlite3
import init_database as indata


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Tabs Example")

        indata.init_database()

        # Create the notebook (tabs)
        self.notebook = ttk.Notebook(self)

        # Connect To Database - Get Bank Account Names
        con = sqlite3.connect('database.db')
        c = con.cursor()
        
        c.execute("SELECT accounts FROM bankAccounts")
        records = c.fetchall()
        
        con.commit()
        con.close()

        # Create frames for the tabs
        self.tab1 = Options(self.notebook)
        self.notebook.add(self.tab1, text="Options")

        self.tab2 = Categories(self.notebook)
        self.notebook.add(self.tab2, text="Categories")

        self.tab3 = CategoryRules(self.notebook)
        self.notebook.add(self.tab3, text="Category Rules")

        self.tab5 = Accounts(self.notebook)
        self.notebook.add(self.tab5, text="Accounts")

        for x in records:
            cat = self.tab3
            name = x[0]
            self.name = BankStatementRecon(self.notebook, name, cat)
            self.notebook.add(self.name, text=f'Bank Acc: {name}')

        # Update Events
        tab_names = []
        for x in self.notebook.tabs():
            if x[12:16] == 'bank':
                tab_names.append(x)

        # Update Event Function
        def update(event):
            selected_tab = event.widget.select()
            if selected_tab in tab_names:
                bsr.refresh_page()


        # #############################################################################
        #               Testing
        # #############################################################################

        # # Create frames for the tabs
        # self.tab1 = Options(self.notebook)
        # self.tab2 = Categories(self.notebook)
        # self.tab3 = CategoryRules(self.notebook)
        # self.tab4 = BankStatementRecon(self.notebook)
        # self.tab5 = Accounts(self.notebook)

        # # Add tabs to notebook
        # self.notebook.add(self.tab1, text="Options")
        # self.notebook.add(self.tab2, text="Categories")
        # self.notebook.add(self.tab3, text="Category Rules")
        # self.notebook.add(self.tab4, text="Bank Statement Recon")
        # self.notebook.add(self.tab5, text="Accounts")        

        #     for w in selected_tab.winfo.children():
        #         print(w)
       
        #     # if selected_tab == 4:
        #     #     self.tab5.query_database()

        

        # #############################################################################

        # Event Bind
        self.notebook.bind("<<NotebookTabChanged>>", update)

        # Window Setup
        self.notebook.pack(expand=True, fill="both")

# Run App
app = App()
app.geometry("1000x500")
app.mainloop()