// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// i=0
@i
M=0

// n=R1
@R1
D=M
@n
M=D

// sum=0
@sum
M=0

// while i < n
(LOOP)
  // D=i
  // M=n
  @i
  D=M
  @n
  // if n - i < 0
  // goto STOP
  D=M-D
  @STOP
  D;JLE
    // else

    //  sum += R0
    //  i+=1
    @R0
    D=M
    @sum
    M=D+M
    @i
    M=M+1
  

    @LOOP
    0;JMP

// end
(STOP)

// R2 = sum
@sum
D=M
@R2
M=D

// EOF
(END)
  @END
  0;JMP
