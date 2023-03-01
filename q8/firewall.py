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

    def _handle_ConnectionUp(self, event):
        """Implement your logic here"""
        self.connection = event.connection
        print("Connection %s" % (dpid_to_str(event.dpid),))

        with open(policyFile, 'r') as f:
            reader = csv.reader(f)
            policies = list(reader)

        for policy in policies:
            src_mac, dst_mac = policy
            match = of.ofp_match()
            match.dl_src = src_mac
            match.dl_dst = dst_mac

            msg = of.ofp_flow_mod()
            msg.match = match
            msg.priority = 1
            msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))

        self.connection.send(msg)
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))


def launch():
    # start Firewall module
    core.registerNew(Firewall)
