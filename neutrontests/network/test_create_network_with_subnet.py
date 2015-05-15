import os
import sys
import logging
import uuid
import unittest
import netaddr
from neutronclient.neutron import client

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from common import common

class TestCreateNetworkWithSubnet(common.TestBaseClass):
	#https://wiki.openstack.org/wiki/Neutron/APIv2-specification
	#https://wiki.openstack.org/wiki/Neutron/APIv2-specification#Subnet

        def _init(self):
                self.network_ids = []
		self.network_name = "sa-nw1"
		self.number_of_subnet = 2
		network_cidr = netaddr.IPNetwork('10.2.2.0/24')
		self.subnet_cidrs =list(network_cidr.subnet(29))

	def test_create_net_work_with_subnet(self):
		network_name = self.network_name
		network = {'name': network_name, 'admin_state_up': True}
		network_info = self.neutron.create_network({'network':network})
		network_id = network_info['network']['id']
		self.logger.info("Created network:{0}".format(network_id))
		self.network_ids.append(network_id)
		subnet_count = 1
		for cidr in self.subnet_cidrs:
			gateway_ip = str(list(cidr)[1])
			subnet = {"network_id": network_id, "ip_version":4, 
				"cidr":str(cidr), "enable_dhcp":True, 
				"host_routes":[{"destination":"0.0.0.0/0", "nexthop":gateway_ip}]
				}
			subnet = {"name":"subnet-"+str(subnet_count), "network_id": network_id, "ip_version":4, "cidr":str(cidr), "enable_dhcp":True}
			print subnet
			self.neutron.create_subnet({'subnet':subnet})
			self.logger.info("Created subnet:{0}".format(str(cidr)))
			if not self.number_of_subnet - 1:
				break
			self.number_of_subnet -= 1
			subnet_count += 1

	def tearDown(self):
		for network_id in self.network_ids:
			#self.neutron.delete_network(network_id)
			self.logger.info("Deleted network:{0}".format(network_id))


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

