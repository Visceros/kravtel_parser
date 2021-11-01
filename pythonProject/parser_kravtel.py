# encoding: utf-8
from bs4 import BeautifulSoup as BS
import requests
import csv
from os import path
sitemap = requests.get('https://www.kravtel.ru/sitemap_iblock_2.xml')
soup_sitemap = BS(sitemap.text, features='lxml')

webpages_to_check = soup_sitemap.find_all('loc')
print('Найдено {} страниц'.format(len(webpages_to_check)))
counter = 0
with open(path.join("C:\\Work", "texts_kravtel_result.csv"), 'w', encoding='utf-8', newline='') as result_csvfile:
    column_names = ['URL', 'Код ответа', 'Наличие текста']
    writer = csv.writer(result_csvfile, delimiter=',')
    writer.writerow(column_names)
    for url in webpages_to_check:
        counter+=1
        print('Проверка страницы №', counter)
        webpage = requests.get(url.get_text())
        soup_webpage = BS(webpage.text, features='lxml')
        if webpage.status_code == 200:
            if soup_webpage.find('div', class_='bx-section-desc') is not None:
                writer.writerow([url.get_text(), webpage.status_code, '1'])
                #print('skipped', url.get_text())
                #continue
            elif soup_webpage.find('span', class_='catalog_item_wrap1') is not None:
                writer.writerow([url.get_text(), webpage.status_code, '0'])
                #lookup_area = soup_webpage.select('div.bx_catalog_list_home > span.catalog_item_wrap1')
                #product_count = len(lookup_area)
                #writer.writerow([url.get_text(), webpage.status_code, product_count])
        else:
            print(url.get_text(), 'status code: 404')
            writer.writerow([url.get_text(), webpage.status_code])
            continue

print('job done')