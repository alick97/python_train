import time

import time
def follow(thefile):
    thefile.seek(0,2)      # Go to the end of the file
    while True:
         line = thefile.readline()
         if not line:
             time.sleep(0.1)    # Sleep briefly
             continue
         yield line

# Example use
if __name__ == '__main__':
    logfile = open("access-log.txt")
    for line in follow(logfile):
        print(line)