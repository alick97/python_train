import psutil
import math
import sys

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def show_p_memory(pid, memory: int, message=""):
    print(f"pid: {pid}, memory: {convert_size(memory)} {message}")


def show_memory(pid: int):
    p = psutil.Process(pid)
    total_mem = p.memory_info().rss
    show_p_memory(p.pid, total_mem, f"parent mem, cmd: {' '.join(p.cmdline())}")
    childs = p.children(recursive=True)
    for c in childs:
        m = c.memory_info().rss
        total_mem += m
        show_p_memory(c.pid, m, message=f"child mem, cmd {' '.join(c.cmdline())}")
    show_p_memory(0, total_mem, "==== total mem")

def main():
    if len(sys.argv) < 2:
        print("need pid")
        return
    show_memory(int(sys.argv[1]))


if __name__ == "__main__":
    main()