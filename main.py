from flask import Flask, render_template

app = Flask(__name__, static_folder='media', static_url_path='/media')
app.config['SECRET_KEY'] = 'your_secret_key'

def get_cake_data():
    # Данные для слайдера на главной
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
    # Популярные торты для меню
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

@app.route('/')
def index():
    cakes = get_cake_data()
    return render_template('index.html',
                            slider_cakes=cakes['slider_cakes'],
                            popular_cakes=cakes['popular_cakes'],
                            page_title="Главная",
                            active_page="home")

@app.route('/menu')
def menu():
    cakes = get_cake_data()
    return render_template('menu.html',
                            cakes=cakes['popular_cakes'],
                            page_title="Меню",
                            active_page="menu")

@app.route('/about')
def about():
    return render_template('about.html',
                            page_title="О нас",
                            active_page="about")

@app.route('/contact')
def contact():
    return render_template('contact.html',
                            page_title="Контакты",
                            active_page="contact")

if __name__ == '__main__':
    app.run(debug=True)
