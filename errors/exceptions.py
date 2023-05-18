class CreateRequiredParametersNotFound(Exception):

    title          = 'CreateRequiredParametersNotFound'

    message_vessel = "name, owner_id, naccs_code are required parameters"
    message_voyage = "start_time, end_time, start_location, end_location, vessel_naccs_code are required parameters"

    def __init__(self, message="", title=title):
        super().__init__(message, title)

class UpdateRequiredParametersNotFound(Exception):

    title          = 'UpdateRequiredParametersNotFound'

    message_vessel = "naccs_code is a required parameter"
    message_voyage = "voyager_id is a required parameter"

    def __init__(self, message="", title=title):
        super().__init__(message, title)

class InvalidTimeRange(Exception):

    title   = "invalid time range"
    message = "start time cannot be greater than end time"

    def __init__(self, message=message, title=title):
        super().__init__(message, title)
