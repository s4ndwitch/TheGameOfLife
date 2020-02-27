import time

tit1 = time.time()

# .....код программы
while True:
    tit2 = time.time()
    print(type(tit2))
    print(u'скорость обработки: %.2f' % (tit2 - tit1))
