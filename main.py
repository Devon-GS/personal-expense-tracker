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
root.title("Tkinter Notebook Example")
root.geometry("1000x500")

# Create a Notebook widget
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create the tabs (Frame)
tab1 = Options(notebook)
tab2 = Categories(notebook)
tab3 = CategoryRules(notebook)
tab4 = Accounts(notebook)
tab5 = BankStatementRecon(notebook)

# Add tab to notebook
notebook.add(tab1, text="Options")
notebook.add(tab2, text="Categories")
notebook.add(tab3, text="Category Rules")
notebook.add(tab4, text="Category Amounts")
notebook.add(tab5, text="Bank Statement Recon")


# Add multiple bank account [upcoming feature]

# gg = ['BankOne', 'BankTwo', 'BankThree']

# for x in gg:
	
# 	name = x
	
# 	name = BankStatementRecon(notebook)
# 	print(type(name))
# 	notebook.add(name, text=x)


# Update Categories tab
def update(event):
	selected_tab = event.widget.index('current')
	# selected_tab = event.widget
	# print(selected_tab)

	if selected_tab == 2:
		tab3.refresh_cat_rules()

	if selected_tab == 3:
		tab4.refresh()

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

