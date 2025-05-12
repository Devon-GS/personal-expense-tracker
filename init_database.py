import os
import sqlite3


# START UP PROCEDURE
# Create Database
def init_database():
	file = 'database.db'

	if os.path.exists(file):
		pass
	else:
		# Connect to database    
		con = sqlite3.connect('database.db')
		c = con.cursor()

		# Create Bank Statement Table
		c.execute(''' CREATE TABLE IF NOT EXISTS bankStatement (
						date TEXT,
						description TEXT,
						amount TEXT,
						category TEXT
					)
				''')

		# Create Income Table 
		c.execute(''' CREATE TABLE IF NOT EXISTS income (
						date TEXT,
						description TEXT,
						amount TEXT
					)
				''')

		# Create options table
		# c.execute("DROP TABLE options")
		c.execute("CREATE TABLE IF NOT EXISTS options (id INTEGER, date INTEGER, amount INTEGER, description INTEGER)")
		c.execute("INSERT INTO options VALUES (:id, :date, :amount, :description)",{
					'id' : 0,
					'date' : 0,
					'amount': 0,
					'description' : 0
				})
		
		# Create Category Table and Insert Default Data
		c.execute("CREATE TABLE IF NOT EXISTS category (category TEXT)")
		
		c.execute("SELECT * FROM category")
		records = c.fetchall()

		if len(records) == 0:
			category_list = ['Income', 'Entertainment Expense', 'Rates and Taxes', 'Fuel']
			for cat in category_list:
					c.execute("INSERT INTO category VALUES (:category)", {'category' : cat})

		con.commit()