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


def haobiquge(bookname):
    """
    :param bookname: 搜索的书名
    :return:         返回一个列表，包含书名，最新章节 作者 更新时间 链接
    """
    book_path = "https://www.haobiquge.com/search/%s/"%(bookname)
    search_page = requests.get(book_path)
    search_page.encoding = 'UTF-8'
    tr_find = re.compile('<div class="info">(.*?)<div class="yuedu">', re.S)
    tr_all = tr_find.findall(search_page.text)
    all_inf = []
    for item in tr_all:
        text_find = re.compile('<a href="(.*?)">(.*?)</a>', re.S)
        author_find = re.compile('<span>(.*?)</span>')
        text_all = text_find.findall(item)
        author_all = author_find.findall(item)
        while '' in text_all:
            text_all.remove('')
        text_all = [text_all[0][1], text_all[1][1], author_all[0], '无更新日期', text_all[0][0]]
        all_inf.append(text_all[:5])

    return all_inf


def get_haobiquge_book(url):
    """
    :param url:  鼠标的链接
    :return:     书的章节列表
    """
    url = "https://www.haobiquge.com"+url
    book_page = requests.get(url)
    book_page.encoding = 'UTF-8'
    box_find = re.compile('<dd>(.*?)</dd>', re.S)
    chapter_box = box_find.findall(book_page.text)

    chapter_list = []

    for item in chapter_box:
        chapter_list += re.findall('<a href="(.*?)">(.*?)</a>', item)

    return chapter_list


def haobiquge_chapter(url):
    """
    :param url: 章节的链接
    :return:    返回章节的题目和正文
    """
    book_page = requests.get("https://www.haobiquge.com" + url)
    book_page.encoding = 'UTF-8'
    title = re.findall('<h1>(.*?)</h1>', book_page.text)

    text_find = re.compile('div class="zhangjieTXT" id="TXT">(.*?)</div>', re.S)
    texts = str(text_find.findall(book_page.text))
    texts = texts[1:-1].replace('<br /><br />', '<br />').replace('<br />', '\n\n    ')

    return title, texts

# gebiqu("斗罗大陆")
# get_gebiqu_book('/read/98174/')
# gebiqu_chapter('/chapter/98174/2800304.html')