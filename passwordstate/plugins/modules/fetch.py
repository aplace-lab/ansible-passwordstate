#!/usr/bin/python3
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: fetch
short_description: Retrieve passwords from Passwordstate
version_added: 0.1.0
description:
  - This module retrieves username and password information from Passwordstate using an API token.
  - Creates a fact that contains credentials to use in other modules.
options:
  url:
    description:
      - Passwordstate URL
    required: true
    type: str
  apikey:
    description:
      - API key used for authentication.
    required: true
    type: str
    no_log: true
  list_id:
    description:
      - ID of the password list that contains the password entry.
    required: false
    type: int
  id:
    description:
      - ID of the specific password entry to retrieve.
    required: true
    type: int
author:
  - Aaron Place (@aplace-lab)
'''

EXAMPLES = r'''
- name: Fetch password details for ID 123
  ansible.passwordstate.fetch:
    url: https://passwordstate.example.com
    apikey: your_api_key
    id: 123
  register: my_user

- name: Display password
  ansible.builtin.debug:
    var: my_user.Password
'''

RETURN = r'''
username:
  description: The username associated with the password ID.
  returned: always
  type: str
  sample: 'user'
password:
  description: The password returned from Passwordstate.
  returned: always
  type: str
  sample: 'password123'
title:
  description: The title of the password.
  returned: always
  type: str
  sample: 'My User'
description:
  description: The description of the password entry details.
  returned: always
  type: str
  sample: 'Used for example services'
expiry:
  description: Account or password expiry date
  returned: always
  type: str
  sample: '15/10/1999'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.passwordstate.plugins.module_utils.utils import Passwordstate

class Password:
    def __init__(self, api, list_id, id):
        self.api = api
        self.list_id = list_id
        self.id = id

    def gather_facts(self):
        fields = self.api.get_password_fields(self.id)
        if not fields:
            self.module.fail_json(msg="No data received from API")
        return fields

def main():
    module = AnsibleModule(
        argument_spec={
            'url': {'required': True, 'type': 'str'},
            'apikey': {'required': True, 'type': 'str', 'no_log': True},
            'list_id': {'required': False, 'type': 'int'},
            'id': {'required': True, 'type': 'int'},
        },
        supports_check_mode=False
    )

    api = Passwordstate(module, module.params['url'], module.params['apikey'])
    password = Password(api, module.params['list_id'], module.params['id'])

    result = password.gather_facts()
    # Spread the entire result into the response
    module.exit_json(changed=False, **result)

if __name__ == '__main__':
    main()