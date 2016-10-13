import argparse
import links_from_header
import requests

parser = argparse.ArgumentParser(description='Transfer stars from one GitHub repository to another')
parser.add_argument('--from', dest='github_from_user', required=True, nargs=1, type=str,
                    help='the GitHub user that is the source of the star list')
parser.add_argument('--token', dest='github_token', required=True, nargs=1, type=str,
                    help='the GitHub API token for the GitHub user account that the star list will be transferred to')

users = vars(parser.parse_args())
github_from_user = users['github_from_user'][0]
github_token = users['github_token'][0]
url = "https://api.github.com/users/%s/starred" % github_from_user
while True:
    github_star_response = requests.get(url)
    link_headers = links_from_header.extract(github_star_response.headers.get('Link', '')) or {}
    url = link_headers.get('next', None)
    repos = github_star_response.json()
    for repo_info in repos:
        owner, repo = repo_info['full_name'].split("/")
        print("Star the following repository: %s/%s" % (owner, repo))
        put_url = 'https://api.github.com/user/starred/%(owner)s/%(repo)s?access_token=%(github_token)s' % {'owner': owner, 'repo': repo, 'github_token': github_token}
        put_return_code = requests.put(put_url)
        print("Resulted in %s" % put_return_code)
    if not url:
        break
