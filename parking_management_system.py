import mysql.connector
import time
from datetime import date


# Setting up the database
global conn, cursor
conn = mysql.connector.connect(
    host='localhost', database='parking_system', user='root', password='root')
cursor = conn.cursor(buffered=True)


# Setting a screen cleaner
def clear():
    for _ in range(65):
        print()


# Setting the system initialization introduction
def introduction():
    print('-' * 100)
    msg = '''
    P A R K I N G     M A N A G E M E N T    S Y S T E M    
    
    Parking is a very big problem in macro-cities, Day by day basis parking system are coming up with new
    technologies to solve this issue. This project is also trying to solve this simple but very useful
    information for the parking management. The whole database is store in MySQL table ParkingSystem that stores
    their parking slot information,as well as how long a vehicle is parked in their parking area and how much
    they need to pay for that. 
    
    Besides all these features, it also tracks the total money collected during the period of time
    with its extensive searching and reporting system. The whole project is divided into four major parts, i.e.,
    addition of data, modification, searching and reporting. All these part are further divided into menus
    for easy navigation\n\n'''

    for x in msg:
        print(x, end='')
        # time.sleep(0.001)
    print('-' * 100)
    input('Press any key to continue...')


# Setting the developer information
def made_by():
    msg = '''
        Parking Management System, made by          : Márcio Mizuhara
        Github                                      : https://github.com/marciomizuhara
        
        Thanks for evaluating my Project. For any concerns, contact me at marciomizu@gmail.com\n\n\n'''

    for x in msg:
        print(x, end='')
        time.sleep(0.002)

    input('Press any key to continue...')


# Showing the registered parking types
def display_parking_type_records():
    cursor.execute('select * from parking_type;')
    records = cursor.fetchall()
    for row in records:
        print(row)


# Showing the registered parking spaces
def display_parking_space_records():
    cursor.execute('select * from parking_space;')
    records = cursor.fetchall()
    for row in records:
        print(row)


# Setting up the login system for users
def login():
    while True:
        clear()
        your_name = input('Enter your username :')
        your_password = input('Enter your password :')
        cursor.execute('select * from login where name="{}" and pwd="{}"'.format(your_name, your_password))
        cursor.fetchall()
        rows = cursor.rowcount
        if rows != 1:
            print('Invalid login details... Please check your details and try again.')
            time.sleep(2.5)
        else:
            print('You have successfully logged into the Parking Management System!!!')
            time.sleep(1)
            print('\n\n\n')
            input('Press any key to continue...')
            break


# Setting an option to register a parking type
def add_parking_type_record():
    clear()
    name = input('Enter Parking Type:\n\n1. Two wheelar\n2. Car\n3. Bus\n4. Truck\n5. Trolly\n\n --> ')
    price = input('Enter Parking Price per day : ')
    sql = 'insert into parking_type(name,price) values("{}",{});'.format(name, price)
    cursor.execute(sql)
    print('\n\n New Parking Type added...')
    time.sleep(2)
    cursor.execute('select max(id) from parking_type')
    number = cursor.fetchone()
    print(' New Parking Type ID is : {} \n\n\n'.format(number[0]))
    input('\n\n\nPress any key to continue...')


# Setting an option to register a parking slot
def add_parking_slot_record():
    clear()
    parking_type_id = input('Enter Parking Type:\n\n1. Two wheelar\n2. Car\n3. Bus\n4. Truck\n5. Trolly\n\n --> ')
    status = input('Enter current Status:\n\nOpen\nFull\n\n -->')
    sql = 'insert into parking_space(type_id,status) values ("{}","{}");'.format(parking_type_id, status)
    cursor.execute(sql)
    print('\n\n New Parking Space Record added...')

    cursor.execute('select max(id) from parking_space;')
    number = cursor.fetchone()
    print(' Your Parking ID is : {} \n\n\n'.format(number[0]))
    display_parking_type_records()
    input('\n\n\nPress any key to continue...')


# Setting an option to modify a parking type
def modify_parking_type_record():
    clear()
    print(' M O D I F Y   P A R K I N G   T Y P E   R E C O R D')
    print('-'*100)
    print('1.   Parking Type Name \n')
    print('2.   Parking Price \n')
    choice = int(input('Enter your choice :'))
    field = ''
    if choice == 1:
        field = 'name'
    elif choice == 2:
        field = 'price'
    else:
        print('Invalid choice! Please enter a valid option (1 or 2) :')
        time.sleep(2)
        modify_parking_type_record()

    park_id = input('Enter Parking Type ID :')
    value = input('Enter the new value :')
    sql = 'update parking_type set ' + field + ' = "' + value + '" where id =' + park_id + ';'
    cursor.execute(sql)
    print('Record updated successfully...')
    display_parking_type_records()
    input('\n\n\nPress any key to continue...')


# Setting an option to modify a parking space
def modify_parking_space_record():
    clear()
    print(' M O D I F Y   P A R K I N G   S P A C E   R E C O R D')
    print('-' * 100)
    print('1.   Parking Type ID (1-Two Wheelar, 2- Car, 3-Bus, etc): ')
    print('2.   Status \n')
    choice = int(input('Enter your choice :'))
    field = ''
    if choice == 1:
        field = 'type_id'
    elif choice == 2:
        field = 'status'
    else:
        print('Invalid choice! Please enter a valid option (1 or 2) :')
        time.sleep(2)
        modify_parking_space_record()
    print('\n\n\n')
    crime_id = input('Enter Parking Space ID :')
    value = input('Enter the new value :')
    sql = 'update parking_space set ' + field + ' = "' + value + '" where id =' + crime_id + ';'
    cursor.execute(sql)
    print('Record updated successfully...')
    display_parking_type_records()
    input('\n\n\nPress any key to continue...')


# Setting an option to check-in a new vehicle
def add_new_vehicle():
    clear()
    print('V E H I C L E   L O G I N   S C R E E N ')
    print('-'*100)
    vehicle_id = input('Enter Vehicle License Plate :')
    parking_id = input('Enter parking ID :')
    entry_date = date.today()
    sql = 'insert into transaction(vehicle_id,parking_id,entry_date) values \
           ("{}","{}","{}");'.format(vehicle_id, parking_id, entry_date)
    cursor.execute(sql)
    cursor.execute('update parking_space set status ="full" where id ={}'.format(parking_id))
    print('Record added successfully...')
    input('\n\n\nPress any key to continue...')


# Setting an option to check-ou a vehicle
def remove_vehicle():
    clear()
    print('V E H I C L E   L O G O U T   S C R E E N')
    print('-'*100)
    vehicle_id = input('Enter Vehicle License Plate :')
    exit_date = date.today()
    sql = 'select parking_id, price, entry_date from transaction tr, parking_space ps, parking_type pt \
    where tr.parking_id = ps.id and ps.type_id = pt.id and vehicle_id ="'+vehicle_id+'" and exit_date is NULL;'
    cursor.execute(sql)
    record = cursor.fetchone()
    days = (exit_date-record[2]).days
    if days == 0:
        days = days + 1
    amount = record[1]*days
    clear()
    print('Logout Details ')
    print('-'*100)
    print('Parking ID : {}'.format(record[0]))
    print('Vehicle ID : {}'.format(vehicle_id))
    print('Parking Date : {}'.format(record[2]))
    print('Current Date : {}'.format(exit_date))
    print('Amount Payable : {}'.format(amount))
    input('\n\n\nPress any key to continue...')

    # update transaction and parking space tables
    sql1 = 'update transaction set exit_date ="{}", amount={} where vehicle_id="{}" \
           and exit_date is NULL;'.format(exit_date, amount, vehicle_id)
    sql2 = 'update parking_space set status ="open" where id = {}'.format(record[0])
    cursor.execute(sql1)
    cursor.execute(sql2)
    input('Vehicle out from our system successfully...\nPress any key to continue... ')


# Setting a search menu to help users acccess information about their parking lot status
def search_menu():
    clear()
    print(' S E A R C H   P A R K I N G   M  E N U ')
    print('1.   Parking ID \n')
    print('2.   Vehicle Parked \n')
    print('3.   Free Space \n')
    choice = int(input('Enter your choice: '))
    field = ''
    if choice == 1:
        field = 'id'
    if choice == 2:
        field = 'vehicle number'
    if choice == 3:
        field = 'status'
    value = input('Enter value to search :')
    if choice == 1 or choice == 3:
        sql = 'select ps.id, name, price, status \
        from parking_space ps, parking_type pt where ps.id = pt.id AND ps.id = {}'.format(value)
    else:
        sql = 'select id, vehicle_id, parking_id, entry_date from transaction where exit_date is NULL;'

    cursor.execute(sql)
    results = cursor.fetchall()
    records = cursor.rowcount
    for row in results:
        print(row)
    if records < 1:
        print('Record not found \n\n\n ')
    input('\n\n\nPress any key to continue...')


# Showing parking status regarding free or occupied spaces
def parking_status(status):
    clear()
    print('Parking Status :', status)
    print('-'*100)
    sql = "select * from parking_space where status ='{}'".format(status)
    cursor.execute(sql)
    records = cursor.fetchall()
    # print(status)
    for row in records:
        print(row)
    input('\n\n\nPress any key to continue...')


# Showing the currently parked vehicles
def vehicle_status_report():
    clear()
    print('Currently Parked Vehicles')
    print('-'*100)
    sql = 'select * from transaction where exit_date is NULL;'
    cursor.execute(sql)
    records = cursor.fetchall()
    for row in records:
        print(row)
    input('\n\n\nPress any key to continue...')


# Showing the money collected in a given period
def money_collected():
    clear()
    start_date = input('Enter Start Date (yyyy-mm-dd): ')
    end_date = input('Enter End Date (yyyy-mm-dd): ')
    sql = 'select sum(amount) from transaction where\
          entry_date = "{}" and exit_date = "{}"'.format(start_date, end_date)
    cursor.execute(sql)
    result = cursor.fetchone()
    clear()
    print('Total money collected from {} to {}'.format(start_date, end_date))
    print('-'*100)
    print(result[0])
    input('\n\n\nPress any key to continue...')


# Setting a report menu to help users get several information about their parking lot status
def report_menu():
    while True:
        clear()
        print(' P A R K I N G    R E P O R T S ')
        print('-'*100)
        print('1.   Parking Types\n')
        print('2.   Free Space\n')
        print('3.   Ocupied Space\n')
        print('4.   Currently Parked Vehicles\n')
        print('5.   Money Collected\n')
        print('6.   Main Menu\n')
        choice = int(input('Enter your choice :'))
        field = ''
        if choice == 1:
            display_parking_type_records()
            time.sleep(2)
        if choice == 2:
            parking_status("open")
            time.sleep(2)
        if choice == 3:
            parking_status("full")
            time.sleep(2)
        if choice == 4:
            vehicle_status_report()
            time.sleep(2)
        if choice == 5:
            money_collected()
            time.sleep(2)
        if choice == 6:
            break


# Setting the main menu
def main_menu():
    clear()
    login()
    clear()
    introduction()

    while True:
        clear()
        print(' P A R K I N G    M A N A G E M E N T    S Y S T E M ')
        print('-'*100)
        print('\n1. Add New Parking Type')
        print('\n2. Add New Parking Slot')
        print('\n3. Modify Parking Type Record')
        print('\n4. Modify Parking Slot Record')
        print('\n5. Vehicle Login')
        print('\n6. Vehicle Logout')
        print('\n7. Search menu')
        print('\n8. Report menu')
        print('\n9. Close application')
        print('\n\n')
        choice = int(input('Enter your choice... '))

        if choice == 1:
            add_parking_type_record()

        if choice == 2:
            add_parking_slot_record()

        if choice == 3:
            modify_parking_type_record()

        if choice == 4:
            modify_parking_space_record()

        if choice == 5:
            add_new_vehicle()

        if choice == 6:
            remove_vehicle()

        if choice == 7:
            search_menu()

        if choice == 8:
            report_menu()

        if choice == 9:
            break

    made_by()


# Preventing program code from being run when the module is imported.
if __name__ == '__main__':
    main_menu()
