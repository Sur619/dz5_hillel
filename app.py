from flask import Flask, request, url_for

from db import get_products, create_product, update_product, delete_product, Product, get_product, get_category_by_id, \
    get_category_by_name, delete_category
from exceptions import ValidationError
from serializers import serialize_product, serialize_category
from deserializers import deserialize_product, deserialize_category

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    # Return hello world
    return "Hello, World!"


@app.route('/products', methods=['GET', 'POST'])
def products_api():
    if request.method == "GET":
        name_filter = request.args.get('name')

        products = get_products(name_filter)

        # Convert products to list of dicts
        products_dicts = [
            serialize_product(product)
            for product in products
        ]

        # Return products
        return products_dicts
    if request.method == "POST":
        # Create a product
        product = deserialize_product(request.get_json())

        # Return success
        return serialize_product(product), 201


@app.route('/products/<int:product_id>', methods=['PUT', 'PATCH', 'DELETE', "GET"])
def product_api(product_id):
    if request.method == "GET":
        # Get a product
        product = get_product(product_id)

        # Return product
        return serialize_product(product)
    if request.method == "PUT":
        # Update a product
        product = deserialize_product(request.get_json(), product_id)
        # Return success
        return serialize_product(product)
    if request.method == "PATCH":
        # Update a product
        product = deserialize_product(request.get_json(), product_id, partial=True)
        # Return success
        return serialize_product(product)
    if request.method == "DELETE":
        delete_product(product_id)

        return "", 204


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return {
        'error': str(e)
    }, 422


@app.errorhandler(Product.DoesNotExist)
def handle_does_not_exist_error(e):
    return {
        'error': 'Product does not exist'
    }, 404


@app.route('/categories', methods=['GET', 'POST'])
def categories_api():
    if request.method == "GET":
        name_filter = request.args.get('name')
        id_filter = request.args.get('id')
        filtered = get_category_by_id()

        if name_filter:
            filtered = get_category_by_name(name_filter)
        if id_filter:
            filtered = get_category_by_id(id_filter)
        if not filtered:
            return 'not found this categgitory', 404
        else:
            categories_dicts = [serialize_category(category) for category in filtered]

        return categories_dicts

    if request.method == "POST":
        category = deserialize_category(request.get_json())

        return serialize_category(category), 201


@app.route('/categories/<int:category_id>', methods=['GET'])
def categories_api_by_id(category_id):
    categories_link = url_for('categories_api')
    if request.method == "GET":
        category_by_id = get_category_by_id(category_id)
        searched = [serialize_category(category) for category in category_by_id]
        if searched:
            return searched, 200
        else:
            return 'not found this category', 404


@app.route('/categories/<int:category_id>', methods=['PUT', 'PATCH', 'DELETE'])
def category_api(category_id):
    categories_link = url_for('categories_api')
    if request.method == "PUT":
        category_by_id = get_category_by_id(category_id)
        searched_category = [serialize_category(category) for category in category_by_id]
        if searched_category:

            category = deserialize_category(request.get_json(), category_id)

            return serialize_category(category), 200
        else:
            return 'not found this category', 404
    if request.method == "PATCH":
        category = deserialize_category(request.get_json(), category_id, partial=True)

        return serialize_category(category)
    if request.method == "DELETE":
        delete_category(category_id)
        return "Category has been Deleted", 204


if __name__ == '__main__':
    app.run(debug=True, port=5001)
