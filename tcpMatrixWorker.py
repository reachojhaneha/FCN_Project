import socket
import time
import matrixOperation as mo

if __name__ == '__main__':
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('10.0.0.1', 10021))
        
        # send init msg 
        s.send('Accept')
        
        # receive matrix1
        while True:
            msg = s.recv(1024)
            total_len = -1
            if msg.startswith('Size1'):
                total_len = int(msg.split(':')[1])
                break
            
        print('Receiving matrix1 of length ' + str(total_len))
        
        s.send('Start1')
        
        received = s.recv(1024)
        work = received
        while len(work) < total_len:
            received = s.recv(1024)
            work += received
            
        print('Finished receiving matrix1 of length ' + str(len(work)))
        matrix1 = mo.convertBytesToMatrix(work)
            
        print('Get matrix1 of size ' + str(len(matrix1)) + 'X' + str(len(matrix1[-1])))
            
        s.send('Done1')
        
        # receive matrix2
        while True:
            msg = s.recv(1024)
            total_len = -1
            if msg.startswith('Size2'):
                total_len = int(msg.split(':')[1])
                break
        
        print('Receiving matrix2 of length ' + str(total_len))
        
        s.send('Start2')
        
        received = s.recv(1024)
        work = received
        while len(work) < total_len:
            received = s.recv(1024)
            work += received
            
        print('Finished receiving matrix2 of length ' + str(len(work)))
        matrix2 = mo.convertBytesToMatrix(work)
        
        print('Get matrix2 of size ' + str(len(matrix2)) + 'X' + str(len(matrix2[-1])))
        print('Performing matrix multiplication')
        
        # perform matrix multiplication
        output_matrix = mo.simpleMultiplication(matrix1, matrix2)
        
        # convert output back to bytes and send back to main node
        result = mo.convertMatrixToBytes(output_matrix)
    
        print('Sending back result matrix of length ' + str(len(result)))
        s.send('OutputSize:' + str(len(result)))
        
        while True:
            msg = s.recv(15)
            if msg == 'StartOutput':
                break

        s.send(result)
        print('Send finish, close socket')
        
        s.close()
    except KeyboardInterrupt:
        print('Keyboard interruption')