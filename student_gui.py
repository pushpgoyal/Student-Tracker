import mysql.connector
import tkinter as tk
from tkinter import messagebox

def connect_db():
    return mysql.connector.connect(
        host = "localhost",
        user = "username", #Your username
        password = "********", #Your database password
        database = "STUDENTS"
    )
def add_student():
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO STUDENT (NAME, AGE, COURSE, MARKS) VALUES(%s, %s, %s, %s)"
    values = (name_var.get(), age_var.get(), course_var.get(), marks_var.get())
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    clear_inputs()
    view_students()
    messagebox.showinfo("Success", "Student added successfully!")


def view_students():
    listbox.delete(0, tk.END)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM STUDENT")

    for row in cursor.fetchall():
        student_text = "ROLLNO: " + str(row[0]) + " | NAME: " + row[1] + " | AGE: " + str(row[2]) + " | COURSE: " + row[3] + " | MARKS: " + str(row[4])
        listbox.insert("end", student_text)
    
    cursor.close()
    conn.close()

def delete_student():
    selected = listbox.curselection()
    if selected:
        student_info = listbox.get(selected[0])
        student_id = int(student_info.split('|')[0].split(':')[1].strip())
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM STUDENT WHERE ROLLNO = %s", (student_id,))
        conn.commit()
        cursor.close()
        conn.close()
        view_students()
        messagebox.showinfo("Deleted", "Student record deleted")    
    else:
        messagebox.showinfo("Select Record", "Please select a student to delete")    


def clear_inputs():
    name_var.set("")
    age_var.set("")
    course_var.set("")
    marks_var.set("")


# --- GUI Setup ---
app = tk.Tk()
app.title("Student Tracker")
app.geometry("500x500")

name_var = tk.StringVar()
age_var = tk.StringVar()
course_var = tk.StringVar()
marks_var = tk.StringVar()

tk.Label(app, text="Name").pack()
tk.Entry(app, textvariable=name_var).pack()

tk.Label(app, text="Age").pack()
tk.Entry(app, textvariable=age_var).pack()

tk.Label(app, text="Course").pack()
tk.Entry(app, textvariable=course_var).pack()

tk.Label(app, text="Marks").pack()
tk.Entry(app, textvariable=marks_var).pack()

tk.Button(app, text="Add Student", command=add_student).pack(pady=10)
tk.Button(app, text="View Students", command=view_students).pack()
tk.Button(app, text="Delete Selected", command=delete_student).pack(pady=10)

listbox = tk.Listbox(app, width=60)
listbox.pack(pady=20)

view_students()

app.mainloop()
