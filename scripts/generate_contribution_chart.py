# generate_contribution_chart.py

import os
import subprocess
import json
from collections import defaultdict
import matplotlib.pyplot as plt

def generate_contribution_chart():
    # Constants
    BAR_COLOR = 'skyblue'

    # GitHub repository info
    repo = "UW-MLGEO/MLGEO2024_Geldingadalir"

    # Step 1: Get all branches using GitHub CLI
    branches_cmd = f"gh api -H 'Accept: application/vnd.github.v3+json' /repos/{repo}/branches"
    branches_result = subprocess.run(branches_cmd, shell=True, capture_output=True, text=True)

    if branches_result.returncode != 0:
        print(f"Error fetching branches: {branches_result.stderr}")
        exit(1)

    branches = json.loads(branches_result.stdout)
    print(f"Branches: {branches}")

    contributions = defaultdict(int)

    # Step 2: Loop through each branch and count commits per contributor
    for branch in branches:
        branch_name = branch["name"]
        print(f"Processing branch: {branch_name}")
        commits_cmd = f"gh api -H 'Accept: application/vnd.github.v3+json' /repos/{repo}/commits?sha={branch_name}"
        commits_result = subprocess.run(commits_cmd, shell=True, capture_output=True, text=True)

        if commits_result.returncode != 0:
            print(f"Error fetching commits for branch {branch_name}: {commits_result.stderr}")
            continue

        commits = json.loads(commits_result.stdout)
        for commit in commits:
            author = commit.get("commit", {}).get("author", {}).get("name")
            if author:
                contributions[author] += 1

    print(f"Contributions: {contributions}")

    # Step 3: Prepare data for the chart
    names = list(contributions.keys())
    commit_counts = list(contributions.values())

    print(f"Names: {names}")
    print(f"Commit counts: {commit_counts}")
    
    # save the plot to images folder
    images_dir = "images"
    os.makedirs(images_dir, exist_ok=True)

    # Step 4: Create a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(names, commit_counts, color=BAR_COLOR)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Total Number of Commits (All Branches)")
    plt.title("Commits per Contributor Across All Branches")
    plt.gca().set_xlim(left=-0.5)  # Adjust x-axis to start at -0.5 to ensure it starts at 0
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))  # Ensure y-axis has integer ticks
    plt.savefig(os.path.join(images_dir, "contribution_chart.png"))
    plt.show()

    return contributions