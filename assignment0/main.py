import argparse
import urllib.request
import sqlite3
import fitz  # PyMuPDF
import os


# Function to download the PDF file
def fetch_incidents(url):
    response = urllib.request.urlopen(url)
    file = response.read()
    pdf_path = '/tmp/incident_report.pdf'  # Temporary file path
    with open(pdf_path, 'wb') as f:
        f.write(file)
    return pdf_path


# Function to extract incident data from the PDF
def extract_incidents(pdf_path):
    doc = fitz.open(pdf_path)
    incidents = []
    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            block_rect = fitz.Rect(block[:4])

            # Define rectangles for each field dynamically
            rect_date_time = fitz.Rect(52.560001373291016, block_rect.y0, 150.86000061035156, block_rect.y1)
            rect_incident_number = fitz.Rect(150.86000061035156, block_rect.y0, 229.82000732421875, block_rect.y1)
            rect_location = fitz.Rect(229.82000732421875, block_rect.y0, 423.1900244140625, block_rect.y1)
            rect_nature = fitz.Rect(423.1900244140625, block_rect.y0, 623.8599853515625, block_rect.y1)

            # Extract text for each field
            date_time_text = page.get_text("text", clip=rect_date_time).strip()
            incident_number_text = page.get_text("text", clip=rect_incident_number).strip()
            location_text = page.get_text("text", clip=rect_location).strip()
            nature_text = page.get_text("text", clip=rect_nature).strip()

            if date_time_text and incident_number_text and location_text and nature_text:
                incidents.append((date_time_text, incident_number_text, location_text, nature_text,
                                  ""))  # "" as placeholder for incident_ori
    return incidents


# Function to create the SQLite database
def create_db():
    # Ensure the resources directory exists
    os.makedirs('resources', exist_ok=True)

    # Connect to the SQLite database within the resources directory
    db_path = os.path.join('resources', 'normandb.db')
    conn = sqlite3.connect(db_path)

    # Create the incidents table if it doesn't exist
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incidents (
                    incident_time TEXT,
                    incident_number TEXT,
                    incident_location TEXT,
                    nature TEXT,
                    incident_ori TEXT
                 )''')
    conn.commit()
    return conn


# Function to insert incidents into the database
def populate_db(conn, incidents):
    c = conn.cursor()
    for incident in incidents:
        try:
            c.execute('INSERT INTO incidents VALUES (?, ?, ?, ?, ?)', incident)
        except sqlite3.IntegrityError as e:
            print(f"Skipping duplicate incident: {incident}, error: {e}")
    conn.commit()


# Function to print nature counts
def print_nature_counts(conn):
    c = conn.cursor()
    c.execute("SELECT nature, COUNT(nature) FROM incidents GROUP BY nature ORDER BY COUNT(nature) DESC, nature")
    for row in c.fetchall():
        print(f"{row[0]}|{row[1]}")


# Main function to orchestrate the operations
def main(url):
    pdf_path = fetch_incidents(url)
    incidents = extract_incidents(pdf_path)
    db_conn = create_db()
    populate_db(db_conn, incidents)
    print_nature_counts(db_conn)
    db_conn.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary URL.")
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)