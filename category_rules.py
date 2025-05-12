import sqlite3
from tkinter import *
from tkinter import ttk


# ADD RULES
#  DISPLAY RULES 
#  UPDATE RULLES AND MOVE ALL TO NEW RULE


# Create a database or connect to one that exists
conn = sqlite3.connect('database.db')
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS categoryRules (ruleName TEXT, appliedTo TEXT, accountName TEXT)")

# c.execute("SELECT rowid, * FROM bankStatement")
# records = c.fetchall()



conn.commit()
conn.close()




























acc_rules = Tk()
acc_rules.title('')
acc_rules.geometry("1000x500")

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
tree_frame = Frame(acc_rules)
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
my_tree['columns'] = ("Category", "Total Amount")

# Format Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Category", anchor=W, width=250)
my_tree.column("Total Amount", anchor=W, width=140)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Category", text="ID", anchor=W)
my_tree.heading("Total Amount", text="Date", anchor=W)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

# SETUP ENTRY BOXES AND BUTTONS
# Add Record Entry Boxes
data_frame = LabelFrame(acc_rules, text="Record")
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

# FUNCTIONS FOR BUTTONS
def add_record():
		# Create a database or connect to one that exists
		conn = sqlite3.connect('database.db')

		# Create a cursor instance
		c = conn.cursor()

		c.execute("INSERT INTO bankStatement VALUES (:date, :description, :amount, :category)",
		{
			'date' : dt_entry.get(),
			'description' : des_entry.get(),
			'amount' : amt_entry.get(),
			'category' : cat_entry.get()
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

	# # Update record
	# def update_record():
	# 	# Grab the record number
	# 	selected = my_tree.focus()
	# 	# Update record
	# 	my_tree.item(selected, text="", values=(id_entry.get(), dt_entry.get(), des_entry.get(), amt_entry.get(), cat_entry.get(),))

	# 	# Create a database or connect to one that exists
	# 	conn = sqlite3.connect('database.db')

	# 	# Create a cursor instance
	# 	c = conn.cursor()

	# 	c.execute('''UPDATE bankStatement SET
	# 		date = :date,
	# 		description = :description,
	# 		amount = :amount,
	# 		category = :category

	# 		WHERE oid = :oid''',
	# 		{
	# 			'date' : dt_entry.get(),
	# 			'description' : des_entry.get(),
	# 			'amount' : amt_entry.get(),
	# 			'category' : cat_entry.get(),
	# 			'oid' : id_entry.get()
	# 		})

	# 	# Commit changes
	# 	conn.commit()

	# 	# Close our connection
	# 	conn.close()

	# 	# Clear entry boxes
	# 	id_entry.delete(0, END)
	# 	dt_entry.delete(0, END)
	# 	des_entry.delete(0, END)
	# 	amt_entry.delete(0, END)
	# 	cat_entry.delete(0, END)

	# # Remove one record
	# def remove_one():
	# 	x = my_tree.selection()[0]
	# 	my_tree.delete(x)

	# 	# Create a database or connect to one that exists
	# 	conn = sqlite3.connect('database.db')

	# 	# Create a cursor instance
	# 	c = conn.cursor()

	# 	c.execute("DELETE FROM bankStatement WHERE oid=" + id_entry.get())

	# 	# Commit changes
	# 	conn.commit()

	# 	# Close our connection
	# 	conn.close()

	# 	# Clear the entry boxes
	# 	clear_entries()

	# 	# Messagebox confirmation
	# 	messagebox.showinfo('Deleted!', 'Your Record Has Been Deleted')
		
	# # Remove all records
	# def remove_all():
	# 	# Messagebox Warning
	# 	messagebox.showwarning('Delete Detected', 'YOU ARE ABOUT TO DELETE ALL RECORDS')

	# 	response = messagebox.askyesno('Delete Detected', 'Are you sure you want to delete ALL RECORDS?')

	# 	# Logic for message box
	# 	if response == 1:
	# 		for record in my_tree.get_children():
	# 			my_tree.delete(record)

	# 		# Create a database or connect to one that exists
	# 		conn = sqlite3.connect('database.db')

	# 		# Create a cursor instance
	# 		c = conn.cursor()

	# 		c.execute("DROP TABLE bankStatement")

	# 		# Commit changes
	# 		conn.commit()

	# 		# Close our connection
	# 		conn.close()

	# 		# Clear the entry boxes
	# 		clear_entries()

	# 		# Add back table to database
	# 		init_database()

	# # Clear entry boxes
	# def clear_entries():
	# 	id_entry.delete(0, END)
	# 	dt_entry.delete(0, END)
	# 	des_entry.delete(0, END)
	# 	amt_entry.delete(0, END)
	# 	cat_entry.delete(0, END)

	# # Select Record
	# def select_record(e):
	# 	# Clear entry boxes
	# 	id_entry.config(state="normal")
	# 	id_entry.delete(0, END)
	# 	dt_entry.delete(0, END)
	# 	des_entry.delete(0, END)
	# 	amt_entry.delete(0, END)
	# 	cat_entry.delete(0, END)

	# 	# Grab record Number
	# 	selected = my_tree.focus()
	# 	# Grab record values
	# 	values = my_tree.item(selected, 'values')

	# 	# output to entry boxes
	# 	id_entry.insert(0, values[0])
	# 	id_entry.config(state="readonly")
	# 	dt_entry.insert(0, values[1])
	# 	des_entry.insert(0, values[2])
	# 	amt_entry.insert(0, values[3])
	# 	cat_entry.insert(0, values[4])

# Add Buttons
button_frame = LabelFrame(acc_rules, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20)

# update_button = Button(button_frame, text="Update Record", command=update_record)
# update_button.grid(row=0, column=0, padx=10, pady=10)

# add_button = Button(button_frame, text="Add Record", command=add_record)
# add_button.grid(row=0, column=1, padx=10, pady=10)

# remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
# remove_all_button.grid(row=0, column=2, padx=10, pady=10)

# remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
# remove_one_button.grid(row=0, column=3, padx=10, pady=10)

# remove_many_button = Button(button_frame, text="Remove Many Selected", state='disabled')
# remove_many_button.grid(row=0, column=4, padx=10, pady=10)

# move_up_button = Button(button_frame, text="Accounts")
# move_up_button.grid(row=0, column=5, padx=10, pady=10)

# # move_down_button = Button(button_frame, text="Move Down", state='disabled')
# # move_down_button.grid(row=0, column=6, padx=10, pady=10)

# move_down_button = Button(button_frame, text="Category", command=c.cat_managment)
# move_down_button.grid(row=0, column=6, padx=10, pady=10)

# clear_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
# clear_record_button.grid(row=0, column=7, padx=10, pady=10)

# # Bind the treeview
# my_tree.bind("<ButtonRelease-1>", select_record)








































acc_rules.mainloop()