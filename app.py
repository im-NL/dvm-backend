import userlogin
import json 
from setup import Course, Section, TimeTable, populate_courses, db

user = userlogin.login()
ADMIN = user[1]["admin"]
users = user[2]
user = user[0]

if "timetable" in users[user].keys():
    timetable = TimeTable(**users[user]["timetable"])
else:
    timetable = TimeTable()

course = Course(code="BITS F111", description="Thermodynamics raddi course")
section = Section(course, "P9", {"Tuesday": [6, 7]})

def help():
    print("""
    List of all functions:\n
    -> h - prints the help command\n 
    -> add - go to 'add courses' menu\n 
    -> rm - remove a section from your timetable\n
    -> viewtt - go to the menu to view available classes\n 
    -> view- view available courses or sections\n 
    -> save- save timetable as CSV and save course/section changes to DB\n
    -> admin- open the admin panel
    """)

def add_section(course=None, section_name=None):
    # get all courses from db, ask which course user wants to add, display sections of that course, add that section
    if not course:
        print("Specify the course you want to add to the timetable. Press enter to go back")
        print(", ".join(list(db["courses"].keys())))
        course = input()
        try:
            course = db["courses"][course]
        except KeyError:
            print("Not a valid course name. Aborting.")
            return False

    if not section_name:
        print("Specify the section name you want to add to the timetable. Press enter to go back")
        print(", ".join(list(db["courses"][course["code"]]["sections"].keys())))
        section = input()
        try:
            section = course["sections"][section]
        except KeyError: 
            print("Not a valid section name. Aborting.")
            return False

    section = Section(**section)
    timetable.enroll_class(section)
    return section


def remove_section(section_name):
    # show all registered courses for the user, ask which course user would like to remove (clarify which T9 in case user enrolled in multiple T9's)
    section = Section(db["sections"][section_name])
    timetable.drop_class(section)
    return section

def view_sections():
    print("Which course's sections would you like to view? ")
    print(", ".join(list(db["courses"].keys())))
    course = input()
    # try:
    #     course = db["courses"][course] # turn this process into a function 
    # except KeyError:
    #     print("Not a valid course name. Aborting.")
    #     return False
    try:
        print(list(db["courses"][course]["sections"].keys()))
    except KeyError:
        print("Not a valid section name. Aborting.")
    
def view_tt():
    # show the current TimeTable
    # cols = list(timetable.tt.keys())
    # rows = list(range(1, 9))
    # data = []
    # for i in rows:
    #     timetable.tt[]
        
    # return timetable.tt

    # print(dict(map(lambda day: dict(map(lambda hour: timetable.tt[day][hour].section_name + timetable.tt[day][hour].course, timetable.tt[day])) , timetable.tt)))
    for day in timetable.tt:
        print(day + ": " + ", ".join(["\n" + hour + ": " + timetable.tt[day][hour].section_name + " " + timetable.tt[day][hour].course for hour in timetable.tt[day]]))

def admin_panel():
    if ADMIN!=True:
        print("You are not an admin, please log in with an admin account to use this panel")  
        return

    # print("What would you like to do?\n 1) Populate sections (type s)" + " "*20 + "2)Populate courses (type c)")
    # answer = input()

    answer = "s"

    if answer == "s":
        sheet = input("Please give the name/path of the excel sheet (name only if it is located in this folder)\n")
        if populate_courses(sheet):
            print("Courses added to database successfully.\n")
        else:
            print("Error while populating courses\n")

    # elif answer == "c":
    #     print(", ".join(course for course in db["courses"].keys())
    #     course = Course(db["courses"][input("Which course would you like to add sections to?: ")])
    #     sheet = input("Please give the name/path of the excel sheet ")
        

def save_data():
    json.dump(db, open("db.json", "w+"), indent=4)
    df = timetable.export_to_csv()
    print("This timetable has been exported to CSV and data has been saved\n" + df)
    return True

# creating a dictionary of functions for easier scaling, just define a function and add it here
funcs = {
    "h": help,
    "add": add_section,
    "rm": remove_section,
    "viewtt": view_tt, # view the tt
    "view": view_sections,
    "save": save_data,
    "admin": admin_panel,
}

print("""
Welcome to DVM TimeTable interface\n
""")
help()

while True:
    prompt = input("What would you like to do? (h for help): ")
    if prompt in funcs.keys():
        funcs[prompt]()
    else:
        print("Invalid command, please try again\n")
