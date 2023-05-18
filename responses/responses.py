from flask import jsonify

class Responses:

    @staticmethod
    def success(message="operation was successful"):
        return jsonify(
            status=translate_http_code(200),
            message=message
        ), 200

    @staticmethod
    def naccs_code_already_exist(
            message="NACCS code must be unqiue for each vessel"
        ):

        return jsonify(
            status=translate_http_code(409),
            message=message
        ), 409

    @staticmethod
    def naccs_code_not_found(
            message="the vessel with the given NACCS code does not exist"
    ):
        return jsonify(
            status=translate_http_code(404),
            message=message
        ), 404

    @staticmethod
    def naccs_code_empty(
            message="NACCS code must not be empty"
    ):
        return jsonify(
            status=translate_http_code(401),
            message=message
        ), 401


    @staticmethod
    def voyage_not_found(
            message="voyage does not exist"
    ):
        return jsonify(
            status=translate_http_code(404),
            message=message
        ), 404

    @staticmethod
    def fail(message="operation was not successful"):
        return jsonify(
            status=translate_http_code(500),
            message=message
        ), 500

    @staticmethod
    def route_does_not_exist():
        return jsonify(
            status="route not found",
            message="the requested route does not exist"
        ), 404

    @staticmethod
    def voyage_mismatch():
        return jsonify(
            status="voyage id mismatch",
            message="the prameters voyage id mismatch with the voyage id provided in voyage/{id} route"
        ), 404


class CreateRequiredParametersNotFoundResponse():

    @staticmethod
    def response(message):
        return jsonify(
            message=message,
            status=translate_http_code(400)
        ), 400

class UpdateRequiredParametersNotFoundResponse():

    @staticmethod
    def response(message):
        return jsonify(
            message=message,
            status=translate_http_code(400)
        ), 400

class InvalidTimeRangeResponse():

    @staticmethod
    def response(message):
        return jsonify(
            message=message,
            status=translate_http_code(401)
        ), 401


def translate_http_code(http_code):
    return {
        200: "ok",
        400: "required parameter(s) not found",
        401: "bad request",
        404: "not found",
        409: "conflict",
        500: "Internal Server Error"
    }.get(http_code, 500)
