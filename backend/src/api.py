import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialie the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

CORS(app, resources={"/": {"origins": "*"}})

@app.after_request
def after_request(res):
    res.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    res.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONs')
    return res

#ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def drinks():
    getDrinks = Drink.query.all()
    drinks = [drink.short() for drink in getDrinks]

    if len(getDrinks) == 0:
        abort(404)
    
    else:
        return jsonify({
            "success": True,
            "drinks": drinks,

        })

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    getDrinks = Drink.query.all()
    drinks = [drink.long() for drink in getDrinks]

    if len(getDrinks) == 0:
        abort(404)
    
    else:
        return jsonify({
            "success": True,
            "drinks": drinks,
            
        })

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drinks(payload):
    getData = request.get_json()
  
    newTitle = getData['title']
    newRecipe = getData['recipe']

    if (len(newTitle)==0) or (len(newRecipe)==0):
        abort(422)
    
    else:
        drink = Drink(
            title = json.dumps(newTitle),
            recipe = json.dumps(newRecipe) )
        
        drink.insert()

        return jsonify({
            "success": True,
            "drinks":drink.long()
        })

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(id, payload):
    getData = request.get_json()

    newTitle = getData['title']
    newRecipe = getData['recipe']

    drink = Drink.query.get(id)

    if drink is None:
        abort(404)
    
    else:
        drink.id = id
        drink.title = json.dumps(newTitle),
        drink.recipe= json.dumps(newRecipe)

        drink.update()

        return jsonify({
            "success": True,
            "drinks":drink.long()
        })

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(id, payload):
    drink = Drink.query.filter(Drink.id==id).one_or_none()

    if drink is None:
        abort(404)
    
    else:
        drink.delete()

        return({
            "success": True,
            "delete": id
        })

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found.'
    }), 404

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(401)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 401,
        'message': 'Unauthorized'
    }), 401

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
