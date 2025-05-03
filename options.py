import sqlite3
from tkinter import *
from tkinter import messagebox


root= Tk()
root.title('')
root.geometry('400x400')

menubar = Menu(root)
root.config(menu=menubar)

# Functions
def hh():
    pass

# Create menu options
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Catagory', command=hh)
file_menu.add_command(label='Bank Statments', command=hh)

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
# Explain Setup
id_label = Label(root, text="Please State which colum the following is in using 'A, B, C, ETC'")
id_label.grid(columnspan=2 , padx=10, pady=10)

# Inputs
date_label = Label(root, text="Date")
date_label.grid(row=1, column=0, padx=10, pady=10)
date_entry = Entry(root)
date_entry.grid(row=1, column=1, padx=10, pady=10)

amount_label = Label(root, text="Amount")
amount_label.grid(row=2, column=0, padx=10, pady=10)
amount_entry = Entry(root)
amount_entry.grid(row=2, column=1, padx=10, pady=10)

description_label = Label(root, text="Description")
description_label.grid(row=3, column=0, padx=10, pady=10)
description_entry = Entry(root)
description_entry.grid(row=3, column=1, padx=10, pady=10)

# Functions
# Dispaly current settings in entrys
def update_entry(): 
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
            update_entry()

            messagebox.showinfo('SAVED', 'Coulmns Have Been Saved Successfully!')

        except KeyError:
            messagebox.showerror('ERROR!', 'Only Single Letters Can Be Used, Please Try Again!')
    else:
        messagebox.showinfo('SAVE', 'Nothing Happened')        

# Buttons
save_button = Button(root, text="Save", command=get_csv_options)
save_button.grid(row=4, column=0, padx=10, pady=10)

# Run setup functions
update_entry()

root.mainloop()