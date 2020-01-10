"""Demo script for the REST API.
Logs in using demo credentials, get the projects, clients and users metadata
and print them on screen.
"""
import requests
import json
from typing import Dict

base_url = 'https://api.cloud.rtloc.com'

def login(user_credentials: Dict[str, str]) -> Dict:
    """Logs in the API's /auth/login endpoint.

    ## Parameters
        user_credentials: Dict containing "email" and "password".

    ## Returns
        A Dict with the response body from the API.
    """
    response = requests.post(base_url + '/auth/login', data=user)
    return response.json()


def get_projects(token: str) -> Dict:
    """Get the projects in the API's /project endpoint.

    ## Parameters
        token: Login token for authentication.

    ## Returns
        A Dict with the response body from the API, containing the projects.
    """
    auth_token = 'Bearer {}'.format(token)
    projects = requests.get(
        base_url + '/project',
        headers={
            'Authorization': auth_token
        }
    )
    return projects.json()

def get_clients(token: str) -> Dict:
    """Get the clients in the API's /client endpoint.

    ## Parameters
        token: Login token for authentication.

    ## Returns
        A Dict with the response body from the API, containing the clients.
    """
    auth_token = 'Bearer {}'.format(token)
    clients = requests.get(
        base_url + '/client',
        headers={
            'Authorization': auth_token
        }
    )
    return clients.json()

def get_client(token: str, client_id: str) -> Dict:
    """Given an id, gets the client in the API's /client/{id} endpoint.

    ## Parameters
        token: Login token for authentication.
        client_id: Client's Id.

    ## Returns
        A Dict with the response body from the API, containing the clients.
    """
    auth_token = 'Bearer {}'.format(token)
    client = requests.get(
        base_url + '/client/{}'.format(client_id),
        headers={
            'Authorization': auth_token
        }
    )
    return client.json()

def get_users(token: str) -> Dict:
    """Get the users in the API's /user endpoint.

    ## Parameters
        token: Login token for authentication.

    ## Returns
        A Dict with the response body from the API, containing the users.
    """
    auth_token = 'Bearer {}'.format(token)
    users = requests.get(
        base_url + '/user',
        headers={
            'Authorization': auth_token
        }
    )
    return users.json()

def main(user: Dict[str, str]) -> None:
    """Main program that logs in the API, get the projects, clients and users,
    and prints on screen.

    ## Parameters
        user_credentials: Dict containing "email" and "password".

    ## Returns
        None
    """
    login_response = login(user)
    token = login_response['token']
    projects = get_projects(token)

    print('--- Projects:')
    print(json.dumps(projects, indent=2))

    clients = get_clients(token)
    print('\n--- Clients:')
    print(json.dumps(clients, indent=2))

    id = '3c7471f1180213232c5a1231'
    client = get_client(token, id)
    print('\n--- Client id = {}:'.format(id))
    print(json.dumps(client, indent=2))

    users = get_users(token)
    print('\n--- Users:')
    print(json.dumps(users, indent=2))

if __name__ == '__main__':
    user = {
        'email': 'demo@rtloc.com',
        'password': 12345
    }

    main(user)