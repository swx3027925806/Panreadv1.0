'''
Author: your name
Date: 2021-07-23 22:51:46
LastEditTime: 2021-07-23 23:30:21
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \pythoncode\gebiqu.py
'''
import requests
import re


def gebiqu(bookname):
    """
    :param bookname: 搜索的书名
    :return:         返回一个列表，包含书名，最新章节 作者 更新时间 链接
    """
    book_path = "https://www.gebiqu.com/modules/article/search.php?searchkey=" + bookname
    search_page = requests.get(book_path)
    search_page.encoding = 'UTF-8'
    tr_find = re.compile('<tr id="nr">(.*?)</tr>', re.S)
    tr_all = tr_find.findall(search_page.text)
    all_inf = []
    for item in tr_all:
        text_find = re.compile('>(.*?)<')
        text_all = text_find.findall(item)
        while '' in text_all:
            text_all.remove('')
        text_all = text_all[:4]
        text_all += re.findall('href="(http.*?)">', item)
        text_all[4] = text_all[4].replace('txt/', 'biquge_').replace('.html', '/')
        all_inf.append(text_all[:5])
    return all_inf


def get_gebiqu_book(url):
    """
    :param url:  鼠标的链接
    :return:     书的章节列表
    """
    book_page = requests.get(url)
    book_page.encoding = 'UTF-8'
    box_find = re.compile('<div id="list">(.*?)</div>', re.S)
    chapter_box = box_find.findall(book_page.text)

    chapter_list = re.findall('<a href="(.*?)">(.*?)</a>', chapter_box[0])

    return chapter_list


def gebiqu_chapter(url):
    """
    :param url: 章节的链接
    :return:    返回章节的题目和正文
    """
    book_page = requests.get("http://www.gebiqu.com" + url)
    book_page.encoding = 'UTF-8'
    title = re.findall('<h1>(.*?)</h1>', book_page.text)

    text_find = re.compile('<div id="content">(.*?)</div>', re.S)
    texts = str(text_find.findall(book_page.text))
    texts = texts[1:-1].replace('\'', '').replace('&nbsp;', ' ').replace('br', '\n').replace('<\n/>', '\n')

    return title, texts


# gebiqu("育")
# get_gebiqu_book('http://www.gebiqu.com/txt/173850.html')
# gebiqu_chapter('/biquge_173850/35304842.html')