import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

import quota_base

#http://pythontesting.net/framework/unittest/unittest-introduction/

class TestQuotaNetworkLimit(quota_base.TestQuotaBase):

	def _init(self):	
		self.network_names = []
		self.quota_limit = self._get_quota_limit('network')

	def test_quota_network_limit(self):		
		while True:
			network_name = uuid.uuid4().get_hex()
			network = {'name': network_name, 'admin_state_up': True}
			self.neutron.create_network({'network':network})
			self.logger.info("Created network:{0}".format(network_name))
			self.network_names.append(network_name)
			if not self.quota_limit:
				break
			self.quota_limit -= 1

	def tearDown(self):
		for network_name in self.network_names:
			networks = self.neutron.list_networks(name=network_name)
			if networks:
				self.neutron.delete_network(networks['networks'][0]['id'])
				self.logger.info("Deleted network:{0}".format(network_name))


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

