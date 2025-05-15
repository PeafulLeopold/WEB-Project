from flask import Flask, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect, generate_csrf
from db.database import db, CartItem, Order
import json

app = Flask(__name__, static_folder='media', static_url_path='/media')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)
db.init_app(app)

def get_cake_data():
    slider_cakes = [
        {
            'image': 'strawberry_basil.jpg',
            'name': 'Клубника-базилик',
            'price': 2800,
            'description': 'Воздушный бисквит с клубничным крем-чизом и листьями свежего базилика'
        },
        {
            'image': 'cherry_mulled_wine.jpg',
            'name': 'Вишня-глинтвейн',
            'price': 3200,
            'description': 'Шоколадный торт с вишневой начинкой и пряностями глинтвейна'
        },
        {
            'image': 'lavender-blueberry.jpg',
            'name': 'Лаванда-черника',
            'price': 3000,
            'description': 'Нежный бисквит с черничной начинкой и лавандовым ароматом'
        }
    ]
    popular_cakes = [
        {
            'image': 'strawberry_basil.jpg',
            'name': 'Клубника-базилик',
            'price': 2800,
            'description': 'Воздушный бисквит с клубничным крем-чизом и листьями свежего базилика'
        },
        {
            'image': 'cherry_mulled_wine.jpg',
            'name': 'Вишня-глинтвейн',
            'price': 3200,
            'description': 'Шоколадный торт с вишневой начинкой и пряностями глинтвейна'
        },
        {
            'image': 'lavender-blueberry.jpg',
            'name': 'Лаванда-черника',
            'price': 3000,
            'description': 'Нежный бисквит с черничной начинкой и лавандовым ароматом'
        }
    ]
    return {
        'slider_cakes': slider_cakes,
        'popular_cakes': popular_cakes
    }

with app.app_context():
    db.create_all()

@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf)

@app.route('/')
def index():
    cakes = get_cake_data()
    cart_items = CartItem.query.all()
    return render_template('index.html',
                           slider_cakes=cakes['slider_cakes'],
                           popular_cakes=cakes['popular_cakes'],
                           page_title="Главная",
                           active_page="home",
                           cart=cart_items,
                           return_url=url_for('index'))

@app.route('/menu')
def menu():
    cakes = get_cake_data()
    cart_items = CartItem.query.all()
    return render_template('menu.html',
                           cakes=cakes['popular_cakes'],
                           page_title="Меню",
                           active_page="menu",
                           cart=cart_items,
                           return_url=url_for('menu'))

@app.route('/about')
def about():
    cart_items = CartItem.query.all()
    return render_template('about.html',
                           page_title="О нас",
                           active_page="about",
                           cart=cart_items)

@app.route('/contact')
def contact():
    cart_items = CartItem.query.all()
    return render_template('contact.html',
                           page_title="Контакты",
                           active_page="contact",
                           cart=cart_items)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    cake_name = request.form.get('cake_name')
    cake_price = int(request.form.get('cake_price'))
    quantity = int(request.form.get('quantity', 1))
    return_url = request.form.get('return_url', url_for('index'))

    cart_item = CartItem.query.filter_by(name=cake_name).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(name=cake_name, price=cake_price, quantity=quantity)
        db.session.add(cart_item)
    db.session.commit()
    return redirect(return_url)

@app.route('/cart')
def cart():
    cart_items = CartItem.query.all()
    cart_items_with_totals = [
        {
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'total': item.price * item.quantity
        } for item in cart_items
    ]
    return render_template('cart.html',
                           cart=cart_items_with_totals,
                           page_title="Корзина",
                           active_page="cart")

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = CartItem.query.all()
    if not cart_items:
        return redirect(url_for('cart'))

    cart_items_with_totals = [
        {
            'id': item.id,
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'total': item.price * item.quantity
        } for item in cart_items
    ]
    total = sum(item['total'] for item in cart_items_with_totals)

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        delivery = 'delivery' in request.form
        address = request.form.get('address') if delivery else None

        if not all([name, email, phone]):
            return render_template('checkout.html',
                                   cart=cart_items_with_totals,
                                   total=total,
                                   page_title="Оформление заказа",
                                   active_page="cart",
                                   error="Пожалуйста, заполните все обязательные поля.")

        order_items = json.dumps(cart_items_with_totals)
        order = Order(
            name=name,
            email=email,
            phone=phone,
            address=address,
            delivery=delivery,
            items=order_items,
            total=total
        )
        db.session.add(order)

        CartItem.query.delete()
        db.session.commit()

        return redirect(url_for('confirmation', order_id=order.id))

    return render_template('checkout.html',
                           cart=cart_items_with_totals,
                           total=total,
                           page_title="Оформление заказа",
                           active_page="cart")

@app.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    items = json.loads(order.items)
    return render_template('confirmation.html',
                           order=order,
                           items=items,
                           page_title="Заказ подтвержден",
                           active_page="cart")

if __name__ == '__main__':
    app.run(debug=True)