import subprocess
import json

with open('/Users/vn552f7/Ajit/A-codes/GitFame/git-fame-input.json', 'r') as f:
    data = json.load(f)

    # for repo in data['repositories']:
    #     print(repo, type(repo))
    #     output = subprocess.check_output(["git", "fame", repo['path']], universal_newlines=True)
    #     print(f"Repository: {repo['name']}")
    #     print(output)


with open('/Users/vn552f7/Ajit/A-codes/GitFame/git-fame-input.json', 'r') as f:
    data = json.load(f)

    for repo in data['repositories']:
        output = subprocess.check_output(["git", "fame", repo], universal_newlines=True)
        print(f"Repository: {repo}")
        print(output)
