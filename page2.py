import os
import time
import haobiquge
import biqooge
import gebiqu
import local


def find_book(course, book):
    books = []
    if course == "新笔趣阁":
        book_inf = biqooge.xbiqooge(book)
        books = book_inf
    elif course == "阁笔趣":
        book_inf = gebiqu.gebiqu(book)
        books = book_inf
    elif course == "3z中文网":
        pass
    elif course == "好笔趣阁":
        book_inf = haobiquge.haobiquge(book)
        books = book_inf
    # 书本信息的规范为 书名 最新章节 作者 日期 链接
    return books


def find_chapter(course, url):
    chapter = []
    if course == "新笔趣阁":
        book_inf = biqooge.get_biqooge_book(url)
        chapter = book_inf
    elif course == "阁笔趣":
        book_inf = gebiqu.get_gebiqu_book(url)
        chapter = book_inf
    elif course == "3z中文网":
        pass
    elif course == "好笔趣阁":
        book_inf = haobiquge.get_haobiquge_book(url)
        chapter = book_inf
    # 链接 + 章节名称
    return chapter


def get_text(course, url):
    title = ''
    text = ''
    if course == "新笔趣阁":
        title, text = biqooge.biqooge_chapter(url)
    elif course == "阁笔趣":
        title, text = gebiqu.gebiqu_chapter(url)
    elif course == "3z中文网":
        pass
    elif course == "好笔趣阁":
        title, text = haobiquge.haobiquge_chapter(url)
    elif course == "local":
        title, text = local.readbook(url)

    # 链接 + 章节名称
    return title, text


def collection(book_inf):
    online_book = open('book_case\\online_book.txt', 'a')
    online_book.write('/*/'.join(book_inf)+'\n')
    online_book.close()


def down_load(course, bookname, chapter):
    if bookname not in os.listdir('book'):
        os.mkdir("book/"+bookname)
        f = open("book/"+bookname+'/chapter.txt', 'w')
        os.mkdir("book/" + bookname + '/text')
        for item in chapter:
            f.writelines(item[1] + '\n')
        f.close()
        for item in range(len(chapter)):
            title, texts = get_text(course, chapter[item][0])
            f = open('book/' + bookname + '/text/' + str(item+1) + '.txt', 'w')
            f.write(texts)
            f.close()
            time.sleep(1.5)
    else:
        f = open("book/" + bookname + '/chapter.txt', 'w')
        for item in chapter:
            f.writelines(item[1] + '\n')
        f.close()
        lists = os.listdir('book/' + bookname + '/text')
        for item in lists:
            os.remove('book/' + bookname + '/text/'+item)
        for item in range(len(chapter)):
            title, texts = get_text(course, chapter[item][0])
            f = open('book/' + bookname + '/text/' + str(item + 1) + '.txt', 'w')
            f.write(texts)
            f.close()
            time.sleep(1.5)
    f = open("book/" + bookname + '/book_message.txt', 'w')
    f.write(bookname + ' ' + chapter[0][1] + ' ' + chapter[-1][1])
    f.close()
