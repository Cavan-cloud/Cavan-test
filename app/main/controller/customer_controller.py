from flask import request
from flask_restplus import Resource

from ..util.dto import CustomerDto
from ..service.customer_service import get_all_customers, save_new_customer, get_a_customer, add_balance, spend_balance

api = CustomerDto.api
_customer = CustomerDto.customer


@api.route('/')
class CustomerList(Resource):
    @api.doc('list_of_customers')
    @api.marshal_list_with(_customer, envelope='data')
    def get(self):
        """List all registered customers"""
        return get_all_customers()

    @api.response(201, 'Customer successfully created.')
    @api.doc('create a new customer')
    @api.expect(_customer, validate=True)
    def post(self):
        """Creates a new Customer """
        data = request.json
        return save_new_customer(data=data)


@api.route('/<customer_id>')
@api.param('customer_id', 'The Customer identifier')
@api.response(404, 'Customer not found.')
class Customer(Resource):
    @api.doc('get a customer')
    @api.marshal_with(_customer)
    def get(self, customer_id):
        """get a user given its identifier"""
        customer = get_a_customer(customer_id)
        if not customer:
            api.abort(404)
        else:
            return customer


"""
change the POST to PUT, PUT is used to update data
"""
@api.route('/add-money')
class AddMoneyToBalance(Resource):
    @api.doc('add money to balance')
    @api.expect(_customer, validate=True)
    def put(self):
        """json include the added money """
        data = request.json
        customer_id = data['id']
        customer = get_a_customer(customer_id)
        if not customer:
            api.abort(404)
        else:
            money = data['money']
            return add_balance(customer_id, money)


"""
change the POST to PUT, PUT is used to update data
"""
@api.route('/spend-money')
class SpendMoneyFromBalance(Resource):
    @api.doc('subtract money from balance')
    @api.expect(_customer, validate=True)
    def put(self):
        """json include the subtracted money """
        data = request.json
        customer_id = data['id']
        customer = get_a_customer(customer_id)
        if not customer:
            api.abort(404)
        else:
            cost = data['money']
            return spend_balance(customer_id, cost)
