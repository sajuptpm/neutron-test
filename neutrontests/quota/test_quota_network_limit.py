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
		self.network_ids = []
		self.quota_limit = self._get_quota_limit('network')

	def test_quota_network_limit(self):		
		while True:
			network_name = uuid.uuid4().get_hex()
			network = {'name': network_name, 'admin_state_up': True}
			network_info = self.neutron.create_network({'network':network})
			network_id = network_info['network']['id']
			self.logger.info("Created Network:{0}".format(network_id))
			self.network_ids.append(network_id)
			if not self.quota_limit:
				break
			self.quota_limit -= 1

	def tearDown(self):
		for network_id in self.network_ids:
			self.neutron.delete_network(network_id)
			self.logger.info("Deleted Network:{0}".format(network_id))


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

