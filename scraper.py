import requests
from os import path
from bs4 import BeautifulSoup

_USER_AGENT = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'}


def _download_from_url(url, mode):
    print('Downloading HTML')
    headers = {}
    headers.update(_USER_AGENT)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    if mode == 'text':
        return response.text
    elif mode == 'binary':
        return response.content
    else:
        raise ValueError('Invalid mode')


def get_html(url):
    print('Downloading HTML')
    return _download_from_url(url, mode='text')


def download_cover(cover_url):
    print('Downloading cover')
    try:
        return _download_from_url(cover_url, mode='binary')
    except Exception as e:
        print(f'Error downloading cover, skipping: {str(e)}')
        return None


def download_covers(cover_urls):
    cover_data = [download_cover(url) for url in cover_urls]
    return list(filter(lambda x: x is not None, cover_data))


def parse_cover_html(cover):
    img = cover.find('img')
    shrunk_url = img['src']
    filename_start = shrunk_url.rfind('/') + 1
    filename = shrunk_url[filename_start:]
    junk_start = filename.find('.')
    new_filename = f'{filename[:junk_start]}.jpg'
    return shrunk_url.replace(filename, new_filename)


def build_filenames(num_covers):
    filenames = ['current.jpg']
    filenames.extend(f'{i:0>2}.jpg' for i in range(1, num_covers))
    return filenames


def save_files(cover_data, filenames, static_folder):
    print(f'Saving {len(filenames)} files')
    image_dir = path.join(static_folder, 'images')
    for cover, filename in zip(cover_data, filenames):
        with open(path.join(image_dir, filename), 'wb') as cover_out:
            cover_out.write(cover)


def scrape(url):
    success = True
    try:
        print(f'Scraping {url}')
        html = get_html(url)
        parsed = BeautifulSoup(html, 'html.parser')
        covers = parsed.find_all('td', {'class': 'cover'})
        cover_urls = [parse_cover_html(cover) for cover in covers]
        print(f'Found {len(cover_urls)} covers')
        cover_data = download_covers(cover_urls)
        print(f'Downloaded {len(cover_data)} covers')
        filenames = build_filenames(len(cover_urls))
        print('Saving covers')
        save_files(cover_data, filenames)
        print('Done scraping')
    except Exception as e:
        success = False
        print(f"Wow we really fucked up, here's your exception: {str(e)}")

    return success
