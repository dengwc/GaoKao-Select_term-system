import sys, os

input_file = "/users2/yizhang/solveSystem/selectTerm/tmp/input.xml"
output_file = "/users2/yizhang/solveSystem/selectTerm/tmp/output.xml"
python_file = "/users2/yizhang/solveSystem/selectTerm/arg_selectTermSystem.py"

fout = file(input_file, "w")
while True:
    line = sys.stdin.readline()
    if len(line) == 0:
        break
    fout.write(line)

fout.close()
#os.system("whoami")
os.system("cd /users2/yizhang/solveSystem/selectTerm/ && python " + python_file + " " + input_file + " " + output_file + " > /dev/null")

#print os.system("python /users1/jhliu/Working/Generation/kernel/main2.py")

fin = file(output_file)


while True:
    line = fin.readline()
    if len(line) == 0:
        break
    print line,

sys.stdout.flush()