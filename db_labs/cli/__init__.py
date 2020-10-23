from pprint import pprint

import click
import requests

APP_DEV_URL = "http://localhost:5000/api"


@click.command()
@click.option('--option', prompt='Your name',
              help='Options: create\nupdate\nget')
def main(option):
    if option == 'create_developer':
        email = click.prompt('Please enter an email', type=str)
        first_name = click.prompt('Please enter a first name', type=str)

        try:
            response = requests.post(f"{APP_DEV_URL}/developer", json=dict(email=email, first_name=first_name))
        except Exception:
            return print("An error occurred while trying to reach the API.")

        if response.status_code != 200:
            return print("An error occurred during the API request.")

        print("New developer created.")
        return pprint(response.json())

    if option == 'update_developer':
        id = click.prompt('Please enter a developer id', type=int)
        email = click.prompt('Please enter an email', type=str)
        first_name = click.prompt('Please enter a first name', type=str)


        try:
            response = requests.patch(f"{APP_DEV_URL}/developer/{id}", json=dict(email=email, first_name=first_name))
        except Exception:
            return print("An error occurred while trying to reach the API.")

        if response.status_code != 200:
            return print("An error occurred during the API request.")

        print(f"Developer with id: {id} was updated.")
        return pprint(response.json())

    if option == 'search_developers':
        query_string = click.prompt('Please enter a search keyword(first/last name or skill name)', type=str)

        try:
            response = requests.get(f"{APP_DEV_URL}/developer?query={query_string}")
        except Exception:
            return print("An error occurred while trying to reach the API.")

        if response.status_code != 200:
            return print("An error occurred during the API request.")

        if not response.json():
            return print(f"No results found for the keyword: {query_string}")

        print(f"{len(response.json())} developers found for the keyword: {query_string}")
        return pprint(response.json())



if __name__ == '__main__':
    main()