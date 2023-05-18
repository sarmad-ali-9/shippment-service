import json

class JSONRequestBody(object):

    def __init__(self, request):

        self.body = {}

        if request.form:
            self.body = request.form

            try:
                for key in self.body.keys():
                    self.body = json.loads(key)
            except:
                pass

        elif request.data:
            in_data = request.data
            if type(in_data) == bytes:
                in_data = in_data.decode()
            self.body = json.loads(in_data)
