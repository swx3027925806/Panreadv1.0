def readbook(url):
    f = open(url, 'r')
    text = f.read()
    f.close()
    return 'wu', text
