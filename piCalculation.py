from __future__ import division
import time

def f(a):
    num = 4 / (1 + (a * a))
    return num

def approximatePi(iteration, starting_index, step):
    h = 1 / iteration
    sum = 0
    
    for i in range(starting_index, iteration, step):
        x = h * (i - 0.5)
        sum += f(x)
        
    return (h * sum)
    
if __name__ == '__main__':
    start_time = time.time()
    pi_approx = approximatePi(10000000, 0, 2)
    
    print('Pi approximation: ' + str(pi_approx))
    
    end_time = time.time()
    diff = end_time - start_time
    
    print('Running time: ' + str(diff))
    