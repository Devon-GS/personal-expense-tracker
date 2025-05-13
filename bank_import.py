import sqlite3
import pandas as pd
from tkinter.filedialog import askopenfile
from tkinter import messagebox
from category_rules import auto_apply_rules

def add_bank_statement():
	try:
		# Get Data
		con = sqlite3.connect('database.db')
		c = con.cursor()

		# Get records from options
		c.execute("SELECT * FROM options")
		o_records = c.fetchall()

		for x in o_records:
			date = x[1]
			amount = x[2]
			description = x[3]

		# Get records from bank Statements
		c.execute("SELECT * FROM bankStatement")
		b_records = c.fetchall()

		# Convert current transactions to list
		curr_trans = []
		for x in b_records:
			curr_trans.append([x[0], x[1], x[2]])

		# Get new transactions
		file = askopenfile(title='Select CSV Bank Statement', initialdir='/', filetypes=(('*', '.csv'),))

		df = pd.read_csv(file)
		df_filter = df.iloc[:, [date, description, amount]].values.tolist()

		# Convert new transactions to list
		new_trans = []
		for x in df_filter:
			new_trans.append([str(x[0]), str(x[1]), str(x[2])])
			
		# Query to insert new tranactions 
		query = "INSERT INTO banKStatement VALUES (?, ?, ?, ?)"
			
		# Filter out unwanted transactions:
		for x in new_trans:
			if x not in curr_trans:
				if x[1] != 'OPEN BALANCE' and x[1] != 'CLOSE BALANCE':
					c.execute(query, (x[0], x[1], x[2], 'Please Select'))

		con.commit()
		con.close()
		
		auto_apply_rules()

		messagebox.showinfo('Added Bank Statement', 'Bank Statement Added Successfully')
	except IndexError:
		messagebox.showerror('ERROR', 'Please Check That The Right Cloumns Are Selected In Options Menu')