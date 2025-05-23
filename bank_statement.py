from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from dateutil import parser
import os
import sqlite3
import pandas as pd
import category as c
import accounts as acc
import category_rules as cr
import init_database as indata

def bank_statments():
	# Date changer function
	def date_changer(date, date_format=None):
		try:
			if date_format == 'display':
				return str(parser.parse(date).strftime('%Y-%m-%d'))
			else:
				return parser.parse(date).strftime('%Y%m%d')
		except OverflowError:
			return date

	# Add data to database
	def query_database():
		# Create a database or connect to one that exists
		conn = sqlite3.connect('database.db')

		# Create a cursor instance
		c = conn.cursor()

		c.execute("SELECT rowid, * FROM bankStatement")
		records = c.fetchall()
		
		# Add our data to the screen
		global count
		count = 0

		for record in records:
			if count % 2 == 0:
				my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], date_changer(record[1],'display'), record[2], record[3], record[4]), tags=('evenrow',))
			else:
				my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], date_changer(record[1],'display'), record[2], record[3], record[4]), tags=('oddrow',))
			# increment counter
			count += 1

		# Commit changes
		conn.commit()

		# Close our connection
		conn.close()

	# PROGRAM
	root = Tk()
	root.title('Bank Statement Management')
	# root.iconbitmap('')
	root.geometry("1000x500")

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
	tree_frame = Frame(root)
	tree_frame.pack(pady=10)

	# Create a Treeview Scrollbar
	tree_scroll = Scrollbar(tree_frame)
	tree_scroll.pack(side=RIGHT, fill=Y)

	# Create The Treeview
	my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
	my_tree.pack()

	# Configure the Scrollbar
	tree_scroll.config(command=my_tree.yview)

	# Define Columns
	my_tree['columns'] = ("ID", "Date", "Description", "Amount", "Category")

	# Format Columns
	my_tree.column("#0", width=0, stretch=NO)
	my_tree.column("ID", anchor=W, width=50)
	my_tree.column("Date", anchor=W, width=140)
	my_tree.column("Description", anchor=W, width=140)
	my_tree.column("Amount", anchor=CENTER, width=100)
	my_tree.column("Category", anchor=CENTER, width=140)

	# Create Headings
	my_tree.heading("#0", text="", anchor=W)
	my_tree.heading("ID", text="ID", anchor=W)
	my_tree.heading("Date", text="Date", anchor=W)
	my_tree.heading("Description", text="Description", anchor=W)
	my_tree.heading("Amount", text="Amount", anchor=CENTER)
	my_tree.heading("Category", text="Category", anchor=CENTER)

	# Create Striped Row Tags
	my_tree.tag_configure('oddrow', background="white")
	my_tree.tag_configure('evenrow', background="lightblue")

	# SETUP ENTRY BOXES AND BUTTONS
	# Add Record Entry Boxes
	data_frame = LabelFrame(root, text="Record")
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
		options = c.get_cat_data()
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

			# Check if catagory is fill out or leave default 
			if cat_entry.get() == '':
				cat = 'Please Select'
			else:
				cat = cat_entry.get()

			c.execute("INSERT INTO bankStatement VALUES (:date, :description, :amount, :category)",
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
			my_tree.delete(*my_tree.get_children())

			# Get data from database again
			query_database()
		except Exception as error:
			messagebox.showerror('ERROR', error)

	# Update record
	def update_record():
		# Grab the record number
		selected = my_tree.focus()
		# Update record
		my_tree.item(selected, text="", values=(id_entry.get(), dt_entry.get(), des_entry.get(), amt_entry.get(), cat_entry.get(),))

		# Create a database or connect to one that exists
		conn = sqlite3.connect('database.db')

		# Create a cursor instance
		c = conn.cursor()

		c.execute('''UPDATE bankStatement SET
			date = :date,
			description = :description,
			amount = :amount,
			category = :category

			WHERE oid = :oid''',
			{
				'date' : date_changer(dt_entry.get()),
				'description' : des_entry.get(),
				'amount' : amt_entry.get(),
				'category' : cat_entry.get(),
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

	# Remove one record
	def remove_one():
		x = my_tree.selection()[0]
		my_tree.delete(x)

		# Create a database or connect to one that exists
		conn = sqlite3.connect('database.db')

		# Create a cursor instance
		c = conn.cursor()

		c.execute("DELETE FROM bankStatement WHERE oid=" + id_entry.get())

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
		messagebox.showwarning('Delete Detected', 'YOU ARE ABOUT TO DELETE ALL RECORDS')

		response = messagebox.askyesno('Delete Detected', 'Are you sure you want to delete ALL RECORDS?')

		# Logic for message box
		if response == 1:
			for record in my_tree.get_children():
				my_tree.delete(record)

			# Create a database or connect to one that exists
			conn = sqlite3.connect('database.db')

			# Create a cursor instance
			c = conn.cursor()

			c.execute("DROP TABLE bankStatement")

			# Commit changes
			conn.commit()

			# Close our connection
			conn.close()

			# Clear the entry boxes
			clear_entries()

			# Add back table to database
			indata.init_database('reinit')

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
		selected = my_tree.focus()
		# Grab record values
		values = my_tree.item(selected, 'values')

		# output to entry boxes
		id_entry.insert(0, values[0])
		id_entry.config(state="readonly")
		dt_entry.insert(0, values[1])
		des_entry.insert(0, values[2])
		amt_entry.insert(0, values[3])
		cat_entry.insert(0, values[4])

	def add_rule():
		top = Toplevel(root)
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

			cr.auto_apply_rules()

			# Clear Tree View
			my_tree.delete(*my_tree.get_children())

			query_database()

			top.destroy()

		save_button = Button(top, text="Save", command=save)
		save_button.grid(row=2, column=0, padx=10, pady=10)

	# Add Buttons
	button_frame = LabelFrame(root, text="Commands")
	button_frame.pack(fill="x", expand="yes", padx=20)

	update_button = Button(button_frame, text="Update Record", command=update_record)
	update_button.grid(row=0, column=0, padx=10, pady=10)

	add_button = Button(button_frame, text="Add Record", command=add_record)
	add_button.grid(row=0, column=1, padx=10, pady=10)

	remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
	remove_all_button.grid(row=0, column=2, padx=10, pady=10)

	remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
	remove_one_button.grid(row=0, column=3, padx=10, pady=10)

	add_category_button = Button(button_frame, text="Add Rule",command=add_rule)
	add_category_button.grid(row=0, column=4, padx=10, pady=10)

	accounts_button = Button(button_frame, text="Accounts", command=acc.accounts_total)
	accounts_button.grid(row=0, column=5, padx=10, pady=10)

	category_button = Button(button_frame, text="Category", command=c.cat_managment)
	category_button.grid(row=0, column=6, padx=10, pady=10)

	clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
	clear_record_button.grid(row=0, column=7, padx=10, pady=10)

	# Bind the treeview
	my_tree.bind("<ButtonRelease-1>", select_record)

	# Get data and disply
	query_database()

	# RUN PROGRAM
	root.mainloop()     