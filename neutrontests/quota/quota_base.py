import os
import sys
import logging
import uuid
import unittest
from neutronclient.neutron import client

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from common import common

class TestQuotaBase(common.TestBaseClass):

        def _get_quota_limit(self, resource_name='network'):
                self.quota_limit = None
                quota = self.neutron.show_quota(self.current_project_id)
                if quota:
                        self.quota_limit = quota.get('quota', {}).get(resource_name)
                self.logger.info("Quota: {resource_name} Limit: {limit}"
			.format(resource_name=resource_name, limit=self.quota_limit))
                if not self.quota_limit:
                        self.quota_limit = 0
                if self.quota_limit in [-1, '-1']:
                        self.quota_limit = 50
		return self.quota_limit







