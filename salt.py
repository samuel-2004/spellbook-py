from random import shuffle

def getsaltlist():
    f = open("saltmessages.txt")
    lines = f.readlines()
    f.close()
    shuffle(lines)
    return lines
def gettaglist():
    f = open("tagmessages.txt")
    lines = f.readlines()
    f.close()
    shuffle(lines)
    return lines
def addsaltmsg(msg):
    f = open("saltshortlist.txt", "a")
    f.write(msg + "\n")
    f.close()
def addtagmsg(msg):
    f = open("tagshortlist.txt", "a")
    f.write(msg + "\n")
    f.close()


if __name__ == "__main__":
    print(len(getsaltlist()))
