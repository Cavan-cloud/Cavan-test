import json
from flask import request
from flask_restplus import Resource
from ..util.dto import LocationDto
from ..service.location_service import add_a_location, get_all_locations, get_a_location
from ..service.bike_service import get_bikes_by_locationId

api = LocationDto.api
_location = LocationDto.location


@api.route('/')
class AddLocation(Resource):
    @api.doc('list_of_registered_bikes')
    @api.marshal_list_with(_location, envelope='data')
    def get(self):
        """List all registered bikes"""
        return get_all_locations()

    @api.response(201, 'Location successfully created.')
    @api.doc('Add a new location')
    @api.expect(_location, validate=True)
    def post(self):
        """Adds a new location"""
        data = request.json
        return add_a_location(data=data)


@api.route('/get_a_location/<location_id>')
@api.param('location_id', 'The location only id')
class GetLocationById(Resource):
    @api.doc('get a location by location_id')
    @api.marshal_with(_location, envelope='data')
    def get(self, location_id):
        location = get_a_location(location_id)
        if not location:
            api.abort(409)
        else:
            return location
