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

def run(num_worker, loss, delay):
    topo = SimpleTopo(num_worker, loss, delay)
    net = Mininet( topo=topo, link=TCLink)
    net.addNAT().configDefault()
    net.start()
    
    CLI( net )
            
if __name__ == '__main__':
    if len(sys.argv) == 4:
        num_worker = int(sys.argv[1])
        loss = int(sys.argv[2])
        delay = int(sys.argv[3])
    else:
        print('Wrong number of arguments.')
        sys.exit(0)

    setLogLevel( 'info' )
    run(num_worker, loss, delay)