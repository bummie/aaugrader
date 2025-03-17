# AAU Grader

The idea is to make a small example binary vulnerable to buffer overflows.
The binary takes a username as input and returns the grades for that student.

Make the binary vulnerable to buffer overflows when providing username.

Hackers can manipulate the grading file.

One version where we can provide our own payload, and one
that is only hackable using ROP as a technique.

## Building and executing

```sh
gcc main.c && ./a.out
```

## Todo
[ ] Make a docker container
[ ] Read file content using `/bin/sh` so it can be used with ROP
