import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from common import common

#http://pythontesting.net/framework/unittest/unittest-introduction/

class TestCreateNetworks(common.TestBaseClass):

	def _init(self):	
		self.network_name = uuid.uuid4().get_hex()

	def test_create_network(self):
		network = {'name': self.network_name, 'admin_state_up': True}
		self.neutron.create_network({'network':network})
		self.logger.info("Created network:{0}".format(self.network_name))
	
	def tearDown(self):
		network = {'name': self.network_name}
		self.neutron.create_network({'network':network})
		self.logger.info("Deleted network:{0}".format(self.network_name))

	#def test_list_networks(self):
	#	print self.neutron.list_networks(name=self.network_name)


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

