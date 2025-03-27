# AAU Grader

The idea is to make a small example binary vulnerable to buffer overflows.
The binary takes a username as input and returns the grades for that student.

Make the binary vulnerable to buffer overflows when providing username.

Hackers can manipulate the grading file.

One version where we can provide our own payload, and one
that is only hackable using ROP as a technique.

## Building and executing

* Disable stack canary `-fno-stack-protector`
* Make stack executable `-z execstack`

### Makefile

```sh
make all # builds both stack executable and only roppable binary
make pwn # builds only stack executable binary
make pwn_rop # builds only non stack exectuable binary, has to ROP
make clean # removes binary builds
````

### Manually
```sh
gcc main.c -m32 -o aaugrader -fno-stack-protector -z execstack && ./aaugrader
```

## Docker
Stolen template from https://github.com/osirislab/CSAW-CTF-2019-Finals/blob/master/pwn/defile/
### Build
```sh
docker build . -t aaugrader
```

### Run
```sh
docker run -p 8000:8000 --rm --name=aaugrader -d -it aaugrader
```

### Stop
```sh
docker stop aaugrader
```

### Enter container to debug
```sh
docker exec -it aaugrader bash
```

### Connect to container

#### Remote
```sh
nc aaugrader.bevster.net 8000
```
#### Local
```sh
nc localhost 8000
 ▗▄▖  ▗▄▖ ▗▖ ▗▖    ▗▄▄▖▗▄▄▖  ▗▄▖ ▗▄▄▄  ▗▄▄▄▖▗▄▄▖ 
▐▌ ▐▌▐▌ ▐▌▐▌ ▐▌   ▐▌   ▐▌ ▐▌▐▌ ▐▌▐▌  █ ▐▌   ▐▌ ▐▌
▐▛▀▜▌▐▛▀▜▌▐▌ ▐▌   ▐▌▝▜▌▐▛▀▚▖▐▛▀▜▌▐▌  █ ▐▛▀▀▘▐▛▀▚▖
▐▌ ▐▌▐▌ ▐▌▝▚▄▞▘   ▝▚▄▞▘▐▌ ▐▌▐▌ ▐▌▐▙▄▄▀ ▐▙▄▄▖▐▌ ▐▌
                                                 
(C) 2025                                         
This program returns the grades for the specified user.
Username: sberge24
	02
	02
	04
	07
	12
```

## Todo
- [X] Make a docker container
- [X] Read file content using `/bin/sh` so it can be used with ROP

## Format

grades.txt file format

Usernames and grades seperated with a colon.
Grades seperated with a semicolon.
```
<username>:grade;grade;grade;grade
```

### Example
```
vfrank21:12;12;12;12;12
slaza24:12;12;12;12;12
lsfr21:12;12;12;12;12
magdan21:12;12;12;12;12
sberge24:02;02;04;07;12
```

## Run exploits
### Examples

```sh
./exploits/exploit.py -b aaugrader
```

```sh
./exploits/exploit.py -s aaugrader.bevster.net -p 8000

[+] Opening connection to aaugrader.bevster.net on port 8000: Done
[*] Switching to interactive mode
Username is too long!
$ ls
aaugrader
grades.txt
run.sh
$ id
uid=1001(jens) gid=1001(jens) groups=1001(jens)
```
### Replace a line in file
`sed -i 's/sberge24:02;02;04;07;12/sberge24:12;12;12;12;12/' grades.txt`

### Help
```sh
usage: exploit.py [-h] [-b BINARY] [-s SERVER] [-p PORT]

AAU GRADER Exploitation Program 3000

options:
  -h, --help           show this help message and exit
  -b, --binary BINARY  Specify local binary
  -s, --server SERVER  Specify server hostname / ip
  -p, --port PORT      Specify port for server
```
