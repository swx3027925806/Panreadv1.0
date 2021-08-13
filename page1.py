import os
import shutil


# 显示书架上的书
def book_case_local():
    local_book = open('book_case\\local_book.txt', 'r')
    lb_list = local_book.readlines()
    local_book.close()

    local_list = []
    for line in lb_list:
        temp = line.split(' ')
        local_list.append(temp)

    return local_list


def book_case_online():
    online_book = open('book_case\\online_book.txt', 'r')
    ob_list = online_book.readlines()
    online_book.close()

    online_list = []
    for line in ob_list:
        temp = line.split('/*/')
        online_list.append(temp)

    return online_list


# 更新本地书架
def fresh():
    book = []
    f = open("book_case/local_book.txt", 'w')
    for item in os.listdir('book'):
        if 'book_message.txt' in os.listdir('book/'+ item):
            files = open('book/' + item + '/book_message.txt', 'r')
            book.append(files.read())
            files.close()
    f.writelines(book)
    f.close()


def del_online_book(lists):
    f = open('book_case\\online_book.txt', 'w')
    for item in lists:
        f.write('/*/'.join(item) + '\n')
    f.close()


def del_local_book(bookname):
    shutil.rmtree("book/"+bookname)


def get_chapter(bookname):
    path = 'book/' + bookname
    answer = []
    f = open(path + '/chapter.txt', 'r')
    chapter_name = f.readlines()
    for item in range(len(chapter_name)):
        answer.append((path+'/text/'+str(item+1)+'.txt', chapter_name[item]))
    return answer
