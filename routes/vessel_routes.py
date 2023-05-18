import sys
sys.path.append("../models")
sys.path.append("../responses")
sys.path.append("../providers")
sys.path.append("../errors")
sys.path.append("../logger")

from models.models       import db, Vessel
from providers.vessel    import VesselProvider
from errors.exceptions   import *
from responses.responses import *
from logger.logger       import log
from responses.request   import JSONRequestBody
from flask               import Blueprint, request, jsonify


logger = log(__name__)
vessel_bp = Blueprint("VesselBlueprint", "vessel")


@vessel_bp.route("/", methods=["GET"])
def home():
    logger.info("Accessing '/' route")
    return "Application running..."


@vessel_bp.route("/vessels", methods=["GET", "POST"])
def get_or_create_vessel():

    if request.method == "GET":
        logger.info("Fetching all vessels")
        vessels_list = []
        try:
            vessels = Vessel.get_all_vessels()

            for vessel in vessels:
                vessel_dict = {
                    "name":       vessel.name,
                    "owner_id":   vessel.owner_id,
                    "naccs_code": vessel.naccs_code
                }
                vessels_list.append(vessel_dict)
            logger.info("Vessels fetched successfully. Vessels: {}".format(vessels_list))
            return jsonify(vessels_list)

        except Exception as e:
            logger.error("Unable to fetch vessels list")
            logger.error(e)
            return Responses.fail()

    elif request.method == "POST":
        session = db.session
        success = False

        try:
            request_body = JSONRequestBody(request).body

            VesselProvider().check_arguments(request_body, "create")

            name       = request_body["name"]
            owner_id   = request_body["owner_id"]
            naccs_code = request_body["naccs_code"]

            logger.info(f"Creating vessel with the following information:"
                        f"\n\t Vessel Name: {name}"
                        f"\n\t Owner ID:    {owner_id}"
                        f"\n\t NACCS Code:  {naccs_code}")

            new_vessel = Vessel(name, owner_id, naccs_code)

            check_naccs = Vessel.filter_by_naccs_code(naccs_code)

            if check_naccs:
                return Responses.naccs_code_already_exist()

            session.add(new_vessel)
            session.commit()

            success = True

            logger.info("Vessel created successfully")
            return Responses.success()

        except CreateRequiredParametersNotFound:
            logger.error("Unable to create vessel")
            logger.error(CreateRequiredParametersNotFound.message_vessel)
            return CreateRequiredParametersNotFoundResponse.response(
                message=CreateRequiredParametersNotFound.message_vessel
            )
        except Exception as e:
            logger.error("Unable to create vessel")
            logger.error(e)
            return Responses.fail()
        finally:
            if not success:
                session.rollback()
            session.close()
            session.remove()


@vessel_bp.route("/vessels/<string:vessel_naccs_code>", methods=["GET", "PUT"])
def get_or_update_vessel(vessel_naccs_code):

    check_vessel = Vessel.filter_by_naccs_code(vessel_naccs_code)
    if request.method == "PUT":
        session = db.session
        success = False
        try:
            logger.info("Updating vessel having the following NACCS code: {}".format(vessel_naccs_code))

            if not check_vessel:
                logger.info("Vessel with the NACCS code {} does not exist".format(vessel_naccs_code))
                return Responses.naccs_code_not_found()

            request_body = JSONRequestBody(request).body

            VesselProvider().check_arguments(request_body, "update")
            optional_args = VesselProvider().check_optional_arguments(request_body)

            for args in optional_args:
                if args == "name":
                    if request_body["name"]:
                        check_vessel.name  = request_body["name"]
                    else:
                        check_vessel.name = ""
                elif args == "owner_id":
                    if request_body["owner_id"]:
                        check_vessel.owner_id = request_body["owner_id"]
                    else:
                        check_vessel.owner_id = ""

            if not request_body["naccs_code"]:
                return Responses.naccs_code_empty()

            request_naccs_code = request_body["naccs_code"]

            if check_vessel.naccs_code != request_naccs_code:
                check_request_vessel = Vessel.filter_by_naccs_code(request_naccs_code)

                if check_request_vessel:
                    logger.info("NACCS code {} already exists".format(request_naccs_code))
                    return Responses.naccs_code_already_exist()

            check_vessel.naccs_code = request_naccs_code

            session.commit()
            success = True

            return Responses.success()

        except UpdateRequiredParametersNotFound:
            logger.error("Unable to update vessel")
            logger.error(UpdateRequiredParametersNotFound.message_vessel)
            return UpdateRequiredParametersNotFoundResponse.response(
                message=UpdateRequiredParametersNotFound.message_vessel
            )
        except Exception:
            return Responses.fail()
        finally:
            if not success:
                session.rollback()
            session.close()
            session.remove()

    elif request.method == "GET":
        logger.info("Fetching vessel with NACCS code: {}".format(vessel_naccs_code))
        try:
            if check_vessel:
                return jsonify(
                    name=check_vessel.name,
                    owner_id=check_vessel.owner_id,
                    naccs_code=check_vessel.naccs_code
                )
            else:
                logger.info("Vessel having the following NACCS code not found: {}".format(vessel_naccs_code))
                return Responses.naccs_code_not_found()
        except Exception as e:
            logger.error("Unable to fetch vessel having the following NACCS code: {}".format(vessel_naccs_code))
            logger.error(e)
            return Responses.fail()


@vessel_bp.app_errorhandler(404)
def handle_not_found_error(error):
    return Responses.route_does_not_exist()
