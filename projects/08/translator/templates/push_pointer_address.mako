## D = (**pointer_addr)[i]
@${index}
D=A
@${pointer_addr}
A=M+D
D=M
## *sp = D
@SP
A=M
M=D
## sp++
@SP
M=M+1
