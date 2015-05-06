import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from common import common

#http://pythontesting.net/framework/unittest/unittest-introduction/

class TestQuotaNetworkLimit(common.TestBaseClass):

	def _init(self):	
		self.network_names = []
		self.quota_network_limit = None
                quota = self.neutron.show_quota(self.current_project_id)
                if quota:
                        self.quota_network_limit = quota.get('quota', {}).get('network')
		self.logger.info("Quota: Number of Virtual Networks limiti: {0}".format(self.quota_network_limit))
		
		if not self.quota_network_limit:
			self.quota_network_limit = 0
		if self.quota_network_limit in [-1, '-1']:
			self.quota_network_limit = 50

	def test_create_network(self):		
		while True:
			network_name = uuid.uuid4().get_hex()
			network = {'name': network_name, 'admin_state_up': True}
			self.neutron.create_network({'network':network})
			self.logger.info("Created network:{0}".format(network_name))
			self.network_names.append(network_name)
			if not self.quota_network_limit:
				break
			self.quota_network_limit -= 1

	def tearDown(self):
		for network_name in self.network_names:
			networks = self.neutron.list_networks(name=network_name)
			if networks:
				self.neutron.delete_network(networks['networks'][0]['id'])
				self.logger.info("Deleted network:{0}".format(network_name))


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

