import unittest
import os
import sqlite3
from assignment0.main import extract_incidents, create_db, populate_db, print_nature_counts

class TestMainScript(unittest.TestCase):
    def setUp(self):
        self.test_pdf_path = "/Users/sourabhrajashekar/Desktop/cis6930sp24-assignment0/ex.pdf"  # Replace with your file path

    def test_extract_incidents(self):
        # Test the extract_incidents function
        incidents = extract_incidents(self.test_pdf_path)
        self.assertIsInstance(incidents, list)
        self.assertGreater(len(incidents), 0)

    def test_create_db(self):
        # Test the create_db function
        conn = create_db()
        self.assertIsInstance(conn, sqlite3.Connection)
        conn.close()  # Close the database connection

    def test_populate_db(self):
        # Test the populate_db function
        incidents = extract_incidents(self.test_pdf_path)
        conn = create_db()
        populate_db(conn, incidents)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM incidents")
        rows = cursor.fetchall()
        self.assertGreater(len(rows), 0)  # Check that the database is not empty
        conn.close()  # Close the database connection

    def test_print_nature_counts(self):
        # Test the print_nature_counts function
        conn = create_db()
        print_nature_counts(conn)
        conn.close()  # Close the database connection

if __name__ == '__main__':
    unittest.main()
