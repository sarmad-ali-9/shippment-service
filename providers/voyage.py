import sys
sys.path.append("../responses")

from errors.exceptions import *

class VoyageProvider:

    required_args_create = ["start_time", "end_time", "start_location", "end_location", "vessel_naccs_code"]
    required_args_update = ["voyage_id"]
    optional_args_update = ["start_time", "end_time", "start_location", "end_location"]

    def check_arguments(self, args, method):

        if method == "create":
            if not all(key in args for key in self.required_args_create):
                raise CreateRequiredParametersNotFound()

        elif method == "update":
            if not all(key in args for key in self.required_args_update):
                raise UpdateRequiredParametersNotFound()

    def check_optional_arguments(self, args):

        optional_args_list = []
        for optional_args in self.optional_args_update:

            if optional_args in args.keys():
                optional_args_list.append(optional_args)

        return optional_args_list

    @staticmethod
    def check_time_range(start_time, end_time):
        if start_time > end_time:
            raise InvalidTimeRange
