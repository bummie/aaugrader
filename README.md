# AAU Grader

This project contains a binary, two exploit techniques and detection systems.


## Docker Compose Setup

```sh
# Download docker compose v2

# Start containers
docker compose up
```

### System call detection system
System call based detection system will be available at http://localhost:8080/


### Executable Stack binary
```sh
nc localhost 8000
```

### Non-executable stack binary
```sh
nc localhost 8001
```

## Run exploits

### Setup python
```sh
# Change directory to root of project
cd AAUGRADER

# Create a virtual python environment
python3 -m venv venv

# Activate virtual environment
. venv/bin/activate
# Or if using fish
. venv/bin/activate.fish

# Install dependencies
pip3 install -r requirements.txt

```
### Executable Stack exploit
```sh
python3 src/exploits/exploit.py -s localhost -p 8000
```

### Non-Executable Stack exploit
```sh
python3 src/exploits/rop_exploit.py -s localhost -p 8001 -b src/binary/aaugrader_rop
```

## Building and executing manually

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
Demo video: https://asciinema.org/a/HXxDZxsyPVmJ0jY3PsEc6kbLE

### Examples

```sh
./exploits/exploit.py -b aaugrader
```

```sh
./exploits/exploit.py -s localhost -p 8000

[+] Opening connection to localhost on port 8000: Done
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
