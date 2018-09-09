import sys

args = sys.argv
if(len(args)==1):
    pass
elif(1<len(args)<=4):
    for i in range(1,len(args)):
        sys.stdout.write(args[i] + '\n')
else:
    for i in range(1, 5):
        sys.stdout.write(args[i] + '\n')
    for i in range(5, len(args)):
        sys.stderr.write(args[i] + '\n')