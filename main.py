import logging
from pathlib import Path
from os import listdir
from flask import Flask, jsonify, render_template, request
from scraper import scrape

app = Flask(__name__)
app.logger.level = logging.INFO
_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}
_SECONDS_TO_MILLISECONDS = 1000
URLS = [
    'https://www.goodreads.com/review/list/17267214-craig?shelf=currently-reading',
    'https://www.goodreads.com/review/list/17267214?shelf=read&per_page=100'
]  # Let's see if I can get this passed in another way


def _is_image_file(filename):
    return Path(filename).suffix.lower() in _IMAGE_EXTENSIONS


def _check_first_run(image_dir):
    listing = list(filter(lambda x: not x.startswith('.'), listdir(image_dir)))
    return len(listing) == 0


def _do_update():
    success = scrape(URLS, app.static_folder)
    return success


def _get_intervals_with_scale():
    rotate = int(request.args.get('rotate', 10))
    refresh = int(request.args.get('refresh', 3600))
    app.logger.info(f'Rotate interval set to {rotate} seconds')
    app.logger.info(f'Refresh interval set to {refresh} seconds')
    return rotate * _SECONDS_TO_MILLISECONDS, refresh * _SECONDS_TO_MILLISECONDS


@app.route('/')
def root():
    return render_template('home.html')


@app.route('/bookshelf')
def bookshelf():
    rotate, refresh = _get_intervals_with_scale()
    image_dir = Path(app.static_folder) / 'images'
    if _check_first_run(image_dir):
        app.logger.info(f'First run detected, filling cover cache')
        _do_update()
    images = sorted([f'images/{filename}' for filename in listdir(image_dir) if _is_image_file(filename)])
    return render_template('bookshelf.html', images=images, rotate=rotate, refresh=refresh)


@app.route('/update')
def update():
    success = _do_update()
    info = {
        'success': success
    }
    return jsonify(info), 200 if success else 400


if __name__ == '__main__':
    app.run(debug=True)
