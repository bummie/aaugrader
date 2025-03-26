all: pwn pwnrop

pwn:
	gcc ./src/main.c -m32 -o aaugrader -z execstack -Wimplicit-function-declaration

pwnrop:
	gcc ./src/main.c -m32 -o aaugrader_rop -Wimplicit-function-declaration

clean:
	rm -rf ./aaugrader ./aaugrader_rop

