"""Demo script for the REST API.
Logs in using demo credentials, get the projects metadata and print them on screen.
"""
import requests
import json
from typing import Dict

base_url = 'https://api.cloud.rtloc.com/'

def login(user_credentials: Dict[str, str]) -> Dict:
    """Logs in the API's /auth/login endpoint.

    ## Parameters
        user_credentials: Dict containing "email" and "password".

    ## Returns
        A Dict with the response body from the API.
    """
    response = requests.post(base_url + 'auth/login', data=user)
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
        'https://api.cloud.rtloc.com/project',
        headers = {
            "Authorization": auth_token
        }
    )
    return projects.json()

def main(user: Dict[str, str]) -> None:
    """Main program that logs in the API, get the projects, and prints on screen.

    ## Parameters
        user_credentials: Dict containing "email" and "password".

    ## Returns
        None
    """
    login_response = login(user)
    token = login_response['token']
    projects = get_projects(token)

    print(json.dumps(projects, indent=2))

if __name__ == '__main__':
    user = {
        'email': 'demo@rtloc.com',
        'password': 12345
    }

    main(user)