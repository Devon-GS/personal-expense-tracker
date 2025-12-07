import sqlite3
import datetime
from ofxtools.Parser import OFXTree
import pandas as pd
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import messagebox
from category_rules import auto_apply_rules


def add_bank_statement(account_name):
	# Get Data
	con = sqlite3.connect('database.db')
	c = con.cursor()

	# Get current records from bank Statements in database
	c.execute(f"SELECT * FROM {account_name}")
	b_records = c.fetchall()

	# Convert current transactions to list
	curr_trans = []
	for x in b_records:
		curr_trans.append([x[0], x[1], x[2]])

	# Get CSV or OFX options
	c.execute("SELECT selected FROM ofxCsv")
	records = c.fetchall() 

	select = records[0][0]

	try:
		if select == 1:
			# Get records from options
			c.execute("SELECT * FROM options")
			o_records = c.fetchall()

			for x in o_records:
				date = x[1]
				amount = x[2]
				description = x[3]

			# Get new transactions
			file = askopenfile(title='Select CSV Bank Statement', initialdir='/', filetypes=(('*', '.csv'),))

			df = pd.read_csv(file)
			df_filter = df.iloc[:, [date, description, amount]].values.tolist()

			# Convert new transactions to list
			new_trans = []
			for x in df_filter:
				new_trans.append([str(x[0]), " ".join(str(x[1]).split()), str("{:.2f}".format(x[2]))])

			# Query to insert new tranactions 
			query = f"INSERT INTO {account_name} VALUES (?, ?, ?, ?)"
				
			# Filter out duplicate transactions and add to database:
			for x in new_trans:
				if x not in curr_trans:
					if x[1] != 'OPEN BALANCE' and x[1] != 'CLOSE BALANCE':
						c.execute(query, (x[0], x[1], x[2], 'Please Select'))

			messagebox.showinfo('Added Bank Statement', 'Bank Statement Added Successfully')
		else:
			ofx = OFXTree()

			file = askopenfilename(title='Select OFX Bank Statement', initialdir='/', filetypes=(('*', '.ofx'),))	

			# Parse file
			ofx.parse(file)

			# Create object
			ofx_obj = ofx.convert()

			# # Get statement and tranactions
			statement = ofx_obj.statements

			transactions = statement[0].transactions

			# Convert transactions to list
			new_trans = []
			for x in transactions:
				date = x.dtposted.strftime("%Y-%m-%d").replace('-','')
				description = x.memo[:30]
				amount = x.trnamt

				new_trans.append([str(date), " ".join(str(description).split()), str("{:.2f}".format(amount))])

			query = f"INSERT INTO {account_name} VALUES (?, ?, ?, ?)"

			# Filter out duplicate transactions and add to database:
			for x in new_trans:
				if x not in curr_trans:
					c.execute(query, (x[0], x[1], x[2], 'Please Select'))

			messagebox.showinfo('Added Bank Statement', 'Bank Statement Added Successfully')

		con.commit()
		con.close()

		# Apply Rules
		# auto_apply_rules()
		
	except IndexError:
		messagebox.showerror('ERROR', 'Please Check That The Right Cloumns Are Selected In Options Menu')

	except FileNotFoundError:
		messagebox.showinfo('No File Selected', 'No Bank Statements Imported')