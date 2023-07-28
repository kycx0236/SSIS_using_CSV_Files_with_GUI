import tkinter as tk
from tkinter import ttk
import csv
from tkinter import messagebox
from tkinter import colorchooser
import customtkinter as ctk

# Windows
root = ctk.CTk()
root.title("SSIS Version 1: CSV Database")
root.geometry("1366x768")
root.iconbitmap("GUI\icon.ico")
root.minsize(800, 600)
root.maxsize(1366, 768)
apperance = ctk.set_appearance_mode("light")
data_of_students = "student_list_CRUDL.csv"
data_of_courses = "courses.csv"


# Functions for Menu
def primary_color():
    primary_color = colorchooser.askcolor()[1]
    if primary_color:
        # Create Striped Row Tags
        treeview_students.tag_configure("evenrow", background=primary_color)
        treeview_courses.tag_configure("evenrow", background=primary_color)


def secondary_color():
    secondary_color = colorchooser.askcolor()[1]
    if secondary_color:
        # Create Striped Row Tags
        treeview_students.tag_configure("oddrow", background=secondary_color)
        treeview_courses.tag_configure("oddrow", background=secondary_color)


def highlight_color():
    highlight_color = colorchooser.askcolor()[1]
    if highlight_color:
        # Change Selected Color
        style.map("Treeview", background=[("selected", highlight_color)])


# Function for CSV database
def query_database_students():
    count = 0

    # Clear the Treeview
    data = treeview_students.get_children()
    for record in data:
        treeview_students.delete(record)

    # Open the CSV file and display the results
    with open(data_of_students, "r") as student_file:
        display_data = csv.reader(student_file)
        next(display_data)
        for data in display_data:
            if count % 2 == 0:
                treeview_students.insert(
                    parent="",
                    index=tk.END,
                    iid=count,
                    values=(
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                    ),
                    tags=("evenrow",),
                )
            else:
                treeview_students.insert(
                    parent="",
                    index=tk.END,
                    iid=count,
                    values=(
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                    ),
                    tags=("oddrow",),
                )
            count = count + 1


def query_database_courses():
    count = 0
    # Clear the Treeview
    data = treeview_courses.get_children()
    for record in data:
        treeview_courses.delete(record)

    # Open the CSV file and display the results
    with open(data_of_courses) as course_file:
        reader = csv.reader(course_file)
        next(reader)
        for data in reader:
            if count % 2 == 0:
                treeview_courses.insert(
                    parent="",
                    index=tk.END,
                    iid=count,
                    values=(
                        data[0],
                        data[1],
                    ),
                    tags=("evenrow",),
                )
            else:
                treeview_courses.insert(
                    parent="",
                    index=tk.END,
                    iid=count,
                    values=(
                        data[0],
                        data[1],
                    ),
                    tags=("oddrow",),
                )
            count = count + 1


def enrollee_checker(selected=None):
    global result
    result = 0
    for course in result:
        code, _, num = course
        if code == selected and num != 0:
            return False

    return True


# searching student data on the database and on the treeview
def search_id():
    lookup_records = search_entry.get()

    # Close the search box
    search.destroy()

    # Clear the TreeView
    treeview_students.delete(*treeview_students.get_children())

    found = False
    with open(data_of_students, "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if row[0] == lookup_records:
                messagebox.showinfo("Found", "ID Number found!")
                treeview_students.insert("", "end", values=row, tags="evenrow")
                found = True
    if not found:
        messagebox.showinfo("Not Found", "ID Number not found.")
        query_database_students()


def search_course():
    lookup_records = search_entry.get()

    # Close the search box
    search.destroy()

    # Clear the TreeView
    treeview_courses.delete(*treeview_courses.get_children())

    found = False
    with open(data_of_courses, "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if row[0] == lookup_records:
                messagebox.showinfo("Found", "Course_code found!")
                treeview_courses.insert("", "end", values=row, tags="evenrow")
                found = True

    if not found:
        messagebox.showinfo("Not Found", "Course_code not found.")
        query_database_courses()


def lookup_records():
    global search_entry, search

    search = tk.Toplevel(root)
    search.title("Search Records")
    search.geometry("400x200")

    # Create Label Frame
    search_frame = ttk.LabelFrame(search, text="ID Number")
    search_frame.pack(padx=10, pady=10)

    # Entry Box
    search_entry = ctk.CTkEntry(search_frame, font=("Helvetica", 18))
    search_entry.pack(padx=20, pady=20)

    # Search Button
    search_button = ttk.Button(search, text="Search", command=search_id)
    search_button.pack(padx=20, pady=20)


def lookup_records_for_courses():
    global search_entry, search

    search = tk.Toplevel(root)
    search.title("Search Courses")
    search.geometry("400x200")

    # Create Label Frame
    search_frame = ttk.LabelFrame(search, text="Course Code")
    search_frame.pack(padx=10, pady=10)

    # Entry Box
    search_entry = ttk.Entry(search_frame, font=("Helvetica", 18))
    search_entry.pack(padx=20, pady=20)

    # Search Button
    search_button = ttk.Button(search, text="Search", command=search_course)
    search_button.pack(padx=20, pady=20)


def exit_app():
    root.destroy()


# Add Menu
my_menu = tk.Menu(root)
root.config(menu=my_menu)

# Configure our menu
option_menu = tk.Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=option_menu)

# Drop down menu
option_menu.add_command(label="Primary Color", command=primary_color)
option_menu.add_command(label="Secondary Color", command=secondary_color)
option_menu.add_command(label="Highlight Color", command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=exit_app)

# Search Menu
search_menu = tk.Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Search", menu=search_menu)

# Drop down menu
search_menu.add_command(label="Search ID Number", command=lookup_records)
search_menu.add_command(label="Search Course Code", command=lookup_records_for_courses)

# Display Menu
display_menu = tk.Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Display", menu=display_menu)

#   Drop down menu
display_menu.add_command(label="Display Students", command=query_database_students)
display_menu.add_command(label="Display Courses", command=query_database_courses)

# Style
style = ttk.Style()

# Theme
style.theme_use("default")
# Configure the Treevieww Colors
style.configure(
    "Treeview",
    background="#D3D3D3",
    foreground="black",
    rowheight=25,
    fieldbackground="#D3D3D3",
)

# Change Selected Color
style.map("Treeview", background=[("selected", "#347083")])

# Create Treeview Frame
treeview_frame = ttk.Frame(root)
tree_frame_course = ttk.Frame(root)

treeview_frame.place(relx=0.1, rely=0, width=870)
tree_frame_course.place(relx=0.65, rely=0, width=450)

# Create Treeview Scrollbar
treeview_scrollbar = ttk.Scrollbar(treeview_frame)
treeview_scrollbar.pack(side="right", fill="y")

treeview_scrollbar_2 = ttk.Scrollbar(tree_frame_course)
treeview_scrollbar_2.pack(side="right", fill="y")


# Create the Treeview
treeview_students = ttk.Treeview(
    treeview_frame, yscrollcommand=treeview_scrollbar.set, selectmode="extended"
)
treeview_students.pack(side="left")

treeview_courses = ttk.Treeview(
    tree_frame_course, yscrollcommand=treeview_scrollbar_2.set, selectmode="extended"
)
treeview_courses.pack(side="left")

# Configure the Scrollbar
treeview_scrollbar.config(command=treeview_students.yview)
treeview_scrollbar_2.config(command=treeview_courses.yview)

# Define our columns
fieldnames = [
    "idnumber",
    "name",
    "course_code",
    "year_level",
    "gender",
    "address",
]
treeview_students["columns"] = fieldnames

fieldnames_courses = ["course_code", "course_name"]
treeview_courses["columns"] = fieldnames_courses

# Format our columns
treeview_students.column("#0", stretch="NO", width=0)
treeview_students.column("idnumber", anchor="w", width=100)
treeview_students.column("name", anchor="w", width=200)
treeview_students.column("course_code", anchor="w", width=80)
treeview_students.column("year_level", anchor="center", width=100)
treeview_students.column("gender", anchor="center", width=100)
treeview_students.column("address", anchor="w", width=310)

treeview_courses.column("#0", stretch="NO", width=0)
treeview_courses.column("course_code", anchor="w", width=100)
treeview_courses.column("course_name", anchor="w", width=350)

# Create Headings
treeview_students.heading("#0", text="", anchor="w")
treeview_students.heading("idnumber", text="ID Number", anchor="center")
treeview_students.heading("name", text="Full Name", anchor="center")
treeview_students.heading("course_code", text="Course Code", anchor="center")
treeview_students.heading("year_level", text="Year Level", anchor="center")
treeview_students.heading("gender", text="Gender", anchor="center")
treeview_students.heading("address", text="Address", anchor="center")

treeview_courses.heading("#0", text="", anchor="w")
treeview_courses.heading("course_code", text="Course Code", anchor="center")
treeview_courses.heading("course_name", text="Course Name", anchor="center")

# Create Striped Row Tags
treeview_students.tag_configure("oddrow", background="white")
treeview_students.tag_configure("evenrow", background="lightblue")

treeview_courses.tag_configure("oddrow", background="white")
treeview_courses.tag_configure("evenrow", background="#FFF9AD")

# Add Students Entry Boxes and Labels
data_frame = ttk.LabelFrame(root, text="Student Record")
data_frame.place(relx=0.1, rely=0.35, width=870)

idnumber_label = ttk.Label(data_frame, text="ID Number")
idnumber_label.grid(row=0, column=0, padx=10, pady=10)
idnumber_entry = ttk.Entry(data_frame)
idnumber_entry.grid(row=0, column=1, padx=10, pady=10)

name_label = ttk.Label(data_frame, text="Name")
name_label.grid(row=0, column=2, padx=10, pady=10)
name_entry = ttk.Entry(data_frame)
name_entry.grid(row=0, column=3, padx=10, pady=10)

course_code_label = ttk.Label(data_frame, text="Course Code")
course_code_label.grid(row=0, column=4, padx=10, pady=10)
course_code_entry = ttk.Entry(data_frame)
course_code_entry.grid(row=0, column=5, padx=10, pady=10)

year_level_label = ttk.Label(data_frame, text="Year Level")
year_level_label.grid(row=1, column=0, padx=10, pady=10)
year_level_entry = ttk.Entry(data_frame)
year_level_entry.grid(row=1, column=1, padx=10, pady=10)

gender_label = ttk.Label(data_frame, text="Gender")
gender_label.grid(row=1, column=2, padx=10, pady=10)
gender_entry = ttk.Entry(data_frame)
gender_entry.grid(row=1, column=3, padx=10, pady=10)

address_label = ttk.Label(data_frame, text="Address")
address_label.grid(row=1, column=4, padx=10, pady=10)
address_entry = ttk.Entry(data_frame)
address_entry.grid(row=1, column=5, padx=10, pady=10)

# Add Courses Entry Boxes and Labels
data_frame_courses = ttk.LabelFrame(root, text="Course Information")
data_frame_courses.place(relx=0.65, rely=0.35, width=450, relheight=0.15)

course_codes_label = ttk.Label(data_frame_courses, text="Course Code")
course_codes_label.grid(row=0, column=0, padx=10, pady=10)
course_codes_entry = ttk.Entry(data_frame_courses)
course_codes_entry.grid(row=0, column=1, padx=10, pady=10)

course_names_label = ttk.Label(data_frame_courses, text="Course Name")
course_names_label.grid(row=1, column=0, padx=10, pady=10)
course_names_entry = ttk.Entry(data_frame_courses)
course_names_entry.grid(row=1, column=1, padx=10, pady=10)


# Functions
# Move row up
def move_up():
    selected = treeview_students.selection()
    for row in selected:
        treeview_students.move(
            row, treeview_students.parent(row), treeview_students.index(row) - 1
        )


def move_up_for_courses():
    selected = treeview_courses.selection()
    for row in selected:
        treeview_courses.move(
            row, treeview_courses.parent(row), treeview_courses.index(row) - 1
        )


# Move row down
def move_down():
    selected = treeview_students.selection()
    for row in reversed(selected):
        treeview_students.move(
            row, treeview_students.parent(row), treeview_students.index(row) + 1
        )


def move_down_for_courses():
    selected = treeview_courses.selection()
    for row in reversed(selected):
        treeview_courses.move(
            row, treeview_courses.parent(row), treeview_courses.index(row) + 1
        )


# Select Record
def select_record(event):
    # Clear Entry Boxes
    idnumber_entry.delete(0, "end")
    name_entry.delete(0, "end")
    course_code_entry.delete(0, "end")
    year_level_entry.delete(0, "end")
    gender_entry.delete(0, "end")
    address_entry.delete(0, "end")

    # Grab record number
    selected = treeview_students.focus()
    # Grab record values
    values = treeview_students.item(selected, "values")

    # Output/Display to entry Boxes
    idnumber_entry.insert(0, values[0])
    name_entry.insert(0, values[1])
    course_code_entry.insert(0, values[2])
    year_level_entry.insert(0, values[3])
    gender_entry.insert(0, values[4])
    address_entry.insert(0, values[5])


def select_courses(event):
    # Clear Entry Boxes
    course_codes_entry.delete(0, "end")
    course_names_entry.delete(0, "end")

    # Grab record number
    selected_course = treeview_courses.focus()
    # Grab record values
    values = treeview_courses.item(selected_course, "values")

    # Output/Display to entry Boxes
    course_codes_entry.insert(0, values[0])
    course_names_entry.insert(0, values[1])


# Clear Entries
def clear_entries():
    idnumber_entry.delete(0, "end")
    name_entry.delete(0, "end")
    course_code_entry.delete(0, "end")
    year_level_entry.delete(0, "end")
    gender_entry.delete(0, "end")
    address_entry.delete(0, "end")


def clear_entries_for_course():
    course_codes_entry.delete(0, "end")
    course_names_entry.delete(0, "end")


# Check if there is a match regarding the course_codes in the CSV files
def check_courses_match(course_code_verifier=None):
    students_courses = set()
    courses = set()

    # Read the students.csv file and extract the enrolled courses
    with open(data_of_students, "r") as students_file:
        student_reader = csv.reader(students_file)
        next(student_reader)  # Skip the header row
        for row in student_reader:
            students_courses.add(row[2])  # Assuming the course column is at index 2
        print(students_courses)
    # Read the courses.csv file and build the course list
    with open(data_of_courses, "r") as courses_file:
        courses_reader = csv.reader(courses_file)
        next(courses_reader)  # Skip the header row
        for row in courses_reader:
            courses.add(row[0])  # Assuming the course code is at index 0
        print(courses)
        print(
            (
                course_code_verifier not in students_courses
                and course_code_verifier not in courses
            )
        )
    # Check if the course code does not exist in student courses and course list
    return (
        course_code_verifier not in students_courses
        or course_code_verifier not in courses
    )


# Remove a student info in the database
def remove_one_student():
    response = messagebox.askyesno(
        "WARNING!",
        "Are you sure you want to delete this data from the table?",
    )
    if response == 1:
        selected_student = treeview_students.selection()
        for data in selected_student:
            id_data = treeview_students.item(data, "values")[0]
        print(id_data)

        lines = list()
        with open(data_of_students, "r") as file:
            reader = csv.reader(file)
            for line in reader:
                lines.append(line)
                if line[0] in id_data:
                    lines.remove(line)
        with open(data_of_students, "w", newline="") as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)

        # Clear Entry Boxes
        clear_entries()

        # Clear the Treeview Table
        treeview_students.delete(*treeview_students.get_children())

        # Run the database again
        query_database_students()

        # Add a little message box for fun
        messagebox.showinfo("Deleted!", "Student Info Has Been Deleted!")


# Remove a course info in the database
def remove_one_course():
    response = messagebox.askyesno(
        "WARNING!",
        "Are you sure you want to delete this data from the table?",
    )
    if response == 1:
        selected_courses = treeview_courses.selection()
        for data in selected_courses:
            course_data = treeview_courses.item(data, "values")[0]
            print(course_data)

            if check_courses_match(course_data):
                print(check_courses_match(course_data))
                lines = list()
                with open(data_of_courses, "r") as file:
                    reader = csv.reader(file)
                    for line in reader:
                        if line[0] != course_data:
                            lines.append(line)

                with open(data_of_courses, "w", newline="") as writeFile:
                    writer = csv.writer(writeFile)
                    writer.writerows(lines)

                # Clear Entry Boxes
                clear_entries_for_course()

                # Clear the Treeview Table
                treeview_courses.delete(*treeview_courses.get_children())

                # Run the database again
                query_database_courses()

                # Add a little message box for fun
                messagebox.showinfo("Deleted!", "Course Info Has Been Deleted!")
            else:
                messagebox.showinfo(
                    "Notice!",
                    "We cannot delete the course as it has students enrolled in it.",
                )


# Verify that student_idnumber is unique or not
def unique_id_verifier(id_verifier=None):
    with open(data_of_students, "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if row[0] == id_verifier:
                return False
    return True


# Verify that course_code is unique or not
def unique_code_verifier(id_verifier=None):
    with open(data_of_courses, "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip the header row
        for row in csv_reader:
            if row[0] == id_verifier:
                return False
    return True


# Add widget
def add_course_widget():
    global course_code_widget_entry, course_name_widget_entry, course_widget_main_frame

    course_widget_main_frame = tk.Toplevel(root)
    course_widget_main_frame.title("Add Courses")
    course_widget_main_frame.geometry("500x300")

    # Create Label Frame
    course_widget_frame = ttk.LabelFrame(
        course_widget_main_frame, text="Course Entries"
    )
    course_widget_frame.place(relx=0.1, rely=0.1, width=400)
    # Entry Box and Label
    course_code_widget_label = ttk.Label(
        course_widget_frame,
        text="Course Code",
    )
    course_name_widget_label = ttk.Label(
        course_widget_frame,
        text="Course Name",
    )
    course_code_widget_entry = ttk.Entry(course_widget_frame, font=("Helvetica", 18))
    course_name_widget_entry = ttk.Entry(course_widget_frame, font=("Helvetica", 18))

    course_code_widget_label.grid(row=0, column=0, padx=10, pady=10, sticky="news")
    course_code_widget_entry.grid(row=0, column=1, padx=10, pady=10, sticky="news")
    course_name_widget_entry.grid(row=1, column=1, padx=10, pady=10, sticky="news")
    course_name_widget_label.grid(row=1, column=0, padx=10, pady=10, sticky="news")

    # Search Button
    add_button = ctk.CTkButton(
        course_widget_main_frame,
        text="Add",
        height=30,
        width=100,
        corner_radius=10,
        fg_color="#336082",
        font=("Montserrat Bold", 12),
        command=add_new_course_2,
    )
    add_button.place(relx=0.75, rely=0.6, relwidth=0.15)


# Add new student info
def add_new_student():
    # Checking id_number if unique or not
    checking_id = idnumber_entry.get()
    checking_course = course_code_entry.get()

    if unique_id_verifier(checking_id) and checking_id != "":
        if unique_code_verifier(checking_course):
            messagebox.showinfo(
                "Notice",
                "Please enter the details of the new course_code and course_name.",
            )
            add_course_widget()
        else:
            with open(data_of_students, "a", newline="") as add_course:
                writer = csv.DictWriter(
                    add_course, fieldnames=fieldnames, lineterminator="\n"
                )
                writer.writerow(
                    {
                        "idnumber": idnumber_entry.get(),
                        "name": name_entry.get(),
                        "course_code": course_code_entry.get(),
                        "year_level": year_level_entry.get(),
                        "gender": gender_entry.get(),
                        "address": address_entry.get(),
                    }
                )
            # Clear Entry Boxes
            clear_entries_for_course()
            # Clear the Treeview Table
            treeview_students.delete(*treeview_students.get_children())

            # Run the query_database again
            query_database_students()
            # Add a little message box for fun
            messagebox.showinfo("Added!", "Student Info has been added!")
    else:
        messagebox.showinfo("Notice!", "Please enter a unique ID number")


# Add new course info
def add_new_course():
    # Checking id_number if unique or not
    checking_id = course_codes_entry.get()

    if unique_code_verifier(checking_id) and checking_id != "":
        with open(data_of_courses, "a", newline="") as add_course:
            writer = csv.DictWriter(
                add_course, fieldnames=fieldnames_courses, lineterminator="\n"
            )
            writer.writerow(
                {
                    "course_code": course_codes_entry.get(),
                    "course_name": course_names_entry.get(),
                }
            )
        # Clear Entry Boxes
        clear_entries_for_course()
        # Clear the Treeview Table
        treeview_courses.delete(*treeview_courses.get_children())

        # Run the query_database again
        query_database_courses()
        # Add a little message box for fun
        messagebox.showinfo("Added!", "Course Info has been added!")
    else:
        messagebox.showinfo("Notice", "Pleate enter a unique course_code!")


def add_new_course_2():
    with open(data_of_courses, "a", newline="") as add_course:
        writer = csv.DictWriter(
            add_course, fieldnames=fieldnames_courses, lineterminator="\n"
        )
        writer.writerow(
            {
                "course_code": course_code_widget_entry.get(),
                "course_name": course_name_widget_entry.get(),
            }
        )
    # Clear the Treeview Table
    treeview_courses.delete(*treeview_courses.get_children())

    # Run the query_database again
    query_database_courses()
    # Add a little message box for fun
    messagebox.showinfo("Added!", "Course Info has been added!")


# Update Student Info
def update_student_info():
    count = 0
    # Contain the info in the list
    list_of_students = list()
    # Grab record numbers
    selected = treeview_students.focus()
    row_number = int(selected)

    print(row_number)
    selected_values = treeview_students.item(selected)["values"]
    id_number = selected_values[0]
    print(id_number)
    # Update Record
    treeview_students.item(
        selected,
        text="",
        values=(
            idnumber_entry.get(),
            name_entry.get(),
            course_code_entry.get(),
            year_level_entry.get(),
            gender_entry.get(),
            address_entry.get(),
        ),
    )
    with open(data_of_students, "r") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            list_of_students.append(row)
            for field in row:
                if field == id_number:
                    list_of_students.remove(row)
                    list_of_students.insert(
                        count,
                        [
                            idnumber_entry.get(),
                            name_entry.get(),
                            course_code_entry.get(),
                            year_level_entry.get(),
                            gender_entry.get(),
                            address_entry.get(),
                        ],
                    )
            count += 1
    with open(data_of_students, "w", newline="") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(list_of_students)

    # Clear Entries
    clear_entries()

    # Clear the Treeview Table
    treeview_students.delete(*treeview_students.get_children())

    # Run the query_database again
    query_database_students()

    # Add a little message box for fun
    messagebox.showinfo("Updated!", "Data has been updated!")


# Update course info
def update_course_info():
    count = 0
    # Contain the info in the list
    list_of_courses = list()
    # Grab record numbers
    selected = treeview_courses.focus()
    row_number = int(selected)

    print(row_number)
    selected_values = treeview_courses.item(selected)["values"]
    course_code_data = selected_values[0]
    print(course_code_data)
    # Update Record
    treeview_students.item(
        selected,
        text="",
        values=(
            idnumber_entry.get(),
            name_entry.get(),
            course_code_entry.get(),
            year_level_entry.get(),
            gender_entry.get(),
            address_entry.get(),
        ),
    )
    with open(data_of_courses, "r") as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            list_of_courses.append(row)
            for field in row:
                if field == course_code_data:
                    list_of_courses.remove(row)
                    list_of_courses.insert(
                        count,
                        [
                            course_codes_entry.get(),
                            course_names_entry.get(),
                        ],
                    )
            count += 1
    with open(data_of_courses, "w", newline="") as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(list_of_courses)

    # Clear Entries
    clear_entries_for_course()

    # Clear the Treeview Table
    treeview_courses.delete(*treeview_courses.get_children())

    # Run the query_database again
    query_database_courses()

    # Add a little message box for fun
    messagebox.showinfo("Updated!", "Data has been updated!")


# Buttons for Students
button_frame = ttk.LabelFrame(root, text="Commands")
button_frame.place(relx=0.1, rely=0.55, relwidth=0.5)

button_frame.columnconfigure((0, 1), weight=0, uniform="a")
button_frame.rowconfigure((0, 1), weight=0, uniform="a")

update_button = ttk.Button(
    button_frame, text="Update Student Info", command=update_student_info
)
update_button.grid(row=0, column=0, padx=10, pady=10, sticky="news")

add_button = ttk.Button(button_frame, text="Add Student Info", command=add_new_student)
add_button.grid(row=0, column=1, padx=10, pady=10, sticky="news")

remove_one_button = ttk.Button(
    button_frame,
    text="Remove One Selected",
    command=remove_one_student,
)
remove_one_button.grid(row=1, column=0, padx=10, pady=10, sticky="news")

move_up_button = ttk.Button(button_frame, text="Move Up", command=move_up)
move_up_button.grid(row=0, column=2, padx=10, pady=10, sticky="news")

move_down_button = ttk.Button(button_frame, text="Move Down", command=move_down)
move_down_button.grid(row=1, column=2, padx=10, pady=10, sticky="news")

clear_entries_button = ttk.Button(
    button_frame, text="Clear Entries", command=clear_entries
)
clear_entries_button.grid(row=1, column=1, padx=10, pady=10, sticky="news")


# Buttons for Courses
button_frame_course = ttk.LabelFrame(root, text="Commands")
button_frame_course.place(relx=0.65, rely=0.55, width=450)

button_frame_course.columnconfigure((0, 1), weight=0, uniform="a")
button_frame_course.rowconfigure((0, 1), weight=0, uniform="a")

update_button_course = ttk.Button(
    button_frame_course, text="Update Course Info", command=update_course_info
)
update_button_course.grid(row=0, column=0, padx=10, pady=10, sticky="news")

add_button_course = ttk.Button(
    button_frame_course, text="Add Course Info", command=add_new_course
)
add_button_course.grid(row=0, column=2, padx=10, pady=10, sticky="news")


remove_one_course_button = ttk.Button(
    button_frame_course, text="Remove One Selected", command=remove_one_course
)
remove_one_course_button.grid(row=1, column=0, padx=10, pady=10, sticky="news")

move_up_button_course_button = ttk.Button(
    button_frame_course, text="Move Up", command=move_up_for_courses
)
move_up_button_course_button.grid(row=0, column=1, padx=10, pady=10, sticky="news")

move_down_course_button = ttk.Button(
    button_frame_course, text="Move Down", command=move_down_for_courses
)
move_down_course_button.grid(row=1, column=1, padx=10, pady=10, sticky="news")

clear_entries_course_button = ttk.Button(
    button_frame_course, text="Clear Entries", command=clear_entries_for_course
)
clear_entries_course_button.grid(row=1, column=2, padx=10, pady=10, sticky="news")


# Bind Treeview
treeview_students.bind("<ButtonRelease-1>", select_record)
treeview_courses.bind("<ButtonRelease-1>", select_courses)
# Run to pull data from the database on start
query_database_students()
query_database_courses()
root.bind("<Escape>", lambda event: root.quit())

# Runner
root.mainloop()
