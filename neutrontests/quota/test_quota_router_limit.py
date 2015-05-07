import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

import quota_base

#http://pythontesting.net/framework/unittest/unittest-introduction/

class TestQuotaRouterLimit(quota_base.TestQuotaBase):

	def _init(self):	
		self.router_ids = []
		self.quota_limit = self._get_quota_limit('router')

	def test_quota_router_limit(self):		
		while True:
			router_name = uuid.uuid4().get_hex()
			router = {'name': router_name, 'admin_state_up': True}
			router_info = self.neutron.create_router({'router':router})
			router_id = router_info['router']['id']
			self.logger.info("Created Router:{0}".format(router_id))
			self.router_ids.append(router_id)
			if not self.quota_limit:
				break
			self.quota_limit -= 1

	def tearDown(self):
		for router_id in self.router_ids:
			self.neutron.delete_router(router_id)
			self.logger.info("Deleted Router:{0}".format(router_id))


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

