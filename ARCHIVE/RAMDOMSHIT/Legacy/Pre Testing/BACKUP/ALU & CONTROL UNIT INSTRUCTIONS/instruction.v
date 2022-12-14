/**
 * @MIPS CPU INSTRUCTIONS TEST BENCH
 * @brief:      Implementation of all of the instructions.
 * @version 0.1
 * @date 2021-11-22
 *
 * @copyright Copyright (c) 2021
 *
 */

module mips_cpu_bus(
    /* Standard signals */
    input logic clk,
    input logic reset,
    output logic active,
    output logic[31:0] register_v0,

    /* Avalon memory mapped bus controller (master) */
    output logic[31:0] address,
    output logic write,
    output logic read,
    input logic waitrequest,
    output logic[31:0] writedata,
    output logic[3:0] byteenable,
    input logic[31:0] readdata
);

//  Wire declarations
    logic[31:0] PC, PC_next, PC_jump;
    logic[1:0] state;


/*
    I have no idea what the heck im doing here,
    I'm just addding the nessesary wires we probably will need. 
    Maybe we should make a blueprint!
*/
    logic[16:0] instruction;
    logic[3:0] logic_opcode;
    logic[11:0] instruction_constants;

/*
    Register formats (ref: https://www.dcc.fc.up.pt/~ricroc/aulas/1920/ac/apontamentos/P04_encoding_mips_instructions.pdf)
    Title       :       Reg #       :       Usage
    $zero       :       0           :       Constantly of value 0
    $v0-$v1     :       2, 3        :       Values for results and expression evaluation
    $a0-$v3     :       4, 7        :       Argus
    $t0-$t7     :       8, 15       :       Temps
    $t8-$t9     :       24, 25      :       More temps
    $s0-$s7     :       16, 23      :       Saved
    $gp         :       28          :       Global pointers
    $sp         :       29          :       Stack Pointer
    $fp         :       30          :       Frame pointer
    $ra         :       31          :       Return address
*/

/*
    Instructions (ref:https://opencores.org/projects/plasma/opcodes)

    Opcodes:
    R types have an opcode of 0d0, therefore are differentiated through their function codes
    J types have uniques opcodes
    I types have uniques opcodes

    I type formatting:  For Transfer, branch and immedaiate instructions
*/
typedef enum logic[5:0]
{
    OPCODE_R = 6'd0,
    OPCODE_J = 6'd2,
    OPCODE_JAL = 6'd3,

    OPCODE_BEQ = 6'd4,
    OPCODE_BGEZ = 6'd1,  //FIXME:    Need to differentiate by RT
    OPCODE_BGEZAL = 6'd1,//FIXME:    Need to differentiate by RT
    OPCODE_BGTZ = 6'd7,
    OPCODE_BLEZ = 6'd6,
    OPCODE_BLTZ = 6'd1,  //FIXME:    Need to differentiate by RT
    OPCODE_BLTZAL = 6'd1,//FIXME:    Need to differentiate by RT
    OPCODE_BNE = 6'd5,

    OPCODE_ADDIU = 6'd9,
    OPCODE_SLTIU = 6'd11,
    OPCODE_LUI = 6'd15,
    OPCODE_ANDI = 6'd12,
    OPCODE_ORI = 6'd13,
    OPCODE_SLTI = 6'd10,
    OPCODE_XORI = 6'd14

    OPCODE_LB = 6'd32,
    OPCODE_LBU = 6'd36,
    OPCODE_LH = 6'd33,
    OPCODE_LHU = 6'd37,
    OPCODE_LW = 6'd35,
    OPCODE_SB = 6'd40,
    OPCODE_SH = 6'd41,
    OPCODE_SW = 6'd43,
} opcode_t;

/*
    R types are differentiated through their function code
*/
typedef enum logics[5:0]
{
    FUNCTION_CODE_ADDU = 6'd33,
    FUNCTION_CODE_SUBU = 6'd35,
    FUNCTION_CODE_AND = 6'd36,
    FUNCTION_CODE_OR = 6'd37,
    FUNCTION_CODE_SLT = 6'd42,
    FUNCTION_CODE_SLTU = 6'd43,
    FUNCTION_CODE_XOR = 6'd38,
    FUNCTION_CODE_SLL = 6'd0,
    FUNCTION_CODE_SLLV = 6'd4,
    FUNCTION_CODE_SRA = 6'd3,
    FUNCTION_CODE_SRAV = 6'd7,
    FUNCTION_CODE_SRL = 6'd2,
    FUNCTION_CODE_SRLV = 6'd6,
    FUNCTION_CODE_DIV = 6'd26,
    FUNCTION_CODE_DIVU = 6'd27,
    FUNCTION_CODE_MULT = 6'd24,
    FUNCTION_CODE_MULTU = 6'd25,
    FUNCTION_CODE_MTHI = 6'd17,
    FUNCTION_CODE_MTLO = 6'd18,
    //FUNCTION_CODE_LWR = 6'd,    //FIXME:  Can't find any of the function codes for the two
    //FUNCTION_CODE_LWL = 6'd,    //FIXME:  Can't find any of the function codes for the two
    FUNCTION_CODE_JALR = 6'd,
    FUNCTION_CODE_JR = 6'd,
} fcode_t;

    //  State Registers
    logic[31:0] PC, PC_next, PC_jump;
    logic[1:0] state;

    //  Registers
        //  General Registers
        logic[31:0][31:0] registers;
        //  Special Registers
        logic[31:0] HI;
        logic[31:0] LO;

/*
        Wires used in ALU
        |Field name: 6 bits |5 bits |5 bits |5 bits  |5 bits     |6 bits     |
        |R format:   op     |rs     |rt     |rd      |shmat      |funct      |
        |I format:   op     |rs     |rt     |address/immediate               |
        |J format:   op     |target address                                  |
*/
        opcode_t opcode;
        logic[4:0] rs;
        logic[4:0] rt;
        logic[4:0] rd;
        logic[4:0] shmat;
        fcode_t funct;
        logic[15:0] address_immediate;
        logic[25:0] targetAddress;


        //  Temporary wiring
            //  Multiplication
                logic[63:0] multWire;
                logic[63:0] multWireU;
            //  Branching
                logic[24:0] threeWords;

//  Instructions:   (ref: https://uweb.engr.arizona.edu/~ece369/Resources/spim/MIPSReference.pdf)
    case(opcode)
        //  TODO:   Maybe assert if rd = 0
        //  R type instructions
        (OPCODE_R): begin
            //  We have to determine what the R type instruction is by virtue of its function code
            case(funct)
            //  Basic arithematic
                    (FUNCTION_CODE_ADDU): begin
                        /*
                            We can conduct register addition with anything except for 
                            destination being $zero, so use a multiplexer to make this
                        */
                        register[rd] <= (rd != 0) ? ($unsigned(register[rs]) + $unsigned(register[rt])) : (0);
                        assert(rd != 0) else $fatal(2, "Error, trying to write to zero register");
                    end

                    (FUNCTION_CODE_SUBU): begin
                        /*
                            Like addition, use a multiplexer to confirm rd is not $zero
                        */
                        register[rd] <= (rd != 0) ? ($unsigned(register[rs]) - $unsigned(register[rt])) : (0);
                        assert(rd != 0) else $fatal(2, "Error, trying to write to zero register");
                    end

                    (FUNCTION_CODE_DIV): begin
                        HI <= register[rs] % register[rt];
                        LO <= register[rs] / register[rt];
                    end

                    (FUNCTION_CODE_DIVU): begin
                        HI <= $unsigned(register[rs]) % $unsigned(register[rt];)
                        LO <= $unsigned(register[rs]) / $unsigned(register[rt];)
                    end


                    (FUNCTION_CODE_MULT): begin
                        multWire = register[rs] * register[rt];
                        HI <= [63:32] multWire;
                        LO <=  [31:0] multWire;
                    end

                    (FUNCTION_CODE_MULTU): begin
                        multWire = $unsigned(register[rs]) * $unsigned(register[rt]);
                        HI <= [63:32] multWire;
                        LO <=  [31:0] multWire;
                    end

            //  Bitwise operation
                    (FUNCTION_CODE_AND): begin
                        register[rd] <= (rd != 0) ? (register[rs] & register[rt]) : (0);
                    end

                    (FUNCTION_CODE_OR): begin
                        register[rd] <= (rd != 0) ? (register[rs] | register[rt]) : (0);
                    end

                    (FUNCTION_CODE_XOR): begin
                        register[rd] <= (rd != 0) ? (register[rs] ^ register[rt]) : (0);
                    end

            //  Set operations      FIXME:  SRA's not finished
                (FUNCTION_CODE_SLT): begin
                    register[rd] = (rd != 0) ? ((register[rs] < register[rt]) ? ({31'b0, 1}) : ({32'b0})) : (0);
                end

                (FUNCTION_CODE_SLTU): begin
                    register[rd] = (rd != 0) ? (($unsigned(register[rs]) < $unsigned(register[rt])) ? ({31'b0, 1}) : ({32'b0})) : (0);
                end

                //  Logical
                    (FUNCTION_CODE_SLL): begin
                            register[rd] <= (rd != 0) ? (register[rs] << shmat) : (0);
                    end

                    (FUNCTION_CODE_SRL): begin
                            register[rd] <= (rd != 0) ? (register[rs] >>> shmat) : (0);
                    end

                    (FUNCTION_CODE_SLLV): begin
                            register[rd] <= (rd != 0) ? (register[rt] << register[rs]) : (0);
                    end

                    (FUNCTION_CODE_SRLV): begin
                            register[rd] <= (rd != 0) ? (register[rs] >>> register[shmat]) : (0);
                    end
                //  Arithmetic
                    (FUNCTION_CODE_SRA): begin  //  FIXME:  What deos this to
                            register[rd] <= (rd != 0) ? (register[rs] >>> shmat) : (0);
                    end

                    (FUNCTION_CODE_SRAV): begin  //  FIXME:  What deos this to
                            register[rd] <= (rd != 0) ? (register[rt] >>> register[rs]) : (0);
                    end



            //  Move instructions
                (FUNCTION_CODE_MTHI): begin
                    register[rd] = (rd != 0) ? (HI) : (0);
                end

                (FUNCTION_CODE_MTLO): begin
                    register[rd] = (rd != 0) ? (LO) : (0);
                end

            endcase

        //  J type instructions
            (OPCODE_J) : begin
                PC_next <= readata;
            end

            (OPCODE_JAL) : begin
                register[31] <= PC + 5'd4;
                PC_next <= readata;
            end

        //  I type instructions
            (OPCODE_ADDIU) : begin
                register[rd] <= (rd != 0) ? ($unsigned(register[rs]) + $unsigned(register[address_immediate])) : (0);
            end

            (OPCODE_ANDI) : begin
                register[rd] <= (rd != 0) ? ($unsigned(register[rs]) & $unsigned(register[address_immediate])) : (0);
            end

            (OPCODE_ORI) : begin
                register[rd] <= (rd != 0) ? ($unsigned(register[rs]) | $unsigned(register[address_immediate])) : (0);
            end

            (OPCODE_XORI) : begin
                register[rd] <= (rd != 0) ? ($unsigned(register[rs]) ^ $unsigned(register[address_immediate])) : (0);
            end

            (OPCODE_LUI) : begin
                register[rd] <= (rd != 0) ? (address_immediate << 16) : (0);
            end

            (OPCODE_SLTI) : begin
                    register[rd] = (rd != 0) ? ((register[rs] < register[address_immediate]) ? (1) : (0)) : (0);
            end

            (OPCODE_SLTIU) : begin
                    register[rd] = (rd != 0) ? (($unsigned(register[rs]) < $unsigned(register[address_immediate])) ? (1) : (0)) : (0);
            end

        //  Branch
            (OPCODE_BEQ) : begin
                //  add 4 since TODO:   Why?
                PC_next <= (register[rs] == register[rt]) ? (address_immediate + 5'd4) : (pc);
    
            end
            
        end
        
            
        
            
            

            


                (OPCODE_BGEZ) : begin
                    // if (rs-rt) >= 0 then pc_next==immediate
                    PC_next <= ((register[rs] >= 0) ? (PC + (address_immediate << 2)) : (PC + 5'd4);
                end

                (OPCODE_BGEZAL) : begin
                    PC_next <= ((register[rs] >= 0) ? (PC + (address_immediate << 2)) : (PC + 5'd4);
                    register[31] = PC;
                end

                (OPCODE_BGTZ) : begin
                    PC_next <= ((register[rs] > 0) ? (PC + (address_immediate << 2)) : (PC + 5'd4);
                end

                (OPCODE_BNE) : begin
                    pc <= (register[rs] != register[rt]) ? (PC + (address_immediate << 2)) : (PC + 5'd4);
                end

                (OPCODE_BLEZ) : begin
                    pc <= (register[rs] <= 0) ? (PC + (address_immediate << 2)) : (PC + 5'd4);
                    //if (rs-rt)==0 or MSB(rs-rt)==1 then pc==immediate
                end

                (OPCODE_BLTZAL) : begin
                    PC_next <= ((register[rs] < 0) ? (PC + (address_immediate << 2)) : (PC + 5'd4);
                    register[31] = PC;
                end

                (OPCODE_BLTZ) : begin
                    PC_next <= ((register[rs] < 0) ? (PC + (address_immediate << 2)) : (PC + 5'd4);
                end

            //  Load / Store https://inst.eecs.berkeley.edu/~cs61c/resources/MIPS_help.html
                (OPCODE_LB) : begin
                    //  Load in the nth byte from the RAMs input to the CPU
                    //  Determine if latter 24 bits are 0 or 1
                    case((register[rs] + address_immediate) % 4) begin
                        (0):
                            register[rt] = {((readata[7]) ? (24'hFFF): (24'h0)), readdata[7:0]};
                        (1):
                            register[rt] = {((readata[15]) ? (24'hFFF): (24'h0)), readdata[15:8]};
                        (2):
                            register[rt] = {((readata[23]) ? (24'hFFF): (24'h0)), readdata[23:16]};
                        (3):
                            register[rt] = {((readata[31]) ? (24'hFFF): (24'h0)), readdata[31:24]};
                    endcase
                end

                (OPCODE_LBU) : begin
                    //  Load in the nth byte from the RAMs input to the CPU (unsigned)
                    case((register[rs] + address_immediate) % 4) begin
                        (0):
                            register[rt] = {24'b0, readdata[7:0]};
                        (1):
                            register[rt] = {24'b0, readdata[15:8]};
                        (2):
                            register[rt] = {24'b0, readdata[23:16]};
                        (3):
                            register[rt] = {24'b0, readdata[31:24]};
                    endcase

                end

                (OPCODE_LH) : begin
                    case((register[rs] + address_immediate) % 2) begin
                        (0):
                            register[rt] = {((readata[15]) ? (16'hFFF): (216'h0)), readdata[15:0]};
                        (1):
                            register[rt] = {((readata[31]) ? (16'hFFF): (16'h0)), readdata[31:16]};
                    endcase
                end

                (OPCODE_LHU) : begin
                    case((register[rs] + address_immediate) % 4) begin
                        (0):
                            register[rt] = {16'b0, readdata[15:0]};
                        (1):
                            register[rt] = {16'b0, readdata[31:16]};
                    endcase
                end

                (OPCODE_LW) : begin
                        register[rt] = readdata;
                end

                (OPCODE_SB) : begin
                    //  Write must be high
                    //  setting values ton writedata
                    //  byte enable will be us choosing byte at address
                    //  Address is determined @ exec1
                    write = 1;  //  Enable write so that memory can be written upon
                    address = (reigser[rs] + address_immediate);
                    case(address % 4) begin
                        (0) : begin
                            byteenable = (4'd1);    //  Byte enable the first byte
                        end
                        (1) : begin
                            byteenable = (4'd2);    //  Byte enable the second byte
                        end
                        (2) : begin
                            byteenable = (4'd4);    //  Byte enable the third byte
                        end
                        (3) : begin
                            byteenable = (4'd8);    //  Byte enable the fourth byte
                        end
                    endcase
                    writedata = register[rt];   //  Write
                end

                (OPCODE_SH) : begin
                    write = 1;  //  Enable write so that memory can be written upon
                    address = (reigser[rs] + address_immediate);
                    case(address % 2) begin
                        (0) : begin
                            byteenable = (4'd3);    //  Byte enable the first two bytes
                        end
                        (1) : begin
                            byteenable = (4'd12);   //  Byte anable the latter two bytes
                        end
                    endcase
                    writedata = register[rt];   //  Write
                end

                (OPCODE_SW) : begin
                    write = 1;                  //  Enable write so that memory can be written upon
                    address = (reigser[rs] + address_immediate);
                    byteenable 4'd15;           //  Byte enable all bytes
                    writedata = register[rt];   //  Write
                end
    endcase
