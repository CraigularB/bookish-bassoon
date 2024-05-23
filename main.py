from pathlib import Path
from os import listdir
from flask import Flask, render_template

app = Flask(__name__)
_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


@app.route('/')
def root():
    return render_template('home.html')


@app.route('/bookshelf')
def bookshelf():
    image_dir = Path(app.static_folder) / 'images'
    images = [f'images/{fname}' for fname in listdir(image_dir) if Path(fname).suffix.lower() in _IMAGE_EXTENSIONS]
    return render_template('bookshelf.html', images=images)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
