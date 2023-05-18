import sys
sys.path.append("../responses")

from errors.exceptions import *

class VesselProvider:

    required_args_create = ["name", "owner_id", "naccs_code"]
    required_args_update = ["naccs_code"]
    optional_args_update = ["name", "owner_id"]

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
