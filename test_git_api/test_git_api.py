import requests
import os

git_token = os.getenv('git_token')
git_name = os.getenv('git_name')
git_repo = os.getenv('git_repo')


url = 'https://api.github.com/'

headers = {
       "Authorization": f"token {git_token}",
       "Accept": "application/vnd.github.v3+json"
    }  


def test_get_repo():
    
    url_get_repo = f'{url}/users/{git_name}/repos'
    
    response = requests.get(url_get_repo, headers=headers)
    
    assert  response.status_code == 200, f'Ошибка: {response.status_code}'   
    repos = response.json()
    repo_names = [repo['name'] for repo in repos]
    print("Список репозиториев:")
    for name in repo_names:
        print(f"  - {name}")
    

def test_new_repo():
      
    data = {
        "name": git_repo,
        "description": None,
    }
    url_create_repo = f'{url}/user/repos'
            
    response = requests.post(url_create_repo, headers=headers, json=data)
   
    if response.status_code == 201:
        repo_data = response.json()
        print(f'Новый репозиторий {git_repo} успешно создан')
        test_get_repo()  
        return repo_data
    elif response.status_code == 422:
        print('Такой репозиторий уже есть')
        return None
    else:
        print(f'Ошибка: {response.status_code}')
        return None
        
    
    
def test_delete_repo():
    url_delete_repo = f'{url}/repos/{git_name}/{git_repo}'   
    
    response = requests.delete(url_delete_repo, headers=headers)

    if response.status_code == 204:
        print(f'Репозиторий {git_repo} успешно  удален')
        test_get_repo()
    elif response.status_code == 404:
        print(f'Ошибка: {response.status_code}, не найден репозиторий')
    else:
        print(f'Ошибка: {response.status_code}')

