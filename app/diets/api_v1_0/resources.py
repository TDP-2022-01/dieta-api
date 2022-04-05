from flask import request, Blueprint, url_for
from flask_restful import Api, Resource
from app.common.error_handling import ObjectNotFound

import pandas as pd

from app.diets.models import Child, Diet

diets_v1_0_bp = Blueprint('diets_v1_0_bp', __name__, url_prefix='/')

data = []


@diets_v1_0_bp.before_app_first_request
def getData():
    url = 'https://raw.githubusercontent.com/aelvismorales/flask_1/main/dataset.csv'
    global data
    data = pd.read_csv(url, encoding='utf8')

api = Api(diets_v1_0_bp)

@diets_v1_0_bp.route('/diet',methods=['POST'])
def get_diet():

    args=request.get_json()
    age=args['age']
    weight=args['weight']
    height=args['height']
    activity=args['activity']
    sex=args['sex']
    days=args['days']

    child = Child(int(age), float(weight),
                      int(height), str(activity), str(sex))
    diet = Diet(child, data)
    
    # Función que obtiene la dieta filtrada en formato Json
    dietList = []
    dietList = diet.getDiets(int(days))

    if dietList is None:
        raise ObjectNotFound('No existen dietas')
    return dietList

class DietListResource(Resource):
    def get(self):
        args = request.args

        print(args)

        child = Child(int(args['age']), float(args['weight']),
                      int(args['height']), args['activity'], args['sex'])
        diet = Diet(child, data)

        # Función que obtiene la dieta filtrada en formato Json
        dietList = []
        dietList = diet.getDiets(int(args['days']))

        if dietList is None:
            raise ObjectNotFound('No existen dietas')
        return dietList

api.add_resource(DietListResource, '/api/v1.0/diets',
                 endpoint='diet_list_resource')
