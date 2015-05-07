import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

import quota_base

#http://pythontesting.net/framework/unittest/unittest-introduction/

class TestQuotaSecurityGroupLimit(quota_base.TestQuotaBase):

	def _init(self):	
		self.sg_ids = []
		self.quota_limit = self._get_quota_limit('security_group')

	def test_quota_security_group_limit(self):		
		while True:
			sg_name = uuid.uuid4().get_hex()
			security_group = {'name': sg_name}
			sg_info = self.neutron.create_security_group({'security_group':security_group})
			sg_id = sg_info['security_group']['id']
			self.logger.info("Created Security Group:{0}".format(sg_id))
			self.sg_ids.append(sg_id)
			if not self.quota_limit:
				break
			self.quota_limit -= 1

	def tearDown(self):
		for sg_id in self.sg_ids:
			self.neutron.delete_security_group(sg_id)
			self.logger.info("Deleted Security Group:{0}".format(sg_id))


if __name__ == '__main__':
	#Run this script: python test_create_networks.py
	unittest.main()

