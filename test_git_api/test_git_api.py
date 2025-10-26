import json
import unittest
import requests

import os

git_token = os.getenv('git_token')
git_name = os.getenv('git_name')
git_repo = os.getenv('git_repo')

url_get_list_repo = f"https://api.github.com/users/{git_name}/repos"
url_create_repo = "https://api.github.com/user/repos"
url_delete_repo = f"https://api.github.com/repos/{git_name}/{git_repo}"

headers = {
    "Authorization": f"token {git_token}",
    "Accept": 'application/vnd.github.v3+json',
    'Cache-Control': 'no-cache',
    "Pragma": "no-cache"
}


class GitHabApiTest(unittest.TestCase):

    def test_post_get_delete_repos(self):
        response_post = post_repos()
        self.assertEqual(response_post.status_code, 201)

        response_get = get_list_repos()
        self.assertEqual(response_get.status_code, 200)
        list_repos = response_get.json()
        add_repo = ' '.join(
            [list_repos[i]['name']
             for i in range(len(list_repos))
             if list_repos[i]['name'] == git_repo])
        self.assertEqual(add_repo, git_repo)

        response_delete = delete_repo()
        self.assertEqual(response_delete.status_code, 204)
        response_get_after = get_list_repos()
        list_repos_after = response_get_after.json()
        repos = [list_repos_after[i]['name'] for i in range(len(list_repos_after))]
        self.assertFalse(git_repo in repos)


def post_repos():
    return requests.post(url=url_create_repo,
                         data=json.dumps({'name': git_repo}),
                         auth=(git_name, git_token),
                         headers={"Content-Type": "application/json"})


def get_list_repos():
    return requests.get(url=url_get_list_repo, headers=headers)


def delete_repo():
    return requests.delete(url=url_delete_repo, headers=headers)