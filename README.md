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

```sh
gcc main.c -o aaugrader -fno-stack-protector -z execstack && ./aaugrader
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
