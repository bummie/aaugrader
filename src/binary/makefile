all: pwn pwnrop

pwn:
	gcc ./main.c -m32 -o aaugrader -z execstack -Wimplicit-function-declaration

pwnrop:
	gcc ./main.c -m32 -o aaugrader_rop -Wimplicit-function-declaration

pwn_cfg:
	gcc ./main_cfg.c -m32 -o aaugrader_cfg -z execstack -Wimplicit-function-declaration

pwnrop_cfg:
	gcc ./main_cfg.c -m32 -o aaugrader_rop_cfg -Wimplicit-function-declaration

clean:
	rm -rf ./aaugrader ./aaugrader_rop

