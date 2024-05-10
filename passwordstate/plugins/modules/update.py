from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ansible.passwordstate.plugins.module_utils.utils import Passwordstate

def main():
    # Define the argument specification for the module
    module = AnsibleModule(
        argument_spec={
            'url': {'required': True, 'type': 'str'},
            'apikey': {'required': True, 'type': 'str', 'no_log': True},
            'id': {'required': True, 'type': 'int'},
            'password': {'required': True, 'type': 'str', 'no_log': True},
            'username': {'type': 'str', 'default': None},
        },
        supports_check_mode=True  # Enable check mode support
    )

    # Initialize API connection
    api = Passwordstate(module, module.params['url'], module.params['apikey'])
    current_password_data = api.get_password_fields(module.params['id'])

    # Determine what needs to be updated
    changes = {}
    current_password = current_password_data.get('Password')
    current_username = current_password_data.get('UserName')
    
    if current_password != module.params['password']:
        changes['Password'] = module.params['password']
    if current_username != module.params['username']:
        changes['UserName'] = module.params['username']

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
