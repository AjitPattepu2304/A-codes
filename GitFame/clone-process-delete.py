import os
import shutil

import json
import subprocess
import re
import matplotlib.pyplot as plt
import numpy as np


with open('/Users/vn552f7/Ajit/A-codes/GitFame/git-fame-input.json', 'r') as f:
    data = json.load(f)

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
            subprocess.check_call(["git", "clone", repo_url, full_local_path])
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.output}")

    return full_local_path

local_path = "/Users/vn552f7/repositories"

local_paths = []
for repo_url in data['repositories']:
    local_paths.append(git_clone_or_pull(repo_url, local_path))


output_data = []

for author in data['authors']:
    print(author, type(author))

    author_dict = {'authorName': author['authorName'], 'gitStats': []}

    for repo in local_paths:
        output = subprocess.check_output(["git", "fame", "--since", "2024-01-01", "--ignore-whitespace"], cwd=repo,
                                         universal_newlines=True)
        print(output)

        lines_changed_total = commits_total = files_total = 0

        for keyword in author['authorKeywords']:
            escaped_keyword = re.escape(keyword)
            pattern = re.compile(rf"\|\s*{escaped_keyword}.*?\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*.*?\|")

            match = pattern.search(output)

            if match:
                print(match)
                lines_changed, commits, files = map(int, match.groups())
                lines_changed_total += lines_changed
                commits_total += commits
                files_total += files

        # printed_matches = set()
        #
        # for keyword in author['authorKeywords']:
        #     escaped_keyword = re.escape(keyword)
        #     pattern = re.compile(rf"\|\s*{escaped_keyword}.*?\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*.*?\|")
        #
        #     match = pattern.search(output)
        #
        #     if match and match.group() not in printed_matches:
        #         print(match)
        #         printed_matches.add(match.group())
        #         lines_changed, commits, files = map(int, match.groups())
        #         lines_changed_total += lines_changed
        #         commits_total += commits
        #         files_total += files

        author_dict['gitStats'].append({
            'repository': repo,
            'numberOfLinesChanged': lines_changed_total,
            'numberOfCommits': commits_total,
            'numberOfFiles': files_total
        })

    output_data.append(author_dict)

with open('output.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

authors = [d['authorName'] for d in output_data]
lines_changed = [sum(d['gitStats'][i]['numberOfLinesChanged'] for i in range(len(d['gitStats']))) for d in output_data]
commits = [sum(d['gitStats'][i]['numberOfCommits'] for i in range(len(d['gitStats']))) for d in output_data]
files = [sum(d['gitStats'][i]['numberOfFiles'] for i in range(len(d['gitStats']))) for d in output_data]

x = np.arange(len(authors))

width = 0.2

fig, ax = plt.subplots()

rects1 = ax.bar(x - width/3, lines_changed, width, label='Lines Changed')
rects2 = ax.bar(x + width/3, commits, width, label='Commits')
rects3 = ax.bar(x + width, files, width, label='Files')


ax.set_ylabel('Counts')
ax.set_title('Git Statistics by author')
ax.set_xticks(x)
ax.set_xticklabels(authors)
ax.legend()

def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)

fig.tight_layout()

plt.savefig('/Users/vn552f7/Ajit/A-codes/GitFame/plot.png')

plt.show()

for local_repo_path in local_paths:
    shutil.rmtree(local_repo_path)

