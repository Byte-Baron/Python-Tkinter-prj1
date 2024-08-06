from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Class")
root.geometry("230x300")
root.resizable(False, False)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------#
#Add

def Add_student():
    student_profile = Toplevel(root)
    student_profile.title("Add Student")
    student_profile.geometry("200x230")
    student_profile.resizable(False, False)
    
    Label(student_profile, text="Student Name :").pack()
    name = Entry(student_profile)
    name.pack()
    
    Label(student_profile, text="Chemistry Grade :").pack()
    chemistry_grade = Entry(student_profile)
    chemistry_grade.pack()
    
    Label(student_profile, text="Math Grade :").pack()
    math_grade = Entry(student_profile)
    math_grade.pack()
    
    Label(student_profile, text="Physics Grade :").pack()
    physics_grade = Entry(student_profile)
    physics_grade.pack()
    
    def save_student():
        chemistry_grade_val = float(chemistry_grade.get())
        math_grade_val = float(math_grade.get())
        physics_grade_val = float(physics_grade.get())
        
        student_data = {
            "name": name.get(),
            "chemistry_grade": chemistry_grade_val,
            "math_grade": math_grade_val,
            "physics_grade": physics_grade_val,
        }
        
        avg_grade = (chemistry_grade_val + math_grade_val + physics_grade_val) / 3
        student_data["avg_grade"] = round(avg_grade, 2)
        
        with open("students.txt", "a") as file:
            file.write(str(student_data) + "\n")
            
        chemistry_grade.delete(0, 'end')
        math_grade.delete(0, 'end')
        physics_grade.delete(0, 'end')
        name.delete(0, 'end')
        
    Button(student_profile, text="Add", command=save_student).pack(pady=7)
    Button(student_profile, text="Exit", command=student_profile.destroy).pack()

#Delete
    
def Delete_student():
    delete_student_page = Toplevel(root)
    delete_student_page.title("Delete Student")
    delete_student_page.geometry("170x180")
    delete_student_page.resizable(False, False)

    try:
        with open("students.txt", "r") as file:
            students = [student.strip() for student in file.readlines()]
            students = [eval(student) for student in students]

        listbox = Listbox(delete_student_page, width=15)
        for student in students:
            listbox.insert("end", student["name"])
        listbox.place(x=10,y=10)

        def delete_selected():
            selected_index = listbox.curselection()[0]
            selected_student = students[selected_index]
            del students[selected_index]

            with open("students.txt", "w") as file:
                for student in students:
                    file.write(str(student) + "\n")

            listbox.delete(0, "end")
            for student in students:
                listbox.insert("end", student["name"])

        Button(delete_student_page, text="Delete", command=delete_selected).place(x=120,y=40)
        Button(delete_student_page, text="Exit", command=delete_student_page.destroy).place(x=127,y=80)

    except FileNotFoundError:
        messagebox.showerror("Error", "No students have been added.")

#Search

def Search_student():
    search_window = Toplevel(root)
    search_window.title("Search")
    search_window.geometry("350x700")
    search_window.resizable(False, False)

    options = ["Name", "Chemistry Grade", "Math Grade", "Physics Grade", "Average Grade"]
    selected_field = StringVar()
    selected_field.set(options[0])

    Label(search_window, text="Search by :").pack()
    field_menu = OptionMenu(search_window, selected_field, *options)
    field_menu.pack()

    Label(search_window, text="Query:").pack()
    query_entry = Entry(search_window)
    query_entry.pack()

    def search_students():
        query = query_entry.get()
        try:
            with open("students.txt", "r") as file:
                students = [eval(line) for line in file.readlines()]
                filtered_students = []
                if selected_field.get() == "Name":
                    for student in students:
                        if student["name"].lower().startswith(query.lower()):
                            filtered_students.append(student)
                elif selected_field.get() == "Chemistry Grade":
                    for student in students:
                        if str(student["chemistry_grade"]).lower().startswith(query.lower()):
                            filtered_students.append(student)
                elif selected_field.get() == "Math Grade":
                    for student in students:
                        if str(student["math_grade"]).lower().startswith(query.lower()):
                            filtered_students.append(student)
                elif selected_field.get() == "Physics Grade":
                    for student in students:
                        if str(student["physics_grade"]).lower().startswith(query.lower()):
                            filtered_students.append(student)
                elif selected_field.get() == "Average Grade":
                    for student in students:
                        if str(student["avg_grade"]).lower().startswith(query.lower()):
                            filtered_students.append(student)

                if filtered_students:
                    result_label = Label(search_window, text="Search Results:")
                    result_label.pack()

                    for student in filtered_students:
                        result_text = ""
                        result_text += f"Name: {student['name']}\n"
                        result_text += f"Chemistry Grade: {student['chemistry_grade']}\n"
                        result_text += f"Math Grade: {student['math_grade']}\n"
                        result_text += f"Physics Grade: {student['physics_grade']}\n"
                        result_text += f"Average Grade: {student['avg_grade']}\n\n"
                        result_label = Label(search_window, text=result_text)
                        result_label.pack()
                else:
                    messagebox.showerror("Error", "No students found matching the query.")
        except FileNotFoundError:
            messagebox.showerror("Error", "No students have been added.")

   
    Button(search_window, text="Search", command=search_students).pack(pady = 5)
    Button(search_window, text="Exit", command=search_window.destroy).pack(pady = 5)
    
#Edit

def Edit_student():
    edit_window = Toplevel(root)
    edit_window.title("Edit Student")
    edit_window.geometry("500x185")
    edit_window.resizable(False, False)
    listbox = Listbox(edit_window, width=15)
    listbox.place(x=10,y=10)

    try:
        with open("students.txt", "r") as file:
            students = [eval(line.strip()) for line in file.readlines()]
            for student in students:
                listbox.insert(END, student["name"])  # Add only the names to the listbox
    except FileNotFoundError:
        messagebox.showerror("Error", "No students have been added.")
        return

    # Entry fields for editing
    Label(edit_window, text="Edit Student Details").place(x=180,y=5)
    Label(edit_window, text="Name : ").place(x=150,y=35)
    name_entry = Entry(edit_window)
    name_entry.place(x=200,y=38)
    Label(edit_window, text="Chemistry Grade : ").place(x=150,y=65)
    chemistry_entry = Entry(edit_window)
    chemistry_entry.place(x=255,y=68)
    Label(edit_window, text="Math Grade : ").place(x=150,y=95)
    math_entry = Entry(edit_window)
    math_entry.place(x=230,y=98)
    Label(edit_window, text="Physics Grade : ").place(x=150,y=125)
    physics_entry = Entry(edit_window)
    physics_entry.place(x=240,y=128)

    # Load student details into the entry fields
    def load_student_details():
        selected_index = listbox.curselection()
        if selected_index:
            student = students[selected_index[0]]
            name_entry.delete(0, END)
            name_entry.insert(0, student["name"])
            chemistry_entry.delete(0, END)
            chemistry_entry.insert(0, student["chemistry_grade"])
            math_entry.delete(0, END)
            math_entry.insert(0, student["math_grade"])
            physics_entry.delete(0, END)
            physics_entry.insert(0, student["physics_grade"])
            saved_message.config(text="")  # Clear saved message
        else:
            messagebox.showwarning("Select Student", "Please select a student to edit.")

    Button(edit_window, text="Load Details", command=load_student_details).place(x=400,y=40)

    # Save changes and recalculate average
    def save_changes():
        selected_index = listbox.curselection()
        if selected_index:
            updated_name = name_entry.get()
            try:
                updated_chemistry = float(chemistry_entry.get())
                updated_math = float(math_entry.get())
                updated_physics = float(physics_entry.get())

                # Recalculate the average grade
                average_grade = round((updated_chemistry + updated_math + updated_physics) / 3, 2)

                # Update the student details
                students[selected_index[0]] = {
                    "name": updated_name,
                    "chemistry_grade": updated_chemistry,
                    "math_grade": updated_math,
                    "physics_grade": updated_physics,
                    "avg_grade": average_grade
                }

                # Write changes back to the file
                with open("students.txt", "w") as file:
                    for student in students:
                        file.write(str(student) + "\n")

                saved_message.config(text="Changes Saved")  # Show saved message
                name_entry.delete(0, END)  # Clear the entry fields
                chemistry_entry.delete(0, END)
                math_entry.delete(0, END)
                physics_entry.delete(0, END)
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers for grades.")
        else:
            messagebox.showwarning("Select Student", "Please select a student to edit.")

    # Label for showing changes saved message
    saved_message = Label(edit_window, text="", fg="green")
    saved_message.place(x=400,y=100)
    
    Button(edit_window, text="Save", command=save_changes).place(x=400,y=70)
    Button(edit_window, text="Exit", command=edit_window.destroy).place(x=445,y=70)

    
#Sort
    
def Sort_students():
    sort_window = Toplevel(root)
    sort_window.title("Sort Students")
    sort_window.geometry("450x350")
    sort_window.resizable(False, False)
    sort_selection = StringVar(value="name")  # Default to name sort

    
    Label(sort_window, text="Sort by:").place(x=100,y=60)
    Radiobutton(sort_window, text="Alphabetical (A-Z)", variable=sort_selection, value="name").place(x=150,y=0)
    Radiobutton(sort_window, text="Average Grade", variable=sort_selection, value="avg").place(x=150,y=30)
    Radiobutton(sort_window, text="Chemistry Grade", variable=sort_selection, value="chemistry").place(x=150,y=60)
    Radiobutton(sort_window, text="Math Grade", variable=sort_selection, value="math").place(x=150,y=90)
    Radiobutton(sort_window, text="Physics Grade", variable=sort_selection, value="physics").place(x=150,y=120)
    
    listbox = Listbox(sort_window, width=70)
    listbox.place(x=10,y=150)

    def sort_students():
        listbox.delete(0, END)
        
        try:
            with open("students.txt", "r") as file:
                students = [eval(line.strip()) for line in file.readlines()]
                
                if sort_selection.get() == "name":
                    students.sort(key=lambda x: x["name"])
                elif sort_selection.get() == "avg":
                    students.sort(key=lambda x: x["avg_grade"], reverse=True)
                elif sort_selection.get() == "chemistry":
                    students.sort(key=lambda x: x["chemistry_grade"], reverse=True)
                elif sort_selection.get() == "math":
                    students.sort(key=lambda x: x["math_grade"], reverse=True)
                elif sort_selection.get() == "physics":
                    students.sort(key=lambda x: x["physics_grade"], reverse=True)

                for student in students:
                    listbox.insert(END, f"{student['name']} - Avg Grade: {student['avg_grade']:.2f}, "
                                         f"Chemistry: {student['chemistry_grade']:.2f}, "
                                         f"Math: {student['math_grade']:.2f}, "
                                         f"Physics: {student['physics_grade']:.2f}")

        except FileNotFoundError:
            messagebox.showerror("Error", "No students have been added.")

    Button(sort_window, text="Sort", command=sort_students).place(x=300,y=35)
    Button(sort_window, text="Exit", command=sort_window.destroy).place(x=300,y=65)


#Top STD
    
def Top_student():
    try:
        with open("students.txt", "r") as file:
            students = [student.strip() for student in file.readlines()]
            students = [eval(student) for student in students]
            
            students.sort(key=lambda x: x["avg_grade"], reverse=True)
            Avg = round(students[0]["avg_grade"],2)
            
            if students:
                top_student_page = Toplevel(root)
                top_student_page.title("Top Student")
                top_student_page.geometry("200x150")
                top_student_page.resizable(False, False)
                                
                Label(top_student_page, text="Top Student is : " + students[0]["name"]).pack()
                Label(top_student_page, text="Chemistry grade: " + str(students[0]["chemistry_grade"])).pack()
                Label(top_student_page, text="Math grade: " + str(students[0]["math_grade"])).pack()
                Label(top_student_page, text="Physics grade: " + str(students[0]["physics_grade"])).pack()
                Label(top_student_page, text="Average grade: " + str(Avg)).pack()
                
            else:
                messagebox.showerror("Error", "No students have been added.")
            
            
            
    except FileNotFoundError:
        messagebox.showerror("Error", "No students have been added.")

    Button(top_student_page , text="return", command=top_student_page.destroy).pack(pady=5)
    top_student_page.mainloop()
#Show

def show_students():
    show_window = Toplevel(root)
    show_window.title("Show Students")
    show_window.geometry("500x800")
    show_window.resizable(False, False)

    try:
        with open("students.txt", "r") as file:
            students = [eval(line) for line in file.readlines()]
            if students:
                table = Frame(show_window)
                table.pack()
                for student in students:
                    Label(table, text=student["name"], font=('Helvetica', 12)).pack()
                    Label(table, text="Chemistry Grade: " + str(student["chemistry_grade"]), font=('Helvetica', 12)).pack()
                    Label(table, text="Math Grade: " + str(student["math_grade"]), font=('Helvetica', 12)).pack()
                    Label(table, text="Physics Grade: " + str(student["physics_grade"]), font=('Helvetica', 12)).pack()
                    Label(table, text="Average Grade: " + str(student["avg_grade"]), font=('Helvetica', 12)).pack()
                    Label(table, text="", font=('Helvetica', 12)).pack()  # empty line for separation
            else:
                messagebox.showerror("Error", "No students have been added.")
                
    except FileNotFoundError:
        messagebox.showerror("Error", "No students have been added.")

    Button(show_window, text="return", command=show_window.destroy).place(x=220,y=760)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------#

Button(root, text="Add", width=9, height=2,command=Add_student).place(x = 20 , y= 20)
Button(root, text="Delete", width=9, height=2,command=Delete_student).place(x = 120 , y= 20)
Button(root, text="Search", width=9, height=2,command=Search_student).place(x = 20 , y= 80)
Button(root, text="Edit", width=9, height=2,command=Edit_student).place(x = 120 , y= 80)
Button(root, text="Sort", width=9, height=2,command=Sort_students).place(x = 20 , y= 140)
Button(root, text="Top STD", width=9, height=2,command=Top_student).place(x = 120 , y= 140)
Button(root, text="Show", width=9, height=5,fg='green',command=show_students).place(x = 20 , y= 200)
Button(root, text="Exit", width=9, height=5,fg='red',command=root.destroy).place(x = 120 , y= 200)


root.mainloop()
