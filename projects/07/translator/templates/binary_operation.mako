## sp--
@SP
M=M-1
## D = *sp
A=M
D=M
## sp--
@SP
M=M-1
## *sp = *sp <op> D
A=M
M=M${operator}D
## sp++
@SP
M=M+1
