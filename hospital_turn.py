import os 
import json
from datetime import datetime , timedelta 

Patient_database = {}
Turn_information_bank = {}
#===================================
#Functions for saving and loading patient and appointment information

PATIENT_FILE = "patient.json"
TURN_FILE = "turn.json"

def load_patient():
    if os.path.exists(PATIENT_FILE):
        with open(PATIENT_FILE , "r") as f:
            data = json.load(f)

            for item in data.values():
                item["birth_day"] = datetime.strptime(item["birth_day"] , "%Y/%m/%d")
            return data 
    return {}

def save_patient():
    serializable_data = {
        pid : {
            "name" : p["name"],
            "birth_day" : p["birth_day"].strftime("%Y/%m/%d"),
            "number_phone" : p["number_phone"]
        }for pid , p in Patient_database.items()
    }
    with open(PATIENT_FILE , "w") as f:
        json.dump(serializable_data , f , indent=2)

def load_turn():
    if os.path.exists(TURN_FILE):
        with open(TURN_FILE , "r") as f:
            data = json.load(f)

            for item in data:
                item["date"] = datetime.strptime(item["date"] , "%Y/%m/%d")
            return data 
    return {}

def save_turn():
    serializable_data = {
        pid : {
            "date" : t["date"].strftime("%Y/%m/%d"),
            "time" : t["time"],
            "turn_status" : t["turn_status"]
        }for pid , t in Turn_information_bank.items()
    }
    with open(TURN_FILE , "w") as f:
        json.dump(serializable_data , f , indent=2)

#===================================
#Patient registration section

def Add_Patient():
    Patient_ID = input('enter ID: ')
    if Patient_ID in Patient_database:
        print('\nThis ID already exists.\n')
        return 
    name = input('name: ')

    try:
        input_birth_day = input('enter birth day (yyyy/mm/dd): ')
        birth_day = datetime.strptime(input_birth_day , "%Y/%m/%d")
    except ValueError:
        print('The date entered is invalid.')
        return
    
    number = input('number of phone: ')
    num_phone = ''.join(char for char in number if char.isdigit())
    if len(num_phone) == 11 and num_phone.startswith('09'):
        number_phone = f'{num_phone[:4]}-{num_phone[4:7]}-{num_phone[7:]}'
    else : 
        print('The contact number is invalid.')
        return
    
    Patient_database[Patient_ID] = {
        'name' : name,
        'birth_day' : birth_day,
        'number_phone' : number_phone
    }
    print('\nRegistration was successful.\n')
    save_patient()

def Search_patient():
    Patient_ID = input('inter ID: ')
    if Patient_ID in Patient_database:
        item = Patient_database[Patient_ID]
        print(f"ID : {Patient_ID} , name : {item['name']} , birth day : {item['birth_day']} , number phone : {item['number_phone']}")
    else:
        print('ID not found')

#=====================================
#Turnaround generation section for each date

start_time = datetime.strptime("8:00" , "%H:%M")
start_end = datetime.strptime("12:00" , "%H:%M")
time_interval = timedelta(minutes=20)
DATA_FILE = "appointment.json"

def management_slot():
    slot = []
    curren = start_time
    while curren <= start_end:
        slot.append(curren.time().isoformat(timespec='minutes'))
        curren += time_interval
    return slot

def load_appointment():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE , "r") as f: 
        return json.load(f)
    
def save_appointment(appointment):
    with open(DATA_FILE , "w") as f:
        return json.dump(appointment , f , indent=2)
    
def assign_next_slot(date):
    date_str = str(date)

    appointment = load_appointment()
    if date_str not in appointment:
        appointment[date_str] = []

    used_slot = appointment[date_str]
    all_slots = management_slot()

    for slot in all_slots:
        if slot not in used_slot:
            appointment[date_str].append(slot)
            save_appointment(appointment)
            return slot
    return None

#=====================================
#The turn registration section
    
def Record_Turn():
    Patient_ID = input('enter ID: ')
    to_day = datetime.today().date()
    if Patient_ID not in Patient_database:
        print('\nThe ID was entered and not found.\n')
        return

    try:
        date_input = input('enter date (yyyy/mm/dd): ')
        date = datetime.strptime(date_input , "%Y/%m/%d").date()
    except ValueError:
        print('The date entered is invalid.')
        return

    days_left = (date - to_day).days
    if days_left <= 0:
        print('\nThe turns have ended.\n')
        return
    
    date_time = date
    next_slot = assign_next_slot(date_time)
    
    if next_slot:
        time = next_slot
    else:
        time = f'The capacity in {date_time} is full.'
    print('''
    ============================
    enter turn status: 
    
    1.planned
    2.canceled
    3.done
    ============================
    
    ''')
    turn_status = input('enter number of choice: ')

    if turn_status == '1':
        turn_status = 'planned'
    elif turn_status == '2':
        turn_status = 'canceled'
    elif turn_status == '3':
        turn_status = 'done'
    else:
        print('\nThe entered option is invalid.\n')
        return

    Turn_information_bank[Patient_ID] = {
        'date' : date,
        'time' : time,
        'turn_status' : turn_status
    }
    print('\nSuccessfully registered\n')
    save_turn()

def Turn_Management():
    Patient_ID = input('enter Patient_ID: ')
    if Patient_ID in Turn_information_bank:
        print('\n\n=====================\n1.view turn\n2.Change turn status\n3.Delete turn\n=====================\n\n')
        choice = input('enter choice number: ')
        if choice == '1':
            item = Turn_information_bank[Patient_ID]
            print(f"\nPatient_ID : {Patient_ID} , date : {item['date']} , time : {item['time']} , turn_status : {item['turn_status']} \n")
        elif choice == '2':
            print('''
            ============================
            enter turn status: 
    
            1.planned
            2.canceled
            3.done
            ============================
    
            ''')
            turn_status = input('enter number of choice: ')

            if turn_status == '1':
                    turn_status = 'planned'
            elif turn_status == '2':
                    turn_status = 'canceled'
            elif turn_status == '3':
                    turn_status = 'done'
            else:
                print('\nThe entered option is invalid.\n')
                return

            Turn_information_bank[Patient_ID]['turn_status'] = turn_status
            print('\nChanged successfully\n')

        elif choice == '3':
            del Turn_information_bank[Patient_ID]
            print('\nCleared successfully\n')
        
        else:
            print('\nThe entered option is invalid.\n')
    else:
        print('\nPatient ID not previously registered\n')
    save_turn()

def Turn_Search():
    keyword = input('enter Patient_ID or date or turn status: ')
    for Patient_ID , item in Turn_information_bank.items():
        if keyword in Patient_ID or keyword in str(item['date']) or keyword in item['turn_status']:
            print(f"\nPatient_ID : {Patient_ID} , date : {item['date']} , time : {item['time']} , turn_status : {item['turn_status']}\n")
            return
    print('\npatient_ID or data or turn status not in database\n')

#=========================================
#main page 

def main_menu():
    while True: 
        print('''
        =============================

        1.Patient registration
        2.Record turn
        3.Manage appointments
        4.Search in turns
        5.View patient
        6.Exit

        =============================
        ''')
        choice = input('enter your choice: ')

        if choice == '1': 
            Add_Patient()
        elif choice == '2': 
            Record_Turn()
        elif choice == '3':
            Turn_Management()
        elif choice == '4':
            Turn_Search()
        elif choice == '5':
            Search_patient()
        elif choice == '6':
            print('Exiting program...')
            break
        else:
            print('\nThe entered option is invalid.\n')

Patient_database = load_patient()
Turn_information_bank = load_turn()

if __name__ == '__main__':
    main_menu()
