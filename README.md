
The Vessel API provides endpoints to manage vessels.

Endpoints

1\. Home

**URL**: / **Method**: GET

**Description**: Returns a message indicating that the application is running.

2\. Get or Create Vessel

**URL**: /vessels **Methods**: GET, POST **Description**:

*GET*: Fetches all vessels and returns a JSON response containing a list of vessels.

*POST*: Creates a new vessel using the provided request body JSON data.
Returns a success response if the vessel is created successfully.
*Request Body (POST):*

*Content-Type*: application/json or application/data or application/form *Required Parameters:*

name (string): The name of the vessel. owner\_id (string): The ID of the vessel owner.
naccs\_code (string): The NACCS code of the vessel.
*Response*:

GET: Returns a JSON response containing a list of vessels.
POST: Returns a success response if the vessel is created successfully.
Otherwise, returns an error response.

3\. Get or Update Vessel

**URL**: /vessels/<string:vessel\_naccs\_code> **Methods**: GET, PUT **Description**:

*GET*: Fetches the vessel with the specified NACCS code and returns a JSON response containing vessel details.

*PUT*: Updates the vessel with the specified NACCS code using the provided
request body JSON data. Returns a success response if the vessel is updated
successfully. *Request Body (PUT):*




<a name="br2"></a>*Content-Type:* application/json or application/data or application/form *Required Parameter:*

naccs\_code (string): The updated NACCS code of the vessel. *Optional Parameters:*

name (string): The updated name of the vessel.
owner\_id (string): The updated ID of the vessel owner.
*Response:*

*GET*: Returns a JSON response containing the details of the vessel with the specified NACCS code.

*PUT*: Returns a success response if the vessel is updated successfully. Otherwise, returns an error response.

Voyage API

The Voyage API provides endpoints to manage voyages.

Endpoints

1\. Get or Create Voyages

**URL**: /voyages **Methods**: GET, POST **Description**:

*GET:* Fetches all voyages.

*Response*: Returns a JSON array of voyage objects, where each object represents a voyage.

*POST:* Creates a new voyage.

*Content-Type:* application/json or application/data or application/form
*Request Body:* Expects a JSON object with the following properties:
start\_time (string, required): The start time of the voyage in ISO 8601 format.
end\_time (string, required): The end time of the voyage in ISO 8601 format.
start\_location (string, required): The start location of the voyage.
end\_location (string, required): The end location of the voyage.
vessel\_naccs\_code (string, required): The NACCS code of the vessel associated
with the voyage.

*Response*: Returns a success message if the voyage is created successfully.

2\. Get Voyages by Vessel NACCS Code

**URL**: /vessels/<string:naccs\_code>/voyages




**Method**: GET

**Description**: Fetches all voyages associated with a vessel specified by the NACCS code.

*Response*: Returns a JSON array of voyage objects, where each object
represents a voyage. If no voyages are found for the specified vessel, a not
found message is returned.

3\. Update Voyage

**URL**: /voyages/<string:voyage\_id> **Method**: GET, PUT **Description**:

*GET:* Fetches a voyage with the specified ID.

*Response*: Returns a JSON object representing the voyage. If the voyage ID doesn't exist, a not found message is returned. *PUT:* Updates a voyage with the specified ID.

*Content-Type:* application/json or application/data or application/form
*Request Body*: Expects a JSON object with the following properties:
voyage\_id (string, required): The ID of the voyage to be updated (should match
the ID in the URL).

start\_time (string, optional): The new start time of the voyage in ISO 8601 format.
end\_time (string, optional): The new end time of the voyage in ISO 8601 format.
start\_location (string, optional): The new start location of the voyage.
end\_location (string, optional): The new end location of the voyage.
*Response*: Returns a success message if the voyage is updated successfully. If
the voyage ID doesn't exist, a not found message is returned. If the provided time
range is invalid, an error message is returned.
