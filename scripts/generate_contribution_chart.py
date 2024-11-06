# generate_contribution_chart.py

import requests
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# GitHub repository info
repo = "UW-MLGEO/MLGEO2024_Geldingadalir"
token = os.getenv("GITHUB_TOKEN")  # Retrieve GitHub token from environment
headers = {"Authorization": f"Bearer {token}"}

# Step 1: Get all branches
branches_url = f"https://api.github.com/repos/{repo}/branches"
branches = []
page = 1
while True:
    response = requests.get(branches_url, headers=headers, params={"page": page})
    data = response.json()
    if not data:
        break
    branches.extend(data)
    page += 1

print(f"Branches: {branches}")

contributions = defaultdict(int)

# Step 2: Loop through each branch and count commits per contributor
for branch in branches:
    branch_name = branch["name"]
    print(f"Processing branch: {branch_name}")
    commits_url = f"https://api.github.com/repos/{repo}/commits"
    page = 1
    while True:
        params = {"sha": branch_name, "page": page}  # Filter commits by branch and page
        commits_response = requests.get(commits_url, headers=headers, params=params)
        commits = commits_response.json()
        if not commits:
            break
        # Tally contributions per user
        for commit in commits:
            author = commit.get("commit", {}).get("author", {}).get("name")
            if author:
                contributions[author] += 1
        page += 1

print(f"Contributions: {dict(contributions)}")

# Step 3: Prepare data for the chart
names = list(contributions.keys())
commit_counts = list(contributions.values())

print(f"Names: {names}")
print(f"Commit counts: {commit_counts}")

# Step 4: Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(names, commit_counts, color='skyblue')
plt.xlabel("Contributors")
plt.ylabel("Total Number of Commits (All Branches)")
plt.title("Commits per Contributor Across All Branches")
plt.xticks(rotation=45, ha="right")

# Save the chart as an image
plt.savefig("contribution_chart.png")
print("Chart saved as contribution_chart.png")
