#
# a1 = "172.14.6.2"
# a2 =map( int, a1.split("."))
#
# print type(a2[0])


def func(self):
    print("func hifewhkfhl")

class MyClass(object):
    myMethod = func

x = MyClass()
x.myMethod()
#
# import threading
#
#
# def worker(num):
#     """thread worker function"""
#     print('Worker: %s' % num)
#
#
# threads = []
# for i in range(5):
#     t = threading.Thread(target=worker, args=(i,))
#     threads.append(t)
#     t.start()
