#
# Copyright 2014-2017 Groupon, Inc.
# Copyright 2014-2017 The Billing Project, LLC
#
# The Billing Project, LLC licenses this file to you under the Apache License, version 2.0
# (the "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.
#
import unittest
from killbill import Account
from killbill import Subscription

class TestIntegration(unittest.TestCase):
    def test_integration(self):
        profiling_data = dict()

        account = Account(currency='USD', state='CA', country='USA')
        account = account.create('test', 'for testing', 'no comment', profilingData=profiling_data)
        self.assertIsNotNone(account.accountId)
        self.assertEqual('USD', account.currency)
        self.assertEqual('CA', account.state)
        self.assertEqual('USA', account.country)

        self.assertEqual(account.accountId, Account.find_by_external_key(account.externalKey).accountId)
        self.assertEqual(0, len(account.bundles()))

        subscription = Subscription(accountId=account.accountId,
                                    productName='Sports',
                                    productCategory='BASE',
                                    billingPeriod='MONTHLY',
                                    priceList='DEFAULT')
        subscription.create('test')

        bundles = account.bundles()
        self.assertEqual(1, len(bundles))

        self.assertEqual(2, len(profiling_data))
        self.assertEqual(1, len(profiling_data['POST:/1.0/kb/accounts']))
        self.assertEqual(1, len(profiling_data['GET:/1.0/kb/accounts/uuid']))

        account.close(True, True, False, 'test')


if __name__ == '__main__':
    unittest.main()
