import os
import sqlite3
from tkinter import *
from tkinter import messagebox
import init_database as indata
import category as cat
import bank_import as bi
import bank_statement as bs
import accounts as acc
import category_rules as cr


# SETUP DATABASE
indata.init_database()

# SORT RULES
cr.auto_apply_rules()

# PROGRAM
root = Tk()
root.title('Income and Expense Tracker')
root.geometry('400x400')

menubar = Menu(root)
root.config(menu=menubar)

# Create menu options
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Category', command=cat.cat_managment)
file_menu.add_command(label='Category Rules', command=cr.category_rules)
file_menu.add_command(label='Import Bank Statements', command=bi.add_bank_statement)
file_menu.add_command(label='Bank Statements', command=bs.bank_statments)
file_menu.add_command(label='Account Totals', command=acc.accounts_total)
# file_menu.add_command(label='Accounts', command=hh)

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

# PROGRAM
# OFX Frame
def selected():
    con = sqlite3.connect('database.db')
    c = con.cursor()

    query = "UPDATE ofxCsv SET selected = ? WHERE id = ?"

    c.execute(query, (int(str(var.get())), 0))  

    con.commit()
    con.close()

# Buttons
ofx_frame = LabelFrame(root, text="OFX or CSV")
ofx_frame.pack(fill="x", padx=20)

choose_label = Label(ofx_frame, text="Date")
choose_label.grid(row=1, column=0, padx=10, pady=10, sticky=E)

var = IntVar()
choose_csv = Radiobutton(ofx_frame, text="CSV", variable=var, value=1, command=selected)
choose_csv.grid(row=1, column=0, padx=10, pady=10, sticky=E)
choose_ofx = Radiobutton(ofx_frame, text="OFX", variable=var, value=2, command=selected)
choose_ofx.grid(row=1, column=2, padx=10, pady=10, sticky=E)

# Dispaly current settings in entrys
def dispaly_choice(): 
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

# CSV Frame
bs_frame = LabelFrame(root, text="CSV Bank Statement Setup")
bs_frame.pack(fill="x", padx=20)

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

# Run setup functions
display_entry()
dispaly_choice()

root.mainloop()