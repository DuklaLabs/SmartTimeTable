# This file generates a basic information file for each class, room, and teacher in separate files.
# It fills the info file with the following information:

import json
from pathlib import Path

# Define the paths
timetable_data_dir = Path(__file__).parent / "timetableData"
classes_path = timetable_data_dir / "classes.json"
rooms_path = timetable_data_dir / "rooms.json"
teachers_path = timetable_data_dir / "teachers.json"
classes_output_path = timetable_data_dir / "info" / "classesInfo.json"
rooms_output_path = timetable_data_dir / "info" / "roomsInfo.json"
teachers_output_path = timetable_data_dir / "info" / "teachersInfo.json"

# Ensure the output directory exists
classes_output_path.parent.mkdir(parents=True, exist_ok=True)
rooms_output_path.parent.mkdir(parents=True, exist_ok=True)
teachers_output_path.parent.mkdir(parents=True, exist_ok=True)


# Read the input files
with open(classes_path, "r", encoding="utf-8") as classes_file:
    classes_data = json.load(classes_file)

with open(rooms_path, "r", encoding="utf-8") as rooms_file:
    rooms_data = json.load(rooms_file)

with open(teachers_path, "r", encoding="utf-8") as teachers_file:
    teachers_data = json.load(teachers_file)


# Extract, store and sort the class names then print them in the console
class_names = []
for class_ in classes_data["classes"]:
    class_name = list(class_.keys())[0]
    class_names.append(class_name)
class_names.sort()
print("Class names: ", class_names)

# Extract, store and sort the room numbers then print them in the console
room_numbers = []
for room in rooms_data["rooms"]:
    room_number = list(room.keys())[0]
    room_numbers.append(room_number)
room_numbers.sort()
print("Room numbers: ", room_numbers)

# Extract, store and sort the teacher names then print them in the console
teacher_names = []
for teacher in teachers_data["teachers"]:
    teacher_name = list(teacher.keys())[0]
    teacher_names.append(teacher_name)
teacher_names.sort()
print("Teacher names: ", teacher_names)


# Check which classes are allready present in the classesInfo.json file and only add the missing ones
# Example of the output:  
#{
#    "classes": [
#        {
#            "1.EE": {
#                "info": "Informace o třídě 1.EE",
#                "name": "Třída 1.EE"
#            }
#        },
#        {
#            "1.EM": {
#                "info": "Informace o třídě 1.EM",
#                "name": "Třída 1.EM"
#            }
#        },
#    ]
#}


# Check which classes are already present in the classesInfo.json file and only add the missing ones
# The file might not exist yet or might be empty
try:
    with open(classes_output_path, "r", encoding="utf-8") as classes_output_file:
        try:
            classes_output_data = json.load(classes_output_file)
        except json.JSONDecodeError:
            classes_output_data = {"classes": []}
except FileNotFoundError:
    classes_output_data = {"classes": []}

existing_class_names = {list(class_.keys())[0] for class_ in classes_output_data["classes"]}
for class_name in class_names:
    if class_name not in existing_class_names:
        classes_output_data["classes"].append({class_name: {"info": f"Informace o třídě {class_name}", "name": f"Třída {class_name}"}})
        print(f"Added class {class_name}")

# Sort the enire list of classes alphabetically
classes_output_data["classes"] = sorted(classes_output_data["classes"], key=lambda x: list(x.keys())[0])

# Write the output files
with open(classes_output_path, "w", encoding="utf-8") as classes_output_file:
    json.dump(classes_output_data, classes_output_file, ensure_ascii=False, indent=4)

    


# Check which rooms are already present in the roomsInfo.json file and only add the missing ones
# The file might not exist yet or might be empty
try:
    with open(rooms_output_path, "r", encoding="utf-8") as rooms_output_file:
        try:
            rooms_output_data = json.load(rooms_output_file)
        except json.JSONDecodeError:
            rooms_output_data = {"rooms": []}
except FileNotFoundError:
    rooms_output_data = {"rooms": []}

existing_room_numbers = {list(room.keys())[0] for room in rooms_output_data["rooms"]}

for room_number in room_numbers:
    if room_number not in existing_room_numbers:
        rooms_output_data["rooms"].append({room_number: {"info": f"Informace o učebně {room_number}", "name": f"Učebna {room_number}"}})
        print(f"Added room {room_number}")

# Sort the enire list of rooms numerically where possible otherwise alphabetically
rooms_output_data["rooms"] = sorted(rooms_output_data["rooms"], key=lambda x: list(x.keys())[0])

# Write the output files
with open(rooms_output_path, "w", encoding="utf-8") as rooms_output_file:
    json.dump(rooms_output_data, rooms_output_file, ensure_ascii=False, indent=4)




# Check which teachers are already present in the teachersInfo.json file and only add the missing ones
# The file might not exist yet or might be empty
try:
    with open(teachers_output_path, "r", encoding="utf-8") as teachers_output_file:
        try:
            teachers_output_data = json.load(teachers_output_file)
        except json.JSONDecodeError:
            teachers_output_data = {"teachers": []}
except FileNotFoundError:
    teachers_output_data = {"teachers": []}

existing_teacher_names = {list(teacher.keys())[0] for teacher in teachers_output_data["teachers"]}

for teacher_name in teacher_names:
    if teacher_name not in existing_teacher_names:
        teachers_output_data["teachers"].append({teacher_name: {"info": f"Informace o učiteli {teacher_name}", "name": f"{teacher_name}"}})
        print(f"Added teacher {teacher_name}")

# Sort the enire list of teachers alphabetically
teachers_output_data["teachers"] = sorted(teachers_output_data["teachers"], key=lambda x: list(x.keys())[0])

# Write the output files
with open(teachers_output_path, "w", encoding="utf-8") as teachers_output_file:
    json.dump(teachers_output_data, teachers_output_file, ensure_ascii=False, indent=4)



print("Info files generated successfully.")
