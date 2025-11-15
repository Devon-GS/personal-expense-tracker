import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from options import Options
from categories import Categories
from category_rules import CategoryRules
from bank_statement_recon import BankStatementRecon
from accounts import Accounts


# #################################################################################################################
#  NEW MAIN APP
# #################################################################################################################

root = tk.Tk()
root.title("Personal Expense Tracker")
# root.iconbitmap("_internal/Dollar.ico")
root.geometry("1000x500")

# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create the tabs (Frame)
tab1 = Options(notebook)
tab2 = Categories(notebook)
tab3 = CategoryRules(notebook)
tab4 = Accounts(notebook)
# tab5 = BankStatementRecon(notebook)

# Add tab to notebook
notebook.add(tab1, text="Options")
notebook.add(tab2, text="Categories")
notebook.add(tab3, text="Category Rules")
notebook.add(tab4, text="Category Amounts")

# Add multiple bank account [upcoming feature]
# Get bank acount names from database
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("SELECT * FROM bankAccountNames")
records = c.fetchall()

conn.commit()
conn.close()

bank_list = []

for x in records:
	name = x[0]
	tab_name = name
	tab_name = BankStatementRecon(notebook, name)
	notebook.add(tab_name, text=name)
	bank_list.append(tab_name)

# bank_list[0].show_data()
# bank_list[1].show_data()

# Update Categories tab
def update(event):
	selected_tab = event.widget.index('current')
	selected_tab_name = notebook.tab(selected_tab, 'text')
	# selected_tab = event.widget
	# print(selected_tab)

	if selected_tab == 2:
		tab3.refresh_cat_rules()

	if selected_tab == 3:
		tab4.refresh()

	# if selected_tab > 3:
	# 	for x in range(0, len(bank_list)):
	# 		bank_list[x].refresh(records[x][0])

	# if selected_tab > 3:
	# 	for x in dir(bank_list[0]):
	# 		print(x)

			

notebook.bind("<<NotebookTabChanged>>", update)

# Start the Tkinter event loop
root.mainloop()

# #################################################################################################################
#  OLD MAIN APP V3.1.0-Alpha
# #################################################################################################################

# class App(tk.Tk):
# 	def __init__(self):
# 		super().__init__()
# 		self.title("Tkinter Tabs Example")

# 		# Create the notebook (tabs)
# 		self.notebook = ttk.Notebook(self)

# 		# Create frames for the tabs
# 		self.tab1 = Options(self.notebook)
# 		self.tab2 = Categories(self.notebook)
# 		self.tab3 = CategoryRules(self.notebook)
# 		self.tab4 = BankStatementRecon(self.notebook)
# 		# self.tab5 = Accounts(self.notebook)
# 		tab5 = Accounts(self.notebook)

# 		# Add tabs to notebook
# 		self.notebook.add(self.tab1, text="Options")
# 		self.notebook.add(self.tab2, text="Categories")
# 		self.notebook.add(self.tab3, text="Category Rules")
# 		self.notebook.add(self.tab4, text="Bank Statement Recon")
# 		# self.notebook.add(self.tab5, text="Accounts")
# 		self.notebook.add(tab5, text="Accounts")

# 		# # Update Accounts tab
# 		# def update(event):
# 		# 	# selected_tab = event.widget.index('current')
# 		# 	selected_tab = event.widget
# 		# 	print(selected_tab)

# 		# 	for w in selected_tab.info.children():
# 		# 		print(w)
	   
# 		# 	# if selected_tab == 4:
# 		# 	#     self.tab5.query_database()

# 		# # self.notebook.bind("<<NotebookTabChanged>>", update)
# 		# self.notebook.bind("<<NotebookTabChanged>>", lambda event: event.widget.winfo_children()[event.widget.index("current")].update())
		
# 		tab5.fff()

		
# 		# Window Setup
# 		self.notebook.pack(expand=True, fill="both")

# Run App
# app = App()
# app.geometry("1000x500")
# app.mainloop()

