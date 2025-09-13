import mysql.connector
import tkinter as tk
from tkinter import messagebox

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "YOUR_PASSWORD_HERE"
DB_NAME = "YOUR_DATABASE_HERE"

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS inputs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input1 VARCHAR(255),
    input2 VARCHAR(255),
    input3 VARCHAR(255),
    input4 VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

app = tk.Tk()
app.title("Personal Database")
app.geometry("800x400")
app.configure(bg="white")

entries = []

def save_row():
    values = [e.get() for e in entries]
    cursor.execute("""
        INSERT INTO inputs (input1, input2, input3, input4)
        VALUES (%s, %s, %s, %s)
    """, values)
    conn.commit()
    messagebox.showinfo("Saved", "Row saved successfully!")
    for e in entries:
        e.delete(0, tk.END)
    load_rows()

def delete_row(row_id):
    cursor.execute("DELETE FROM inputs WHERE id=%s", (row_id,))
    conn.commit()
    load_rows()

def update_cell(row_id, column, entry_widget):
    new_value = entry_widget.get()
    cursor.execute(f"UPDATE inputs SET {column}=%s WHERE id=%s", (new_value, row_id))
    conn.commit()
    load_rows()

def load_rows():
    for widget in app.grid_slaves():
        if int(widget.grid_info()["row"]) > 1:
            widget.destroy()

    cursor.execute("SELECT id, input1, input2, input3, input4, created_at FROM inputs ORDER BY id")
    rows = cursor.fetchall()
    
    for i, row in enumerate(rows, start=2):
        row_id = row[0]
        for j, value in enumerate(row[1:5]):
            entry = tk.Entry(app, width=15, relief="solid", bd=1, justify="center")
            entry.insert(0, value if value else "")
            entry.grid(row=i, column=j, padx=1, pady=1)
            entry.bind("<FocusOut>", lambda e, rid=row_id, col=f"input{j+1}", ent=entry: update_cell(rid, col, ent))
        tk.Button(app, text="Delete", command=lambda rid=row_id: delete_row(rid), bg="red", fg="white").grid(row=i, column=5, padx=2)

for idx, col_name in enumerate(["Input 1", "Input 2", "Input 3", "Input 4"]):
    tk.Label(app, text=col_name, bg="lightgray", relief="solid", bd=1, width=15).grid(row=0, column=idx, padx=1, pady=1)

for i in range(4):
    e = tk.Entry(app, width=15, relief="solid", bd=1)
    e.grid(row=1, column=i, padx=1, pady=1)
    entries.append(e)

tk.Button(app, text="Save Row", command=save_row, bg="lightgreen").grid(row=1, column=4, padx=5)

load_rows()
app.mainloop()

cursor.close()
conn.close()

