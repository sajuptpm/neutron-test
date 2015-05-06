import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

import quota_base


class TestQuotaSubnetLimit(quota_base.TestQuotaBase):

        def _init(self):
                self.network_names = []
                self.quota_limit = self._get_quota_limit('subnet')

	def test_quota_subnet_limit(self):
		network_name = uuid.uuid4().get_hex()
		network = {'name': network_name, 'admin_state_up': True}
		network_info = self.neutron.create_network({'network':network})
		self.logger.info("Created network:{0}".format(network_name))
		self.network_names.append(network_name)
		network_id = network_info['network']['id']
		subnet_cidrs = ['10.2.2.{0}/29'.format(8*x) for x in range(32)]
		for cidr in subnet_cidrs:
			subnet = {"network_id": network_id, "ip_version":4, "cidr": cidr}
			self.neutron.create_subnet({'subnet':subnet})
			self.logger.info("Created subnet:{0}".format(cidr))
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

