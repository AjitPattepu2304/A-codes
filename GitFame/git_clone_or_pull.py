import os
import subprocess
import shutil


def git_clone_or_pull(repo_url, local_path):
    repo_name = repo_url.split('/')[-1].split('.git')[0]
    full_local_path = os.path.join(local_path, repo_name)

    if os.path.exists(os.path.join(full_local_path, ".git")):
        try:
            subprocess.check_call(["git", "-C", full_local_path, "pull"])
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.output}")
    else:
        try:
            # clone the repo
            subprocess.check_call(["git", "clone", repo_url, full_local_path])
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.output}")

    return full_local_path

repo_urls = [
"https://github.com/AjitPattepu2304/A-codes.git"
]
local_path = "/Users/vn552f7/repositories"

local_paths = []
for repo_url in repo_urls:
    local_paths.append(git_clone_or_pull(repo_url, local_path))

# process your files
subprocess.call(["python3", "fame-process.Git-Fame.py"])



# # delete the repositories
# for repo_url in repo_urls:
#     repo_name = repo_url.split('/')[-1].split('.git')[0]
#     full_local_path = os.path.join(local_path, repo_name)
#     shutil.rmtree(full_local_path)

for local_repo_path in local_paths:
    shutil.rmtree(local_repo_path)

