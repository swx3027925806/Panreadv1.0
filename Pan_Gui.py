import tkinter as tk
import tkinter.ttk as ttk
import threading
import page1
import page2
import page4


class PanGui:
    def __init__(self):
        self.root = tk.Tk()

        # 窗口设置
        w = self.root.winfo_screenwidth()
        h = int(self.root.winfo_screenheight()*0.9)
        self.root.geometry("%dx%d+0+0" % (w, h))
        self.root.state("zoomed")
        self.root.title("Pan读")

        # 参数区
        self.config = {}
        self.book_course = {"新笔趣阁": "https://www.xbiquge.la/",
                              "阁笔趣": "https://www.gebiqu.com/",
                            "好笔趣阁": "https://www.haobiquge.com"}  # 未载入

        # 变量管理
        self.local_book_list = []   # 书名 章节 作者 更新日期
        self.online_book_list = []  # 书名 章节 链接 书源 书架
        self.book_inf = []          # 书名 章节 作者 更新日期 链接 书城
        self.chapter_last = []      # 章节信息  链接+章节
        self.chapter_index = 0
        self.book_link = ''
        self.course = ''

        # 载入配置文件
        self.load_config()
        if "font_size" in self.config.keys():
            self.config['font_size'] = int(self.config['font_size'])

        # 主窗口设计
        self.main_page = ttk.Notebook(self.root)
        self.main_page.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

        # 分页设计
        # 书架页面设计
        self.tab1 = tk.Frame(self.main_page)
        self.tab1.place(x=0, y=30)
        self.main_page.add(self.tab1, text='书架')

        tk.Label(self.tab1, text='本地书架', font=(self.config['font'], self.config['font_size']))\
            .place(relx=0.48, rely=0.01)
        self.local_case_box = tk.Listbox(self.tab1, font=(self.config['font'], self.config['font_size']))
        self.local_case_box.place(relx=0.02, rely=0.05, relwid=0.96, relhei=0.42)

        local_refresh_btn = tk.Button(self.tab1, text='刷新',
                                      font=(self.config['font'], self.config['font_size']), command=self.local_fresh)
        local_refresh_btn.place(relx=0.7, rely=0.01, relwid=0.08, relhei=0.04)
        local_case_btn = tk.Button(self.tab1, text='打开',
                                   font=(self.config['font'], self.config['font_size']), command=self.open_local_book)
        local_case_btn.place(relx=0.8, rely=0.01, relwid=0.08, relhei=0.04)
        local_del_btn = tk.Button(self.tab1, text='删除',
                                  font=(self.config['font'], self.config['font_size']), command=self.del_local_book)
        local_del_btn.place(relx=0.9, rely=0.01, relwid=0.08, relhei=0.04)

        tk.Label(self.tab1, text='在线书架', font=(self.config['font'], self.config['font_size']))\
            .place(relx=0.48, rely=0.48)
        self.online_case_box = tk.Listbox(self.tab1, font=(self.config['font'], self.config['font_size']))
        self.online_case_box.place(relx=0.02, rely=0.52, relwid=0.96, relhei=0.42)

        online_refresh_btn = tk.Button(self.tab1, text='刷新',
                                       font=(self.config['font'], self.config['font_size']), command=self.online_fresh)
        online_refresh_btn.place(relx=0.7, rely=0.48, relwid=0.08, relhei=0.04)
        online_case_btn = tk.Button(self.tab1, text='打开',
                                    font=(self.config['font'], self.config['font_size']), command=self.open_online_thread)
        online_case_btn.place(relx=0.8, rely=0.48, relwid=0.08, relhei=0.04)
        online_del_btn = tk.Button(self.tab1, text='删除',
                                   font=(self.config['font'], self.config['font_size']), command=self.del_online_book)
        online_del_btn.place(relx=0.9, rely=0.48, relwid=0.08, relhei=0.04)

        self.local_fresh()
        self.online_fresh()

        ####################################################################################

        # 书城搜索页面设计
        self.tab2 = tk.Frame(self.main_page)
        self.tab2.place(x=0, y=30)
        self.main_page.add(self.tab2, text='书城')

        tk.Label(self.tab2, text='书源:', font=(self.config['font'], self.config['font_size']))\
            .place(relx=0.01, rely=0.1, relwid=0.05, relhei=0.04)
        # 下拉菜单
        self.com = ttk.Combobox(self.tab2, font=(self.config['font'], self.config['font_size']))  # #创建下拉菜单
        self.com.place(relx=0.08, rely=0.1, relwid=0.4, relhei=0.04)  # #将下拉菜单绑定到窗体
        self.com["value"] = tuple(self.book_course.keys())  # #给下拉菜单设定值
        self.com.current(0)  # #设定下拉菜单的默认值为第0个

        tk.Label(self.tab2, text='搜书:', font=(self.config['font'], self.config['font_size'])) \
            .place(relx=0.01, rely=0.01, relwid=0.05, relhei=0.04)

        self.search_cin = tk.Entry(self.tab2, font=(self.config['font'], self.config['font_size']))
        self.search_cin.place(relx=0.08, rely=0.01, relwid=0.4, relhei=0.04)

        com_button = tk.Button(self.tab2, text="搜索", font=(self.config['font'], self.config['font_size']),
                               command=self.search_thread)
        com_button.place(relx=0.5, rely=0.01, relwid=0.08, relhei=0.04)

        self.book_list_page2 = tk.Listbox(self.tab2, font=(self.config['font'], self.config['font_size']),
                                          selectmode=tk.BROWSE)
        self.book_list_page2.place(relx=0.01, rely=0.2, relwid=0.57, relhei=0.7)

        book_button = tk.Button(self.tab2, text="确定书本",
                                font=(self.config['font'], self.config['font_size']), command=self.get_book_thread)
        book_button.place(relx=0.5, rely=0.1, relwid=0.08, relhei=0.04)

        save_button = tk.Button(self.tab2, text="收藏", font=(self.config['font'], self.config['font_size'])
                                , command=self.collection)
        save_button.place(relx=0.6, rely=0.01, relwid=0.08, relhei=0.04)

        self.star_page = tk.Entry(self.tab2, font=(self.config['font'], self.config['font_size']))
        self.star_page.place(relx=0.7, rely=0.01, relwid=0.08, relhei=0.04)

        self.end_page = tk.Entry(self.tab2, font=(self.config['font'], self.config['font_size']))
        self.end_page.place(relx=0.8, rely=0.01, relwid=0.08, relhei=0.04)

        down_button = tk.Button(self.tab2, text="下载",
                                font=(self.config['font'], self.config['font_size']), command=self.down_load_thread)
        down_button.place(relx=0.9, rely=0.01, relwid=0.08, relhei=0.04)

        self.book_name_page2 = tk.Entry(self.tab2, font=(self.config['font'], self.config['font_size']))
        self.book_name_page2.place(relx=0.6, rely=0.1, relwid=0.28, relhei=0.04)

        read_button_2 = tk.Button(self.tab2, text="阅读", font=(self.config['font'], self.config['font_size']),
                                  command=self.read_page2_thread)
        read_button_2.place(relx=0.9, rely=0.1, relwid=0.08, relhei=0.04)

        self.chapter_list_box = tk.Listbox(self.tab2, font=(self.config['font'], self.config['font_size']))
        self.chapter_list_box.place(relx=0.6, rely=0.2, relwid=0.38, relhei=0.7)

        #########################################################################################

        self.tab3 = tk.Frame(self.main_page)
        self.tab3.place(x=0, y=30)
        self.main_page.add(self.tab3, text='阅读')

        self.book_name2 = tk.Text(self.tab3, font=(self.config['font'], self.config['font_size']), state='disable')
        self.book_name2.place(relx=0.01, rely=0.01, relwid=0.15, relhei=0.04)

        self.chapter_list_box2 = tk.Listbox(self.tab3, font=(self.config['font'], self.config['font_size']))
        self.chapter_list_box2.place(relx=0.01, rely=0.06, relwid=0.15, relhei=0.9)

        self.text_area = tk.Text(self.tab3, font=(self.config['font'], self.config['font_size']), state='disable')
        self.text_area.place(relx=0.18, rely=0.06, relwid=0.8, relhei=0.9)

        read_button_3 = tk.Button(self.tab3, text='阅读',
                                  font=(self.config['font'], self.config['font_size']), command=self.read_page3_thread)
        read_button_3.place(relx=0.18, rely=0.01, relwid=0.08, relhei=0.04)

        bookmarks = tk.Button(self.tab3, text='收藏',
                              font=(self.config['font'], self.config['font_size']))
        bookmarks.place(relx=0.28, rely=0.01, relwid=0.08, relhei=0.04)

        pre_button = tk.Button(self.tab3, text='上一章',
                               font=(self.config['font'], self.config['font_size']), command=self.pre_page2)
        pre_button.place(relx=0.8, rely=0.01, relwid=0.08, relhei=0.04)

        next_button = tk.Button(self.tab3, text='下一章',
                                font=(self.config['font'], self.config['font_size']), command=self.next_page2)
        next_button.place(relx=0.9, rely=0.01, relwid=0.08, relhei=0.04)

        ######################################################################################################

        self.tab4 = tk.Frame(self.main_page)
        self.tab4.place(x=0, y=30)
        self.main_page.add(self.tab4, text='设置')

        tk.Label(self.tab4, text='字体设置:', font=(self.config['font'], self.config['font_size'])) \
            .place(relx=0.05, rely=0.04, relwid=0.08, relhei=0.05)
        self.font_label = ttk.Combobox(self.tab4, font=(self.config['font'], self.config['font_size']))  # #创建下拉菜单
        self.font_label.place(relx=0.15, rely=0.05, relwid=0.1)  # #将下拉菜单绑定到窗体
        self.font_label["value"] = ("宋体", "楷体", "黑体")  # #给下拉菜单设定值
        self.font_label.current(0)  # #设定下拉菜单的默认值为第3个，即山东

        tk.Label(self.tab4, text='字体大小:', font=(self.config['font'], self.config['font_size'])) \
            .place(relx=0.3, rely=0.04, relwid=0.08, relhei=0.05)
        self.font_size = tk.Entry(self.tab4, font=(self.config['font'], self.config['font_size']))
        self.font_size.place(relx=0.4, rely=0.05, relwid=0.05)

        tk.Label(self.tab4, text='背景颜色:', font=(self.config['font'], self.config['font_size'])) \
            .place(relx=0.05, rely=0.14, relwid=0.08, relhei=0.05)
        background = ttk.Combobox(self.tab4, font=(self.config['font'], self.config['font_size']))  # #创建下拉菜单
        background.place(relx=0.15, rely=0.15, relwid=0.1)  # #将下拉菜单绑定到窗体
        background["value"] = ("浅蓝", "蛋黄", "纯白")  # #给下拉菜单设定值
        background.current(0)  # #设定下拉菜单的默认值为第3个，即山东

        tk.Label(self.tab4, text='人声朗读:', font=(self.config['font'], self.config['font_size'])) \
            .place(relx=0.05, rely=0.24, relwid=0.08, relhei=0.05)
        read_aloud = ttk.Combobox(self.tab4, font=(self.config['font'], self.config['font_size']))  # #创建下拉菜单
        read_aloud.place(relx=0.15, rely=0.25, relwid=0.1)  # #将下拉菜单绑定到窗体
        read_aloud["value"] = ("windows", "女声", "男声")  # #给下拉菜单设定值
        read_aloud.current(0)  # #设定下拉菜单的默认值为第3个，即山东

        setting_button = tk.Button(self.tab4, text="确定设置",
                                font=(self.config['font'], self.config['font_size']), command=self.setting)
        setting_button.place(relx=0.05, rely=0.8, relwid=0.08, relhei=0.04)

        # 热键绑定
        self.root.bind('<F1>', self.bind_pre_page)
        self.root.bind('<F2>', self.bind_next_page)

        self.root.mainloop()

    def load_config(self):
        f = open("config.txt", 'r')
        lines = f.readlines()
        for line in lines:
            self.config[line.split(':')[0]] = line.split(':')[1]
        f.close()

    def load_book_course(self):
        f = open("course.txt", 'r')
        lines = f.readlines()
        for line in lines:
            self.book_course[line.split(':')[0]] = line.split(':')[1]
        f.close()

    # 书架的函数——————————————————————————————————————————————————————————————————————————————————————————
    def local_fresh(self):
        page1.fresh()
        self.local_book_list = page1.book_case_local()
        self.local_case_box.delete(0, tk.END)
        for item in self.local_book_list:
            self.local_case_box.insert("end", item)

    def online_fresh(self):
        self.online_book_list = page1.book_case_online()
        self.online_case_box.delete(0, tk.END)
        for item in self.online_book_list:
            self.online_case_box.insert("end", item[:3])

    def open_local_book(self):
        self.course = "local"
        index = self.local_case_box.curselection()[0]

        self.chapter_last = page1.get_chapter(self.local_book_list[index][0])
        title, text = page2.get_text(self.course, self.chapter_last[0][0])
        book_name = self.local_book_list[index][0]

        self.book_name2.delete(1.0, 'end')
        self.book_name2.insert(1.0, book_name)
        self.book_name2['state'] = tk.DISABLED

        self.chapter_list_box2.delete(0, tk.END)
        for item in range(1, len(self.chapter_last) + 1):
            temp = str(item) + ' ' + self.chapter_last[item - 1][-1]
            self.chapter_list_box2.insert("end", temp)

        self.text_area['state'] = tk.NORMAL
        self.text_area.delete(1.0, 'end')
        self.text_area.insert(1.0, text)
        self.text_area['state'] = tk.DISABLED
        pass

    def open_online_thread(self):
        thread = threading.Thread(target=self.open_online_book)
        thread.start()

    def open_online_book(self):
        book_inf = page1.book_case_online()
        index = self.online_case_box.curselection()
        index = index[0]
        book_inf = self.online_book_list[index]

        self.course = book_inf[2]

        self.book_name2['state'] = tk.NORMAL
        book_name = book_inf[0]
        self.book_name2.delete(1.0, 'end')
        self.book_name2.insert(1.0, book_name)
        self.book_name2['state'] = tk.DISABLED

        self.chapter_last = page2.find_chapter(self.course, book_inf[-1])
        self.chapter_list_box2.delete(0, tk.END)
        for item in range(1, len(self.chapter_last) + 1):
            temp = str(item) + ' ' + self.chapter_last[item - 1][-1]
            self.chapter_list_box2.insert("end", temp)

        self.text_area['state'] = tk.NORMAL
        self.text_area.delete(1.0, 'end')
        text_title, text_content = page2.get_text(self.course, book_inf[-2])
        self.text_area.insert(1.0, text_content)
        self.text_area.insert(1.0, text_title[0] + '\n')
        self.text_area['state'] = tk.DISABLED

        self.chapter_index = int(book_inf[1].split()[0])

    def del_local_book(self):
        index = self.local_case_box.curselection()
        index = index[0]
        book_name = self.local_book_list[index][0]
        page1.del_local_book(book_name)
        self.local_fresh()

    def del_online_book(self):
        index = self.online_case_box.curselection()
        index = index[0]
        del self.online_book_list[index]
        page1.del_online_book(self.online_book_list)
        self.online_fresh()

    # 书城的函数——————————————————————————————————————————————————————————————————————————————————————————
    def search_thread(self):
        thread = threading.Thread(target=self.search_book_list)
        thread.start()

    def search_book_list(self):
        self.course = self.com.get()
        book = self.search_cin.get()
        self.book_inf = page2.find_book(self.course, book)
        self.book_list_page2.delete(0, tk.END)
        for item in self.book_inf:
            temp = "{0:{4}<12}{1:{4}<20}{2:{4}<10}{3:{4}<8}"\
                .format(item[0], item[1], item[2], item[3], chr(12288))
            self.book_list_page2.insert("end", temp)

    def get_book_thread(self):
        thread = threading.Thread(target=self.get_book)
        thread.start()

    def get_book(self):
        book = self.book_list_page2.curselection()
        book_inf = self.book_inf[book[0]]
        self.book_link = book_inf[-1]
        self.chapter_last = page2.find_chapter(self.course, book_inf[-1])

        self.book_name_page2.delete(0, 'end')
        self.book_name_page2.insert(0, book_inf[0])

        self.chapter_list_box.delete(0, tk.END)
        for item in range(1, len(self.chapter_last)+1):
            temp = str(item) + ' ' + self.chapter_last[item-1][-1]
            self.chapter_list_box.insert("end", temp)

    def read_page2_thread(self):
        thread = threading.Thread(target=self.read_book_page2)
        thread.start()

    def read_book_page2(self):
        chapter = self.chapter_list_box.curselection()
        self.chapter_index = chapter[0]
        chapter = self.chapter_last[chapter[0]]

        self.book_name2['state'] = tk.NORMAL
        book_name = self.book_name_page2.get()
        self.book_name2.delete(1.0, 'end')
        self.book_name2.insert(1.0, book_name)
        self.book_name2['state'] = tk.DISABLED

        self.chapter_list_box2.delete(0, tk.END)
        for item in range(1, len(self.chapter_last) + 1):
            temp = str(item) + ' ' + self.chapter_last[item - 1][-1]
            self.chapter_list_box2.insert("end", temp)

        self.text_area['state'] = tk.NORMAL
        self.text_area.delete(1.0, 'end')
        text_title, text_content = page2.get_text(self.course, chapter[0])
        self.text_area.insert(1.0, text_content)
        self.text_area.insert(1.0, text_title[0] + '\n')
        self.text_area['state'] = tk.DISABLED

    def down_load_thread(self):
        thread = threading.Thread(target=self.down_load_book)
        thread.start()

    def down_load_book(self):
        star = int(self.star_page.get())
        end = int(self.end_page.get())
        bookname = self.book_name_page2.get()
        chapter_list = []
        if end < len(self.chapter_last)-1:
            chapter_list = self.chapter_last[star:end+1]
        else:
            chapter_list = self.chapter_last[star:]

        page2.down_load(self.course, bookname, chapter_list)
        pass

    def collection(self):
        book_name = self.book_name_page2.get()
        chapter = self.chapter_list_box.curselection()
        self.chapter_index = chapter[0]
        chapter = self.chapter_last[chapter[0]]
        book_inf = [book_name, str(self.chapter_index+1)+' '+chapter[1],  self.course, chapter[0], self.book_link]
        page2.collection(book_inf)
        pass

    # 阅读的函数——————————————————————————————————————————————————————————————————————————————————————————
    def next_page2(self):
        thread = threading.Thread(target=self.goto_next)
        thread.start()

    def pre_page2(self):
        thread = threading.Thread(target=self.goto_pre)
        thread.start()

    def read_page3_thread(self):
        thread = threading.Thread(target=self.read_book_page3)
        thread.start()

    def read_book_page3(self):
        chapter = self.chapter_list_box2.curselection()
        self.chapter_index = chapter[0]
        chapter = self.chapter_last[chapter[0]]

        self.text_area['state'] = tk.NORMAL
        self.text_area.delete(1.0, 'end')
        text_title, text_content = page2.get_text(self.course, chapter[0])
        self.text_area.insert(1.0, text_content)
        self.text_area.insert(1.0, text_title[0] + '\n')
        self.text_area['state'] = tk.DISABLED

    # 设置的函数——————————————————————————————————————————————————————————————————————————————————————————
    def setting(self):
        font = self.font_label.get()
        font_size = self.font_size.get()
        page4.setting(font, font_size)
        pass

    # 热键绑定函数—————————————————————————————————————————————————————————————————————————————————————————
    def bind_next_page(self, event):
        thread = threading.Thread(target=self.goto_next)
        thread.start()

    def goto_next(self):
        if self.chapter_index < len(self.chapter_last) - 1:
            self.chapter_index += 1
            chapter = self.chapter_last[self.chapter_index]
            self.text_area['state'] = tk.NORMAL
            self.text_area.delete(1.0, 'end')
            text_title, text_content = page2.get_text(self.course, chapter[0])
            self.text_area.insert(1.0, text_content)
            self.text_area.insert(1.0, text_title[0] + '\n')
            self.text_area['state'] = tk.DISABLED

    def bind_pre_page(self, event):
        thread = threading.Thread(target=self.goto_pre)
        thread.start()

    def goto_pre(self):
        if self.chapter_index > 0:
            self.chapter_index -= 1
            chapter = self.chapter_last[self.chapter_index]
            self.text_area['state'] = tk.NORMAL
            self.text_area.delete(1.0, 'end')
            text_title, text_content = page2.get_text(self.course, chapter[0])
            self.text_area.insert(1.0, text_content)
            self.text_area.insert(1.0, text_title[0] + '\n')
            self.text_area['state'] = tk.DISABLED
