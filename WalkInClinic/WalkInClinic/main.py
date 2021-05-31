import sys
import csv
import sqlite3
import re
import stdiomask

# Make a regular expression
# for validating an Email
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


# Class For Showing Colors in Print Messages
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def run_db_migrations():
    create_user_table()
    create_doctor_table()
    create_patient_table()
    create_appointment_table()
    create_visit_table()
    create_prescription_table()
    create_admin_staff_user()


def drop_tables():
    try:
        connection = sqlite3.connect('Clinic.db')
        connection.execute("DROP TABLE IF EXISTS USER")
        connection.execute("DROP TABLE IF EXISTS DOCTOR")
        connection.execute("DROP TABLE IF EXISTS PATIENT")
        connection.execute("DROP TABLE IF EXISTS APPOINTMENT")
        connection.execute("DROP TABLE IF EXISTS VISIT")
        connection.execute("DROP TABLE IF EXISTS PRESCRIPTION")
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Dropping Tables: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def create_admin_staff_user():
    try:
        connection = sqlite3.connect('Clinic.db')
        cursor = connection.cursor()
        admin_query = """SELECT *
                    FROM USER
                    WHERE Email='david@clinic.com' AND Password='David1234'"""
        cursor.execute(admin_query)
        admin_rows = cursor.fetchall()
        # print(admin_rows)
        if len(admin_rows) == 0:
            admin_user_query = """  INSERT INTO USER(Email, Password, First_name, Last_name, Role)
                                    VALUES("david@clinic.com", "David1234", "David", "Marsh", "Admin")
                               """
            connection.execute(admin_user_query)
            connection.commit()
        admin_query = """SELECT *
                            FROM USER
                            WHERE Email='john@clinic.com' AND Password='John1234'"""
        cursor.execute(admin_query)
        staff_rows = cursor.fetchall()
        # print(staff_rows)
        if len(staff_rows) == 0:
            staff_user_query = """  INSERT INTO USER(Email, Password, First_name, Last_name, Role)
                                    VALUES("john@clinic.com", "John1234", "John", "Smith", "Staff")
                               """
            connection.execute(staff_user_query)
            connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Inserting Admin and Staff User: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def create_user_table():
    try:
        # SELECT User_ID, Email, First_name, Last_name, datetime(Created_at, 'unixepoch', 'localtime') as Created_at
        # FROM USER;
        connection = sqlite3.connect('Clinic.db')
        connection.execute("""CREATE TABLE IF NOT EXISTS USER
         (
            User_ID     INTEGER PRIMARY KEY NOT NULL,
            Email       TEXT NOT NULL,
            First_name  TEXT NOT NULL,
            Last_name   TEXT NOT NULL,
            Password    TEXT NOT NULL,
            Created_at  INTEGER(4) not null default (strftime('%s','now')),
            Role        TEXT CHECK( Role IN ('Staff','Admin') )   NOT NULL DEFAULT 'Staff'
         );""")
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Creating Table User: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def create_doctor_table():
    try:
        connection = sqlite3.connect('Clinic.db')
        connection.execute("""CREATE TABLE IF NOT EXISTS DOCTOR
         (
            Doctor_ID           INTEGER PRIMARY KEY NOT NULL,
            First_name          TEXT NOT NULL,
            Last_name           TEXT NOT NULL,
            Phone               TEXT NOT NULL,
            Address             TEXT NOT NULL,
            Specialization      TEXT NOT NULL,
            Consultation_Fee    INTEGER NOT NULL,
            Created_at          INTEGER(4) not null default (strftime('%s','now'))
         );""")
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Creating Table DOCTOR: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def create_patient_table():
    try:
        connection = sqlite3.connect('Clinic.db')
        connection.execute("""CREATE TABLE IF NOT EXISTS PATIENT
         (
            Patient_ID      INTEGER PRIMARY KEY NOT NULL,
            First_name      TEXT NOT NULL,
            Last_name       TEXT NOT NULL,
            Phone           TEXT NOT NULL,
            Address         TEXT NOT NULL,
            Created_at      INTEGER(4) not null default (strftime('%s','now')),
            CONSTRAINT Phone_len_Chk CHECK (LENGTH(Phone) == 10)
         );""")
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Creating Table PATIENT: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def create_appointment_table():
    try:
        connection = sqlite3.connect('Clinic.db')
        connection.execute("""CREATE TABLE IF NOT EXISTS APPOINTMENT
         (
             Appointment_ID INTEGER PRIMARY KEY NOT NULL,
             Patient_ID     INTEGER  NOT NULL,
             Doctor_ID      INTEGER  NOT NULL,
             Apt_DateTime   TEXT NOT NULL,
             Created_at     INTEGER(4) not null default (strftime('%s','now')),
             FOREIGN KEY (Patient_ID) REFERENCES PATIENT (Patient_ID),
             FOREIGN KEY (Doctor_ID) REFERENCES DOCTOR (Doctor_ID)
         );""")
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Creating Table User: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def create_visit_table():
    try:
        connection = sqlite3.connect('Clinic.db')
        connection.execute("""CREATE TABLE IF NOT EXISTS VISIT
         (
             Visit_ID           INTEGER PRIMARY KEY NOT NULL,
             Patient_ID         INTEGER  NOT NULL,
             Appointment_ID     INTEGER  NOT NULL,
             Apt_DateTime   TEXT NOT NULL,
             Created_at         INTEGER(4) not null default (strftime('%s','now')),
             Payment_Amount INTEGER NOT NULL,
             FOREIGN KEY (Patient_ID) REFERENCES PATIENT (Patient_ID),
             FOREIGN KEY (Appointment_ID) REFERENCES APPOINTMENT (Appointment_ID)
         );""")
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Creating Table User: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def create_prescription_table():
    try:
        connection = sqlite3.connect('Clinic.db')
        connection.execute("""CREATE TABLE IF NOT EXISTS PRESCRIPTION
         (
             Prescription_ID    INTEGER PRIMARY KEY NOT NULL,
             Patient_ID         INTEGER  NOT NULL,
             Visit_ID           INTEGER  NOT NULL,
             Created_at         INTEGER(4) not null default (strftime('%s','now')),
             Prescription_Details TEXT NOT NULL,
             FOREIGN KEY (Patient_ID) REFERENCES PATIENT (Patient_ID),
             FOREIGN KEY (Visit_ID) REFERENCES VISIT (Visit_ID)
         );""")
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Creating Table PRESCRIPTION: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


# def create_bill_table():
#     try:
#         connection = sqlite3.connect('Clinic.db')
#         connection.execute("""CREATE TABLE IF NOT EXISTS BILL
#          (User_ID      INTEGER PRIMARY KEY NOT NULL,
#          Login         TEXT NOT NULL,
#          Password      TEXT NOT NULL,
#          AccessCount   INT DEFAULT 0);""")
#         connection.commit()
#     except:
#         error = sys.exc_info()
#         print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
#         print(bcolors.FAIL + "Error While Creating Table User: ", error, "" + bcolors.ENDC)
#         print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
#     finally:
#         if connection:
#             connection.close()


def start_application():
    login_user()


# Function Login For user
def login_user():
    user = taking_user_inputs()
    logged_in_user = get_user(user['email'], user['password'])
    if logged_in_user is not None:
        print(bcolors.HEADER + "**********************************************" + bcolors.ENDC)
        print(bcolors.HEADER + "User is logged in" + bcolors.ENDC)
        print(bcolors.HEADER + "Email: ", logged_in_user[1], "Name: ", logged_in_user[3], "" + bcolors.ENDC)
        print(bcolors.HEADER + "**********************************************" + bcolors.ENDC)
        print(logged_in_user[6])
        if (logged_in_user[6]) == 'Staff':
            get_staff_choice()
        elif (logged_in_user[6]) == 'Admin':
            get_admin_choice()
    else:
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Invalid Credentials, Please Try Again" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        start_application()


# Function Get User
def get_user(email, password):
    try:
        connection = sqlite3.connect('Clinic.db')
        cursor = connection.cursor()
        query = """SELECT * FROM USER WHERE Email='{}' AND Password='{}'""" \
            .format(email, password)

        cursor.execute(query)
        rows = cursor.fetchall()

        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Fetching user from database: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()

    return rows[0] if len(rows) else None


# Function User Credentials Input
def taking_user_inputs():
    user = dict()
    print(bcolors.WARNING + "**********************************************" + bcolors.ENDC)
    print("Please Enter Email and Password to Login")
    print(bcolors.WARNING + "**********************************************" + bcolors.ENDC)
    email = taking_email_input()
    password = taking_password_input()
    user["email"] = email
    user["password"] = password
    return user


# Function Getting Email Input
def taking_email_input():
    while True:
        try:
            email = raw_input("Type Your Email: ")
            if re.match(regex, email):
                break
            else:
                 raise ValueError("Invalid Email")
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Email Format, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)

    return email


# Function Getting Password Input
def taking_password_input():
    while True:
        try:
            password = raw_input("Type Your Password: ")
            if len(password) > 0:
                break
            else:
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
                print(bcolors.FAIL + "Password length cannot be 0, Please Try Again" + bcolors.ENDC)
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Password, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)

    return password


def get_admin_choice():
    select_statement = """
    Select any of the following
    1) Add a new doctor
    2) Add a new staff member
    3) Generate Report Data
    4) Sign out
    5) Exit
    """
    while True:
        try:
            admin_choice = int(input(select_statement))
            if admin_choice < 1 or admin_choice > 5:
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
                print(bcolors.FAIL + "Choice must be from 1 and 5 only, Please Try Again" + bcolors.ENDC)
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            else:
                break
        except:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Choice. Must be a number only" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)

    if admin_choice == 1:
        creating_doctor()
    elif admin_choice == 2:
        creating_staff()
    elif admin_choice == 3:
        Generate_report_data()
    elif admin_choice == 4:
        sign_out()
    elif admin_choice == 5:
        exit()

def creating_doctor():
    print(bcolors.WARNING + "Some information is required to Add a new doctor to Database" + bcolors.ENDC)
    doctor = taking_doctor_input()
    try:
        connection = sqlite3.connect('Clinic.db')
        doctor_query = """  INSERT INTO DOCTOR(First_name, Last_name, Phone, Address, Specialization, Consultation_Fee)
                                       VALUES("{}", "{}", "{}", "{}","{}","{}")
                                                  """.format(doctor['FirstName']
                                                             , doctor['LastName'], doctor['PhoneNumber']
                                                             , doctor['Address'], doctor['Specialization'],
                                                             doctor['Consultation_Fee'])
        connection.execute(doctor_query)
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Inserting Doctor Data: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()
    print(bcolors.WARNING + "**********************************************" + bcolors.WARNING)
    print(bcolors.WARNING + "Doctor information has been stored in database" + bcolors.WARNING)
    print(bcolors.WARNING + "**********************************************" + bcolors.WARNING)
    admin_input = input("""
    Select one of the following.
    1) To Continue
    2) Sign Out
    3) Exit
    """)
    if (admin_input == 1):
        get_admin_choice()
    elif (admin_input == 2):
        sign_out()
    elif (admin_input == 3):
        exit()

def taking_doctor_input():
    doctor = dict()
    doctor["FirstName"] = taking_firstName()
    doctor["LastName"] = taking_lastName()
    doctor["PhoneNumber"] = taking_phoneNumber()
    doctor["Address"] = taking_address()
    doctor["Specialization"] = taking_specialization()
    doctor["Consultation_Fee"] = taking_consultation_fee()
    return doctor


def get_staff_choice():
    select_statement = """
    Select any of the following
    1) Add a patient
    2) Add new appointment
    3) Add new Visit
    4) Sign out
    5) Exit
    """
    while True:
        try:
            staff_choice = int(input(select_statement))
            if staff_choice < 1 or staff_choice > 5:
                print("Choice must be from 1 to 5 only. Please try again")
            break
        except:
            print("Invalid Choice. Must be a Number only")

    if staff_choice == 1:
        creating_patient()
    elif staff_choice == 2:
        add_new_appointment()
    elif staff_choice == 3:
        add_new_visit()
    elif staff_choice == 4:
        sign_out()
    elif staff_choice == 5:
        exit()

def creating_staff():
    print(bcolors.WARNING + "Some information is required to Add a new staff member to Database" + bcolors.ENDC)
    FirstName = taking_firstName()
    LastName = taking_lastName()
    Email = taking_email_input()
    Password = taking_password_input()

    try:
        connection = sqlite3.connect('Clinic.db')
        staff_query = """  INSERT INTO USER(Email, First_name, Last_name, Password, Role)
                        VALUES("{}", "{}", "{}", "{}","{}")
                        """.format(Email,FirstName,LastName,Password,'Staff')
        connection.execute(staff_query)
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Inserting Staff Data: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()
    print(bcolors.OKBLUE + "**********************************************" + bcolors.OKBLUE)
    print(bcolors.OKBLUE + "Staff information has been stored in database" + bcolors.OKBLUE)
    print(bcolors.OKBLUE + "**********************************************" + bcolors.OKBLUE)
    admin_input = input("""
       Select one of the following.
       1) To Continue
       2) Sign Out
       3) Exit
       """)
    if (admin_input == 1):
        get_admin_choice()
    elif (admin_input == 2):
        sign_out()
    elif (admin_input == 3):
        exit()

def Generate_report_data():
    Query = """select DOCTOR.First_name as 'DoctorFirstName',
                DOCTOR.Last_name as 'DoctorLastName',
                DOCTOR.Phone as 'DoctorPhone',
                DOCTOR.Address as 'DoctorAddress',
                DOCTOR.Specialization,
                DOCTOR.Consultation_Fee,
                PATIENT.First_name as 'PatientFirstName',
                PATIENT.Last_name as 'PatientLastName',
                PATIENT.Phone as 'PatientPhone',
                PATIENT.Address as 'PatientAddress',
                APPOINTMENT.Apt_DateTime as 'Appointment',
                datetime(VISIT.Created_at, 'unixepoch', 'localtime') as 'VisitDate',
                VISIT.Payment_Amount as 'Payment',
                PRESCRIPTION.Prescription_Details as 'PRESCRIPTION'
                from Doctor
                LEFT JOIN APPOINTMENT on DOCTOR.Doctor_ID = APPOINTMENT.Doctor_ID
                 LEFT JOIN PATIENT on APPOINTMENT.Patient_ID = PATIENT.Patient_ID
                 LEFT JOIN Visit on APPOINTMENT.Appointment_ID = VISIT.Appointment_ID
                 LEFT JOIN PRESCRIPTION on VISIT.Visit_ID = PRESCRIPTION.Visit_ID"""

    try:
        connection = sqlite3.connect('Clinic.db')
        cursor = connection.cursor()
        cursor.execute(Query)
        results = cursor.fetchall()
        connection.commit()

        with open('data.csv', 'wb') as f:
            fieldnames = ['DoctorFirstName', 'DoctorLastName','DoctorPhone','DoctorAddress','Specialization',
                          'ConsultationFee','PatientFirstName','PatientLastName','PatientPhone','PatientAddress',
                          'Appointment','VisitDate','Payment','Prescription']

            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in results:
                writer.writerow({'DoctorFirstName': row[0], 'DoctorLastName': row[1],
                                 'DoctorPhone': row[2], 'DoctorAddress': row[3],
                                 'Specialization': row[4], 'ConsultationFee': row[5],
                                 'PatientFirstName': row[6], 'PatientLastName': row[7],
                                 'PatientPhone': row[8], 'PatientAddress': row[9],
                                 'Appointment': row[10], 'VisitDate': row[11],
                                 'Payment': row[12], 'Prescription': row[13]})
        f.close()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While fetching report data: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()

def sign_out():
    print("You are successfully signed out")
    login_user()


def creating_patient():
    patient = taking_patient_input()
    try:
        connection = sqlite3.connect('Clinic.db')
        patient_query = """  INSERT INTO PATIENT(First_name, Last_name, Phone, Address)
                                   VALUES("{}", "{}", "{}", "{}")
                                              """.format(patient['FirstName']
                                                         , patient['LastName'], patient['PhoneNumber']
                                                         , patient['Address'])
        connection.execute(patient_query)
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Inserting Patient Data: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()
    print(bcolors.OKBLUE + "**********************************************" + bcolors.OKBLUE)
    print(bcolors.OKBLUE + "Patient information has been stored in database" + bcolors.OKBLUE)
    print(bcolors.OKBLUE + "**********************************************" + bcolors.OKBLUE)
    staff_input = input("""
    Select one of the following.
    1) To Continue
    2) Sign Out
    3) Exit
    """)
    if (staff_input == 1):
        get_staff_choice()
    elif (staff_input == 2):
        sign_out()
    elif (staff_input == 3):
        exit()

def taking_patient_input():
    patient = dict()
    patient["FirstName"] = taking_firstName()
    patient["LastName"] = taking_lastName()
    patient["PhoneNumber"] = taking_phoneNumber()
    patient["Address"] = taking_address()
    return patient


def taking_firstName():
    while True:
        try:
            FirstName = raw_input("Type First Name: ")
            if len(FirstName) > 0:
                break
            else:
                raise ValueError
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid First Name, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return FirstName


def taking_lastName():
    while True:
        try:
            LastName = raw_input("Type Last Name: ")
            if len(LastName) > 0:
                break
            else:
                raise ValueError
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Last Name, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return LastName


def taking_phoneNumber():
    while True:
        try:
            PhoneNumber = raw_input("Type PhoneNumber(10 Digits): ")
            if PhoneNumber.isdigit():
                if len(PhoneNumber) == 10:
                    break
                else:
                    print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
                    print(bcolors.FAIL + "Phone Number must be 10 digits only" + bcolors.ENDC)
                    print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + "***********************************************************************" + bcolors.ENDC)
                print(bcolors.FAIL + "Phone number cannot be a text value. All characters must be digits only"+ bcolors.ENDC)
                print(bcolors.FAIL + "***********************************************************************" + bcolors.ENDC)
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid PhoneNumber, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return PhoneNumber


def taking_address():
    while True:
        try:
            Address = raw_input("Type Address: ")
            if len(Address) > 0:
                break
            else:
                raise ValueError
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Address, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return Address

def taking_specialization():
    while True:
        try:
            Specialization = raw_input("Type Specialization: ")
            if len(Specialization) > 0:
                break
            else:
                raise ValueError
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Specialization, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return Specialization


def taking_consultation_fee():
    while True:
        try:
            Consultation_Fee = int(raw_input("Type Consultation Fees: "))
            if Consultation_Fee < 100:
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
                print(bcolors.FAIL + "Consultation Fees cannot be less than 100" + bcolors.ENDC)
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            else:
                break
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Input, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return Consultation_Fee


def add_new_appointment():
    patient_data = retrieve_patient_data_by_firstName()
    patient_id = select_patient(patient_data)
    doctor_data = retrieve_doctor_data_by_firstName()
    doctor_id = select_doctor(doctor_data)
    datetime = take_datetime()

    try:
        connection = sqlite3.connect('Clinic.db')
        appointment_query = """  INSERT INTO APPOINTMENT(Patient_ID, Doctor_ID, Apt_DateTime)
                                   VALUES("{}", "{}", "{}")
                                              """.format(patient_id, doctor_id, datetime)
        connection.execute(appointment_query)
        connection.commit()
        print(bcolors.OKBLUE + "**********************************************" + bcolors.OKBLUE)
        print(bcolors.OKBLUE + "Appointment information has been stored in database" + bcolors.OKBLUE)
        print(bcolors.OKBLUE + "**********************************************" + bcolors.OKBLUE)
        staff_input = input("""
        Select one of the following.
        1) To Continue
        2) Sign Out
        3) Exit
        """)
        if (staff_input == 1):
            get_staff_choice()
        elif (staff_input == 2):
            sign_out()
        elif (staff_input == 3):
            exit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Inserting Appointment Information: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def select_patient(patient_data):
    patient_ids = []
    print(bcolors.WARNING + "List of Patient" + bcolors.ENDC)
    print(bcolors.WARNING + "**********************************************" + bcolors.ENDC)
    # for patient in patient_data:
    for index in range(len(patient_data)):
        patient = patient_data[index]
        patient_ids.append(patient[0])
        print("{} - First name = {}, Last name = {}".format(index +1 , patient[1], patient[2]))

    while True:
        try:
            number = int(raw_input("Select Patient number from above list: "))
            if number not in range(1,len(patient_data) + 1):
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
                print(bcolors.FAIL + "Please select the number from the above list only" + bcolors.ENDC)
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            else:
                break
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Input, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return patient_data[number-1][0]


def retrieve_patient_data_by_firstName():
    while True:
        try:
            firstName = taking_firstName_for_search("patient")
            connection = sqlite3.connect('Clinic.db')
            cursor = connection.cursor()
            patient_query = """SELECT *
                               FROM patient
                               WHERE First_name LIKE '%{}%'""".format(firstName)
            cursor.execute(patient_query)
            patient_rows = cursor.fetchall()
            if len(patient_rows) == 0:
                print("No data found. Please try again")
            else:
                break
        except:
            error = sys.exc_info()
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Error while retrieving patient info: ", error, "" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        finally:
            if connection:
                connection.close()
    return patient_rows

def taking_firstName_for_search(keyword):
    print(bcolors.WARNING + "Finding " +keyword+" information by First Name to book an appointment/visit" + bcolors.ENDC)
    while True:
        try:
            FirstName = raw_input("Type "+keyword+" First Name: ")
            if len(FirstName) > 0:
                break
            else:
                raise ValueError
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid First Name, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return FirstName

def select_doctor(doctor_data):
    doctor_ids = []
    print(bcolors.WARNING + "List of Doctors" + bcolors.ENDC)
    print(bcolors.WARNING + "**********************************************" + bcolors.ENDC)
    #for patient in doctor_data:
    for index in range(len(doctor_data)):
        doctor = doctor_data[0]
        print("{} - First name = {}, Last name = {}".format(index + 1, doctor[1], doctor[2]))
    while True:
        try:
            number = int(raw_input("Select Doctor Number from above list: "))
            if number not in range(1,len(doctor_data)+1):
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
                print(bcolors.FAIL + "Please select number from the above list only." + bcolors.ENDC)
                print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            else:
                break
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Input, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return doctor_data[number-1][0]


def retrieve_doctor_data_by_firstName():
    while True:
        try:
            firstName = taking_firstName_for_search("doctor")
            connection = sqlite3.connect('Clinic.db')
            cursor = connection.cursor()
            doctor_query = """SELECT *
                               FROM DOCTOR
                               WHERE First_name LIKE '%{}%'""".format(firstName)
            cursor.execute(doctor_query)
            doctor_rows = cursor.fetchall()
            if len(doctor_rows) == 0:
                print("No data found. Please try again")
            else:
                break
        except:
            error = sys.exc_info()
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Error while retrieving Doctor info: ", error, "" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        finally:
            if connection:
                connection.close()
    return doctor_rows


def take_datetime():
    regex_datetime = '(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})'
    while True:
        try:
            datetime = raw_input("Type Date and Time(Format : YYYY-MM-DD HH:MM): ")
            if re.match(regex_datetime, datetime):
                break
            else:
                raise ValueError
        except ValueError:
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
            print(bcolors.FAIL + "Invalid Datetime, Please Try Again" + bcolors.ENDC)
            print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    return datetime


def add_new_visit():
    patient_data = retrieve_patient_data_by_firstName()
    patient_id = select_patient(patient_data)
    appointment = show_appointment_by_patientid(patient_id)
    appointment_rows = find_appointment(patient_id, appointment)
    appointment_id = appointment_rows[0]

    try:
        connection = sqlite3.connect('Clinic.db')
        cursor = connection.cursor()
        visit_query = """INSERT INTO VISIT(Patient_ID, Appointment_ID, Apt_DateTime, Payment_Amount)
                                       VALUES("{}", "{}", "{}","{}")
                                                  """.format(patient_id,
                                                             appointment_id, appointment[3], appointment[11])
        cursor.execute(visit_query)
        visit_id = cursor.lastrowid
        connection.commit()
        add_new_prescription(patient_id,visit_id)

        print(bcolors.OKBLUE + "**********************************************" + bcolors.OKBLUE)
        print(bcolors.OKBLUE + "Visit and Prescription information has been stored in database" + bcolors.OKBLUE)
        print(bcolors.OKBLUE + "**********************************************" + bcolors.OKBLUE)
        staff_input = input("""
            Select one of the following.
            1) To Continue
            2) Sign Out
            3) Exit
            """)
        if (staff_input == 1):
            get_staff_choice()
        elif (staff_input == 2):
            sign_out()
        elif (staff_input == 3):
            exit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Inserting Visit Information: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()


def add_new_prescription(patient_id,visit_id):
    try:
        connection = sqlite3.connect('Clinic.db')
        cursor = connection.cursor()
        prescription = raw_input("Add prescription for the recent visit: ")

        add_prescription_query = """INSERT INTO PRESCRIPTION(Patient_ID, Visit_ID, Prescription_Details)
                                               VALUES("{}", "{}", "{}")
                                                          """.format(patient_id,
                                                                     visit_id,prescription)
        cursor.execute(add_prescription_query)
        connection.commit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error While Inserting Prescription Information: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()

def show_appointment_by_patientid(patient_id):
    connection = sqlite3.connect('Clinic.db')
    cursor = connection.cursor()
    appointment_query = """SELECT *
                               FROM APPOINTMENT AP JOIN Doctor D on AP.Doctor_ID = D.Doctor_ID 
                               WHERE Patient_ID = {} order by AP.Created_at DESC""".format(patient_id)
    cursor.execute(appointment_query)
    appointment_rows = cursor.fetchall()
    print("Following is the appointment detail")
    print("Date - {} , Doctor Name - {} , Fees - {}".format(appointment_rows[0][3],
                                                            appointment_rows[0][6],appointment_rows[0][11]))
    return appointment_rows[0]

# def get_appointment_date_month():
#     while True:
#         try:
#             Date = int(raw_input("Type Appointment Date: "))
#             Month = int(raw_input("Type Appointment Month: "))
#             if (Date < 1 or Date > 31) or (Month < 1 or Month > 12):
#                 print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
#                 print(bcolors.FAIL + "Either Date(From 1 to 31) or Month(From 1 to 12) is not in range.Please try again" + bcolors.ENDC)
#                 print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
#             else:
#                 break
#         except ValueError:
#             print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
#             print(bcolors.FAIL + "Invalid Date/Month, Please Try Again" + bcolors.ENDC)
#             print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
#     return Date, Month


def find_appointment(patient_id, appointment):
    try:
        connection = sqlite3.connect('Clinic.db')
        cursor = connection.cursor()
        appointment_query = """SELECT *
                           FROM APPOINTMENT
                           WHERE Patient_ID = {} and Apt_DateTime LIKE '%{}%'""".format(patient_id, appointment[3])
        cursor.execute(appointment_query)
        appointment_rows = cursor.fetchall()
        if len(appointment_rows) == 0:
            print("No data found. Please try again")
            add_new_visit()
    except:
        error = sys.exc_info()
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
        print(bcolors.FAIL + "Error while retrieving appointment info: ", error, "" + bcolors.ENDC)
        print(bcolors.FAIL + "**********************************************" + bcolors.ENDC)
    finally:
        if connection:
            connection.close()
    return appointment_rows[0]


if __name__ == '__main__':
    print(bcolors.HEADER + "**********************************************" + bcolors.ENDC)
    print(bcolors.HEADER + "*****     Welcome TO WALK IN CLINIC      *****" + bcolors.ENDC)
    print(bcolors.HEADER + "**********************************************" + bcolors.ENDC)
    # drop_tables()
    run_db_migrations()
    start_application()
