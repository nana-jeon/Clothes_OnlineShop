from flask import render_template, abort
from app import app
from model.product import Product  # import your Product model

@app.route('/product_detail/<int:product_id>')
def product_detail(product_id):
    # Fetch product from the database
    product = Product.query.get(product_id)

    if not product:
        abort(404)  # Return 404 if product not found

    return render_template('product_detail.html', item=product)








# def get_product_by_id(product_id):
#     # Search through pro_list to find the product with matching ID
#     for product in pro_list:
#         if product['id'] == product_id:
#             return product
#     return None  # Return None if product not found
#
#
# @app.route('/product_detail/<int:product_id>')
# def product_detail(product_id):
#     product = get_product_by_id(product_id)
#
#     if not product:
#         abort(404)  # Return 404 if product not found
#
#     return render_template('product_detail.html', item=product)


