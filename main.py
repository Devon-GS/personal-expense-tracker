# from distutils import command
import os
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from turtle import onclick
import pandas as pd
import catagory as c

# START UP PROCEDURE
# Create Database
def init_database():
	# Connect to database    
	con = sqlite3.connect('database.db')
	c = con.cursor()

	# Create Bank Statement Table
	c.execute(''' CREATE TABLE IF NOT EXISTS bankStatement (
					date TEXT,
					description TEXT,
					amount TEXT,
					catagory TEXT
				)
			''')

	# Create Income Table 
	c.execute(''' CREATE TABLE IF NOT EXISTS income (
					date TEXT,
					description TEXT,
					amount TEXT
				)
			''')

	# Create Catagory Table and Insert Default Data
	c.execute("CREATE TABLE IF NOT EXISTS catagory (catagory TEXT)")
	
	c.execute("SELECT * FROM catagory")
	records = c.fetchall()

	if len(records) == 0:
		print('yes')
		catagory_list = ['Income', 'Entertainment Expense', 'Rates and Taxes', 'Fuel']
		for cat in catagory_list:
				c.execute("INSERT INTO catagory VALUES (:catagory)", {'catagory' : cat})

	con.commit()

init_database()

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
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
		# increment counter
		count += 1

	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

# PROGRAM
root = Tk()
root.title('Income and Expense Tracker')
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
my_tree['columns'] = ("ID", "Date", "Description", "Amount", "Catagory")

# Format Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=50)
my_tree.column("Date", anchor=W, width=140)
my_tree.column("Description", anchor=W, width=140)
my_tree.column("Amount", anchor=CENTER, width=100)
my_tree.column("Catagory", anchor=CENTER, width=140)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Date", text="Date", anchor=W)
my_tree.heading("Description", text="Description", anchor=W)
my_tree.heading("Amount", text="Amount", anchor=CENTER)
my_tree.heading("Catagory", text="Catagory", anchor=CENTER)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

# SETUP ENTRY BOXES AND BUTTONS
# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

id_label = Label(data_frame, text="ID")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = Entry(data_frame)
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

# Add catagoryto drop down
cat_label = Label(data_frame, text="Catagory")
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

	c.execute("INSERT INTO bankStatement VALUES (:date, :description, :amount, :catagory)",
	{
		'date' : dt_entry.get(),
		'description' : des_entry.get(),
		'amount' : amt_entry.get(),
		'catagory' : cat_entry.get()
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
		catagory = :catagory

		WHERE oid = :oid''',
		{
			'date' : dt_entry.get(),
			'description' : des_entry.get(),
			'amount' : amt_entry.get(),
			'catagory' : cat_entry.get(),
			'oid' : id_entry.get()
		})

	# Commit changes
	conn.commit()

	# Close our connection
	conn.close()

	# Clear entry boxes
	id_entry.delete(0, END)
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
		init_database()

# Clear entry boxes
def clear_entries():
	id_entry.delete(0, END)
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

remove_many_button = Button(button_frame, text="Remove Many Selected", state='disabled')
remove_many_button.grid(row=0, column=4, padx=10, pady=10)

move_up_button = Button(button_frame, text="Move Up", state='disabled')
move_up_button.grid(row=0, column=5, padx=10, pady=10)

# move_down_button = Button(button_frame, text="Move Down", state='disabled')
# move_down_button.grid(row=0, column=6, padx=10, pady=10)

move_down_button = Button(button_frame, text="Catagory", command=c.cat_managment)
move_down_button.grid(row=0, column=6, padx=10, pady=10)

clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
clear_record_button.grid(row=0, column=7, padx=10, pady=10)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

























# # UPLOAD BANK STATEMENT FOR PROCESSING 

# # statement = Askopenfile

# ###############################################################################################
# 					INITIAL DATABASE WITH TEST DATA
# ###############################################################################################

# statement = 'statement.csv'

# df = pd.read_csv(statement).values.tolist()

# # Connect to database    
# con = sqlite3.connect('database.db')
# c = con.cursor()
    
# # Add Bank Statement Data
# query = ''' INSERT INTO bankStatement (
#     				date,
#                     description,
#                     amount,
#                     catagory
#     			)
#             VALUES
#                 (?, ?, ?, ?)    
#         '''

# for x in df:
#     c.execute(query, (x[0], x[1], x[2], 'Please Select') )
    
# con.commit()

# ###############################################################################################

query_database()

# RUN PROGRAM
root.mainloop()        