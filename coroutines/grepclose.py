# grepclose.py
#
# A coroutine that catches the close() operation

from coroutine import coroutine

@coroutine
def grep(pattern):
    print("Looking for %s" % pattern)
    try:
        while True:
            line = (yield)
            # print('=====', type(line))
            print('debug: grep line: {}'.format(line))
            if pattern in line:
                print(line)
    except GeneratorExit:
        print("Going away. Goodbye")

# Example use
if __name__ == '__main__':
    g = grep("python")
    g.send("Yeah, but no, but yeah, but no\n")
    g.send("A series of tubes\n")
    g.send("python generators rocka!\n")
    g.close()
