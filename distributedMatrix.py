from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
import time
import sys

class SimpleTopo( Topo ):
    "Simple topology with 1 main node connecting to 4 worker nodes."

    def __init__( self , num_worker, loss, delay):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts
        #host0 = self.addHost('h0', ip='10.0.1.100/24')
        #host1 = self.addHost('h1', ip='10.0.1.1/24')
        #host2 = self.addHost('h2', ip='10.0.2.1/24')
        #host3 = self.addHost('h3', ip='10.0.3.1/24')
        #host4 = self.addHost('h4', ip='10.0.4.1/24')
        
        # use switch
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        host0 = self.addHost('main', ip='10.0.0.1/16')
        worker_nodes = []
        for i in range(num_worker):
            worker_name = 'h' + str(i)
            worker_ip = '10.0.1.' + str((i + 1)) + '/16'
            worker = self.addHost(worker_name, ip=worker_ip)
            worker_nodes.append(worker)

        # Add links
        self.addLink(host0, s1)
        #self.addLink(host0, s2)
        
        delay_str = str(delay) + 'ms'
        
        for i in range(len(worker_nodes)):
            self.addLink(s1, worker_nodes[i], loss=loss, delay=delay_str)

def run(num_worker, work_split, loss, delay, infile1, infile2, out_file):
    topo = SimpleTopo(num_worker, loss, delay)
    net = Mininet( topo=topo, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    
    net['main'].cmd('python tcpMatrixMain.py ' + str(num_worker) + ' ' + str(work_split) + ' ' + infile1 + ' ' + infile2 + ' ' + out_file + ' &')
    time.sleep(1)
    for i in range(num_worker):
        worker_name = 'h' + str(i)
        net[worker_name].cmd('python tcpMatrixWorker.py &')
    
    CLI( net )
            
if __name__ == '__main__':
    if len(sys.argv) == 8:
        num_worker = int(sys.argv[1])
        work_split = int(sys.argv[2])
        loss = int(sys.argv[3])
        delay = int(sys.argv[4])
        infile1 = sys.argv[5]
        infile2 = sys.argv[6]
        out_file = sys.argv[7]
    else:
        print('Wrong number of arguments.')
        sys.exit(0)

    setLogLevel( 'info' )
    run(num_worker, work_split, loss, delay, infile1, infile2, out_file)