import requests
import os
from dotenv import load_dotenv

load_dotenv()

git_token = os.getenv('git_token')
git_name = os.getenv('git_name')
git_repo = os.getenv('git_repo')

url_get_list_repo = f"https://api.github.com/users/{git_name}/repos"
url_create_repo = 'https://api.github.com/user/repos'
url_delete_repo = f"https://api.github.com/repos/{git_name}/{git_repo}"



def new_repo(git_token, git_repo):
    
    headers = {
       "Authorization": f"token {git_token}",
       "Accept": "application/vnd.github.v3+json"
    }  
        
    data = {
        "name": git_repo,
        "description": None,
    }
    
        
    response = requests.post(url_create_repo, headers=headers, json=data)

    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 201:
        repo_data = response.json()
        print("New public repo created successfully!")
        return repo_data
    elif response.status_code == 422:
        print('Repository already exists')
        return None
    else:
        print('Some error')
        return None
    
def delete_repo(git_token):
     
    headers = {
       "Authorization": f"token {git_token}",
       "Accept": "application/vnd.github.v3+json"
    }  
    
    response = requests.delete(url_delete_repo, headers=headers)

    if response.status_code == 204:
        print(f"Repository has been deleted successfully. Status code: {response.status_code}")
    elif response.status_code == 404:
        print(f"Repository not found or already deleted. Status code: {response.status_code}")
    else:
        print(f"Failed to delete repository. Status code: {response.status_code}")

def get_repo(git_token):
    
    headers = {
       "Authorization": f"token {git_token}",
       "Accept": "application/vnd.github.v3+json"
    }  
    
    response = requests.get(url_get_list_repo, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        repo_names = [repo['name'] for repo in repos]
        print(repo_names)
        return repo_names
    else:
        print(f"Ошибка: {response.status_code}")
        return None
    
get_repo(git_token)   
new_repo(git_token, git_repo) 
get_repo(git_token)    
delete_repo(git_token)
get_repo(git_token) 
