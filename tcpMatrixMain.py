import socket
import thread
import math
import matrixOperation as mo
import time
import sys
    
def createWork(matrix, fold):
    work = []
    
    split = int(math.ceil(len(matrix) / fold))
    
    index = 0
    for i in range(fold):
        split_matrix = matrix[index : index + split]
        work.append(mo.convertMatrixToBytes(split_matrix))
        index += split
        
    return work

def workerNode(workersocket, addr, work_index, matrix1, matrix2, result):
    # initialization
    while True:
        msg = workersocket.recv(10)
        if msg == 'Accept':
            print(str(addr) + ':' + msg)
            break
    
    # send matrix1 to worker
    workersocket.send('Size1:' + str(len(matrix1)))
    
    while True:
        msg = workersocket.recv(10)
        if msg == 'Start1':
            print(str(addr) + ': ' + msg)
            break
    
    print(str(addr) + ': Send matrix1 of length ' + str(len(matrix1)))
    workersocket.send(matrix1)
    
    # wait for response for matrix1
    while True:
        msg = workersocket.recv(10)
        if msg == 'Done1':
            print(str(addr) + ': ' + msg)
            break
            
    # send matrix2 to worker
    workersocket.send('Size2:' + str(len(matrix2)))
    
    while True:
        msg = workersocket.recv(10)
        if msg == 'Start2':
            print(str(addr) + ': ' + msg)
            break
    
    print(str(addr) + ': Send matrix2 of length ' + str(len(matrix2)))
    workersocket.send(matrix2)
    
    # wait for response for output
    while True:
        msg = workersocket.recv(1024)
        result_len = -1
        if msg.startswith('OutputSize'):
            result_len = int(msg.split(':')[1])
            print(str(addr) + ': Receiving result of length ' + str(result_len))
            break
    
    workersocket.send('StartOutput')
    
    received = workersocket.recv(1024)
    result_received = received
    while len(result_received) < result_len:
        received = workersocket.recv(1024)
        result_received += received
    
    print(str(addr) + ': Received result of length ' + str(len(result_received)))
            
    result[work_index] = result_received
    workersocket.close()

if __name__ == '__main__':
    num_worker = -1
    work_split = -1
    
    if len(sys.argv) == 6:
        num_worker = int(sys.argv[1])
        work_split = int(sys.argv[2])
        try:
            infile1 = open(sys.argv[3], 'r')
            infile2 = open(sys.argv[4], 'r')
            out_file = open(sys.argv[5], 'w')
        except:
            print('Cannot open output file.')
            sys.exit(0)
    else:
        print('Wrong number of arguments.')
        sys.exit(0)
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('10.0.0.1', 10021))
    s.listen(100)
    
    print('Listening to all incoming worker nodes')
    start_time = time.time()
    
    # get connections from all worker nodes
    free_workers = []
    while len(free_workers) < num_worker:
        try:
            (workersocket, addr) = s.accept()
            free_workers.append((workersocket, addr))
        except KeyboardInterrupt:
            print('Keyboard interruption')
            break
            
    print(free_workers)
    
    # read matrices from files and split work     
    matrix1 = mo.readMatrix(infile1)
    works = createWork(matrix1, work_split)
    
    matrix2_work = createWork(mo.readMatrix(infile2), 1)[0]
    
    print('Start distributing work')
    
    # send splitted work to free worker nodes
    result = dict()
    for work_index in range(len(works)):
        # get one worker from free worker list
        (workersocket, addr) = free_workers.pop(0)
        thread.start_new_thread(workerNode, (workersocket, addr, work_index, works[work_index], matrix2_work, result))
    
    # wait until all results received
    while len(result) < len(works):
        try:
            pass
        except KeyboardInterrupt:
            print('Keyboard interruption')
            break
        
    print(len(result))
    
    s.close()
    
    # write output to file
    for r_key in result:
        byte_str = result[r_key]
        out_file.write(byte_str.decode())
        out_file.write('\n')
    
    end_time = time.time()
    diff = end_time - start_time
    print('Running time: ' + str(diff))
    out_file.write('\n\nRunning time: ' + str(diff))
    
    infile1.close()
    infile2.close()
    out_file.close()