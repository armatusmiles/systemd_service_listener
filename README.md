## This is an example how you can test the systemd service

### Run
```
python3 notify_listener.py
```

### Dependency
```
sudo apt-get install libsystemd-dev
```

### Service compile
```
gcc -o service service.c -lsystemd
```
