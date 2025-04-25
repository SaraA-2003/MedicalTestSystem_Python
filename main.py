# Shiyar Mohammad - 1210766 - sec: 3
# Sara Allahaleh  - 1211083 - sec: 5
import csv
import re
from datetime import datetime


#patients class
class Patient:
    def __init__(self, Patient_ID):
        self.Patient_ID = Patient_ID
        self.Patient_data = []

    def addNewRecord(self, Tname,Tdate, result, unit, status, c_date = None):
        new_rec = {
            'test_name': Tname,
            'test_date': Tdate,
            'result': result,
            'unit': unit,
            'status': status,
            'comp_date': c_date
        }

        self.Patient_data.append(new_rec)

    def update_record(self, test_name, date_time, result, unit, status, Rdate_time=None):
        test_record = {
            'test_name': test_name,
            'date_time': date_time,
            'result': result,
            'unit': unit,
            'status': status,
            'Result date_time': Rdate_time
        }
        self.Patient_data.append(test_record)

#medical test class
class MedicalTest:
    def __init__(self, MedicalTest_name):
        self.MedicalTest_name = MedicalTest_name
        self.MedicalTest_data = []

    def add_newTest(self, abbrev, range1, unit, day, hour, min, range2=None):
        turnaround = f"{day}-{hour}-{min}"
        test_details = {
            'abbreviation': abbrev,
            'first range': range1,
            'second range': range2,
            'unit': unit,
            'turnaround': turnaround
        }
        self.MedicalTest_data.append(test_details)

    def upate_test(self, range, unit, turnaround):
        test_new = {
            'range': range,
            'unit': unit,
            'turnaround': turnaround
        }
        self.MedicalTest_data.append(test_new)

class Main:
    def __init__(self):
        self.main()

    #main process
    def main(self):
        # main loop
        while True:
            #load the patients
            patients = Main.load_patient_records(self)
            #load the medical tests
            medicalTests = Main.loadTests(self)
            Main.menu(self)
            choice = input("Please choose one operation:")

            if choice == '1':
                Main.addTypeTest(self)
            elif choice == '2':
                Main.addRecord(self)
            elif choice == '3':
                Main.update_patient(self, patients)
            elif choice == '4':
                Main.update_test(self)
            elif choice == '5':
                criteria = Main.choose_criteria(self)
                filtered_records = Main.filter_medicalRecords(self, patients, criteria, medicalTests)
                if not filtered_records:
                    print("\nTHERE IS NO RECORDS MATCH THE SELECTED CRITERIA.")
                else:
                    print("\nFILTERED RECORDS:\n")
                    for patient_id, test in filtered_records:
                        print (f"Patient ID: {patient_id}, Test Name: {test['test_name']}, Test DateTime: {test['test_datetime']}, Result: {test['result_value']} {test['result_unit']}, Status: {test['status']}, Result DateTime: {test['result_datetime']}")
            elif choice == '6':
                criteria = Main.choose_criteria(self)
                filtered_records = Main.filter_medicalRecords(self,patients,criteria,medicalTests)
                calc = Main.calculat_vals(self,filtered_records)
                report = Main.get_report(self, filtered_records,calc)
                print(report)
            elif choice == '7':
                Main.ExportToCSV(self)
            elif choice == '8':
                Main.import_records(self)
            elif choice == '9':
                print("\nThank you")
                break
            else:
                print("\n\tInvalid choice. Please enter a number between 1 and 9\n")

# **************************************************************************
    # function to display menu
    def menu(self):
        print("\nChoose an operation:")
        print("1) Add new medical test.")
        print("2) Add new medical test record.")
        print("3) Update patient records.")
        print("4) Update medical tests.")
        print("5) Filter medical tests.")
        print("6) Generate textual summary reports.")
        print("7) Export medical records to a comma separated file.")
        print("8) Import medical records from a comma separated file.")
        print("9) Exit.")

# **************************************************************************

    # function to load the tests data from the file
    def loadTests(self):
        medicalTests = {}
        filename = "medicalTest.txt"
        with open(filename, "r") as file:
            for line in file:
                # remove white spaces
                line = line.strip()

                if line:
                    # extract the line
                    fullName, range, unit, turnaround = line.split('; ')

                    # take just the observiation of the name
                    name = fullName.split('(')[-1].replace(')', '')
                    range = range.replace('Range: ', '').split(',')
                    if len(range) == 1:  # have just one result
                        if '>' in range[0]:
                            test_low = float(range[0].replace('>', ''))
                            test_high = None
                        elif '<' in range[0]:
                            test_low = None
                            test_high = float(range[0].replace('<', ''))
                    else:
                        # this mean I have two results
                        test_low = float(range[0].replace('>', '').strip())
                        test_high = float(range[1].replace('<', '').strip())

                    # store the test record to thhe dictionary
                    medicalTests[name] = {
                        "range": (test_low, test_high),
                        "unit": unit.replace('Unit: ', ''),
                        "turnaround": turnaround
                    }
        return medicalTests

# **************************************************************************

    #function to load patients records and store them in dictionary
    def load_patient_records(self):
        records = {}

        with open("medicalRecord.txt", 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    # Split the line into patient ID and the rest of the record
                    parts = line.split(': ')

                    if len(parts) != 2:
                        print(f"Skipping line due to unexpected format: {line}")
                        continue

                    patient_id = parts[0].strip()
                    rest_of_record = parts[1].strip()

                    # Split the rest of the record into individual fields
                    record_parts = rest_of_record.split(', ')

                    if len(record_parts) < 5:
                        print(f"Skipping line due to insufficient parts: {line}")
                        continue

                    test_name = record_parts[0].strip()
                    test_datetime = record_parts[1].strip()
                    result_value = record_parts[2].strip()
                    result_unit = record_parts[3].strip()

                    # Determine the status and optional result datetime
                    if len(record_parts) == 5:
                        status = record_parts[4].strip()
                        result_datetime = None
                    elif len(record_parts) == 6:
                        status = record_parts[4].strip()
                        result_datetime = record_parts[5].strip()
                    else:
                        print(f"Skipping line due to unexpected format: {line}")
                        continue

                    # Create the test record
                    test_record = {
                        'test_name': test_name,
                        'test_datetime': test_datetime,
                        'result_value': result_value,
                        'result_unit': result_unit,
                        'status': status,
                        'result_datetime': result_datetime
                    }

                    # Add the record to the dictionary
                    if patient_id not in records:
                        records[patient_id] = []
                    records[patient_id].append(test_record)

        return records

#*************************************************************************
    def addTypeTest(self):
        # entered the test type name and check if its contains only char
        while True:
            typeN = input("\nPlease enter the name of the new type of medical test: ")
            if typeN.replace(" ", "").isalpha():
                break  # Exit the loop if the name is correct
            else:
                print("\nThe name contains numbers or other characters. Please try again.")
        # entered the test type abbreviation and check if its contains only char
        while True:
            abbrev = input("\nPlease enter the abbreviation of the new type of medical test: ")
            if abbrev.isalpha():
                break  # Exit the loop if the abbreviation is correct
            else:
                print("\nThe abbreviation contains numbers or other characters. Please try again.")
        # large loop
        while True:
            checkR = input("\nDoes this test have one (1) or two (2) ranges? ")
            if checkR == "1":
                while True:
                    range = input("\nPlease enter the normal range of the new type of medical test: ")
                    pattern = r'^\d*\.?\d+$'
                    if re.match(pattern, range):
                        break  # Exit the loop if the range is correct
                    else:
                        print(
                            "\nThe Range contains letters or other characters than decimal point. Please try again.")
                break  # out of large loop

            elif checkR == "2":
                while True:
                    while True:
                        range1 = input(
                            "\nPlease enter the first normal range (the smallest) of the new type of medical test: ")
                        pattern = r'^\d*\.?\d+$'
                        # check if the number is integer or float
                        if re.match(pattern, range1):
                            break  # Exit the loop if the range is correct
                        else:
                            print(
                                "\nThe Range contains letters or other characters than decimal point. Please try again.")

                    while True:
                        range2 = input(
                            "\nPlease enter the second normal range (the largest) of the new type of medical test: ")
                        pattern = r'^\d*\.?\d+$'
                        # check if the number is integer or float
                        if re.match(pattern, range2):
                            break  # Exit the loop if the range is correct
                        else:
                            print(
                                "\nThe Range contains letters or other characters than decimal point. Please try again.")
                    # check if the range 1 is less than rang 2
                    if range1 >= range2:
                        print("\nThe first range is greater than or equal to the second range. Please try again.")
                    else:
                        break  # out of loop case 2

                break  # out of large loop
            else:
                print("\nInvalid number. Please try again.")
        # enter unit
        while True:
            unit = input("\nPlease enter the unit of the new type of medical test (can contains space or /): ")
            pattern = r'^[a-zA-Z\s/]+$'
            # check if the unit is valid
            if re.match(pattern, unit):
                break
            else:
                print("\nThe unit contains numbers or other characters besides `/` or spaces. Please try again.")
        print("\nThe time required to complete the test")
        # number of days
        while True:
            day = input("\nPlease enter the number of days needed to complete the test, in the format (DD): ")
            pattern = r'^\d{2}$'  # only 2 digits
            if re.match(pattern, day):
                break
            else:
                print("\nThe number of days is not in 2 digits format. Please try again.")

        # number of hours
        while True:
            hour = input("\nPlease enter the number of hours needed to complete the test, in the format (hh): ")
            pattern = r'^\d{2}$'  # only 2 digits
            if re.match(pattern, hour) and int(hour) >= 0 and int(hour) < 25:
                break
            else:
                print("\nThe number of hours is not in 2 digits format. Please try again.")
        # number of minutes
        while True:
            min = input("\nPlease enter the number of minutes needed to complete the test, in the format (mm): ")
            pattern = r'^\d{2}$'  # only 2 digits
            if re.match(pattern, min) and int (min) >= 0 and int(min) < 60:
                break
            else:
                print("\nThe number of minutes is not in 2 digits format. Please try again.")

        # add the new test to class MedicalTest

        if checkR == "1":
            newTest = MedicalTest(typeN)
            newTest.add_newTest(abbrev, range, unit, day, hour, min)
        if checkR == "2":
            newTest = MedicalTest(typeN)
            newTest.add_newTest(abbrev, range1, unit, day, hour, min, range2)

        # write on medicalTest.txt
        fo = open("medicalTest.txt", "a")
        if checkR == "1":
            fo.write(
                '\n' + "Name: " + typeN + " (" + abbrev + "); Range: < " + range + "; Unit: " + unit + "; " + day + "-" + hour + "-" + min)
        elif checkR == "2":
            fo.write(
                '\n' "Name: " + typeN + " (" + abbrev + "); Range: > " + range1 + ", < " + range2 + "; Unit: " + unit + "; " + day + "-" + hour + "-" + min)
        fo.close()
        print("\nTHE NEW TYPE OF MEDICAL TEST HAS BEEN ADDED SUCCESSFULLY!!\n")

    # ***************************************************************************

# **************************************************************************

    # function to check if the year is leap year to deal with days
    def isLeap(self,year):
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

# **************************************************************************

    # function to get the date
    def get_date(self):
        # get the date
        # first we will get the year
        while True:
            count_y = 0
            year = input("\n please enter the year - YYYY: ")
            if year.isdigit() and len(year) == 4:
                year = int(year)
                if year > 0 and year < 2025:
                    break
                else:
                    print("\nInvalid year. try again\n")
            else:
                print("\nInvalid . it should be YYYY.\n")

        # get the month
        while True:
            count_m = 0
            month = input("\n please enter the month - MM: ")
            if month.isdigit() and len(month) == 2:
                month = int(month)
                if month >= 1 and month <= 12:
                    break
                else:
                    print("\nInvalid month. try again\n")
            else:
                print("\nInvalid . it should be MM.\n")

        # get the day
        while True:
            count_d = 0
            day = input("\n please enter the day - DD: ")
            if day.isdigit() and len(day) == 2:
                day = int(day)
                if month in (1, 3, 5, 7, 8, 10, 12):
                    if day >= 1 and day <= 31:
                        break
                    else:
                        print("\nInvalid it should be from 1 to 31\n")
                elif month in (4, 6, 9, 11):
                    if day >= 1 and day <= 30:
                        break
                    else:
                        print("\nInvalid it should be from 1 to 30\n")
                elif month == 2:
                    if Main.isLeap(self,year):
                        if day >= 1 and day <= 29:
                            break
                        else:
                            print("\nInvalid it should be from 1 to 29\n")
                    else:
                        if day >= 1 and day <= 28:
                            break
                        else:
                            print("\nInvalid it should be from 1 to 28\n")

            else:
                print("\nInvalid . it should be DD.\n")

        # get the time
        # get the hours
        while True:
            count_h = 0
            hours = input("\nPlease enter the hour - hh: ")
            if hours.isdigit() and len(hours) == 2:
                hours = int(hours)
                if hours >= 1 and hours <= 24:
                    break
                else:
                    print("\nInvalid it should be from 01 to 24\n")
            else:
                print("\nInvalid . it should be hh.\n")
        # get the minutes
        while True:
            count_min = 0
            minutes = input("\nPlease enter the minutes - mm: ")
            if minutes.isdigit() and len(minutes) == 2:
                minutes = int(minutes)
                if minutes >= 0 and minutes <= 59:
                    break
                else:
                    print("\nInvalid it should be from 00 to 59\n")
            else:
                print("\nInvalid . it should be mm.\n")
        final_date = f"{year:04d}-{month:02d}-{day:02d} {hours:02d}:{minutes:02d}"
        return final_date

#**************************************************************************

    # function to check the validity of the test result
    def isValid(self,res):
        try:
            int(res)
            return True
        except ValueError:
            try:
                float(res)
                return True
            except ValueError:
                return False

#***************************************************************************

    # function to add new Test
    def addRecord(self):
        # take the id and check the validity
        while True:
            P_ID = input("\nPlease enter the ID: ")
            count = 0
            # to check if i have just digits
            if P_ID.isdecimal():
                # to check the number of digits
                for i in P_ID:
                    count += 1
                if count == 7:
                    break
                else:
                    print("\nInavlid it should be 7 digits.\n")
            else:
                print("\nInvalid ID it should be integer.\n")
        patient = Patient(P_ID)
        # get the tests name
        medical_test = Main.loadTests(self)
        while True:
            tName = input("\n Please enter the test name: ")

            if tName in medical_test:
                break
            else:
                print("\nInvalid name. try again.\n")

        # get the date
        date_r = Main.get_date(self)

        # get the result
        while True:
            result = input("\nPlease enter the test result:")
            if Main.isValid(self,result):
                break
            else:
                print("\nInvalid . Try again\n")

        # get the unit
        unit = medical_test[tName]["unit"]

        # get the status

        while True:
            print("\nchoose a status:\n1)Pending\n2)Completed\n3)Reviewed")
            ch = input("Enter your choice:")
            if ch == '1':
                status = 'pending'
                final_line = f"{P_ID}: {tName}, {date_r}, {result}, {unit}, {status}"
                break
            elif ch == '2':
                status = 'completed'
                # get the date
                comp_date = Main.get_date(self)
                final_line = f"{P_ID}: {tName}, {date_r}, {result}, {unit}, {status}, {comp_date}"
                patient.addNewRecord(self, tName, date_r, unit, status, comp_date)
                break
            elif ch == '3':
                status = 'reviewed'
                final_line = f"{P_ID}: {tName}, {date_r}, {result}, {unit}, {status}"
                patient.addNewRecord(self, tName, date_r, unit, status)
                break
            else:
                print("\n\tInvalid choice. Please enter a number between 1 and 3\n")

        # append the new record to the file

        with open("medicalRecord.txt", 'a') as file:

            file.write(final_line + '\n')

        print("\nRECORD HAS BEEN ADDED SUCCESSFULLY.\n")

# ***************************************************************************

    # Update Patient records
    def update_patient(self, patients):
        while True:
            PID = input("\nPlease enter the ID of the patient whose records you want to modify: ")
            if re.fullmatch(r'\d{7}', PID):
                if PID in patients:
                    break
                else:
                    print("\nThis PID does not exist. Please try again.")
            else:
                print("\nThe ID must be 7 digits long and contain only digits. Please try again.")
        print("\n")
        i = 1
        for test in patients[PID]:
            # Extract and print the values from each dictionary for PID
            print(
                f"{i}) {test['test_name']}, {test['test_datetime']}, {test['result_value']}, {test['result_unit']}, {test['status']}, {test['result_datetime']}")
            i += 1

        while True:
            choice = input("\nChoose the line you want to modify its records: ")
            if choice.isdigit():
                if int(choice) > 0 and int(choice) <= i:
                    break
                else:
                    print("\nInvalid choice. Please try again.")

        index = 1
        # find the choosen record to do operataion on it
        for test in patients[PID]:
            if index == int(choice):
                record = patients[PID][index - 1]
                recordr = f"{test['test_name']}, {test['test_datetime']}, {test['result_value']}, {test['result_unit']}, {test['status']}, {test['result_datetime']}"
                break
            else:
                index += 1

        # --------------------------prepare for file update--------------------------------
        # remove null so we can compare the chosen line and the lines from the file
        if record['result_datetime'] is None:
            recordr = f"{test['test_name']}, {test['test_datetime']}, {test['result_value']}, {test['result_unit']}, {test['status']}"
        lineNumber = 1
        with open("medicalRecord.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                # Strip any leading/trailing whitespace
                line = line.strip()

                # Split the line at the first colon and get the part after the colon
                if ':' in line:
                    _, data = line.split(':', 1)
                    # Print the data without the patient ID
                    lineD = data.strip()  # remove PID from the line for comparison purpose
                if lineD == recordr:
                    break
                else:
                    lineNumber += 1  # increment line if it is not the index for the  chosen line
        # ---------------------------------------------------------------------------------------------

        # choose the field that we want to update
        while True:
            print(
                f"\n1) Test Name: {record['test_name']}\n2) Test date and time: {record['test_datetime']}\n3) Result: {record['result_value']}\n4) Unit: {record['result_unit']}"
                f"\n5) Status: {record['status']}\n6) Result date and time: {record['result_datetime']}")
            testName = record['test_name']
            date_time = record['test_datetime']
            Result = record['result_value']
            Unit = record['result_unit']
            Status = record['status']
            if record['result_datetime'] is None:
                Rdate_time = ''
            else:
                Rdate_time = record['result_datetime']

            ch = input("\nChoose the field you want to modify: ")
            # test name
            if ch == "1":
                # entered the test type abbreviation and check if its contains only char
                while True:
                    abbrev = input("\nPlease enter the abbreviation of the new type of medical test: ")
                    if abbrev.isalpha():
                        # update to file
                        if record['result_datetime'] is None:
                            new_value = f"{PID}: {abbrev}, {date_time}, {Result}, {Unit}, {Status}"
                        else:
                            new_value = f"{PID}: {abbrev}, {date_time}, {Result}, {Unit}, {Status}, {Rdate_time}"

                        lines[lineNumber - 1] = new_value + '\n'
                        with open("medicalRecord.txt", 'w') as file:
                            file.writelines(lines)
                        print("\n\n------The record has been updated successfully!!-----")
                        # update class patient
                        update_patient = Patient(PID)
                        update_patient.update_record(abbrev, date_time, Result, Unit, Status, Rdate_time)

                        break  # Exit the loop if the abbreviation is correct
                    else:
                        print("\nThe abbreviation contains numbers or other characters. Please try again.")
                break
            # date and time
            elif ch == "2":
                testDate = Main.checkDateT(self,record['result_datetime'])
                # update to file
                if record['result_datetime'] is None:
                    new_value = f"{PID}: {testName}, {testDate}, {Result}, {Unit}, {Status}"
                else:
                    new_value = f"{PID}: {testName}, {testDate}, {Result}, {Unit}, {Status}, {Rdate_time}"

                lines[lineNumber - 1] = new_value + '\n'
                with open("medicalRecord.txt", 'w') as file:
                    file.writelines(lines)
                print("\n\n------The record has been updated successfully!!-----")
                # update class patient
                update_patient = Patient(PID)
                update_patient.update_record(testName, testDate, Result, Unit, Status, Rdate_time)
                break

            # Result
            elif ch == "3":
                while True:
                    result = input("\nEnter the new result: ")
                    # Regular expression to check for valid integer or float
                    pattern = r'^\d+(\.\d+)?$'
                    # Check if the input matches the pattern
                    if re.match(pattern, result):
                        # update to file
                        if record['result_datetime'] is None:
                            new_value = f"{PID}: {testName}, {date_time}, {result}, {Unit}, {Status}"
                        else:
                            new_value = f"{PID}: {testName}, {date_time}, {result}, {Unit}, {Status}, {Rdate_time}"

                        lines[lineNumber - 1] = new_value + '\n'
                        with open("medicalRecord.txt", 'w') as file:
                            file.writelines(lines)
                        print("\n\n------The record has been updated successfully!!-----")
                        # update class patient
                        update_patient = Patient(PID)
                        update_patient.update_record(testName, date_time, result, Unit, Status, Rdate_time)
                        break
                    else:
                        print("\nInvalid result, it should be integer or float. Please try again.")
                break
            # unit
            elif ch == "4":
                while True:
                    unit = input("\nEnter the new unit(can contains space or /): ")
                    pattern = r'^[a-zA-Z\s/]+$'
                    # check if the unit is valid
                    if re.match(pattern, unit):
                        # update to file
                        if record['result_datetime'] is None:
                            new_value = f"{PID}: {testName}, {date_time}, {Result}, {unit}, {Status}"
                        else:
                            new_value = f"{PID}: {testName}, {date_time}, {Result}, {unit}, {Status}, {Rdate_time}"

                        lines[lineNumber - 1] = new_value + '\n'
                        with open("medicalRecord.txt", 'w') as file:
                            file.writelines(lines)
                        print("\n\n------The record has been updated successfully!!-----")
                        # update class patient
                        update_patient = Patient(PID)
                        update_patient.update_record(testName, date_time, Result, unit, Status, Rdate_time)

                        break
                    else:
                        print(
                            "\nThe unit contains numbers or other characters besides `/` or spaces. Please try again.")
                break

            # status
            elif ch == "5":
                while True:
                    status = input("\nEnter the status (pending, completed, reviewed): ")
                    if status != "pending" and status != "completed" and status != "reviewed":
                        print("\nInvalid status. Please try again.")

                    if status == "completed":
                        if record['result_datetime'] is None:
                            resultDate = Main.checkDate(self,record['test_datetime'])
                            # update to file
                            new_value = f"{PID}: {testName}, {date_time}, {Result}, {Unit}, {status}, {resultDate}"
                            lines[lineNumber - 1] = new_value + '\n'
                            with open("medicalRecord.txt", 'w') as file:
                                file.writelines(lines)
                            print("\n\n------The record has been updated successfully!!-----")
                            # update class patient
                            update_patient = Patient(PID)
                            update_patient.update_record(testName, date_time, Result, Unit, status, resultDate)
                            break
                        else:
                            # update to file
                            new_value = f"{PID}: {testName}, {date_time}, {Result}, {Unit}, {status}, {Rdate_time}"
                            lines[lineNumber - 1] = new_value + '\n'
                            with open("medicalRecord.txt", 'w') as file:
                                file.writelines(lines)
                            print("\n\n------The record has been updated successfully!!-----")
                            # update class patient
                            update_patient = Patient(PID)
                            update_patient.update_record(testName, date_time, Result, Unit, status, Rdate_time)
                            break
                    elif Status == "pending" or Status == "reviewed":
                        break
                    elif status == "pending" or status == "reviewed":
                        # update to file
                        new_value = f"{PID}: {testName}, {date_time}, {Result}, {Unit}, {status}"
                        lines[lineNumber - 1] = new_value + '\n'
                        with open("medicalRecord.txt", 'w') as file:
                            file.writelines(lines)
                        print("\n\n------The record has been updated successfully!!-----")
                        # update class patient
                        update_patient = Patient(PID)
                        update_patient.update_record(testName, date_time, Result, Unit, status)
                        break
                break

            # resultDate
            elif ch == "6":
                while True:
                    if record['status'] == "pending" or record['status'] == "reviewed":
                        print("\nInvalid operation. You cannot enter a result date for an incomplete test.")
                        break
                    elif record['status'] == "completed":
                        resultDate1 = Main.checkDate(self,record['test_datetime'])
                        # update to file
                        new_value = f"{PID}: {testName}, {date_time}, {Result}, {Unit}, {Status}, {resultDate1}"
                        lines[lineNumber - 1] = new_value + '\n'
                        with open("medicalRecord.txt", 'w') as file:
                            file.writelines(lines)
                        print("\n\n------The record has been updated successfully!!-----")
                        # update class patient
                        update_patient = Patient(PID)
                        update_patient.update_record(testName, date_time, Result, Unit, Status, resultDate1)
                        break
                break
            else:
                print("invalid choice. Please try again")

# ***************************************************************************

    # ---------------------------FUNCTIONS-----------------------------
    def checkDate(self,testDate):
        date_object2 = datetime.strptime(testDate, "%Y-%m-%d %H:%M")
        # Extract components
        yearT = date_object2.year
        monthT = date_object2.month
        dayT = date_object2.day
        hourT = date_object2.hour
        minT = date_object2.minute

        while True:
            resultDate = Main.get_date(self)
            date_object1 = datetime.strptime(resultDate, "%Y-%m-%d %H:%M")
            # Extract components
            yearR = date_object1.year
            monthR = date_object1.month
            dayR = date_object1.day
            hourR = date_object1.hour
            minR = date_object1.minute

            if int(yearT) == int(yearR) and int(monthT) == int(monthR) and int(dayT) == int(dayR):
                if int(hourT) == int(hourR) and int(minT) == int(minR):
                    print(f"\nInvalid date, test date and time should not equal result date and time."
                          " Please try again.")
                elif int(hourT) == int(hourR) and int(minT) + 10 <= int(minR):
                    break
                elif int(hourT) < int(hourR):
                    break
                elif int(hourT) > int(hourR):
                    print(f"\nInvalid date, test hour should not be grater than result hour."
                          " Please try again.")
                elif int(minT) > int(minR):
                    print(f"\nInvalid date, test minutes should not be grater than result minutes."
                          " Please try again.")


            elif int(yearT) == int(yearR) and int(monthT) == int(monthR) and int(dayT) != int(dayR):
                if int(dayT) < int(dayR):
                    break
                else:
                    print("\nInvalid date, test day should not be greater than result day. "
                          "Please try again.")
            elif int(yearT) == int(yearR) and int(monthT) != int(monthR):
                if int(monthT) < int(monthR):
                    break
                else:
                    print("\nInvalid date, test month should not be greater than result month. "
                          "Please try again.")
            elif int(yearT) < int(yearR):
                break
            else:
                print("\nInvalid date, test year should not be greater than result year. "
                      "Please try again.")

        return resultDate

# ***************************************************************************

    def checkDateT(self,resultDate):
        date_object2 = datetime.strptime(resultDate, "%Y-%m-%d %H:%M")
        # Extract components
        yearR = date_object2.year
        monthR = date_object2.month
        dayR = date_object2.day
        hourR = date_object2.hour
        minR = date_object2.minute

        while True:
            TestDate = Main.get_date(self)
            date_object1 = datetime.strptime(TestDate, "%Y-%m-%d %H:%M")
            # Extract components
            yearT = date_object1.year
            monthT = date_object1.month
            dayT = date_object1.day
            hourT = date_object1.hour
            minT = date_object1.minute

            if int(yearT) == int(yearR) and int(monthT) == int(monthR) and int(dayT) == int(dayR):
                if int(hourT) == int(hourR) and int(minT) == int(minR):
                    print(f"\nInvalid date, test date and time should not equal result date and time."
                          " Please try again.")
                elif int(hourT) == int(hourR) and int(minT) + 10 <= int(minR):
                    break
                elif int(hourT) < int(hourR):
                    break
                elif int(hourT) > int(hourR):
                    print(f"\nInvalid date, test hour should not be grater than result hour."
                          " Please try again.")
                elif int(minT) > int(minR):
                    print(f"\nInvalid date, test minutes should not be grater than result minutes."
                          " Please try again.")


            elif int(yearT) == int(yearR) and int(monthT) == int(monthR) and int(dayT) != int(dayR):
                if int(dayT) < int(dayR):
                    break
                else:
                    print("\nInvalid date, test day should not be greater than result day. "
                          "Please try again.")
            elif int(yearT) == int(yearR) and int(monthT) != int(monthR):
                if int(monthT) < int(monthR):
                    break
                else:
                    print("\nInvalid date, test month should not be greater than result month. "
                          "Please try again.")

            elif int(yearT) < int(yearR):
                break
            else:
                print("\nInvalid date, test year should not be greater than result year. "
                      "Please try again.")

        return TestDate

    # ***************************************************************************

# ***************************************************************************

    def update_test(self):
        medicalTests = Main.loadTests(self)
        while True:
            name = input("\n Please enter the test name to update:")

            # read the file and search for the test
            with open("medicalTest.txt", "r") as file:
                lines = file.readlines()
            # flag to check if the name is exist
            found = False
            for i, line in enumerate(lines):
                if f"({name})" in line:
                    found = True
                    print("\n Test found: ", line.strip())

                    while True:

                        # Ask ghe user to choose the feild
                        choice = input(
                            "\nWhat do you want to update?\n1-range\n2-Unit\n3-Turnaround time\n4-Exit\nEnter your choice: ")

                        if choice == '1':
                            lines[i] = Main.update_ranges(self, line, name)
                        elif choice == '2':
                            lines[i] = Main.update_unit(self, line)
                        elif choice == '3':
                            lines[i] = Main.update_turnaround(self, line)
                        elif choice == '4':
                            break
                        else:
                            print("\nInvalid choice.choose from 1 -4 ")

                    updated_line = line[i].strip()
                    parts = updated_line.split("; ")

                    #take each attribute
                    test_name = parts[0].replace("Name: ","").strip()
                    test_range = parts[1].replace("Range: ", "").strip()
                    test_unit = parts[2].replace("Unit: ", "").strip()
                    test_turn = parts[3].strip()

                    updated_test = MedicalTest(test_name)
                    updated_test.upate_test(self, test_range, test_unit, test_turn)

            if not found:
                print("\nTest not found. Try again.\n")
            else:
                # write updated lines
                with open("medicalTest.txt", 'w') as file:
                    file.writelines(lines)
                    break
        print("\nTEST HAS BEEN UPDATED SUCCESSFULLY!!\n")

# ***************************************************************************

    def update_ranges(self,line, name):

        # split the range
        start = line.find("Range: ")
        end = line.find(";", start)
        current_range = line[start + 7:end].strip()

        if ", <" in current_range:  # check if there is two values
            print(f"Current range for {name}: {current_range}")
            while True:
                new_range_l = input("Enter the new lower range value: ")
                if Main.isValid(self, new_range_l):
                    break
                else:
                    print("\nInvalid input. try again.\n")
            while True:
                new_range_h = input("Enter the new upper range value: ")
                if Main.isValid(self,new_range_h):
                    break
                else:
                    print("\nInvalid input. try again.\n")

            new_range = f"> {new_range_l}, < {new_range_h}"

        else:  # only one value
            print(f"Current range for {name}: {current_range}")

            operator = current_range[0]
            value = current_range[2:]

            while True:

                new_range_v = input("Enter the new range value: ")
                if Main.isValid(self, new_range_v):
                    break
                else:
                    print("\nInvalid input. try again.\n")

            new_range = f"{operator} {new_range_v}"

        # set the updated line
        updated_line = line[:start + 7] + new_range + line[end:]
        return updated_line

# ***************************************************************************

    def update_unit(self, line):
        while True:
            unit = input("\nPlease enter the unit of the new type of medical test (can contains space or /): ")
            pattern = r'^[a-zA-Z\s/]+$'
            # check if the unit is valid
            if re.match(pattern, unit):
                break
            else:
                print("\nThe unit contains numbers or other characters besides `/` or spaces. Please try again.")

        start = line.find("Unit: ")
        end = line.find(";", start)

        updated_line = line[:start + 6] + unit + line[end:]
        return updated_line

# ***************************************************************************

    def update_turnaround(self, line):
        start = line.find("; ", line.find("Unit: ")) + 2
        current_time = line[start:].strip()

        # split the turnaround
        day, hour, min = current_time.split("-")

        while True:
            choice = input("\nWhat do you want to update?\n1-Days\n2-Hours\n3-Minutes\n4-Exit\nEnter your choice: ")

            if choice == '1':
                while True:
                    day = input("\nPlease enter the number of days needed to complete the test, in the format (DD): ")
                    pattern = r'^\d{2}$'  # only 2 digits
                    if re.match(pattern, day):
                        break
                    else:
                        print("\nThe number of days is not in 2 digits format. Please try again.")
            elif choice == '2':
                # number of hours
                while True:
                    hour = input("\nPlease enter the number of hours needed to complete the test, in the format (hh): ")
                    pattern = r'^\d{2}$'  # only 2 digits
                    if re.match(pattern, hour):
                        break
                    else:
                        print("\nThe number of hours is not in 2 digits format. Please try again.")
            elif choice == '3':
                # number of minutes
                while True:
                    min = input(
                        "\nPlease enter the number of minutes needed to complete the test, in the format (mm): ")
                    pattern = r'^\d{2}$'  # only 2 digits
                    if re.match(pattern, min):
                        break
                    else:
                        print("\nThe number of minutes is not in 2 digits format. Please try again.")
            elif choice == '4':
                break
            else:
                print("\nInvalid choice.Try again.\n")

        new_time = f"{day.zfill(2)}-{hour.zfill(2)}-{min.zfill(2)}"
        updated_line = line[:start] + new_time
        return updated_line

# ***************************************************************************



# ***************************************************************************
    #----------- implement textual reports------------------------
    def filter_medicalRecords(self, records,criteria,medicalTests):

        filtered_record = [] #list to store filtered records

        for patient_id ,tests in records.items():
            for test in tests:
                match = True #flag to determine if the record match or not

                #filter according to the id
                if "patient_id" in criteria:
                    if patient_id != criteria["patient_id"]:
                        match = False

                #filter according to the test name
                if "test_name" in criteria:
                    if test["test_name"] != criteria["test_name"]:
                        match = False

                #filter according to status
                if "status" in criteria:
                    if test["status"].lower() != criteria["status"].lower():
                        match = False

                #filter according to the period
                if "start_date" in criteria:
                    test_datetime = datetime.strptime(test["test_datetime"], "%Y-%m-%d %H:%M")
                    if test_datetime < criteria["start_date"]:
                        match = False

                if "end_date" in criteria:
                    test_datetime = datetime.strptime(test["test_datetime"], "%Y-%m-%d %H:%M")
                    if test_datetime > criteria["end_date"]:
                        match = False

                #filter according to the turnaround period
                if "min_turnaround" in criteria:
                    if test["status"] == "completed" and test["result_datetime"]:
                        result_datetime = datetime.strptime(test["result_datetime"], "%Y-%m-%d %H:%M")
                        test_datetime = datetime.strptime(test["test_datetime"], "%Y-%m-%d %H:%M")
                        turnaround_time = (result_datetime - test_datetime).total_seconds() / 60

                        if turnaround_time < criteria ["min_turnaround"]:
                            match =False
                    else:
                        match = False

                if "max_turnaround" in criteria:
                    if test["status"] == "completed" and test["result_datetime"]:
                        result_datetime = datetime.strptime(test["result_datetime"], "%Y-%m-%d %H:%M")
                        test_datetime = datetime.strptime(test["test_datetime"], "%Y-%m-%d %H:%M")
                        turnaround_time = (result_datetime - test_datetime).total_seconds() / 60

                        if turnaround_time > criteria["max_turnaround"]:
                            match = False
                    else:
                        match = False


                #check for abnormal
                if "abnormal" in criteria and match:
                    test_name = test["test_name"]
                    if test_name in medicalTests:

                        test_record = medicalTests[test_name]
                        test_low, test_high = test_record["range"]
                        if test_low is None:
                            test_low = 0
                        else:
                            test_low = float(test_low)
                        if test_high is None:
                            test_high = 0
                        else:
                            test_high = float(test_high)
                        try:
                            result_value = float(test["result_value"])
                            if result_value <= test_low or result_value >= test_high:
                                match = True #it is abnormal
                            else:
                                match = False
                        except ValueError:
                            print("\nInvalid\n")
                            match = False

                if match:
                    filtered_record.append((patient_id,test))
        return filtered_record

    #***************************************************
    #function to calculate the needed data for the report

    def calculat_vals(self, filtered_records):
        test_values = [] #list to store values
        turnaround_times = [] #list to store turnarounds

        for record in filtered_records:
            try:
                result_value = float(record[1]["result_value"])
                test_values.append(result_value)

            except ValueError:
                print("\nCan not convert\n")
                continue

            if record[1]["status"].lower() == "completed" and record[1]["result_datetime"]:
                result_datetime = datetime.strptime(record[1]["result_datetime"], "%Y-%m-%d %H:%M")
                test_datetime = datetime.strptime(record[1]["test_datetime"], "%Y-%m-%d %H:%M")
                turnaround_time = (result_datetime - test_datetime).total_seconds() / 60
                turnaround_times.append(turnaround_time)

        if test_values:
            min_test_value = min(test_values)
            max_test_value = max(test_values)
            avg_test_value = sum(test_values) / len(test_values)
        else:
            min_test_value = None
            max_test_value = None
            avg_test_value = None

        if turnaround_times:

            min_turnaround = min(turnaround_times)
            max_turnaround = max(turnaround_times)
            avg_turnaround = sum(turnaround_times) / len(turnaround_times)
        else:
            min_turnaround = None
            max_turnaround = None
            avg_turnaround = None

        calcultions = {
                'min_test_value': min_test_value,
                'max_test_value': max_test_value,
                'avg_test_value': avg_test_value,
                'min_turnaround_time': min_turnaround,
                'max_turnaround_time': max_turnaround,
                'avg_turnaround_time': avg_turnaround
            }

        return calcultions

    #***********************************************
    def get_report(self, filtered_record, calculations):
        if not filtered_record:
            return "\nTHERE IS NO RECORDS MATCH THE SELECTED CRITERIA."

        report = "\n-----SUMMARY REPORT-----\n"
        report += "\nFILTERED RECORDS:\n"
        for patient_id, test in filtered_record:
            report += (f"Patient ID: {patient_id}, Test Name: {test['test_name']}, Test DateTime: {test['test_datetime']}, Result: {test['result_value']} {test['result_unit']}, Status: {test['status']}, Result DateTime: {test['result_datetime']}\n")


        #add calculations
        report += "\nCALCULATIONS:\n"
        report += f"Minimum Test Value: {calculations['min_test_value']}\n"
        report += f"Maximum Test Value: {calculations['max_test_value']}\n"
        report += f"Average Test Value: {calculations['avg_test_value']}\n"
        report += f"Minimum Turnaround Time: {calculations['min_turnaround_time']} minutes\n"
        report += f"Maximum Turnaround Time: {calculations['max_turnaround_time']} minutes\n"
        report += f"Average Turnaround Time: {calculations['avg_turnaround_time']} minutes\n"

        return report

# ***************************************************************************
    #function to choose the criteria
    def choose_criteria(self):
        criteria = {}
        turnaround_selected = False
        medical = Main.loadTests(self)
        while True:
            print("\nSelect criteria to filter records:")
            print("1. Filter by patient ID")
            print("2. Filter by test name")
            print("3. Filter by status")
            print("4. Filter by date range")
            print("5. Filter by turnaround time")
            print("6. Filter by abnormal results")

            choice = input("Enter your choices(seperated by ','): ").split(',')
            in_valid = False
            for ch in choice:
                if ch not in ('1', '2', '3', '4', '5', '6'):
                    in_valid = True
                    print("\nInvalid choice:", ch)

            if in_valid:
                print("\nChoose from these criteria.\n")
            else:
                break

        for op in choice:
            op = op.strip()
            if op == '1':
                while True:
                    id = input("\nEnter Patient ID: ").strip()
                    if id.isdigit() and len(id) == 7:
                        break
                    else:
                        print("Invalid . Try again.\n")

                criteria["patient_id"] = id
            elif op == '2':
                while True:
                    name = input("Enter Test Name: ").strip()

                    if name in medical:
                        break

                    else:
                        print("Invalid. Try again\n")
                criteria["test_name"] = name

            elif op == '3':
                while True:
                    status = input("Enter status - completed/pending/reviewed: ").strip()
                    if status in ('completed','pending','reviewed'):
                        break
                    else:
                        print("Invalid.Try again.\n")

                criteria["status"] = status

            elif op == '4':
                print("Enter the start Date:\n")
                start_d = Main.get_date(self).strip()
                print("\nEnter the end Date:")
                end_d = Main.get_date(self).strip()


                criteria["start_date"] = datetime.strptime(start_d, "%Y-%m-%d %H:%M")
                criteria["end_date"] = datetime.strptime(end_d, "%Y-%m-%d %H:%M")

            elif op == '5':
                while True:
                    min_t = input("Enter minimum turnaround time in minutes: ").strip()

                    if Main.isValid(self, min_t):
                        break
                    else:
                        print("\nInvalid.Try again.\n")
                while True:
                    max_t = input("Enter maximum turnaround time in minutes: ").strip()

                    if Main.isValid(self, max_t):
                        break
                    else:
                        print("\nInvalid.Try again.\n")

                min_t = float(min_t)
                max_t = float(max_t)

                criteria["min_turnaround"] = min_t
                criteria["max_turnaround"] = max_t
                turnaround_selected = True

            elif op == '6':
                criteria["abnormal"] = True

        if turnaround_selected and "status" not in criteria:
            criteria["status"] = "completed"

        return criteria

    #*********************************

    # Export medical record to csv
    def ExportToCSV(self):
        while True:
            fileName = input("\nPlease enter the file name .csv:")
            try:
                f = open(fileName, "w")
                break
            except IOError:
                print("\nERROR OPENNING FILE!!!\n")
        try:
            f1o = open("medicalRecord.txt", 'r')
            f2o = open(fileName, 'w', newline='')
            # Initialize CSV writer
            writer = csv.writer(f2o)

            # write header
            writer.writerow(['Record ID', 'Test Type', 'Date and Time', 'Value', 'Unit', 'Status', 'Completion Time'])

            for line in f1o:
                # Strip any whitespace and split the line by commas
                records = [record.strip() for record in line.strip().split(',')]

                # Split the first part by colon to separate PatientID and TestName
                PID, testType = records[0].split(':', 1)
                PID = PID.strip()
                testT = testType.strip()

                # Handle cases where time completion does not exist
                if len(records) == 6:
                    # If completion time does not exist, append an empty string for it
                    records.append('')

                # Ensure that we have 7 elements
                row = [PID, testType] + records[1:]

                # Write row to CSV file
                writer.writerow(row)
        except Exception as e:
            print(f"An error occurred: {e}")
        print("\n-------Export medical records to CSV has be completed successfully!!-------\n")

# ***************************************************************************

    # function to import records from a comma separated file
    def import_records(self):
        # check if file exists
        while True:
            fileName = input("\nPlease enter the file name .csv:")
            try:
                f = open(fileName, "r")
                break
            except IOError:
                print("\nFile not found!!!\n")

        new_records = []

        with open(fileName, 'r') as comma_file:
            file_read = csv.reader(comma_file)

            # skip the header
            next(file_read)

            # main proccess
            for line in file_read:
                if len(line) == 6:
                    id, test_name, test_date, result, unit, status = line[:6]
                    record = f"{id}: {test_name}, {test_date}, {result}, {unit}, {status}"
                    new_records.append(record)
                elif len(line) > 6:
                    id, test_name, test_date, result, unit, status = line[:6]
                    comp_date = line[6]
                    record = f"{id}: {test_name}, {test_date}, {result}, {unit}, {status}, {comp_date}"
                    new_records.append(record)

            # save the records to medical records file
        with open("medicalRecord.txt", 'a') as dest_file:
            for rec in new_records:
                dest_file.write(rec + '\n')

        print("\nRECORDS IMPORTED SUCCESSFULLY FROM THE COMMA SEPERATED FILE.\n")

main = Main()

#* ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *
