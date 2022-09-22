## D = *addr
@${addr}
D=M
## *sp = D
@SP
A=M
M=D
## sp++
@SP
M=M+1
