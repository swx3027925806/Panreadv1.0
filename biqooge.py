import requests
import re


def xbiqooge(bookname):
    """
    :param bookname: 搜索的书名
    :return:         返回一个列表，包含书名，最新章节 作者 更新时间 链接
    """
    book_path = "https://www.xbiquge.la/modules/article/waps.php?searchkey=" + bookname
    search_page = requests.get(book_path)
    search_page.encoding = 'UTF-8'
    tr_find = re.compile('<tr>(.*?)</tr>', re.S)
    tr_all = tr_find.findall(search_page.text)
    all_inf = []
    for item in tr_all:
        text_find = re.compile('>(.*?)<')
        text_all = text_find.findall(item)
        while '' in text_all:
            text_all.remove('')
        text_all += re.findall('href="(http.*?)"', item)
        all_inf.append(text_all)
    return all_inf


def get_biqooge_book(url):
    """
    :param url:  鼠标的链接
    :return:     书的章节列表
    """
    book_page = requests.get(url)
    book_page.encoding = 'UTF-8'
    box_find = re.compile('<div class="box_con">(.*?)</div>', re.S)
    chapter_box = box_find.findall(book_page.text)[1]

    chapter_list = re.findall('<a href=\'(.*?)\' >(.*?)</a>', chapter_box)

    return chapter_list


def biqooge_chapter(url):
    """
    :param url: 章节的链接
    :return:    返回章节的题目和正文
    """
    book_page = requests.get("https://www.xbiquge.la/" + url)
    book_page.encoding = 'UTF-8'
    title = re.findall('<h1>(.*?)</h1>', book_page.text)

    text_find = re.compile('<div id="content">(.*?)<p>', re.S)
    texts = str(text_find.findall(book_page.text))
    texts = texts[1:-1].replace('\'', '').replace('&nbsp;', ' ').replace('br', '').replace(r'\r< />', '\n')

    return title, texts


# biqooge("育")
# get_biqooge_book('https://www.xbiquge.la/11/11433/')
# biqooge_chapter('https://www.xbiquge.la//11/11433/4855559.html')