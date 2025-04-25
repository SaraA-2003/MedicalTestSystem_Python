# Medical Test Management System (Python)

A Python-based system designed to manage patient medical test records with advanced filtering, summary reporting, and CSV import/export features.


##  Features

- Add new medical test types (e.g., BGT, LDL)
- Add new test records for patients
- Update existing patient test records or test types
- Filter medical test records by:
  - Patient ID
  - Test Name
  - Status (`completed`, `pending`, `reviewed`)
  - Date Range (Start and End Date)
  - Turnaround Time (in minutes)
  - Abnormal Results (outside defined value range)
- Generate textual summary reports including:
  - Filtered record details
  - Min/Max/Average test result values
  - Min/Max/Average turnaround times
- Export medical records to a CSV file
- Import medical records from a CSV file


## File Structure
```
medical_test_management/
├── main.py
├── medicalRecord.txt
├── medicalTest.txt
├── README.md
├── Report.pdf
```

## Data Files
- medicalRecord.txt: Stores individual test records for each patient

- medicalTest.txt: Stores metadata and normal range for each test

## ▶️ How to Run the Project

To run this project on your system, make sure you have the following:

### Requirements

- Python 3.x installed  
  Download it from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

- Or use a Python environment like:
  - VS Code
  - PyCharm
  - 
### Steps to Run

1. Clone or download this repository to your local machine.
2. Ensure `main.py`, `medicalRecord.txt`, and `medicalTest.txt` are in the same folder.
3. Open a terminal or command prompt in that folder.
4. Run the following command:
```
python main.py
```
or 
If your system uses python3, then run:
```
python3 main.py
```
