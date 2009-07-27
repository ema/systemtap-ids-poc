all: build

build: 
	#stap -DSTP_NO_OVERLOAD -vvv -p 4 -I tapsets/ syscall-database.stp -m builddb.ko
	stap -vvv -p 4 -I tapsets/ syscall-database.stp -m syscalldatabase.ko
	stap -vvv -p 4 all-sequences.stp -m allsequences.ko

clean:
	-rm *.ko
