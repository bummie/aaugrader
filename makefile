all: pwn pwnrop

pwn:
	gcc ./src/main.c -m32 -o aaugrader -no-pie -fno-stack-protector -z execstack -Wimplicit-function-declaration

pwnrop:
	gcc ./src/main.c -m32 -o aaugrader_rop -no-pie -fno-stack-protector -Wimplicit-function-declaration

clean:
	rm -rf ./aaugrader ./aaugrader_rop

