#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import re
import json

def get_html(url):
    response = urllib.request.urlopen((url))
    return response.read().decode('utf-8')


def parser_ekdc_org(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', {"id" : "services-accordion"})
    h3 = table.find_all('h3')
    category = table.find_all('table', class_='services-items-table')

    list1 = []
    list2 = []

    for c in category:
        rows = c.find_all('tr')
        for col in rows:
            c = col.find_all('td')[::2]
            list1.append({
                'name': c[0].div.text.strip(),
                'price': c[1].div.text.strip()
            })

    for i in range(len(h3)):
        list1[i] = {h3[i].text: list1[i]}

    return list1

def parser_ekamedcenter_ru(html):
    soup = BeautifulSoup(html)
    table = soup.find('ul', class_='course-list list')

    list2 = []

    for i in table:
        head = i.find('a')
        if head != -1:
            name = i.find_all('span', {'class' : 'list-name'})
            price = i.find_all('span', {'class' : 'list-price'})
            for j in range(len(name)):
                list2.append({head.text: {
                    'name' : name[j].text,
                    'price' : price[j].text
                }})

    return list2



    # for i in head2:
    #     li = i.find_all('li', recursive = False)
    #     print(li)
    #     break

    # print(head2[1], '\n')
    # if head2 != -1:
    #     for j in head2:
    #         # print(j)
    #         head22 = j.find('a')
    #         print(head22)
    #         # list2.append(head22.text)


    # head = table.find_all('a', class_='list-open cu-p')
    #
    #
    # list_shapka_2 = []
    #
    # for i in table:
    #     head = i.find('a')
    #     list_shapka_1.append(head)
    #
    # for i in table.find_all('ul'):
    #     category = i.find_all('li')
    #     for j in category:
    #         podcategory = j.find('a', class_='list-open cu-p')
    #         list_shapka_2.append(podcategory)



    # print(table)


def parser2(html):
    ##########################

    soup = BeautifulSoup(html)
    table = soup.find('div', {'id' : 'imCell_3'})
    row = table.find_all('tr')

    ##########################
    list1 = []
    lolka1 = 0

    ##########################

    for col in row[1::]:
        price = col.find('b')
        name = col.find('span', {'class' : 'fs17'})

        list1.append({
            'name': name.text,
            'price': price.text
        })
        
    return list1

############olololololo##############


def get_urls(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', {'id' : 'content'})
    li = table.find_all('a')

    str = 'http://www.kdc-lab.ru/'
    list = []

    for l in li[3::]:
        list.append(l.get('href'))

    for i in range(len(list)):
        list[i] = str + list[i]

    list.remove('http://www.kdc-lab.ru/./prejskurant_laboratorii_gemostaza')
    list.remove('http://www.kdc-lab.ru/./prejskurant_laboratorii_mbmi')

    return list


def parser3(html):
    soup = BeautifulSoup(html)
    table = soup.find('div', {'id' : 'content'})
    tableS = table.find_all('table', class_='pintable')

    list1 = []

    for i in tableS:
        tr = i.find_all('tr')
        for j in tr[1::]:
            td = j.find_all('td')
            list1.append({
                'name': re.sub(r'\s+', ' ', td[1].text),
                'price': td[2].text
            })
    #
    # for i in head:
    #     list2.append(i.text)
    #
    # for i in range(len(list2)):
    #     list3.append({
    #         list2[i] : list1[i]
    #     })


    return list1

def parser4(html):
    soup = BeautifulSoup(html)
    table = soup.find('table', class_='table_products')
    tr = table.find_all('tr')

    list = []

    for i in tr[1::]:
        td = i.find_all('td')
        name = i.find('a')
        list.append({
            'name' : name.text,
            'price' : td[2].text
        })

    return list

def main():
    parser_ekamedcenter_ru(get_html("http://www.ekamedcenter.ru/services/"))
    # parser2(get_html("http://lesnoy-zdorove.ru/page-3.html"))
    # get_urls(get_html("http://www.kdc-lab.ru/napravlenija_dejatelnosti/prajs_list"))

    # for i in get_urls(get_html("http://www.kdc-lab.ru/napravlenija_dejatelnosti/prajs_list")):
    #     parser3(get_html(i))

    # parser4(get_html("http://center-light.ru/analysis/index.php?cat"))

    # f = open('file.txt', 'w')
    # f.write(str(parser_ekdc_org(get_html("http://ekdc.org/services"))))

    # with open('data.txt', 'w') as outfile:
    #     json.dump(parser_ekdc_org(get_html("http://ekdc.org/services")), outfile)

if __name__ == '__main__':
    main()
