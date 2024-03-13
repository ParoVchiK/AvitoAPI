from flask import Flask, request
from flask_restful import Resource, Api
from db import getPriceWithData
from discount_segments import getDiscountSegmentFromUserID
from microcategory_tree import getCategoriesWithID, getChildrenCategories
from location_tree import getLocationWithID, getChildrenLocations

app = Flask(__name__)
api = Api(app)

@app.errorhandler(500)
def not_found(e):
    print(e)

@app.errorhandler(404)
def not_found(e):
    print(e)

class GetPriceData(Resource):
    def post(self):
        microcategory_id = request.get_json()['microcategory_id']
        location_id = request.get_json()['location_id']
        user_id = request.get_json()['user_id']
        user_segment = getDiscountSegmentFromUserID(user_id)
        priceData = getPriceWithData(getCategoriesWithID(microcategory_id), getLocationWithID(location_id), user_segment)
        return {'price': priceData['price'],
                'location_id': priceData['location_id'],
                'microcategory_id': priceData['microcategory_id'],
                'matrix_id': 1,
                'user_segment_id': int(priceData['user_segment_id'])}



class GetCategoryData(Resource):
    def post(self):
        category_id = request.get_json()['category_id']
        return getChildrenCategories(category_id)


class GetLocationsData(Resource):
    def post(self):
        location_id = request.get_json()['location_id']
        return getChildrenLocations(location_id)


api.add_resource(GetPriceData, '/api')
api.add_resource(GetCategoryData, '/getCategories')
api.add_resource(GetLocationsData, '/getLocations')

if __name__ == '__main__':
    app.run(debug=True)