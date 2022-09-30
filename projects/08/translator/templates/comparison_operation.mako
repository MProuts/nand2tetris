## sp--
@SP
M=M-1
## D = *sp
A=M
D=M
## sp--
@SP
M=M-1
## setup condition
A=M
D=M-D
@TRUE${line_number}
D;${operator}
## i D != *sp
@SP
A=M
M=0
@END${line_number}
0;JMP
## i D == *sp)
(TRUE${line_number})
@SP
A=M
M=-1
@END${line_number}
0;JMP
## *sp++
(END${line_number})
@SP
M=M+1
