import tkinter as tk
import tkinter.ttk as ttk
from turtle import width
from options import Options
from categories import Categories
from category_rules import CategoryRules
from bank_statement_recon import BankStatementRecon
from accounts import Accounts


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Tabs Example")

        # Create the notebook (tabs)
        self.notebook = ttk.Notebook(self)

        # Create frames for the tabs
        self.tab1 = Options(self.notebook)
        self.tab2 = Categories(self.notebook)
        self.tab3 = CategoryRules(self.notebook)
        self.tab4 = BankStatementRecon(self.notebook)
        self.tab5 = Accounts(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.tab1, text="Options")
        self.notebook.add(self.tab2, text="Categories")
        self.notebook.add(self.tab3, text="Category Rules")
        self.notebook.add(self.tab4, text="Bank Statement Recon")
        self.notebook.add(self.tab5, text="Accounts")

        # # Update Accounts tab
        # def update(event):
        #     # selected_tab = event.widget.index('current')
        #     selected_tab = event.widget
        #     print(selected_tab)

        #     for w in selected_tab.winfo.children():
        #         print(w)
       
        #     # if selected_tab == 4:
        #     #     self.tab5.query_database()

        # self.notebook.bind("<<NotebookTabChanged>>", update)
        
        # Window Setup
        self.notebook.pack(expand=True, fill="both")

# Run App
app = App()
app.geometry("1000x500")
app.mainloop()