import requests

class Passwordstate:
    def __init__(self, module, url, apikey):
        self.module = module
        self.url = url
        self.apikey = apikey

    def get_password_fields(self, id):
        response = self._request('passwords/' + str(id), 'GET')
        if response and isinstance(response, list) and len(response) > 0:
            return response[0]  # Assuming the first item in the list is the data dictionary
        else:
            return {}  # Return an empty dictionary if the response is not as expected

    def update_password(self, id, data):
        # Ensure the endpoint and HTTP method are correctly configured.
        return self._request('passwords/', 'PUT', json=data)

    def _request(self, uri, method, json=None, params=None):
        methods = {
            'GET': requests.get,
            'PUT': requests.put
        }
        headers = {'APIKey': self.apikey, 'Content-Type': 'application/json'}
        try:
            response = methods[method](self.url + '/api/' + uri, headers=headers, params=params, json=json)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.module.fail_json(msg="API request failed: %s" % str(e))
