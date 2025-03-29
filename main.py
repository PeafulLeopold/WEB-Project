from flask import Flask, render_template
import os

app = Flask(__name__, static_folder='media', static_url_path='/media')
app.config['SECRET_KEY'] = 'your_secret_key'

# Данные для примера (в реальном приложении нужно брать из БД)
def get_cake_data():
    return {
        'slider_cakes': [
            {'image': 'strawberry_basil.jpg', 'name': 'Клубника-базилик', 'price': 2800},
            {'image': 'cherry_mulled_wine.jpg', 'name': 'Вишня-глинтвейн', 'price': 3200},
            {'image': 'lavender-blueberry.jpg', 'name': 'Лаванда-черника', 'price': 2900}
        ],
        'popular_cakes': [
            {'image': 'strawberry_basil.jpg', 'name': 'Клубника-базилик', 
             'description': 'Нежный бисквит с клубникой и свежим базиликом', 'price': 2800},
            {'image': 'cherry_mulled_wine.jpg', 'name': 'Вишня-глинтвейн', 
             'description': 'Нежный чизкейк с ягодами вишни, сочной прослойкой со вкусом глинтвейна', 'price': 2700},
            {'image': 'lavender-blueberry.jpg', 'name': 'Лаванда-черника', 
             'description': 'Нежный торт с лавандой и черникой', 'price': 2900}
        ]
    }

@app.route('/')
def index():
    cakes = get_cake_data()
    return render_template('index.html', 
                         slider_cakes=cakes['slider_cakes'],
                         popular_cakes=cakes['popular_cakes'])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run()
