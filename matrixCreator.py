import sys
import random

if __name__ == '__main__':

    n = 0
    out_file = ''

    if len(sys.argv) == 3:
        n = int(sys.argv[1])
        try:
            out_file = open(sys.argv[2], 'w')
        except:
            print('Cannot open output file.')
            sys.exit(0)
    else:
        print('Wrong number of arguments.')
        sys.exit(0)
    print('n = ' + str(n))
    
    for i in range(n):
        for i in range(n):
            #num = random.uniform(0, 1)
            num = random.randrange(100)
            out_file.write(str(num))
            if i + 1 < n:
                out_file.write(',')
    
        out_file.write("\n")

    out_file.close()
