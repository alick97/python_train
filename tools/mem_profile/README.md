#### show process and subprocess memory usage

##### example
```
python3 mem.py [parent process id]
```
##### result
```
python3 mem.py 1468
pid: 1468, memory: 14.38 MB parent mem, cmd: /usr/local/opt/redis/bin/redis-server 127.0.0.1:6379
pid: 0, memory: 14.38 MB ==== total mem
```

> for more feature, you can use python tool [memory_profiler](https://github.com/pythonprofilers/memory_profiler)

