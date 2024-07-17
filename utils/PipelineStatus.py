""" The Actions Pipeline Status Check Script
###USAGE###
 1. Retrieve all available Pipeline Statuses
 RUN > python3 PipelineStatus.py
 2. Retrieve specific Pipeline Status
 RUN > python3 PipelineStatus.py <Pipeline Name>
 Example: 
 RUN > python3 PipelineStatus.py fleet
 """
import requests
from datetime import datetime
import logging
import argparse
import os

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    raise ValueError("GitHub token not set. Please set the GITHUB_TOKEN environment variable.")

REPOS = {
    'factory': 'IndustryFusion/FactoryManager5.0',
    'fleet': 'IndustryFusion/FleetManager5.0',
    'icid': 'IndustryFusion/icidservice-poc',
    'ifricplatform': 'IndustryFusion/IfricPlatform',
    'ifricregservice': 'IndustryFusion/IfricRegistryService',
    'dppcreator': 'IndustryFusion/ProductPassCreator',
    'dppviewer': 'IndustryFusion/ProductPassViewer'
}

def get_latest_workflow_status(repo):
    try:
        url = f'https://api.github.com/repos/{repo}/actions/runs'
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        runs = response.json().get('workflow_runs', [])
        if not runs:
            return 'No workflow runs found'
        
        latest_run = runs[0]
        status = latest_run['status']
        conclusion = latest_run['conclusion']
        workflow_name = latest_run['name']
        run_timestamp = latest_run['created_at']
        actor = latest_run['actor']['login']
        event = latest_run['event']
      
        triggered_by = "scheduled" if event == "schedule" else actor

        return {
            'status': status,
            'conclusion': conclusion,
            'workflow_name': workflow_name,
            'run_timestamp': run_timestamp,
            'triggered_by': triggered_by
        }
              
    except requests.RequestException as e:
        logging.error(f"Error fetching workflow status for {repo}: {e}")
        return f'Error fetching workflow status: {e}'

def main(repo_name=None):
    if repo_name:
        repo = REPOS.get(repo_name)
        if not repo:
            print(f"Repository {repo_name} not found in the mapping.")
            return
        
        result = get_latest_workflow_status(repo)
        if isinstance(result, dict):
            run_timestamp = datetime.strptime(result['run_timestamp'], "%Y-%m-%dT%H:%M:%SZ")
            formatted_time = run_timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Repo: {repo}\n  Workflow: {result['workflow_name']}\n  Status: {result['status']}\n  Conclusion: {result['conclusion']}\n  Timestamp: {formatted_time}\n  Triggered By: {result['triggered_by']}\n")
        else:
            print(f"Repo: {repo} - {result}")
    else:
        for repo in REPOS.values():
            result = get_latest_workflow_status(repo)
            if isinstance(result, dict):
                run_timestamp = datetime.strptime(result['run_timestamp'], "%Y-%m-%dT%H:%M:%SZ")
                formatted_time = run_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                print(f"Repo: {repo}\n  Workflow: {result['workflow_name']}\n  Status: {result['status']}\n  Conclusion: {result['conclusion']}\n  Timestamp: {formatted_time}\n")
            else:
                print(f"Repo: {repo} - {result}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch GitHub Actions workflow status.')
    parser.add_argument('repo', nargs='?', type=str, help='Name of the repository to fetch the result for.')
    args = parser.parse_args()

    main(args.repo)
