import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from   app import app
import unittest
import json


class TestVesselAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_home(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_vessels(self):
        response = self.app.get("/vessels")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIsInstance(data, list)

    def test_create_vessel(self):
        data = {
            "name": "Test Vessel",
            "owner_id": 123,
            "naccs_code": "TEST123"
        }
        headers = {"Content-Type": "application/json"}
        response = self.app.post("/vessels", headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)

    def test_create_vessel_same_naccs_code(self):
        data = {
            "name": "Test Vessel 2",
            "owner_id": 1234,
            "naccs_code": "TEST123"
        }
        headers = {"Content-Type": "application/json"}
        response = self.app.post("/vessels", headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 409)

    def test_update_vessel(self):
        data = {
            "name": "Updated Vessel",
            "owner_id": 123,
            "naccs_code": "TEST123"
        }
        headers = {"Content-Type": "application/json"}
        response = self.app.put("/vessels/TEST123", headers=headers, data=json.dumps(data))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
