

Number Bases
-------------

12 apples
0xC apples
0b1100 apples

Binary    Base 2  0-1
Octal     Base 8  0-7
Decimal   Base 10 0-9
Hex       Base 16 0-9 a-f
          Base 64 0-9 a-f A-F +/

assumptions are base 10
a = 123 base 10
0b indicates binary
0x indicates hexidecimal

# Base 10
0
1
2
3
4
5
6
7
8
9

1234

one 1000
two 100
three 10
1 4

1 * 1000 +
2 * 100 +
3 * 10 +
4 * 1

# Binary (base 2)

+-----8's place (0b1000's place)
|+----4's place (0b100's place)
||+---2's place (0b10's place)
|||+--1's place (0b1's place)
||||
   0
   1
  10
  11
 100
 101
 110
 111
1000

Binary to Hex
--------------

4 binary digits == 1 hex digit
  ^^         ^
Byte is 8 bits

11010011

1101 0011
  d    3

0b 11010011 == 0xd3

0xff

 f      f
1111   1111

0b11111111 == 255 == 0xff

Bitwise Operations
-------------------

Boolean:
  and or True False
  &&  ||  ( Javascript )

  A    B     A BITWISE-AND B
-----------------------------
  0    0           0
  0    1           0
  1    0           0
  1    1           1

Bitwise Operators:
and: &
or: |
not: ~
xor: ^
shift right: >>
shift left:  <<



  10100100
& 10110111
----------
  10100100


  10100100
& 11111111   "AND mask"
----------
  10100100

can use the "AND mask" to extract individual bits from a number

LDI 1000010
LDI R2,37

pc += 3
       vv
ir = 0b10000010 # LDI

  10000010
& 11000000
-----------
  10000000
  01000000
  00100000
  ..
  00000010

  inst_len = ((ir & 0b1100000) >> 6)+ 1 #3
  pc += inst_len


The elements of computing systems

AND: clear bits to 0, mask out bits
OR: set bits to 1
SHIFT: with AND to extract sets of bits

Stack Frames
-------------
#Stack grows downward
#
#701:
#700


def mult2(x, y):
  z = x * y
  return z

def main():
  a = 2
  
  b = mult2(a, 7)
  
  # return pint 2
  
  print(b) # 14
  
  return

main() 

# return point 1
print("All Done)