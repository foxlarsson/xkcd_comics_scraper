import requests
import bs4
import re
import os
import openpyxl
from openpyxl.styles import Font


start_url = 'https://xkcd.com/4'
download_prompt = 'How many images do you want to download and catalog?\n' \
                  'Enter a number for specific number of images\n' \
                  'Type ALL if you want to download and catalog all available images\n'
number_img_to_download = input(download_prompt)
workbook = openpyxl.Workbook()
workbook.create_sheet('xkcd_catalog', 0)
wb_sheet = workbook['xkcd_catalog']

wb_sheet['A1'] = 'File Name'
wb_sheet['B1'] = 'Image Title'
wb_sheet['C1'] = 'Hover Text'
wb_sheet['D1'] = 'Permalink'
wb_sheet['E1'] = 'Embed URL'


for cell in wb_sheet['1']:
    cell.font = Font(bold=True)


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
    img_prev_url = find_next_url(soup)

    img_data = {'soup': soup,
                'url': clean_url,
                'hover': img_alt,
                'title': img_title,
                'permalink': img_permalink,
                'embed_url': img_embed_url,
                'prev_url': img_prev_url,
                }

    return img_data


def download_xkcd_image(img_url, img_num):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 '
                      'Safari/537.36',
    }
    response = requests.get(img_url, headers=headers)
    response.raise_for_status()

    with open(os.path.join('.', 'xkcd_comics', f'img_{img_num}.png'), 'wb') as img_file:
        # counter = 0
        for chunk in response.iter_content(100000):
            img_file.write(chunk)
            # print(f'chunk {counter}')
            # counter += 1


def write_image_data_to_file(sheet, row, img_data):
    row += 1
    sheet[f'A{row}'] = img_data['file_name']
    sheet[f'B{row}'] = img_data['title']
    sheet[f'C{row}'] = img_data['hover']
    sheet[f'D{row}'] = img_data['permalink']
    sheet[f'E{row}'] = img_data['embed_url']


def find_next_url(soup):
    url_selector = 'ul.comicNav li a'
    urls = soup.select(url_selector)
    prev_url = 'https://xkcd.com' + urls[1].attrs.get('href')
    return prev_url


def print_progress(img_data, num):
    print('File name:', f'img_{num}.png')
    print('Title:', img_data['title'])
    print('Text on hover:', img_data['hover'])
    print('Permalink:', img_data['permalink'])
    print('Embed URL:', img_data['embed_url'])
    print('Previous image:', img_data['prev_url'])


def download_sequence(img_data, num):
    download_xkcd_image(img_data['url'], num)
    img_data['file_name'] = f'img_{num}.png'
    print_progress(img_data, num)
    write_image_data_to_file(wb_sheet, num, img_data)
    img_data = get_xkcd_image_data(img_data['prev_url'])
    print('-' * 25, '\n\n')
    return img_data


data = get_xkcd_image_data(start_url)


if number_img_to_download.isnumeric():
    for i in range(1, int(number_img_to_download) + 1):
        data = download_sequence(data, i)
if number_img_to_download == 'ALL':
    i = 1
    while True:
        data = download_sequence(data, i)
        if data['permalink'] == 'https://xkcd.com/1/':
            download_sequence(data, i)
            break
        i += 1


workbook.save(os.path.join('.', 'xkcd_comics', 'xkcd_catalog4.xlsx'))
workbook.close()
