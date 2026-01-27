from flask import Flask, render_template, request, json, jsonify
from flask_mail import Mail, Message
from telegram_bot_function import sendText
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate

import os
# from app import app, db
from flask import request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash






from werkzeug.security import  check_password_hash
from datetime import timedelta
from flask_jwt_extended import create_access_token, get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


# Create Flask app
app = Flask(__name__)


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "sjahd487365"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)


# Session
app.config["SECRET_KEY"] = "sjahd487365"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=24)


jwt = JWTManager(app)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db FIRST
db = SQLAlchemy(app)
migrate = Migrate(app, db)




import Route

from model.user import User

# Import admin routes


# Flask Mail setup
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'romdoul1997@gmail.com'
app.config['MAIL_PASSWORD'] = 'ulqw zeqw mwtr yaxq'
app.config['MAIL_DEFAULT_SENDER'] = 'romdoul1997@gmail.com'

mail = Mail(app)

# --- blocklist for revoked JTIs (in-memory demo) ---
REVOKED_JTIS = set()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    return jwt_data["jti"] in REVOKED_JTIS



@app.post("/login")
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    sql_string = text("select * from user where username = :username")
    result = db.session.execute(sql_string, {"username": username}).fetchone()




    if not result:
        return jsonify({"msg": "incorrect username or password"}), 401

    user_id = result[1]
    hash_password = result[4]

    if check_password_hash(hash_password, password):
        access_token = create_access_token(identity=str(user_id))
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "incorrect username or password"}), 401



@app.post("/logout")
@jwt_required()  # revoke current access token
def logout():
    jti = get_jwt()["jti"]
    REVOKED_JTIS.add(jti)
    return jsonify(msg="Access token revoked")


# @app.post("/register")
# @jwt_required()
# def register():
#     username = request.json.get("username", None)
#     return jsonify(msg="User Registered Success", username=username)

@app.post("/register")
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    email = request.form.get("email")

    if not email:
        return jsonify({"msg": "Email is required"}), 400
    if not password:
        return jsonify({"msg": "Password is required"}), 400

    file = request.files.get("profile")
    profile_image = None
    if file and file.filename != "":
        file_name = f"{username}_{secure_filename(file.filename)}"
        save_path = os.path.join('./static/images/users/', file_name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)
        profile_image = file_name

    user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        profile=profile_image
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "msg": "User Registered Success",
        "username": username,
        "email": email,
        "profile_image": profile_image
    }), 200


# ==================================================================

@app.before_request
def before_request():
    from flask import session, redirect, url_for, request
    admin_url = request.path
    is_admin = admin_url.startswith('/admin')
    if is_admin:
        if not session.get("user_id"):
            return redirect(url_for("admin_login"))

    print(admin_url)



# ==================================================================



@app.errorhandler(403)
def error_403(error):
    return render_template('Error_Page/403_error.html')


@app.errorhandler(404)
def error_404(error):
    return render_template('Error_Page/404_error.html')


@app.errorhandler(500)
def error_500(error):
    return render_template('Error_Page/500_error.html')


@app.route('/sendMail')
def send_email():
    msg = Message('Invoice From Nana Shop', recipients=['sreylis534@gmail.com'])
    msg.body = 'This is a plain text email sent from Flask'
    message = render_template('invoice.html')
    msg.html = message
    mail.send(msg)
    return 'Email sent succesfully!'


@app.get('/Scripts')
def script():
    script = [
        {
            "category": "men's clothing",
            "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
            "id": 1,
            "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg",
            "price": 109.95,
            "rating": {
                "count": 120,
                "rate": 3.9
            },
            "title": "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops"
        },
        {
            "category": "men's clothing",
            "description": "Slim-fitting style, contrast raglan long sleeve, three-button henley placket, light weight & soft fabric for breathable and comfortable wearing. And Solid stitched shirts with round neck made for durability and a great fit for casual fashion wear and diehard baseball fans. The Henley style round neckline includes a three-button placket.",
            "id": 2,
            "image": "https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg",
            "price": 22.3,
            "rating": {
                "count": 259,
                "rate": 4.1
            },
            "title": "Mens Casual Premium Slim Fit T-Shirts "
        },
        {
            "category": "men's clothing",
            "description": "great outerwear jackets for Spring/Autumn/Winter, suitable for many occasions, such as working, hiking, camping, mountain/rock climbing, cycling, traveling or other outdoors. Good gift choice for you or your family member. A warm hearted love to Father, husband or son in this thanksgiving or Christmas Day.",
            "id": 3,
            "image": "https://fakestoreapi.com/img/71li-ujtlUL._AC_UX679_.jpg",
            "price": 55.99,
            "rating": {
                "count": 500,
                "rate": 4.7
            },
            "title": "Mens Cotton Jacket"
        },
        {
            "category": "men's clothing",
            "description": "The color could be slightly different between on the screen and in practice. / Please note that body builds vary by person, therefore, detailed size information should be reviewed below on the product description.",
            "id": 4,
            "image": "https://fakestoreapi.com/img/71YXzeOuslL._AC_UY879_.jpg",
            "price": 15.99,
            "rating": {
                "count": 430,
                "rate": 2.1
            },
            "title": "Mens Casual Slim Fit"
        },
        {
            "category": "jewelery",
            "description": "From our Legends Collection, the Naga was inspired by the mythical water dragon that protects the ocean's pearl. Wear facing inward to be bestowed with love and abundance, or outward for protection.",
            "id": 5,
            "image": "https://fakestoreapi.com/img/71pWzhdJNwL._AC_UL640_QL65_ML3_.jpg",
            "price": 695,
            "rating": {
                "count": 400,
                "rate": 4.6
            },
            "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet"
        },
        {
            "category": "jewelery",
            "description": "Satisfaction Guaranteed. Return or exchange any order within 30 days.Designed and sold by Hafeez Center in the United States. Satisfaction Guaranteed. Return or exchange any order within 30 days.",
            "id": 6,
            "image": "https://fakestoreapi.com/img/61sbMiUnoGL._AC_UL640_QL65_ML3_.jpg",
            "price": 168,
            "rating": {
                "count": 70,
                "rate": 3.9
            },
            "title": "Solid Gold Petite Micropave "
        },
        {
            "category": "jewelery",
            "description": "Classic Created Wedding Engagement Solitaire Diamond Promise Ring for Her. Gifts to spoil your love more for Engagement, Wedding, Anniversary, Valentine's Day...",
            "id": 7,
            "image": "https://fakestoreapi.com/img/71YAIFU48IL._AC_UL640_QL65_ML3_.jpg",
            "price": 9.99,
            "rating": {
                "count": 400,
                "rate": 3
            },
            "title": "White Gold Plated Princess"
        },
        {
            "category": "jewelery",
            "description": "Rose Gold Plated Double Flared Tunnel Plug Earrings. Made of 316L Stainless Steel",
            "id": 8,
            "image": "https://fakestoreapi.com/img/51UDEzMJVpL._AC_UL640_QL65_ML3_.jpg",
            "price": 10.99,
            "rating": {
                "count": 100,
                "rate": 1.9
            },
            "title": "Pierced Owl Rose Gold Plated Stainless Steel Double"
        },
        {
            "category": "electronics",
            "description": "USB 3.0 and USB 2.0 Compatibility Fast data transfers Improve PC Performance High Capacity; Compatibility Formatted NTFS for Windows 10, Windows 8.1, Windows 7; Reformatting may be required for other operating systems; Compatibility may vary depending on user\u2019s hardware configuration and operating system",
            "id": 9,
            "image": "https://fakestoreapi.com/img/61IBBVJvSDL._AC_SY879_.jpg",
            "price": 64,
            "rating": {
                "count": 203,
                "rate": 3.3
            },
            "title": "WD 2TB Elements Portable External Hard Drive - USB 3.0 "
        },
        {
            "category": "electronics",
            "description": "Easy upgrade for faster boot up, shutdown, application load and response (As compared to 5400 RPM SATA 2.5\u201d hard drive; Based on published specifications and internal benchmarking tests using PCMark vantage scores) Boosts burst write performance, making it ideal for typical PC workloads The perfect balance of performance and reliability Read/write speeds of up to 535MB/s/450MB/s (Based on internal testing; Performance may vary depending upon drive capacity, host device, OS and application.)",
            "id": 10,
            "image": "https://fakestoreapi.com/img/61U7T1koQqL._AC_SX679_.jpg",
            "price": 109,
            "rating": {
                "count": 470,
                "rate": 2.9
            },
            "title": "SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s"
        },
        {
            "category": "electronics",
            "description": "3D NAND flash are applied to deliver high transfer speeds Remarkable transfer speeds that enable faster bootup and improved overall system performance. The advanced SLC Cache Technology allows performance boost and longer lifespan 7mm slim design suitable for Ultrabooks and Ultra-slim notebooks. Supports TRIM command, Garbage Collection technology, RAID, and ECC (Error Checking & Correction) to provide the optimized performance and enhanced reliability.",
            "id": 11,
            "image": "https://fakestoreapi.com/img/71kWymZ+c+L._AC_SX679_.jpg",
            "price": 109,
            "rating": {
                "count": 319,
                "rate": 4.8
            },
            "title": "Silicon Power 256GB SSD 3D NAND A55 SLC Cache Performance Boost SATA III 2.5"
        },
        {
            "category": "electronics",
            "description": "Expand your PS4 gaming experience, Play anywhere Fast and easy, setup Sleek design with high capacity, 3-year manufacturer's limited warranty",
            "id": 12,
            "image": "https://fakestoreapi.com/img/61mtL65D4cL._AC_SX679_.jpg",
            "price": 114,
            "rating": {
                "count": 400,
                "rate": 4.8
            },
            "title": "WD 4TB Gaming Drive Works with Playstation 4 Portable External Hard Drive"
        },
        {
            "category": "electronics",
            "description": "21. 5 inches Full HD (1920 x 1080) widescreen IPS display And Radeon free Sync technology. No compatibility for VESA Mount Refresh Rate: 75Hz - Using HDMI port Zero-frame design | ultra-thin | 4ms response time | IPS panel Aspect ratio - 16: 9. Color Supported - 16. 7 million colors. Brightness - 250 nit Tilt angle -5 degree to 15 degree. Horizontal viewing angle-178 degree. Vertical viewing angle-178 degree 75 hertz",
            "id": 13,
            "image": "https://fakestoreapi.com/img/81QpkIctqPL._AC_SX679_.jpg",
            "price": 599,
            "rating": {
                "count": 250,
                "rate": 2.9
            },
            "title": "Acer SB220Q bi 21.5 inches Full HD (1920 x 1080) IPS Ultra-Thin"
        },
        {
            "category": "electronics",
            "description": "49 INCH SUPER ULTRAWIDE 32:9 CURVED GAMING MONITOR with dual 27 inch screen side by side QUANTUM DOT (QLED) TECHNOLOGY, HDR support and factory calibration provides stunningly realistic and accurate color and contrast 144HZ HIGH REFRESH RATE and 1ms ultra fast response time work to eliminate motion blur, ghosting, and reduce input lag",
            "id": 14,
            "image": "https://fakestoreapi.com/img/81Zt42ioCgL._AC_SX679_.jpg",
            "price": 999.99,
            "rating": {
                "count": 140,
                "rate": 2.2
            },
            "title": "Samsung 49-Inch CHG90 144Hz Curved Gaming Monitor (LC49HG90DMNXZA) \u2013 Super Ultrawide Screen QLED "
        },
        {
            "category": "women's clothing",
            "description": "Note:The Jackets is US standard size, Please choose size as your usual wear Material: 100% Polyester; Detachable Liner Fabric: Warm Fleece. Detachable Functional Liner: Skin Friendly, Lightweigt and Warm.Stand Collar Liner jacket, keep you warm in cold weather. Zippered Pockets: 2 Zippered Hand Pockets, 2 Zippered Pockets on Chest (enough to keep cards or keys)and 1 Hidden Pocket Inside.Zippered Hand Pockets and Hidden Pocket keep your things secure. Humanized Design: Adjustable and Detachable Hood and Adjustable cuff to prevent the wind and water,for a comfortable fit. 3 in 1 Detachable Design provide more convenience, you can separate the coat and inner as needed, or wear it together. It is suitable for different season and help you adapt to different climates",
            "id": 15,
            "image": "https://fakestoreapi.com/img/51Y5NI-I5jL._AC_UX679_.jpg",
            "price": 56.99,
            "rating": {
                "count": 235,
                "rate": 2.6
            },
            "title": "BIYLACLESEN Women's 3-in-1 Snowboard Jacket Winter Coats"
        },
        {
            "category": "women's clothing",
            "description": "100% POLYURETHANE(shell) 100% POLYESTER(lining) 75% POLYESTER 25% COTTON (SWEATER), Faux leather material for style and comfort / 2 pockets of front, 2-For-One Hooded denim style faux leather jacket, Button detail on waist / Detail stitching at sides, HAND WASH ONLY / DO NOT BLEACH / LINE DRY / DO NOT IRON",
            "id": 16,
            "image": "https://fakestoreapi.com/img/81XH0e8fefL._AC_UY879_.jpg",
            "price": 29.95,
            "rating": {
                "count": 340,
                "rate": 2.9
            },
            "title": "Lock and Love Women's Removable Hooded Faux Leather Moto Biker Jacket"
        },
        {
            "category": "women's clothing",
            "description": "Lightweight perfet for trip or casual wear---Long sleeve with hooded, adjustable drawstring waist design. Button and zipper front closure raincoat, fully stripes Lined and The Raincoat has 2 side pockets are a good size to hold all kinds of things, it covers the hips, and the hood is generous but doesn't overdo it.Attached Cotton Lined Hood with Adjustable Drawstrings give it a real styled look.",
            "id": 17,
            "image": "https://fakestoreapi.com/img/71HblAHs5xL._AC_UY879_-2.jpg",
            "price": 39.99,
            "rating": {
                "count": 679,
                "rate": 3.8
            },
            "title": "Rain Jacket Women Windbreaker Striped Climbing Raincoats"
        },
        {
            "category": "women's clothing",
            "description": "95% RAYON 5% SPANDEX, Made in USA or Imported, Do Not Bleach, Lightweight fabric with great stretch for comfort, Ribbed on sleeves and neckline / Double stitching on bottom hem",
            "id": 18,
            "image": "https://fakestoreapi.com/img/71z3kpMAYsL._AC_UY879_.jpg",
            "price": 9.85,
            "rating": {
                "count": 130,
                "rate": 4.7
            },
            "title": "MBJ Women's Solid Short Sleeve Boat Neck V "
        },
        {
            "category": "women's clothing",
            "description": "100% Polyester, Machine wash, 100% cationic polyester interlock, Machine Wash & Pre Shrunk for a Great Fit, Lightweight, roomy and highly breathable with moisture wicking fabric which helps to keep moisture away, Soft Lightweight Fabric with comfortable V-neck collar and a slimmer fit, delivers a sleek, more feminine silhouette and Added Comfort",
            "id": 19,
            "image": "https://fakestoreapi.com/img/51eg55uWmdL._AC_UX679_.jpg",
            "price": 7.95,
            "rating": {
                "count": 146,
                "rate": 4.5
            },
            "title": "Opna Women's Short Sleeve Moisture"
        },
        {
            "category": "women's clothing",
            "description": "95%Cotton,5%Spandex, Features: Casual, Short Sleeve, Letter Print,V-Neck,Fashion Tees, The fabric is soft and has some stretch., Occasion: Casual/Office/Beach/School/Home/Street. Season: Spring,Summer,Autumn,Winter.",
            "id": 20,
            "image": "https://fakestoreapi.com/img/61pHAEJ4NML._AC_UX679_.jpg",
            "price": 12.99,
            "rating": {
                "count": 145,
                "rate": 3.6
            },
            "title": "DANVOUY Womens T Shirt Casual Cotton Short"
        }
    ]
    return script




@app.post('/process_checkout')
def process_checkout():
    from model import Order, OrderItem, Customer
    from flask_login import current_user

    form = request.form
    first_name = form.get('first_name', '')
    last_name = form.get('last_name', '')
    email = form.get('email', '')
    phone = form.get('phone', '')
    address = form.get('address', '')
    cart_data_str = form.get('cart_data', '[]')

    try:
        cart_data = json.loads(cart_data_str)
    except json.JSONDecodeError:
        cart_data = []

    exchange_rate = 4100  # 1 USD ≈ 4100 KHR

    # ------------------- CALCULATE TOTAL -------------------
    total = 0
    for item in cart_data:
        quantity = item.get('quantity', 1)
        unit_price = float(item.get('price', 0))
        total += unit_price * quantity
    total_khr = total * exchange_rate

    # ------------------- CREATE / GET CUSTOMER -------------------
    customer = Customer.query.filter_by(email=email).first()
    if not customer:
        username = f"{first_name} {last_name}".strip() or email.split("@")[0]
        customer = Customer(
            username=username,
            email=email,
            password="guest",  # or generate a random password
            remark="Guest checkout"
        )
        db.session.add(customer)
        db.session.commit()

    # ------------------- CREATE ORDER -------------------
    new_order = Order(
        user_id=0,  # if you have logged-in users, use current_user.id
        customer_id=customer.id,
        status='pending',
        total_usd=total,
        total_khr=total_khr
    )
    db.session.add(new_order)
    db.session.commit()

    # ------------------- SAVE ORDER ITEMS -------------------
    for item in cart_data:
        product_id = item.get('id')
        if not product_id:
            continue
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product_id,
            price=float(item.get('price', 0)),
            qty=int(item.get('quantity', 1)),
            total=float(item.get('price', 0)) * int(item.get('quantity', 1))
        )
        db.session.add(order_item)
    db.session.commit()

    # ------------------- TELEGRAM / EMAIL -------------------
    html = f"<b>🛒 New Order Received</b>\n\n"
    html += f"<b>Customer:</b> {customer.username}\n"
    html += f"<b>Address:</b> {address}\n"
    html += f"<b>Phone:</b> {phone}\n"
    html += f"<b>Email:</b> {email}\n\n"

    table = "<pre>"
    table += "┌──────────────────────────────────┬──────────┬──────────┐\n"
    table += "│ Item                             │ Quantity │ Price    │\n"
    table += "├──────────────────────────────────┼──────────┼──────────┤\n"

    for item in cart_data:
        title = item.get('title', 'No title')[:30]
        quantity = item.get('quantity', 1)
        unit_price = float(item.get('price', 0))
        item_total = unit_price * quantity
        table += f"│ {title.ljust(32)} │ {str(quantity).center(8)} │ ${str(item_total).ljust(7)} │\n"

    table += "└──────────────────────────────────┴──────────┴──────────┘\n"
    formatted_khr = "{:,.0f}".format(total_khr)
    table += f"\n<b>TOTAL: ${total:.2f} USD\n"
    table += f"TOTAL: ៛{formatted_khr} KHR</b>"
    table += "</pre>"

    html += table
    sendText(chat_id='@O_Romdoul', message=html)

    # ------------------- SEND EMAIL -------------------
    # msg = Message('Invoice From Nana Shop', recipients=[email])
    # msg.body = 'This is a plain text email sent from Flask'
    # msg.html = render_template(
    #     'invoice.html',
    #     customer_name=customer.username,
    #     customer_email=email,
    #     customer_address=address,
    #     customer_phone=phone,
    #     items=cart_data,
    #     total=f"${total:.2f}",
    #     total_khr=f"{formatted_khr}"
    # )
    # mail.send(msg)

    return "Checkout successful!"










if __name__ == '__main__':
    app.run(debug=True)
