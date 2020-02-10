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

*DEBUG* levels goes from 0 to 3, and changes the way that the script prints data.\
See [*DEBUG* examples](#debug-examples) for some screenshots.

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

# *DEBUG* examples
Here is some examples for different *#DEBUG* values.

```
#define DEBUG 0
```
![Console view](/Data%20API/TCP_binary/C/debug_0.png?raw=true "Debug 0")

```
#define DEBUG 1
```
![Console view](/Data%20API/TCP_binary/C/debug_1.png?raw=true "Debug 1")

```
#define DEBUG 2
```
![Console view](/Data%20API/TCP_binary/C/debug_2.png?raw=true "Debug 2")

```
#define DEBUG 3
```
![Console view](/Data%20API/TCP_binary/C/debug_3.png?raw=true "Debug 3")