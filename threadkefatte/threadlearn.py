import threading,time


def run():
    print("balle balle")


def worker():
    """thread worker function"""
    print("chaked")
    time.sleep(2)


def threadstartkare():
    threads = list()
    for x in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()
        if len(threads) < 3:
            while t.isAlive():
                print (t.name)

    for x in range(5):
        t.join()
    print("yahoo")

threadstartkare()

# list12 = [1,2,3,5]
# #print(list12[:2])