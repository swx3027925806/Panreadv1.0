def setting(font="宋体", font_size=16, bg="white"):
    f = open("config.txt", 'w')
    text = 'font:'+font+'\n'+'font_size:'+str(font_size)+'\n'+'bg:'+bg
    f.write(text)
    f.close()
