import time
import os
import requests
import pandas as pd
from collections import deque

# Set the depth limit
DEPTH_LIMIT = 3

# GitHub API base URL
BASE_URL = "https://api.github.com"

# Read GitHub token from environment variable
TOKEN = os.getenv('GITHUB_TOKEN')

# Function to fetch GitHub profile data
def fetch_github_profile(username):
    url = f"{BASE_URL}/users/{username}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    handle_rate_limit(response)
    print_rate_limit(response)
    return response.json() if response.status_code == 200 else None

# Function to handle rate limit
def handle_rate_limit(response):
    if response.status_code == 403:
        reset_time = int(response.headers['X-RateLimit-Reset'])
        sleep_time = max(0, reset_time - time.time()) + 5  # Wait a few extra seconds
        print(f"Rate limit exceeded. Waiting for {sleep_time} seconds.")
        time.sleep(sleep_time)

# Function to print remaining rate limit
def print_rate_limit(response):
    limit = response.headers.get('X-RateLimit-Limit')
    remaining = response.headers.get('X-RateLimit-Remaining')
    reset = response.headers.get('X-RateLimit-Reset')
    if limit and remaining and reset:
        print(f"Rate limit - Limit: {limit}, Remaining: {remaining}, Reset: {reset}")

# Function to follow a GitHub user
def follow_user(username):
    url = f"{BASE_URL}/user/following/{username}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.put(url, headers=headers)
    handle_rate_limit(response)
    if response.status_code == 204:
        print(f"Followed user: {username}")
    else:
        print(f"Failed to follow user: {username}. Status code: {response.status_code}")

# Function to fetch a user's followers
def fetch_followers(username):
    url = f"{BASE_URL}/users/{username}/followers"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    handle_rate_limit(response)
    print_rate_limit(response)
    return response.json() if response.status_code == 200 else None

# Function to fetch a user's repositories
def fetch_repositories(username):
    url = f"{BASE_URL}/users/{username}/repos"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    handle_rate_limit(response)
    print_rate_limit(response)
    return response.json() if response.status_code == 200 else None

# Function to star a repository
def star_repository(username, repo_name):
    url = f"{BASE_URL}/user/starred/{username}/{repo_name}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.put(url, headers=headers)
    handle_rate_limit(response)
    if response.status_code == 204:
        print(f"Starred repository: {username}/{repo_name}")
    else:
        print(f"Failed to star repository: {username}/{repo_name}. Status code: {response.status_code}")

# Function to display profile data
def display_profile_data(profile_data):
    if profile_data:
        print(f"Name: {profile_data.get('name')}")
        print(f"Company: {profile_data.get('company')}")
        print(f"Location: {profile_data.get('location')}")
        print(f"Public Repos: {profile_data.get('public_repos')}")
        print(f"Followers: {profile_data.get('followers')}")
        print(f"Following: {profile_data.get('following')}")
    else:
        print("User not found.")

# Function to display repositories
def display_repositories(username):
    repos_data = fetch_repositories(username)
    if repos_data:
        repos_df = pd.DataFrame(
            repos_data, columns=["name", "html_url", "stargazers_count", "forks_count"]
        )
        print(repos_df)
    else:
        print("No repositories found or user not found.")

# Initialize queue and visited set
queue = deque([("torvalds", 0)])
visited = set()

while queue:
    current_user, current_depth = queue.popleft()
    if current_depth > DEPTH_LIMIT:
        break
    if current_user in visited:
        continue
    visited.add(current_user)
    print(f"Crawling user: {current_user}, Depth: {current_depth}")
    profile_data = fetch_github_profile(current_user)
    display_profile_data(profile_data)
    
    # Follow user if they have more than 300 followers
    if profile_data and profile_data.get('followers', 0) > 300:
        follow_user(current_user)
    
    # Display repositories after displaying profile data
    print("\nRepositories:")
    display_repositories(current_user)
    
    # Star repositories if they are popular (e.g., high star count)
    if profile_data:
        repositories = fetch_repositories(current_user)
        if repositories:
            for repo in repositories:
                if repo['stargazers_count'] > 100:  # Example threshold for popular repo
                    star_repository(current_user, repo['name'])
    
    if current_depth < DEPTH_LIMIT:
        followers = fetch_followers(current_user)
        if followers:
            for follower in followers:
                if follower["login"] not in visited:
                    queue.append((follower["login"], current_depth + 1))
    print()
