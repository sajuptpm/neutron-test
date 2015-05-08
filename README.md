# neutron-test
neutron-test


### How to run the test

* Export the credential.

export OS_USERNAME=admin
export OS_PASSWORD=password
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://192.168.56.102:35357/v2.0

* $python neutrontests/quota/test_quota_subnet_limit.py

