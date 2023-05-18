import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import unittest
from   errors.exceptions import *
from   providers.vessel import VesselProvider


class TestVesselProvider(unittest.TestCase):

    def setUp(self):
        self.vessel_provider = VesselProvider()

    def test_check_arguments_create_success(self):
        args = {"name": "Test Vessel", "owner_id": 1, "naccs_code": "12345"}
        self.assertIsNone(self.vessel_provider.check_arguments(args, "create"))

    def test_check_arguments_create_missing_params(self):
        args = {"name": "Test Vessel", "naccs_code": "12345"}
        with self.assertRaises(CreateRequiredParametersNotFound):
            self.vessel_provider.check_arguments(args, "create")

    def test_check_arguments_update_success(self):
        args = {"naccs_code": "12345"}
        self.assertIsNone(self.vessel_provider.check_arguments(args, "update"))

    def test_check_arguments_update_missing_params(self):
        args = {"name": "Test Vessel"}
        with self.assertRaises(UpdateRequiredParametersNotFound):
            self.vessel_provider.check_arguments(args, "update")

if __name__ == '__main__':
    unittest.main()
