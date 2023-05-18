import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from   app import app
import unittest

class TestVoyageAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True

    def test_get_voyages(self):
        response = self.app.get('/voyages')
        self.assertEqual(response.status_code, 200)

    def test_create_voyage(self):
        voyage_data = {
            "start_time": "2022-01-01T10:00:00Z",
            "end_time": "2022-01-01T13:00:00Z",
            "start_location": "LA",
            "end_location": "NYC",
            "vessel_naccs_code": "TEST123"
        }
        response = self.app.post('/voyages', json=voyage_data)
        self.assertEqual(response.status_code, 200)

    def test_create_voyage_with_invalid_vessel_naccs_code(self):
        voyage_data = {
            "start_time": "2022-01-01T10:00:00Z",
            "end_time": "2022-01-01T13:00:00Z",
            "start_location": "LA",
            "end_location": "NYC",
            "vessel_naccs_code": "invalid_code"
        }
        response = self.app.post('/voyages', json=voyage_data)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"the vessel with the given NACCS code does not exist", response.data)

if __name__ == '__main__':
    unittest.main()
