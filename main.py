from pathlib import Path
from os import listdir
from flask import Flask, jsonify, render_template, request
from scraper import scrape

app = Flask(__name__)
_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
_SECONDS_TO_MILLISECONDS = 1000


def _is_image_file(filename):
    return Path(filename).suffix.lower() in _IMAGE_EXTENSIONS


def _get_intervals():
    rotate = int(request.args.get('rotate', 10)) * _SECONDS_TO_MILLISECONDS
    refresh = int(request.args.get('refresh', 3600)) * _SECONDS_TO_MILLISECONDS
    return rotate, refresh


@app.route('/')
def root():
    return render_template('home.html')


@app.route('/bookshelf')
def bookshelf():
    rotate, refresh = _get_intervals()
    image_dir = Path(app.static_folder) / 'images'
    images = sorted([f'images/{filename}' for filename in listdir(image_dir) if _is_image_file(filename)])
    return render_template('bookshelf.html', images=images, rotate=rotate, refresh=refresh)


@app.route('/update')
def update():
    # scrape both currently reading and recently read
    urls = [
        'https://www.goodreads.com/review/list/17267214-craig?shelf=currently-reading',
        'https://www.goodreads.com/review/list/17267214?shelf=read',
    ]
    success = scrape(urls, app.static_folder)
    info = {
        'success': success,
        'urls': urls
    }
    return jsonify(info), 200 if success else 400


if __name__ == '__main__':
    app.run(debug=True)
