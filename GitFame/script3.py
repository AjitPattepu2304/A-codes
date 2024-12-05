import subprocess

# Run the first Python script
subprocess.call(["python3", "git_clone_or_pull.Git-Fame.py"])

# Once the first script finishes, run the second script
subprocess.call(["python3", "fame-process.Git-Fame.py"])