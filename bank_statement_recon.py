from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from dateutil import parser
import os
import sqlite3
import pandas as pd
import categories as ca
import accounts as acc
import category_rules as cr
from bank_import import add_bank_statement
import init_database as indata
from accounts import Accounts


# Date changer function
def date_changer(date, date_format=None):
	try:
		if date_format == 'display':
			return str(parser.parse(date).strftime('%Y-%m-%d'))
		else:
			return parser.parse(date).strftime('%Y%m%d')
	except OverflowError:
		return date

class BankStatementRecon(Frame):
	def __init__(self, parent, account_name, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)

		# Add data to database
		# global query_database
		def query_database(account_name):
			# Create a database or connect to one that exists
			conn = sqlite3.connect('database.db')

			# Create a cursor instance
			c = conn.cursor()

			c.execute(f"SELECT rowid, * FROM {account_name}")
			records = c.fetchall()
			
			# Add our data to the screen
			global count
			count = 0

			for record in records:
				if count % 2 == 0:
					self.my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], date_changer(record[1],'display'), record[2], record[3], record[4]), tags=('evenrow',))
				else:
					self.my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], date_changer(record[1],'display'), record[2], record[3], record[4]), tags=('oddrow',))
				# increment counter
				count += 1

			# Commit changes
			conn.commit()

			# Close our connection
			conn.close()

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
		tree_frame = Frame(self)
		tree_frame.pack(pady=10)

		# Create a Treeview Scrollbar
		self.tree_scroll = Scrollbar(tree_frame)
		self.tree_scroll.pack(side=RIGHT, fill=Y)

		# Create The Treeview
		# global my_tree
		self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
		self.my_tree.pack()

		# Configure the Scrollbar
		self.tree_scroll.config(command=self.my_tree.yview)

		# Define Columns
		self.my_tree['columns'] = ("ID", "Date", "Description", "Amount", "Category")

		# Format Columns
		self.my_tree.column("#0", width=0, stretch=NO)
		self.my_tree.column("ID", anchor=W, width=50)
		self.my_tree.column("Date", anchor=W, width=140)
		self.my_tree.column("Description", anchor=W, width=140)
		self.my_tree.column("Amount", anchor=CENTER, width=100)
		self.my_tree.column("Category", anchor=CENTER, width=140)

		# Create Headings
		self.my_tree.heading("#0", text="", anchor=W)
		self.my_tree.heading("ID", text="ID", anchor=W)
		self.my_tree.heading("Date", text="Date", anchor=W)
		self.my_tree.heading("Description", text="Description", anchor=W)
		self.my_tree.heading("Amount", text="Amount", anchor=CENTER)
		self.my_tree.heading("Category", text="Category", anchor=CENTER)

		# Create Striped Row Tags
		self.my_tree.tag_configure('oddrow', background="white")
		self.my_tree.tag_configure('evenrow', background="lightblue")

		# SETUP ENTRY BOXES AND BUTTONS
		# Add Record Entry Boxes
		data_frame = LabelFrame(self, text="Record")
		data_frame.pack(fill="x", expand="yes", padx=20)

		id_label = Label(data_frame, text="ID")
		id_label.grid(row=0, column=0, padx=10, pady=10)
		id_entry = Entry(data_frame, state='readonly')
		id_entry.grid(row=0, column=1, padx=10, pady=10)

		dt_label = Label(data_frame, text="Date")
		dt_label.grid(row=0, column=2, padx=10, pady=10)
		dt_entry = Entry(data_frame)
		dt_entry.grid(row=0, column=3, padx=10, pady=10)

		des_label = Label(data_frame, text="Description")
		des_label.grid(row=0, column=4, padx=10, pady=10)
		des_entry = Entry(data_frame)
		des_entry.grid(row=0, column=5, padx=10, pady=10)

		amt_label = Label(data_frame, text="Amount")
		amt_label.grid(row=0, column=6, padx=10, pady=10)
		amt_entry = Entry(data_frame)
		amt_entry.grid(row=0, column=7, padx=10, pady=10)

		# Add category to drop down
		cat_label = Label(data_frame, text="Category")
		cat_label.grid(row=1, column=0, padx=10, pady=10)

		def update_combobox_options():
			options = ca.get_cat_data()
			cat_entry['values']= options

		n = StringVar()
		cat_entry = ttk.Combobox(data_frame, width = 18, textvariable = n, postcommand=update_combobox_options) 
		cat_entry.grid(row=1, column=1, padx=10, pady=10)

		# FUNCTIONS FOR BUTTONS
		def add_record():
			# Create a database or connect to one that exists
			conn = sqlite3.connect('database.db')

			# Create a cursor instance
			c = conn.cursor()

			try:
				# Check if all entrys are filled out
				if dt_entry.get() == '' or des_entry.get() == '' or amt_entry.get() == '':
					raise Exception("Sorry, Please fill out all information")
				elif len(dt_entry.get()) < 8 or len(dt_entry.get()) > 10:
					raise Exception("Date format YYYYMMDD or YYYY/MM/DD or DD/MM/YYYY")

				# Check if catagory is fill out or leave default or if not allowed string
				get_cat = cat_entry.get()
				if get_cat == '':
					cat = 'Please Select'
				elif get_cat not in ca.get_cat_data():
					cat = 'Please Select'
				else:
					cat = get_cat

				c.execute(f"INSERT INTO {account_name} VALUES (:date, :description, :amount, :category)",
					{
						'date' : date_changer(dt_entry.get()),
						'description' : des_entry.get(),
						'amount' : amt_entry.get(),
						'category' : cat
					})

				# Commit changes
				conn.commit()

				# Close our connection
				conn.close()

				# Clear entry boxes
				dt_entry.delete(0, END)
				des_entry.delete(0, END)
				amt_entry.delete(0, END)
				cat_entry.delete(0, END)

				# Clear Tree View
				self.my_tree.delete(*self.my_tree.get_children())

				# Get data from database again
				query_database(account_name)
			except Exception as error:
				messagebox.showerror('ERROR', error)

		# Update record
		def update_record():
			# Grab the record number
			selected = self.my_tree.focus()
			# Update record
			self.my_tree.item(selected, text="", values=(id_entry.get(), dt_entry.get(), des_entry.get(), amt_entry.get(), cat_entry.get(),))

			# Create a database or connect to one that exists
			conn = sqlite3.connect('database.db')

			# Create a cursor instance
			c = conn.cursor()

			try:
				if cat_entry.get() != 'Please Select':
					if cat_entry.get() not in ca.get_cat_data():
						raise Exception("Selected Category Not In Category List")
					else:
						cat = cat_entry.get()

				c.execute(f'''UPDATE {account_name} SET
					date = :date,
					description = :description,
					amount = :amount,
					category = :category

					WHERE oid = :oid''',
					{
						'date' : date_changer(dt_entry.get()),
						'description' : des_entry.get(),
						'amount' : amt_entry.get(),
						'category' : cat,
						'oid' : id_entry.get()
					})

				# Commit changes
				conn.commit()

				# Close our connection
				conn.close()

				# Clear entry boxes
				id_entry.config(state="normal")
				id_entry.delete(0, END)
				id_entry.config(state="readonly")
				dt_entry.delete(0, END)
				des_entry.delete(0, END)
				amt_entry.delete(0, END)
				cat_entry.delete(0, END)

			except Exception as error:
				messagebox.showerror('ERROR', error)

		# Remove one record
		def remove_one():
			x = self.my_tree.selection()[0]
			self.my_tree.delete(x)

			# Create a database or connect to one that exists
			conn = sqlite3.connect('database.db')

			# Create a cursor instance
			c = conn.cursor()

			c.execute(f"DELETE FROM {account_name} WHERE oid=" + id_entry.get())

			# Commit changes
			conn.commit()

			# Close our connection
			conn.close()

			# Clear the entry boxes
			clear_entries()

			# Messagebox confirmation
			messagebox.showinfo('Deleted!', 'Your Record Has Been Deleted')
			
		# Remove all records
		def remove_all():
			# Messagebox Warning
			messagebox.showwarning('Delete Detected', 'YOU ARE ABOUT TO DELETE ALL RECORDS AND REMOVE BANK ACCOUNT')

			response = messagebox.askyesno('Delete Detected', 'Are you sure you want to delete ALL RECORDS?')

			# Logic for message box
			if response == 1:
				for record in self.my_tree.get_children():
					self.my_tree.delete(record)

				# Create a database or connect to one that exists
				conn = sqlite3.connect('database.db')

				# Create a cursor instance
				c = conn.cursor()

				c.execute(f"DROP TABLE {account_name}")
				c.execute(f"DELETE FROM bankAccountNames WHERE account = ?", (account_name,))

				# Commit changes
				conn.commit()
				conn.close()

				# Add back table to database
				indata.init_database('reinit')
				
				# Destroy tab
				Frame.destroy(self)

		# Clear entry boxes
		def clear_entries():
			id_entry.config(state="normal")
			id_entry.delete(0, END)
			id_entry.config(state="readonly")
			dt_entry.delete(0, END)
			des_entry.delete(0, END)
			amt_entry.delete(0, END)
			cat_entry.delete(0, END)

		# Select Record
		def select_record(e):
			# Clear entry boxes
			id_entry.config(state="normal")
			id_entry.delete(0, END)
			dt_entry.delete(0, END)
			des_entry.delete(0, END)
			amt_entry.delete(0, END)
			cat_entry.delete(0, END)

			# Grab record Number
			selected = self.my_tree.focus()
		
			# Grab record values
			values = self.my_tree.item(selected, 'values')

			# output to entry boxes
			id_entry.insert(0, values[0])
			id_entry.config(state="readonly")
			dt_entry.insert(0, values[1])
			des_entry.insert(0, values[2])
			amt_entry.insert(0, values[3])
			cat_entry.insert(0, values[4])

		def add_rule():
			top = Toplevel(self)
			top.geometry("300x150")
			top.title("Rule Name")

			name_label = Label(top, text="Enter Rule Name:")
			name_label.grid(row=0, column=0, padx=10, pady=10)
			name_entry = Entry(top)
			name_entry.grid(row=0, column=1, padx=10, pady=10)

			def save():
				rule_name = name_entry.get()
				appliedTo = des_entry.get()
				category = cat_entry.get()

				cr.auto_add_rule(rule_name, appliedTo, category)

				cr.auto_apply_rules(account_name)

				# Clear Tree View
				self.my_tree.delete(*self.my_tree.get_children())

				query_database(account_name)

				top.destroy()

			save_button = Button(top, text="Save", command=save)
			save_button.grid(row=2, column=0, padx=10, pady=10)

		def add_statements():
			# function to import bankstatements
			add_bank_statement(account_name)
			
			# Refresh page
			query_database(account_name)  

		# Add Buttons
		button_frame = LabelFrame(self, text="Commands")
		button_frame.pack(fill="x", expand="yes", padx=20)

		import_statement_button = Button(button_frame, text="Import Statement", command=add_statements)
		import_statement_button.grid(row=0, column=1, padx=10, pady=10)

		update_button = Button(button_frame, text="Update Record", command=update_record)
		update_button.grid(row=0, column=2, padx=10, pady=10)

		add_button = Button(button_frame, text="Add Record", command=add_record)
		add_button.grid(row=0, column=3, padx=10, pady=10)

		remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
		remove_all_button.grid(row=0, column=4, padx=10, pady=10)

		remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
		remove_one_button.grid(row=0, column=5, padx=10, pady=10)

		add_category_button = Button(button_frame, text="Add Rule",command=add_rule)
		add_category_button.grid(row=0, column=6, padx=10, pady=10)

		clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
		clear_record_button.grid(row=0, column=7, padx=10, pady=10)

		# Bind the treeview
		self.my_tree.bind("<ButtonRelease-1>", select_record)

		# Get data and disply
		query_database(account_name) 
		cr.auto_apply_rules(account_name) 
	
	def refresh(self):
		# Clear Tree View
		self.my_tree.delete(*self.my_tree.get_children())
		# query_database(account_name) 	