import sys
import time

def readMatrix(infile):
    matrix = []
    for line in infile.readlines():
        if len(line) == 0:
            continue
        line.replace('\n', '')
        val_str = line.split(',')
        matrix.append([int(i) for i in val_str])
    
    print(len(matrix))
    print(len(matrix[-1]))
    
    return matrix

def convertMatrixToBytes(matrix):
    matrix_str = ''
    
    for i in range(len(matrix)):
        row = matrix[i]
        row_vals = [str(val) for val in row]
        line = ','.join(row_vals)
        
        matrix_str += line + '\n'
    
    byte_str = matrix_str.encode('ascii')
    
    #print(len(byte_str))
    return byte_str
    #return matrix_str
    
def convertBytesToMatrix(byte_str):
    matrix_str = byte_str.decode()
    rows = matrix_str.split('\n')
    matrix = []
    
    for row in rows:
        if len(row) == 0:
            continue
        val_str = row.split(',')
        matrix.append([int(i) for i in val_str])
        
    print(len(matrix))
    print(len(matrix[-1]))
    
    return matrix

def simpleMultiplication(matrix1, matrix2):
    start_time = time.time()
    output_matrix = []
    
    for i in range(len(matrix1)):
        row = matrix1[i]
        output_row = []
        
        for j in range(len(matrix2[0])):
            column = [matrix2[k][j] for k in range(len(matrix2))]
            
            #print(row)
            #print(column)
            #print()
            sum = 0
            for l in range(len(row)):
                sum += row[l] * column[l]
            
            output_row.append(sum)
        output_matrix.append(output_row)
    
    end_time = time.time()
    diff = end_time - start_time
    print('Running time: ' + str(diff))
    #print(output_matrix)
    return output_matrix
            
if __name__ == '__main__':

    in_file_1 = ''
    in_file_2 = ''
    out_file = ''

    if len(sys.argv) == 4:
        try:
            in_file_1 = open(sys.argv[1], 'r')
            in_file_2 = open(sys.argv[2], 'r')
            out_file = open(sys.argv[3], 'w')
        except:
            print('Cannot open files.')
            sys.exit(0)
    else:
        print('Wrong number of arguments.')
        sys.exit(0)
    
    matrix1 = readMatrix(in_file_1)
    matrix2 = readMatrix(in_file_2)
    
    if len(matrix1[0]) != len(matrix2):
        print('Matrix size error')
        sys.exit(0)
    
    simpleMultiplication(matrix1, matrix2)
    
    in_file_1.close()
    in_file_2.close()
    out_file.close()