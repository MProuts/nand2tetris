## sp--
@SP
M=M-1
## R13 = *sp
@SP
A=M
D=M
@R13
M=D
## @R14 = *pointer_addr + i
@${index}
D=A
@${pointer_addr}
D=M+D
@R14
M=D
## (**pointer_address)[i] = *sp
@R13
D=M
@R14
A=M
M=D
