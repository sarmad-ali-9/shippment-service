import sys
sys.path.append("../models")
sys.path.append("../responses")
sys.path.append("../providers")
sys.path.append("../errors")
sys.path.append("../logger")

from datetime            import datetime
from models.models       import db, Voyage, Vessel
from providers.voyage    import VoyageProvider
from errors.exceptions   import *
from responses.responses import *
from logger.logger       import log
from responses.request   import JSONRequestBody
from flask               import Blueprint, request, jsonify


logger    = log(__name__)
voyage_bp = Blueprint("VoyageBlueprint", "voyage")


@voyage_bp.route("/voyages", methods=["GET", "POST"])
def get_or_create_voyage():

    if request.method == "GET":
        logger.info("Fetching all voyages")
        voyages_list = []
        try:
            voyages = Voyage.get_all_voyages()
            for voyage in voyages:
                voyage_object = {
                    "voyage_id":         voyage.id,
                    "start_time":        voyage.start_time,
                    "end_time":          voyage.end_time,
                    "start_location":    voyage.start_location,
                    "end_location"  :    voyage.end_location,
                    "vessel_naccs_code": voyage.vessel_naccs_code
                }
                voyages_list.append(voyage_object)
            logger.info("Voyages fetched successfully. Voyages: {}".format(voyages_list))
            return jsonify(voyages_list)

        except Exception as e:
            logger.error("Unable to fetch voyages list")
            logger.error(e)
            return Responses.fail()

    elif request.method == "POST":
        session = db.session
        success = False

        try:
            request_body = JSONRequestBody(request).body

            VoyageProvider().check_arguments(request_body, "create")

            start_time, end_time = (datetime.fromisoformat(request_body["start_time"]),
                                    datetime.fromisoformat(request_body["end_time"]))
            start_location       = request_body["start_location"]
            end_location         = request_body["end_location"]
            vessel_naccs_code    = request_body["vessel_naccs_code"]

            vessel = Vessel.filter_by_naccs_code(vessel_naccs_code)
            if not vessel:
                return Responses.naccs_code_not_found()

            VoyageProvider.check_time_range(start_time, end_time)

            logger.info(f"Creating voyage with the following information:"
                        f"\n\t Start Time:        {start_time}"
                        f"\n\t End Time:          {end_time}"
                        f"\n\t Start Location:    {start_location}"
                        f"\n\t End Location:      {end_location}"
                        f"\n\t Vessel Naccs Code: {vessel_naccs_code}")

            new_vessel = Voyage(start_time, end_time, start_location, end_location, vessel_naccs_code)

            session.add(new_vessel)
            session.commit()

            success = True

            logger.info("Voyage created successfully")
            return Responses.success()

        except CreateRequiredParametersNotFound:
            logger.error("Unable to create voyage")
            logger.error(CreateRequiredParametersNotFound.message_voyage)
            return CreateRequiredParametersNotFoundResponse.response(
                message=CreateRequiredParametersNotFound.message_voyage
            )
        except InvalidTimeRange:
            logger.error("Invalid time range")
            logger.error(InvalidTimeRange.message)
            return InvalidTimeRangeResponse.response(
                message=InvalidTimeRange.message
            )
        except Exception as e:
            logger.error("Unable to create voyage")
            logger.error(e)
            return Responses.fail()
        finally:
            if not success:
                session.rollback()
            session.close()
            session.remove()


@voyage_bp.route("/vessels/<string:naccs_code>/voyages", methods=["GET"])
def get_voyages(naccs_code):
    logger.info("Fetching voyage(s) of the vessel with NACCS code: {}".format(naccs_code))
    try:
        check_voyage = Voyage.filter_by_naccs_code(naccs_code)
        if check_voyage:
            voyages = [voyage.to_dict() for voyage in check_voyage]
            return jsonify(voyages)
        logger.info("Voyage of the vessel having the following NACCS code not found: {}".format(naccs_code))
        return Responses.voyage_not_found()

    except Exception as e:
        logger.error("Unable to fetch voyage of the vessel having the following NACCS code: {}".format(naccs_code))
        logger.error(e)
        return Responses.fail()


@voyage_bp.route("/voyages/<string:voyage_id>", methods=["PUT"])
def update_voyage(voyage_id):
    check_voyage = Voyage.filter_by_voyage_id(voyage_id)
    session = db.session
    success = False
    try:
        logger.info("Updating voyage having the following ID: {}".format(voyage_id))

        if check_voyage is None:
            success = True
            return Responses.voyage_not_found()

        request_body = JSONRequestBody(request).body

        VoyageProvider().check_arguments(request_body, "update")
        optional_args = VoyageProvider().check_optional_arguments(request_body)

        if voyage_id != request_body["voyage_id"]:
            logger.error("Voyage ID mismatch")
            return Responses.voyage_mismatch()

        for args in optional_args:
            if args == "start_time":
                start_time = datetime.fromisoformat(request_body["start_time"])
                if "end_time" in optional_args:
                    end_time = datetime.fromisoformat(request_body["end_time"])
                    VoyageProvider.check_time_range(start_time, end_time)

                else:
                    end_time_in_db = Voyage.get_end_time_for_voyage(voyage_id)
                    VoyageProvider.check_time_range(start_time, end_time_in_db)
                check_voyage.start_time = start_time
            elif args == "end_time":
                end_time         = datetime.fromisoformat(request_body["end_time"])
                start_time_in_db = Voyage.get_start_time_for_voyage(voyage_id)
                VoyageProvider.check_time_range(start_time_in_db, end_time)

                check_voyage.end_time = end_time
            elif args == "start_location":
                check_voyage.start_location = request_body["start_location"]
            elif args == "end_location":
                check_voyage.end_location = request_body["end_location"]

        session.commit()
        success = True

        return Responses.success()

    except UpdateRequiredParametersNotFound:
        logger.error("Unable to update voyage")
        logger.error(UpdateRequiredParametersNotFound.message_voyage)
        return UpdateRequiredParametersNotFoundResponse.response(
            message=UpdateRequiredParametersNotFound.message_voyage
        )
    except InvalidTimeRange:
        logger.error("In valid time range")
        logger.error(InvalidTimeRange.message)
        return InvalidTimeRangeResponse.response(
            message=InvalidTimeRange.message
        )
    except Exception as e:
        logger.error(e)
        return Responses.fail()
    finally:
        if not success:
            session.rollback()
        session.close()
        session.remove()

@voyage_bp.route("/voyages/<string:voyage_id>", methods=["GET"])
def get_voyage(voyage_id):
    logger.info("Fetching voyage of ID: {}".format(voyage_id))
    try:
        voyage = Voyage.filter_by_voyage_id(voyage_id)
        if voyage:
            logger.info("Voyage fetched successfully. Voyage: {}".format(voyage.to_dict))
            return jsonify(voyage.to_dict())

        logger.info("Voyage with the ID {} does not exist".format(voyage_id))
        return Responses.voyage_not_found()
    except Exception as e:
        logger.error("Unable to fetch voyages list")
        logger.error(e)
        return Responses.fail()
