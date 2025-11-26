import sqlite3
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
# from options import Options
from categories import Categories
from category_rules import CategoryRules
from bank_statement_recon import BankStatementRecon
from accounts import Accounts


import init_database as indata
from category_rules import auto_apply_rules


class Options(Frame):
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)

		# SETUP DATABASE
		indata.init_database()

		# SORT RULES
		# auto_apply_rules()

		# SELECT OPTIONS
		# SETUP
		COLUMNS = {'A': 0,
		'B': 1,
		'C': 2,
		'D': 3,
		'E': 4,
		'F': 5,
		'G': 6,
		'H': 7,
		'I': 8,
		'J': 9,
		'K': 10,
		'L': 11,
		'M': 12,
		'N': 13,
		'O': 14,
		'P': 15,
		'Q': 16,
		'R': 17,
		'S': 18,
		'T': 19,
		'U': 20,
		'V': 21,
		'W': 22,
		'X': 23,
		'Y': 24,
		'Z': 25,
		}

		# Create reverse dic to lookup letter
		COLUMNS_LOOKUP = {v: k for k, v in COLUMNS.items()}
		
		# #############################################################################################
		# PROGRAM 
		# OFX Frame
		# #############################################################################################  
		def selected():
			con = sqlite3.connect('database.db')
			c = con.cursor()

			query = "UPDATE ofxCsv SET selected = ? WHERE id = ?"

			c.execute(query, (int(str(var.get())), 0))  

			con.commit()
			con.close()

		# Buttons
		ofx_frame = LabelFrame(self, text="OFX or CSV")
		# ofx_frame.pack(fill="x", padx=20)
		# ofx_frame.pack(padx=20, pady=(20, 50))
		ofx_frame.grid(row=0, column=0, padx=20, pady=(20, 50))

		choose_label = Label(ofx_frame, text="Date")
		choose_label.grid(row=1, column=0, padx=10, pady=10, sticky=E)

		var = IntVar()
		choose_csv = Radiobutton(ofx_frame, text="CSV", variable=var, value=1, command=selected)
		choose_csv.grid(row=1, column=0, padx=10, pady=10, sticky=E)
		choose_ofx = Radiobutton(ofx_frame, text="OFX", variable=var, value=2, command=selected)
		choose_ofx.grid(row=1, column=2, padx=10, pady=10, sticky=E)

		# Dispaly current settings in entrys
		def display_choice(): 
			con = sqlite3.connect('database.db')
			c = con.cursor()

			c.execute("SELECT selected FROM ofxCsv")
			records = c.fetchall() 

			select = records[0][0]

			if select == 1:
				choose_csv.invoke()
			else:
				choose_ofx.invoke()

			con.commit()
			con.close()
			
		# #############################################################################################
		# CSV Frame
		# ############################################################################################# 
		
		bs_frame = LabelFrame(self, text="CSV Bank Statement Setup")
		# bs_frame.pack(fill="x", padx=20)
		bs_frame.grid(row=1, column=0, sticky=N, padx=20, pady=(0,0))

		# Explain Setup
		id_label = Label(bs_frame, text="Please State which column the following is in using 'A, B, C, ETC'")
		id_label.grid(columnspan=2 , padx=(5,5), pady=10)

		# Inputs
		date_label = Label(bs_frame, text="Date")
		date_label.grid(row=1, column=0, padx=10, pady=10, sticky=E)
		date_entry = Entry(bs_frame)
		date_entry.grid(row=1, column=1, padx=10, pady=10, sticky=W)

		amount_label = Label(bs_frame, text="Amount")
		amount_label.grid(row=2, column=0, padx=10, pady=10, sticky=E)
		amount_entry = Entry(bs_frame)
		amount_entry.grid(row=2, column=1, padx=10, pady=10, sticky=W)

		description_label = Label(bs_frame, text="Description")
		description_label.grid(row=3, column=0, padx=10, pady=10, sticky=E)
		description_entry = Entry(bs_frame)
		description_entry.grid(row=3, column=1, padx=10, pady=10, sticky=W)

		# Functions
		# Dispaly current settings in entrys
		def display_entry(): 
			con = sqlite3.connect('database.db')
			c = con.cursor()

			c.execute("SELECT * FROM options")
			records = c.fetchall() 

			for x in records:
				date_entry.insert(0, COLUMNS_LOOKUP.get(x[1]))
				amount_entry.insert(0, COLUMNS_LOOKUP.get(x[2]))
				description_entry.insert(0, COLUMNS_LOOKUP.get(x[3]))

			con.commit()

		# Get Options
		def get_csv_options():
			d = date_entry.get()
			amt = amount_entry.get()
			des = description_entry.get()

			aws = messagebox.askyesno('SAVE', 'Are You Sure You Want To Save?')
			if aws == 1:
				try:
					date = COLUMNS[d.upper()]
					amount = COLUMNS[amt.upper()]
					description = COLUMNS[des.upper()]

					# Connect to database 
					con = sqlite3.connect('database.db')
					c = con.cursor()

					query = ''' UPDATE options SET 
										date = ?, 
										amount = ?,
										description = ?
									WHERE 
										id = ?
							'''

					c.execute(query, (date, amount, description, 0))       

					con.commit()
					
					# Update entry display
					date_entry.delete(0, END)
					amount_entry.delete(0, END)
					description_entry.delete(0, END)
					display_entry()

					messagebox.showinfo('SAVED', 'Coulmns Have Been Saved Successfully!')

				except KeyError:
					messagebox.showerror('ERROR!', 'Only Single Letters Can Be Used, Please Try Again!')
			else:
				messagebox.showinfo('SAVE', 'Nothing Happened')        
		# Buttons
		save_button = Button(bs_frame, text="Save", command=get_csv_options)
		save_button.grid(row=4, column=0, columnspan=2, padx=(10,20), pady=10, sticky=NSEW)
		
		# #############################################################################################
		# BANK Frame
		# ############################################################################################# 
		b_frame = LabelFrame(self, text="Bank Account Setup")
		# bs_frame.pack(fill="x", padx=20)
		b_frame.grid(row=0, column=2, rowspan=2, padx=20, pady=(20, 50)) 

		# Explain Setup
		id_label = Label(b_frame, text="Add / Remove Bank Accounts")
		id_label.grid(columnspan=2 , padx=(5,5), pady=10)
		
		# SETUP TREE VIEW
		# Add Some Style
		style = ttk.Style()

		# Pick A Theme
		style.theme_use('default')

		# Configure the Treeview Colors
		style.configure("Treeview",
			background="#D3D3D3",
			foreground="black",
			rowheight=25,
			fieldbackground="#D3D3D3")

		# Change Selected Color
		style.map('Treeview',
			background=[('selected', "#347083")])

		# Create a Treeview Frame
		tree_frame = Frame(b_frame)
		tree_frame.grid(row=0, column=0)

		# Create a Treeview Scrollbar
		tree_scroll = Scrollbar(tree_frame)
		tree_scroll.pack(side=RIGHT, fill=Y)

		# Create The Treeview
		global my_tree
		my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
		my_tree.pack()

		# Configure the Scrollbar
		tree_scroll.config(command=my_tree.yview)

		# Define Columns
		my_tree['columns'] = ("ID", "Bank Account Name")

		# Format Columns
		my_tree.column("#0", width=0, stretch=NO)
		my_tree.column("ID", anchor=W, width=50)
		my_tree.column("Bank Account Name", anchor=W, width=140)
		
		# Create Headings
		my_tree.heading("#0", text="", anchor=W)
		my_tree.heading("ID", text="ID", anchor=W)
		my_tree.heading("Bank Account Name", text="Bank Account Name", anchor=W)
		

		# Create Striped Row Tags
		my_tree.tag_configure('oddrow', background="white")
		my_tree.tag_configure('evenrow', background="lightblue")

		# FUNCTIONS
		global query_database
		def query_database():
			# Create a database or connect to one that exists
			conn = sqlite3.connect('database.db')

			# Create a cursor instance
			c = conn.cursor()

			c.execute("SELECT rowid, * FROM bankAccountNames")
			records = c.fetchall()
			
			# Add our data to the screen
			global count
			count = 0

			for record in records:
				if count % 2 == 0:
					my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('evenrow',))
				else:
					my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1]), tags=('oddrow',))
				# increment counter
				count += 1

			# Commit changes
			conn.commit()
			conn.close()

		def add_button():
			try:
				# Connect to database    
				con = sqlite3.connect('database.db')
				c = con.cursor()

				# Get bank account name
				get_name = name_entry.get()

				# Check name lenth
				if get_name == '':
					raise Exception("Name cannot be blank")
				elif len(get_name) > 25:
					raise Exception("Name longer than 25 characters")

				# Put name in camelCase
				name = get_name.lower().split()
				bank_acc_name = ''
				for x in range(0, len(name)):
					if x == 0:
						bank_acc_name += name[x]
					else:
						bank_acc_name += name[x].capitalize()
				
				c.execute("INSERT INTO bankAccountNames VALUES (:account)", {'account' : bank_acc_name})

				# Create Bank Statement Table
				c.execute(f''' CREATE TABLE IF NOT EXISTS {bank_acc_name} (
						date TEXT,
						description TEXT,
						amount TEXT,
						category TEXT
					)
				''')
			
				con.commit()
				con.close()

				# Clear entry
				name_entry.delete(0, END)

				# Reload tree
				my_tree.delete(*my_tree.get_children())
				query_database()

				# Add bank account tabs
				add_banks()
			except Exception as error:
				messagebox.showerror('ERROR', error)

		# def remove_button():
		# 	pass

		# SETUP ENTRY BOXES AND BUTTONS
		# Add Record Entry Box
		data_frame = LabelFrame(b_frame, text="Record")
		data_frame.grid(row=1, column=0)

		name_label = Label(data_frame, text="Bank Account Name")
		name_label.grid(row=0, column=0, padx=10, pady=10)
		name_entry = Entry(data_frame)
		name_entry.grid(row=0, column=1, padx=10, pady=10)

		# Add button
		add_button = Button(data_frame, text="Add", command=add_button)
		add_button.grid(row=2, column=0, columnspan=2, sticky=NSEW, padx=10, pady=10)

		# remove_button = Button(data_frame, text="Remove", command=remove_button)
		# remove_button.grid(row=3, column=0, columnspan=2, sticky=NSEW, padx=10, pady=10)

		# Run setup functions
		display_entry()
		display_choice()
		query_database()

	def refresh(self):
		my_tree.delete(*my_tree.get_children())
		query_database()


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

# List of already added bank accounts
bank_acc_created = []

def add_banks():
	conn = sqlite3.connect('database.db')
	c = conn.cursor()

	c.execute("SELECT * FROM bankAccountNames")
	records = c.fetchall()

	conn.commit()
	conn.close()

	# Create new bank acount tabs
	bank_list = []

	for x in records:
		name = x[0]

		if name not in bank_acc_created:
			# Add to created list 
			bank_acc_created.append(name)

			# Add tab
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

	if selected_tab == 0:
		tab1.refresh()

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

# Add bank accounts if any
add_banks()

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