from pathlib import Path
from os import listdir
from flask import Flask, jsonify, render_template
from scraper import scrape

app = Flask(__name__)
_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def _is_image_file(filename):
    return Path(filename).suffix.lower() in _IMAGE_EXTENSIONS


@app.route('/')
def root():
    return render_template('home.html')


@app.route('/bookshelf')
def bookshelf():
    image_dir = Path(app.static_folder) / 'images'
    images = [f'images/{filename}' for filename in listdir(image_dir) if _is_image_file(filename)]
    images = sorted(images, key=lambda x: ('current' not in x, x))
    return render_template('bookshelf.html', images=images)


@app.route('/update')
def update():
    # this is the currently reading bookshelf
    url = 'https://www.goodreads.com/review/list/17267214-craig?shelf=currently-reading'
    success = scrape(url)
    info = {
        'success': success,
        'url': url
    }
    return jsonify(info), 200 if success else 400


if __name__ == '__main__':
    app.run(debug=True)
