#!/usr/bin/python3
# -*- coding: utf-8 -*-

DOCUMENTATION = r'''
---
module: update
short_description: Update an existing password ID
version_added: 0.1.0
description:
  - Update an existing password ID
options:
  url:
    description:
      - Passwordstate URL
    required: true
    type: str
  api_key:
    description:
      - API key used for authentication.
    required: true
    type: str
    no_log: true
  id:
    description:
      - ID of the specific password entry to retrieve.
    required: true
    type: int
  username:
    description:
      - Username for the password ID
    required: false
    type: str
  password:
    description:
      - Password for the password ID
    required: false
    type: str
author:
  - Aaron Place (@aplace-lab)
'''

EXAMPLES = r'''
- name: Update password for ID 123
  ansible.passwordstate.update:
    url: https://passwordstate.example.com
    api_key: your_api_key
    id: 123
    password: my_pass
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.passwordstate.plugins.module_utils.utils import Passwordstate

def main():
    # Define the argument specification for the module
    module = AnsibleModule(
        argument_spec={
            'url':      {'required': True, 'type': 'str'},
            'api_key':  {'required': True, 'type': 'str', 'no_log': True},
            'id':       {'required': True, 'type': 'int'},
            'username': {'required': False, 'type': 'str', 'default': None},
            'password': {'required': False, 'type': 'str', 'default': None, 'no_log': True},
        },
        required_one_of = [('username', 'password')]
        supports_check_mode=True  # Enable check mode support
    )

    # Initialize API connection
    api = Passwordstate(module, module.params['url'], module.params['api_key'])
    current_password_data = api.get_password_fields(module.params['id'])

    # Determine what needs to be updated
    changes = {}
    if current_password_data.get('UserName') != module.params['username']:
        changes['UserName'] = module.params['username']
    if current_password_data.get('Password') != module.params['password']:
        changes['Password'] = module.params['password']

    # Report potential changes in check mode
    if module.check_mode:
        # Exit without making any changes but report what would have been changed
        module.exit_json(changed=bool(changes), changes=changes)

    # Update password data if there are changes
    if changes:
        update_data = {'PasswordID': module.params['id'], **changes}
        result = api.update_password(module.params['id'], update_data)
        module.exit_json(changed=True, result=result)
    else:
        module.exit_json(changed=False, result="No update necessary")

if __name__ == '__main__':
    main()
