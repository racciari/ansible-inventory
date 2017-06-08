#!/usr/bin/env python

'''
Ansible dynamic inventory for Dnsmasq
'''

import argparse

try:
    import json
except ImportError:
    import simplejson as json


class DnsmasqInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.dnsmasq_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return an empty inventory.
        else:
            self.inventory = self.empty_inventory()

        print json.dumps(self.inventory)

    def dnsmasq_inventory(self):
        return {
            'group': {
                'hosts': self.parse_leases(),
                'vars': {
                }
            },
        }

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}

    def parse_leases(self, file='/var/lib/dnsmasq/dnsmasq.leases'):
        with open(file) as f:
            return [l.split()[3] for l in f]

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--host', action='store')
        self.args = parser.parse_args()


# Get the inventory.
DnsmasqInventory()

