import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

import quota_base
import settings

#http://pythontesting.net/framework/unittest/unittest-introduction/

class TestQuotaNetworkLimit(quota_base.TestQuotaBase):

	def _init(self):	
		self.fip_ids = []
		self.quota_limit = self._get_quota_limit('floatingip')
		self.floating_nw_id = settings.FLOATING_NETWORK_ID

	def test_quota_floatingip_limit(self):		
		while True:
			floatingip = {"floating_network_id": self.floating_nw_id}
			fip_info = self.neutron.create_floatingip({'floatingip':floatingip})
			fip_id = fip_info['floating']['id']
			self.logger.info("Created Floating IP:{0}".format(fip_id))
			self.fip_ids.append(fip_id)
			if not self.quota_limit:
				break
			self.quota_limit -= 1

	def tearDown(self):
		for fip_id in self.fip_ids:
			self.neutron.delete_floatingip(fip_id)
			self.logger.info("Deleted Floating IP:{0}".format(fip_id))


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

