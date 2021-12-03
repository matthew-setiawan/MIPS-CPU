#
# @MIPS CPU TESTBENCH
# @brief:  TESTBENCH FOR MIPS CPU
# @version 0.1
# @date 2021-11-22
#
# @copyright Copyright (c) 2021
#
#
#!/bin/bash
set -eou pipefail
#$1 is absolute or relative

#echo $1
#echo $2 which is the instruction to be tested

#$1 is the location of a cpu.v
#we must recompile for every instruction (iterate through)
#we must rename the RAM output txt parameter for each instruction.

#list of instructions?
#problem is the compilation - $1 is the directory i.e. rtl, not the .v file


if [ $# -eq 1 ]
then
    testcases=test/testcases/*.txt
elif [ $# -eq 2 ]
then
    testcases=test/testcases/${2^^}.txt #IF YOU HAVE MULTIPLE TEST CASES, YOU MAY NEED TO ADD AN ASTERISK, LIKE _*
else
    echo too many/few arguments
    exit 1
fi



#echo $testcases

for test in $testcases #directory containing all the RAM outputs so we can compare against. iterate since it could be one, or all
    do
    echo $test
    test=$(basename ${test} .txt)


    iverilog -Wall -g 2012 -s tb_cpu -o tb_cpu \
    -P tb.RAM_FILE=\"${test}.txt\" \
    -P tb.OUT_FILE=\"${test}expected.txt\" \
    rtl/${ye}/tb_cpu.v ${1}/*.v  #> /dev/null 2>&1 #change mips_avlong to *.v

    #./tb #this should output with display? Ok - i really don't know how it's handled. I'll assume it can fail on the execution level
    #except it can't it really can't. So all the pass fail is inside the testbench I think

    #echo test
    done


#./cleardecals.sh