from flask import request
from flask_restplus import Resource

from ..util.dto import BikeOperationDto
from ..service.operations_service import get_bikes, get_data

api = BikeOperationDto.api
_bikeOperation = BikeOperationDto.bike_operation


@api.route('/get_bikes_count')
class GetBikesCount(Resource):
    @api.doc('get bikes count by time and operational')
    def post(self):
        data = request.json
        operational = data['operational']
        start_time = data['start_time']
        end_time = data['end_time']
        bins = data['bins']
        return get_data(operational, start_time, end_time, bins)
