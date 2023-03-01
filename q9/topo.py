from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class Q9Topo(Topo):
    def __init__(self, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)

        ### Implement your logic here ###
        lastSwitch = None
        for i in range(1, 4):
            host = self.addHost("h%s" % i)
            switch = self.addSwitch("s%s" % i)
            self.addLink(host, switch)
            if lastSwitch:
                self.addLink(switch, lastSwitch)
            lastSwitch = switch




topos = {"custom": (lambda: Q9Topo())}
