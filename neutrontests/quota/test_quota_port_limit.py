##Create a new user "user1" and project "project1"
##Add "_member_" role for "user1" on project "project1"
##Export "user1's" credential and run this script

import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

import quota_base


class TestQuotaSubnetLimit(quota_base.TestQuotaBase):

        def _init(self):
                self.network_ids = []
		self.port_ids = []
                self.quota_limit = self._get_quota_limit('port')

	def test_quota_subnet_limit(self):
		network_name = uuid.uuid4().get_hex()
		network = {'name': network_name, 'admin_state_up': True}
		network_info = self.neutron.create_network({'network':network})
		self.logger.info("Created network:{0}".format(network_name))
		network_id = network_info['network']['id']
		self.network_ids.append(network_id)
		subnet_cidrs = ['11.2.2.0/29',  '11.2.2.8/29']
		for cidr in subnet_cidrs:
			subnet = {"network_id": network_id, "ip_version":4, "cidr": cidr}
			subnet_info = self.neutron.create_subnet({'subnet':subnet})
			subnet_id = subnet_info['subnet']['id']
			self.logger.info("Created subnet:{0}".format(cidr))

		while True:
			port = {"network_id": network_id, "admin_state_up": True}
			port_info = self.neutron.create_port({'port':port})
			port_id = port_info['port']['id']
			self.port_ids.append(port_id)
			self.logger.info("Created Port:{0}".format(port_info['port']['id']))
			if not self.quota_limit:
				break
			self.quota_limit -= 1

	def tearDown(self):
		for port_id in self.port_ids:
                        self.neutron.delete_port(port_id)
                        self.logger.info("Deleted Port:{0}".format(port_id))
		for network_id in self.network_ids:
			self.neutron.delete_network(network_id)
			self.logger.info("Deleted Network:{0}".format(network_id))


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

