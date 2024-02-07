import unittest
from unittest.mock import patch
from assignment0.main import fetch_incidents


class TestFetchIncidents(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_fetch_incidents(self, mock_urlopen):
        # Setup mock response to emulate `urlopen` behavior
        mock_urlopen.return_value.read.return_value = b'Test PDF content'

        # Expected temporary file path
        expected_pdf_path = '/tmp/incident_report.pdf'

        # Call the function with a mock URL
        pdf_path = fetch_incidents('http://mockurl.com/incident_report.pdf')

        # Assert the PDF path is as expected
        self.assertEqual(pdf_path, expected_pdf_path)

        # Optionally, you can check if the file with expected content exists
        # This part is skipped here as it requires file system operations


if __name__ == '__main__':
    unittest.main()
