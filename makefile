all: pwn pwnrop

pwn:
	gcc ./src/main.c -m32 -o aaugrader -fno-stack-protector -z execstack

pwnrop:
	gcc ./src/main.c -m32 -o aaugrader_rop -fno-stack-protector

clean:
	rm -rf ./aaugrader ./aaugrader_rop

