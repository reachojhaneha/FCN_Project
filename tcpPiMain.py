import socket
import thread
import time
import sys
    
def workerNode(workersocket, addr, work_index, iteration, worker_num, result):
    # initialization
    while True:
        msg = workersocket.recv(10)
        if msg == 'Accept':
            print(str(addr) + ': ' + msg)
            break
    
    # send num of iteration to worker
    print(str(addr) + ': Sending number of iteration ' + str(iteration))
    workersocket.send('Iteration:' + str(iteration))
    
    while True:
        msg = workersocket.recv(100)
        if msg == 'IterationReceived':
            print(str(addr) + ': Iteration received')
            break
    
    # send work index to worker
    print(str(addr) + ': Sending work index ' + str(work_index))
    workersocket.send('WorkIndex:' + str(work_index))
    
    while True:
        msg = workersocket.recv(100)
        if msg == 'WorkIndexReceived':
            print(str(addr) + ': Work index received')
            break
            
    # send work index to worker
    print(str(addr) + ': Send worker number ' + str(worker_num))
    workersocket.send('WorkerNum:' + str(worker_num))
    
    # wait for response from worker node
    while True:
        msg = workersocket.recv(1024)
        if len(msg) > 3:
            print(str(addr) + ': Received result ' + msg)
            break
    
    result[work_index] = msg
    workersocket.close()

if __name__ == '__main__':
    num_worker = -1
    work_split = -1
    num_iteration = -1
    
    if len(sys.argv) == 4:
        num_worker = int(sys.argv[1])
        work_split = int(sys.argv[2])
        num_iteration = int(sys.argv[3])
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

    works = [i for i in range(work_split)]
    print('Start distributing work')
    
    # send splitted work to free worker nodes
    result = dict()
    for work_index in range(len(works)):
        # get one worker from free worker list
        (workersocket, addr) = free_workers.pop(0)
        thread.start_new_thread(workerNode, (workersocket, addr, work_index, num_iteration, num_worker, result))
    
    # wait until all results received
    while len(result) < len(works):
        try:
            pass
        except KeyboardInterrupt:
            print('Keyboard interruption')
            break
        
    print(len(result))
    
    s.close()
    
    pi_approx = 0
    # write output to file
    for r_key in result:
        result_str = result[r_key]
        try:
            pi_approx += float(result_str)
        except:
            print('Error occurs when converting to float')
    
    print('Pi approximation: ' + str(pi_approx))
    
    end_time = time.time()
    diff = end_time - start_time
    print('Running time: ' + str(diff))
