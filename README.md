# cis6930sp24 -- Assignment0

## Name
Sourabh Rajashekar

## Assignment Description
This assignment involves writing a Python script to fetch a PDF file, extract incident data from the PDF, create a SQLite database, populate the database with the incidents, and then print counts of different types of incidents.

## How to install
To install the necessary dependencies, run the following command:

pip install argparse urllib sqlite3 PyMuPDF


## How to run
To run the script with the provided URL, use the following command:

python main.py --incidents https://www.normanok.gov/sites/default/files/documents/2024-01/2024-01-01_daily_incident_summary.pdf
## Functions
#### main.py
- `fetch_incidents(url)`: Downloads the PDF file from the given URL or opens the local file path. Returns the local path to the PDF file.
- `extract_incidents(pdf_path)`: Extracts incident data from the PDF at the given path. Returns a list of incidents.
- `create_db()`: Creates a SQLite database and returns the connection.
- `populate_db(conn, incidents)`: Populates the database with the given incidents.
- `print_nature_counts(conn)`: Prints counts of different types of incidents in the database.

## Database Development
The SQLite database is created with a single table named 'incidents'. Each row in the table represents an incident, with columns for the incident time, incident number, location, nature, and incident_ori.

## Bugs and Assumptions
- The `fetch_incidents` function assumes that the input is either a valid URL or a valid local file path.
- The `extract_incidents` function assumes that the PDF is structured in a certain way, with specific rectangles for each field.
- The `populate_db` function assumes that the incidents list is not empty.
- The `print_nature_counts` function assumes that the database has been populated with incidents.

## Demo
!Demo video
# cis6930sp24-assignment0
