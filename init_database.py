import os
import sqlite3


# START UP PROCEDURE
# Create Database
def init_database(reinit=None):
	file = 'database.db'

	if not os.path.exists(file) or reinit == 'reinit':
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

		# Create options table
		c.execute("CREATE TABLE IF NOT EXISTS options (id INTEGER, date INTEGER, amount INTEGER, description INTEGER)")
		if reinit != 'reinit':
			c.execute("INSERT INTO options VALUES (:id, :date, :amount, :description)",{
					'id' : 0,
					'date' : 0,
					'amount': 0,
					'description' : 0
				})
		
		# Create Category Table and Insert Default Data
		c.execute("CREATE TABLE IF NOT EXISTS category (category TEXT, budget TEXT)")
		
		c.execute("SELECT * FROM category")
		records = c.fetchall()

		if len(records) == 0:
			category_list = ['Income', 'Entertainment Expense', 'Rates and Taxes', 'Fuel', 'Delete']
			for cat in category_list:
					c.execute("INSERT INTO category VALUES (:category, :budget)", {'category' : cat, 'budget': 'None'})

		# Create Rules Table
		c.execute("CREATE TABLE IF NOT EXISTS categoryRules (ruleName TEXT, appliedTo TEXT, category TEXT)")

		# Create CSV or OFX Table
		c.execute("CREATE TABLE IF NOT EXISTS ofxCsv (id INTEGER, selected INTEGER)")
		if reinit != 'reinit':
			c.execute("INSERT INTO ofxCsv VALUES (:id, :selected)", {'id': 0, 'selected' : 0})

		con.commit()
		con.close()