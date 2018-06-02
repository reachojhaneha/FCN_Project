import socket
import time
import piCalculation as pc

if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.0.0.1', 10021))
        
        # send init msg 
        s.send('Accept')
        
        iteration = -1
        work_index = -1
        worker_num = -1
        
        # receive num of iteration
        while True:
            msg = s.recv(1024)
            if msg.startswith('Iteration'):
                iteration = int(msg.split(':')[1])
                break
            
        print('Received num of iteration: ' + str(iteration))
        
        s.send('IterationReceived')
        
        # receive work index
        while True:
            msg = s.recv(1024)
            if msg.startswith('WorkIndex'):
                work_index = int(msg.split(':')[1])
                break
        
        print('Received work index: ' + str(work_index))
        
        s.send('WorkIndexReceived')
        
        # receive worker num
        while True:
            msg = s.recv(1024)
            if msg.startswith('WorkerNum'):
                worker_num = int(msg.split(':')[1])
                break
        
        print('Received worker num: ' + str(worker_num))
        
        # perform pi approximation
        result = pc.approximatePi(iteration, work_index, worker_num)
        print('Sending back to main node. Result: ' + str(result))
        s.send(str(result))
        print('Send finish, close socket')
        
        s.close()
    except KeyboardInterrupt:
        print('Keyboard interruption')