memo = {}

def tobin(integer,bits):
      return bin(int(integer))[2:].zfill(bits)

def tohex(B):
      intval = int(B,2)
      hexval = hex(intval)[2:].zfill(8)
      return hexval[0:2], hexval[2:4], hexval[4:6], hexval[6:8]

def translator(command):
      op = command.split(" ")[0]
      oprd = command.split(" ")

      for i in range(len(oprd)):
            if oprd[i][len(oprd[i])-1]==",":
                  oprd[i]=oprd[i][:-1]

      B = "00000000000000000000000000000000"
      H1 = "0"
      H2 = "0"
      H3 = "0"
      H4 = "0"

      if op=="ADDIU":
            B = "001001" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],16)
      elif op=="ADDU":
            B = "000000" + tobin(oprd[2],5) + tobin(oprd[3],5) + tobin(oprd[1],5) + "00000100001"
      elif op=="AND":
            B = "000000" + tobin(oprd[2],5) + tobin(oprd[3],5) + tobin(oprd[1],5) + "00000100100"
      elif op=="ANDI":
            B = "001100" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],16)
      elif op=="BEQ":
            B = "000100" + tobin(oprd[1],5) + tobin(oprd[2],5) + tobin(oprd[3],16)
      elif op=="BGEZ":
            B = "000001" + tobin(oprd[1],5) + "00001" + tobin(oprd[2],16)
      elif op=="BGEZAL":
            B = "000001" + tobin(oprd[1],5) + "10001" + tobin(oprd[2],16)
      elif op=="BGTZ":
            B = "000111" + tobin(oprd[1],5) + "00000" + tobin(oprd[2],16)
      elif op=="BLEZ":
            B = "000110" + tobin(oprd[1],5) + "00000" + tobin(oprd[2],16)
      elif op=="BLTZ":
            B = "000001" + tobin(oprd[1],5) + "00000" + tobin(oprd[2],16)
      elif op=="BLTZAL":
            B = "000001" + tobin(oprd[1],5) + "10000" + tobin(oprd[2],16)
      elif op=="BNE":
            B = "000101" + tobin(oprd[1],5) + tobin(oprd[2],5) + tobin(oprd[3],16)
      elif op=="DIV":
            B = "000000" + tobin(oprd[1],5) + tobin(oprd[2],5) + "0000000000011010"
      elif op=="DIVU":
            B = "000000" + tobin(oprd[1],5) + tobin(oprd[2],5) + "0000000000011011"
      elif op=="J":
            B = "000010" + tobin(oprd[1],26)
      elif op=="JALR":
            B = "000000" + tobin(oprd[2],5) + "00000" + tobin(oprd[1],5) + "00000001001"
      elif op=="JAL":
            B = "000011" + tobin(oprd[1],26)
      elif op=="JR":
            B = "000000" + tobin(oprd[1],5) + "000000000000000001000"
      elif op=="LB":
            B = "100000" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="LBU":
            B = "100100" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="LH":
            B = "100001" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="LHU":
            B = "100101" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="LUI":
            B = "00111100000" + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="LW":
            B = "100011" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="LWL":
            B = "100010" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="LWR":
            B = "100110" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="MTHI":
            B = "000000" + tobin(oprd[1],5) + "000000000000000010001"
      elif op=="MTLO":
            B = "000000" + tobin(oprd[1],5) + "000000000000000010011"
      elif op=="MFHI":
            B = "0000000000000000" + tobin(oprd[1],5) + "00000010000"
      elif op=="MFLO":
            B = "0000000000000000" + tobin(oprd[1],5) + "00000010010"
      elif op=="MULT":
            B = "000000" + tobin(oprd[1],5) + tobin(oprd[2],5) + "0000000000011000"
      elif op=="MULTU":
            B = "000000" + tobin(oprd[1],5) + tobin(oprd[2],5) + "0000000000011001"
      elif op=="OR":
            B = "000000" + tobin(oprd[2],5) + tobin(oprd[3],5) + tobin(oprd[1],5) + "00000100101"
      elif op=="ORI":
            B = "001101" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],16)
      elif op=="SB":
            B = "101000" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="SH":
            B = "101001" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="SLL":
            B = "00000000000" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],5) + "000000"
      elif op=="SLLV":
            B = "000000" + tobin(oprd[3],5) + tobin(oprd[2],5) + tobin(oprd[1],5) + "00000000100"
      elif op=="SLT":
            B = "000000" + tobin(oprd[2],5) + tobin(oprd[3],5) + tobin(oprd[1],5) + "00000101010"
      elif op=="SLTI":
            B = "001010" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],16)
      elif op=="SLTIU":
            B = "001011" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],16)
      elif op=="SLTU":
            B = "000000" + tobin(oprd[2],5) + tobin(oprd[3],5) + tobin(oprd[1],5) + "00000101011"
      elif op=="SRA":
            B = "00000000000" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],5) + "000011"
      elif op=="SRAV":
            B = "000000" + tobin(oprd[3],5) + tobin(oprd[2],5) + tobin(oprd[1],5) + "00000000111"
      elif op=="SRL":
            B = "00000000000" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],5) + "000010" 
      elif op=="SRLV":
            B = "000000" + tobin(oprd[3],5) + tobin(oprd[2],5) + tobin(oprd[1],5) + "00000000110" 
      elif op=="SUBU":
            B = "000000" + tobin(oprd[2],5) + tobin(oprd[3],5) + tobin(oprd[1],5) + "00000100011" 
      elif op=="SW":
            B = "101011" + tobin(oprd[3],5) + tobin(oprd[1],5) + tobin(oprd[2],16)
      elif op=="XOR":
            B = "000000" + tobin(oprd[2],5) + tobin(oprd[3],5) + tobin(oprd[1],5) + "00000100110"
      elif op=="XORI":
            B = "001110" + tobin(oprd[2],5) + tobin(oprd[1],5) + tobin(oprd[3],16)


      H1, H2, H3, H4 = tohex(B)

      memo[H1+H2+H3+H4] = command

      return H1, H2, H3, H4

def create(RAM,TESTRAM,inst):
      FILE1 = ""
      FILE2 = ""
      for i in range(len(RAM)):
            FILE1 = FILE1 + RAM[i].upper() + "\n"
            FILE2 = FILE2 + TESTRAM[i].upper() + "\n"

      f = open(inst+".txt","a+")
      f.write(FILE1)
      f.close()
      f = open(inst+"expected.txt","a+")
      f.write(FILE2)
      f.close()

def mips_cpu_bus(TESTRAM,startline):
      RAM = TESTRAM
      register = ["00000000"]*32
      HI = "00000000"
      LO = "00000000"
      i=startline
      while(i!=len(RAM)-4):
            print(RAM[i+3] + RAM[i+2] + RAM[i+1] + RAM[i])
            if RAM[i+3] + RAM[i+2] + RAM[i+1] + RAM[i] == "00000000":
                  i = i + 4
            else:
                  command = memo[RAM[i+3] + RAM[i+2] + RAM[i+1] + RAM[i]]
                  op = command.split(" ")[0]
                  oprd = command.split(" ")
                  for j in range(len(oprd)):
                        if oprd[j][len(oprd[j])-1]==",":
                              oprd[j]=oprd[j][:-1]
                  if op == "SW":
                        n = int(oprd[2])+int(oprd[3])
                        RAM[n], RAM[n+1], RAM[n+2], RAM[n+3] = register[int(oprd[1])][6:8], register[int(oprd[1])][4:6], register[int(oprd[1])][2:4], register[int(oprd[1])][0:2]
                  elif op == "LW":
                        n = int(oprd[2])+int(oprd[3])
                        register[int(oprd[1])] = RAM[n+3] + RAM[n+2] + RAM[n+1] + RAM[n]
                  elif op == "ADDIU":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16) + int(oprd[3]))[2:].zfill(8)
                  elif op == "ADDU":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16) + int(register[int(oprd[3])],16))[2:].zfill(8)
                  elif op == "AND":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16)&int(register[int(oprd[3])],16))[2:].zfill(8)
                  elif op == "ANDI":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16)&int(oprd[3]))[2:].zfill(8)
                  elif op == "BEQ":
                        if register[op[1]]==register[op[2]]:
                              i = i + int(oprd[3]*4)
                  elif op == "BGEZ":
                        if int(register[oprd[1]])>=0:
                              i = i + int(oprd[2]*4)
                  elif op == "BGEZAL":
                        if int(register[oprd[1]])>=0:
                              i = i + int(oprd[2]*4)
                              register[31]=hex(i+4)[2:].zfill(8)
                  elif op == "BGTZ":
                        if int(register[oprd[1]])>=0:
                              i = i + int(oprd[2]*4)
                  elif op == "BLEZ":
                        if int(register[oprd[1]])<=0:
                              i = i + int(oprd[2]*4)
                  elif op == "BLTZ":
                        if int(register[oprd[1]])<0:
                              i = i + int(oprd[2]*4)
                  elif op == "BLTZAL":
                        if int(register[oprd[1]])<0:
                              i = i + int(oprd[2]*4)
                              register[31]=hex(i+4)[2:].zfill(8)
                  elif op == "BNE":
                        if register[op[1]]!=register[op[2]]:
                                    i = i + int(oprd[3]*4)
                  elif op == "DIV":
                        HI = hex(int(oprd[1])%int(oprd[2]))[2:].zfill(8)
                        LO = hex(int(int(oprd[1])/int(oprd[2])))[2:].zfill(8)
                  elif op == "DIVU":
                        HI = hex(int(oprd[1])%int(oprd[2]))[2:].zfill(8)
                        LO = hex(int(int(oprd[1])/int(oprd[2])))[2:].zfill(8)
                  elif op == "J":
                        i = int(oprd[1])*4 - 4
                  elif op == "JALR":
                        i = int(oprd[2])*4 - 4
                        register[int(oprd[1])]=hex(i+4)[2:0].zflip(8)
                  elif op == "JAL":
                        i = int(oprd[1])*4 - 4
                        register[31]=hex(i+4)[2:0].zflip(8)
                  elif op == "JR":
                        i = int(register[int(oprd[1])])
                  elif op == "LB":
                        pos=["00","00","00","00"]
                        pos[(int(oprd[2])+int(oprd[3]))%4]=RAM[int(oprd[2])+int(oprd[3])]
                        register[int(oprd[1])]=pos[0] + pos[1] + pos[2] + pos[3]
                  elif op == "LBU":
                        pos=["00","00","00","00"]
                        pos[(int(oprd[2])+int(oprd[3]))%4]=RAM[int(oprd[2])+int(oprd[3])]
                        register[int(oprd[1])]=pos[0] + pos[1] + pos[2] + pos[3]
                  elif op == "LH":
                        pos=["0000","0000"]
                        pos[(int(oprd[2])+int(oprd[3]))%4==0]=RAM[int(oprd[2])+int(oprd[3])]+RAM[int(oprd[2])+int(oprd[3])+1]
                        register[int(oprd[1])]=pos[0] + pos[1]
                  elif op == "LHU":
                        pos=["0000","0000"]
                        pos[(int(oprd[2])+int(oprd[3]))%4==0]=RAM[int(oprd[2])+int(oprd[3])]+RAM[int(oprd[2])+int(oprd[3])+1]
                        register[int(oprd[1])]=pos[0] + pos[1]
                  elif op == "LUI":
                        register[int(oprd[1])]=hex(int(oprd[2]))[2:].zfill(16) + "0000000000000000"
                  elif op == "LWL":
                        R1 = register[int(oprd[1])][0:2]
                        R2 = register[int(oprd[1])][2:4]
                        R3 = register[int(oprd[1])][4:6]
                        R4 = register[int(oprd[1])][6:8]
                        if (int(oprd[2])+int(oprd[3]))%4==3:
                              R1 = RAM[int(oprd[2])+int(oprd[3])]
                              R2 = RAM[int(oprd[2])+int(oprd[3])-1]
                              R3 = RAM[int(oprd[2])+int(oprd[3])-2]
                              R4 = RAM[int(oprd[2])+int(oprd[3])-3]
                        if (int(oprd[2])+int(oprd[3]))%4==2:
                              R1 = RAM[int(oprd[2])+int(oprd[3])]
                              R2 = RAM[int(oprd[2])+int(oprd[3])-1]
                              R3 = RAM[int(oprd[2])+int(oprd[3])-2]
                        if (int(oprd[2])+int(oprd[3]))%4==1:
                              R1 = RAM[int(oprd[2])+int(oprd[3])]
                              R2 = RAM[int(oprd[2])+int(oprd[3])-1]
                        if (int(oprd[2])+int(oprd[3]))%4==0:
                              R1 = RAM[int(oprd[2])+int(oprd[3])]
                  elif op == "LWR":
                        R1 = register[int(oprd[1])][0:2]
                        R2 = register[int(oprd[1])][2:4]
                        R3 = register[int(oprd[1])][4:6]
                        R4 = register[int(oprd[1])][6:8]
                        if (int(oprd[2])+int(oprd[3]))%4==0:
                              R1 = RAM[int(oprd[2])+int(oprd[3])+3]
                              R2 = RAM[int(oprd[2])+int(oprd[3])+2]
                              R3 = RAM[int(oprd[2])+int(oprd[3])+1]
                              R4 = RAM[int(oprd[2])+int(oprd[3])]
                        if (int(oprd[2])+int(oprd[3]))%4==1:
                              R2 = RAM[int(oprd[2])+int(oprd[3])+2]
                              R3 = RAM[int(oprd[2])+int(oprd[3])+1]
                              R4 = RAM[int(oprd[2])+int(oprd[3])]
                        if (int(oprd[2])+int(oprd[3]))%4==2:
                              R3 = RAM[int(oprd[2])+int(oprd[3])+1]
                              R4 = RAM[int(oprd[2])+int(oprd[3])]
                        if (int(oprd[2])+int(oprd[3]))%4==3:
                              R4 = RAM[int(oprd[2])+int(oprd[3])]
                  elif op == "MFHI":
                        register[int(oprd[1])]=HI
                  elif op == "MFLO":
                        register[int(oprd[1])]=LO
                  elif op == "MTHI":
                        HI=register[int(oprd[1])]
                  elif op == "MTLO":
                        LO=register[int(oprd[1])]
                  elif op == "MULT":
                        result = hex(int(register[int(oprd[1])],16)*int(register[int(oprd[2])],16))[2:].zfill(64)
                        HI = result[64:32]
                        LO = result[32:0]
                  elif op == "MULTU":
                        result = hex(int(register[int(oprd[1])],16)*int(register[int(oprd[2])],16))[2:].zfill(64)
                        HI = result[64:32]
                        LO = result[32:0]
                  elif op == "OR":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16)|int(register[int(oprd[3])],16))[2:].zfill(8)
                  elif op == "ORI":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16)|int(oprd[3]))[2:].zfill(8)
                  elif op == "SB":
                        RAM[int(oprd[2])+int(oprd[3])] = register[int(oprd[1])][2:0]
                  elif op == "SH":
                        RAM[int(oprd[2])+int(oprd[3])] = register[int(oprd[1])][2:0]
                        RAM[int(oprd[2])+int(oprd[3])+1] = register[int(oprd[1])][4:2]
                  elif op == "SLL":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16) << int(int(oprd[3]),16))[2:0].zfill(8)
                  elif op == "SLLV":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16) << int(register[int(oprd[3])],16))[2:0].zfill(8)
                  elif op == "SLT":
                        if int(register[oprd[2]]) < int(register[oprd[3]]):
                              register[oprd[1]]="00000001"
                        else:
                              register[oprd[1]]="00000000"
                  elif op == "SLTI":
                        if int(register[oprd[2]]) < int(oprd[3]):
                              register[oprd[1]]="00000001"
                        else:
                              register[oprd[1]]="00000000"
                  elif op == "SLTIU":
                        if int(register[oprd[2]]) < int(oprd[3]):
                              register[oprd[1]]="00000001"
                        else:
                              register[oprd[1]]="00000000"
                  elif op == "SLTU":
                        if int(register[oprd[2]]) < int(register[oprd[3]]):
                              register[oprd[1]]="00000001"
                        else:
                              register[oprd[1]]="00000000"
                  elif op == "SRA":
                        if register[int(oprd[2])][0]=="0":
                              register[int(oprd[1])] = hex(int(register[int(oprd[2])]) >> int(oprd[3]))[2:].zfill(8)
                        else:
                              sum = 0
                              for i in range(32,32-int(oprd[3])):
                                    sum = sum + 2**i
                              register[int(oprd[1])] = hex((int(register[int(oprd[2])]) >> int(oprd[3]))+sum)[2:].zfill(8)
                  elif op == "SRAV":
                        if register[int(oprd[2])][0]=="0":
                              register[int(oprd[1])] = hex(int(register[int(oprd[2])]) >> int(register[int(oprd[3])]))[2:].zfill(8)
                        else:
                              sum = 0
                              for i in range(32,32-int(oprd[3])):
                                    sum = sum + 2**i
                              register[int(oprd[1])] = hex((int(register[int(oprd[2])]) >> int(register[int(oprd[3])])+sum))[2:].zfill(8)
                  elif op == "SRL":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16) >> int(int(oprd[3]),16))[2:0].zfill(8)
                  elif op == "SRLV":
                        register[int(oprd[1])] = hex(int(int(register[int(oprd[2])],16) >> int(register[int(oprd[3])],16)))[2:0].zfill(8)
                  elif op == "SUBU":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16) - int(register[int(oprd[3])],16))[2:].zfill(8)
                  elif op == "XOR":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16)^int(register[int(oprd[3])],16))[2:].zfill(8)
                  elif op == "XORI":
                        register[int(oprd[1])] = hex(int(register[int(oprd[2])],16)^int(oprd[3]))[2:].zfill(8)
                  #1, 2, 
                  i = i + 4
            
      return RAM

#Start Initializing RAM below here

#Multiply by the size of RAM
RAM = ["00"]*200

#Initialize memory here
RAM[4], RAM[5], RAM[6], RAM[7] = "AA", "BB", "CC", "DD"

#Start writing instructions here
RAM[103], RAM[102], RAM[101], RAM[100] = translator("LW 1, 4, 0")
RAM[107], RAM[106], RAM[105], RAM[104] = translator("SW 1, 8, 0")

#Leave this
TESTRAM = RAM.copy()
TESTRAM = mips_cpu_bus(TESTRAM,100)#<- put where the instructions start to read here, now it is 100

create(RAM, TESTRAM, "LW")
create(RAM, TESTRAM, "SW")

for i in range(200):
      print(i, RAM[i], TESTRAM[i])

