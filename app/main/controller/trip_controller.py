from flask import request
from flask_restplus import Resource

from ..util.dto import TripDto
from ..service.trip_service import get_trips, get_data

api = TripDto.api
_trip = TripDto.trip


@api.route('/get_trips_cost')
class GetTripsCost(Resource):
    @api.doc('get trips cost by time')
    def post(self):
        data = request.json
        start_time = data['start_time']
        end_time = data['end_time']
        bins = data['bins']
        return get_data(start_time, end_time, bins)
