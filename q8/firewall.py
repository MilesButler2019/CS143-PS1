from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
import os
import csv
""" Add your imports here ... """


log = core.getLogger()
policyFile = f"{os.environ['HOME']}/pox/pox/misc/firewall-policies.csv"
### Add global variables and data preprocessing here ###

class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
        core.openflow.addListenerByName("ConnectionUp", self._handle_ConnectionUp)
        with open(policyFile, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            self.policies = list(reader)

        self.policies_set = set()

        for i in self.policies:
            self.policies_set.update([((EthAddr(i[1]), EthAddr(i[2])))])


    def _handle_ConnectionUp(self, event):
        dpid = dpidToStr(event.dpid)
        #Allow all traffic 
        switch = event.connection
        match = of.ofp_match()
        action = of.ofp_action_output(port=of.OFPP_CONTROLLER)
        flow_mod = of.ofp_flow_mod(match=match, actions=[action])
        switch.send(flow_mod)
        
        # Set up flow rules to block pairs of MAC addresses
        for  mac in self.policies_set:
             match = of.ofp_match(dl_src=mac[0], dl_dst=mac[1])
             flow_mod = of.ofp_flow_mod(match=match)
             switch.send(flow_mod)

def launch():
    # start Firewall module
    core.registerNew(Firewall)
