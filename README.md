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

### Connec to container
```sh
nc localhost 8000                                                                                                           11:27:27
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
[ ] Make a docker container
[X] Read file content using `/bin/sh` so it can be used with ROP

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
