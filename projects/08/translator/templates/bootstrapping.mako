// SP = 256
@256
D=A
@SP
M=D

// call Sys.init
${call_asm}

// infinite loop
(INFINITE_LOOP)
@INFINITE_LOOP
0;JMP
