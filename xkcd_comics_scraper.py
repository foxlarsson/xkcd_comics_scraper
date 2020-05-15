import requests
import bs4
import re

start_url = 'https://xkcd.com/'


def get_xkcd_image_data(page_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                      'Safari/537.36',
    }
    response = requests.get(page_url, headers=headers)
    response.raise_for_status()

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    images = soup.select('div#comic img')
    img_url = images[0].attrs.get('src')
    img_alt = images[0].attrs.get('title')
    clean_url = 'http://' + img_url[2:]

    titles = soup.select('div#ctitle')
    img_title = titles[0].text

    permalink_container = soup.find('div', id='middleContainer')

    permalink_regex = re.compile(r'https://xkcd\.com/\d+/', re.I)
    embed_url_regex = re.compile(r'https://imgs\.xkcd\.com/comics/.+\.(png|jpg)', re.I)
    # .png or .jpg, names have letters, numbers, underscores, and parentheses

    img_permalink = permalink_regex.search(permalink_container.text).group()

    img_embed_url = embed_url_regex.search(permalink_container.text).group()

    data = {'soup': soup,
            'url': clean_url,
            'hover': img_alt,
            'title': img_title,
            'permalink': img_permalink,
            'embed_url': img_embed_url,
            }

    return data


def download_xkcd_image(img_url, img_num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                      'Safari/537.36',
    }
    response = requests.get(img_url, headers=headers)
    response.raise_for_status()

    with open(f'.\\xkcd_comics\\img_{img_num}.png', 'wb') as img_file:
        # counter = 0
        for chunk in response.iter_content(100000):
            img_file.write(chunk)
            # print(f'chunk {counter}')
            # counter += 1


def find_next_url(soup):
    url_selector = 'ul.comicNav li a'
    urls = soup.select(url_selector)
    prev_url = 'https://xkcd.com' + urls[1].attrs.get('href')
    return prev_url


data = get_xkcd_image_data(start_url)

for i in range(1, 3):
    download_xkcd_image(data['url'], i)
    print('File name:', f'img_{i}.png')
    print('Title:', data['title'])
    print('Text on hover:', data['hover'])
    print('Permalink:', data['permalink'])
    print('Embed URL:', data['embed_url'])
    prev_image_url = find_next_url(data['soup'])
    data = get_xkcd_image_data(prev_image_url)
    print('__________________________________________________________________________\n\n')
