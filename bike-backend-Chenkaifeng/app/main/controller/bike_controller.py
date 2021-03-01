from flask import request
from flask_restplus import Resource

from ..util.dto import BikeDto
from ..service.bike_service import get_all_bikes, add_new_bike, change_bike_location, get_bike_location
from ..service.bike_service import get_bikes_by_locationId, set_bike_defective, get_a_bike, get_all_bikes, set_bike_repaired


api = BikeDto.api
_bike = BikeDto.bike


@api.route('/')
class BikeList(Resource):
    @api.doc('list_of_bikes')
    @api.marshal_list_with(_bike, envelope='data')
    def get(self):
        """List all bikes"""
        return get_all_bikes()

    @api.response(201, 'A bike successfully created.')
    @api.doc('create a new bike')
    @api.expect(_bike, validate = True)
    def post(self):
        """Creates a new bike """
        data = request.json
        return add_new_bike(data=data)


"""
change the POST to PUT
when update data use PUT
"""
@api.route('/change-bike-location')
class ChangeBikeLocation(Resource):
    @api.doc('change the location of bike')
    @api.expect(_bike, validate=True)
    def put(self):
        data = request.json
        bike_id = data['id']
        new_loc_id = data['new_loc_id']
        return change_bike_location(bike_id, new_loc_id)


"""
I change the PUT to GET,and correct the name of function.
This function will help us to get bike current location
"""
@api.route('/get-bike-location')
class GetBikeLocation(Resource):
    @api.doc('get the location of bike')
    @api.expect(_bike, validate=True)
    def get(self):
        data = request.json
        bike_id = data['id']
        return get_bike_location(bike_id)


@api.route('/mark-defective')
class BikeUpdateAsDefective(Resource):
    @api.doc('Whether a bike is operational or not')
    @api.expect(_bike)
    def put(self):
        """set bike as defective - required bike_id and broken_part"""
        data = request.json
        bike = get_a_bike(data['id'])
        if not bike:
            api.abort(404)

        else:
            """Updates bike status """
            return set_bike_defective(bike_id=data['id'], broken_part=data['broken_part'])


@api.route('/mark-repaired')
class BikeUpdateAsRepaired(Resource):
    @api.doc('Whether a bike is operational or not')
    @api.expect(_bike)
    def put(self):
        """set bike as repaired - required bike_id"""
        data = request.json
        bike = get_a_bike(data['id'])
        if not bike:
            api.abort(404)

        else:
            """Updates bike status """
            return set_bike_repaired(bike_id=data['id'])


"""
change the class name "User" to "Bike"
"""
@api.route('/<bike_id>')
@api.param('bike_id', 'The bike id')
class Bike(Resource):
    @api.doc('get a bike')
    @api.marshal_with(_bike)
    def get(self, bike_id):
        """get a bike given its identifier"""
        bike = get_a_bike(bike_id)
        if not bike:
            api.abort(404)
        else:
            return bike




@api.route('/get_bikes_by_location_id/<location_id>')
@api.param('location_id', 'The location only id')
class GetBikesByLocationId(Resource):
    @api.doc('get bikes by location_id')
    @api.marshal_list_with(_bike, envelope='data')
    def get(self, location_id):
        return get_bikes_by_locationId(location_id)

