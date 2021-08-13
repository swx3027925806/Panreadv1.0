import os


# 初始化书架
def init_book_case():
    list_dir = os.listdir()
    if "book_case" not in list_dir:
        os.mkdir("book_case")
        f = open("book_case/local_book.txt", 'w')
        f.close()
        f = open("book_case/online_book.txt", 'w')
        f.close()
    else:
        ls = os.listdir("book_case")
        if "local_book.txt" not in ls:
            f = open("book_case/local_book.txt", 'w')
            f.close()
        if "online_book.txt" not in ls:
            f = open("book_case/online_book.txt", 'w')
            f.close()


# 初始化书本信息
def init_book():
    list_dir = os.listdir()
    if "book" not in list_dir:
        os.mkdir("book")


# 初始化配置文件信息
def init_config():
    list_dir = os.listdir()
    if "config.txt" not in list_dir:
        f = open("config.txt", 'w')
        config = ['font:宋体', 'font_size:16', 'bg:white']
        f.write('\n'.join(config))
        f.close()


def init_book_course():
    list_dir = os.listdir()
    if "course.txt" not in list_dir:
        f = open("course.txt", 'w')
        config = ['新笔趣阁:https://www.xbiquge.la/', '免费小说网:', '5z中文网:']
        f.write('\n'.join(config))
        f.close()
