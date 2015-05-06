import os
import sys
import logging
import unittest
from neutronclient.neutron import client

class TestBaseClass(unittest.TestCase):
        def setUp(self):
                self.auth_url= os.environ['OS_AUTH_URL']
                self.username= os.environ['OS_USERNAME']
                self.password= os.environ['OS_PASSWORD']
                self.tenant_name= os.environ['OS_TENANT_NAME']
                self.neutron = client.Client('2.0', auth_url=self.auth_url,
                                        username=self.username, password=self.password,
                                        tenant_name=self.tenant_name)

                self.log_setting()

                self.logger.info("Connected to neutron client as user:{user}, tenant:{tenant}"
                                        .format(user=self.username, tenant=self.tenant_name) )

                self._init()

        def log_setting(self):
                self.logger = logging.getLogger(self.__class__.__name__)
                self.logger.setLevel(logging.DEBUG)
                handler = logging.StreamHandler(sys.stdout)
                self.logger.addHandler(handler)


	def _init(self):
		pass




