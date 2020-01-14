# Info
Simple example of protocol parser in C.


# Build
```
cd /C/
gcc parser.c -o parser
```
This will generate the program 'parser'. See above on how to run it.

In case you want to debug the code, run with the flag '-g':
```
cd /C/
gcc -g parser.c -o parser
```

The contains multiple debug levels.
Set the define *DEBUG* in the file *parser.c* accordingly:
```
#define DEBUG 0
```

# Run
Parameter: IP-address of server.
```
cd /C/
./parser 192.168.0.216
```
`Note:` the port (13100) is hardcoded.

# Issues
 - Segmentation fault happens when there is a lot of data

# Todos
 - Add timing
 - Make more robust (fix some minor bugs)
