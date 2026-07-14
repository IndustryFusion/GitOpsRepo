import os
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import argparse

def load_kube_config(kubeconfig_path=None):
    # Load the kubeconfig file from the specified path or default location
    if kubeconfig_path:
        config.load_kube_config(config_file=kubeconfig_path)
    else:
        config.load_kube_config()

def get_namespace_of_deployment(deployment_name):
    # Initialize the API client
    apps_v1 = client.AppsV1Api()
    
    try:
        # List all deployments across all namespaces
        deployments = apps_v1.list_deployment_for_all_namespaces()
        
        # Search for the deployment by name
        for deployment in deployments.items:
            if deployment.metadata.name == deployment_name:
                return deployment.metadata.namespace
        
        raise ValueError(f"Deployment '{deployment_name}' not found in any namespace.")
    
    except ApiException as e:
        print(f"Exception when calling AppsV1Api->list_deployment_for_all_namespaces: {e}")
        raise

def get_env_vars_from_deployment(namespace, deployment_name):
    # Initialize the API client
    apps_v1 = client.AppsV1Api()

    try:
        # Get the specified deployment
        deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)
        
        # Extract the environment variables from the deployment spec
        env_vars = {}
        for container in deployment.spec.template.spec.containers:
            if container.env:
                for env_var in container.env:
                    env_vars[env_var.name] = env_var.value

        return env_vars
    
    except ApiException as e:
        print(f"Exception when calling AppsV1Api->read_namespaced_deployment: {e}")
        return {}

def parse_env_file(env_file_path):
    env_vars = {}
    with open(env_file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith('#'):
                name, value = line.strip().split('=', 1)
                env_vars[name] = value
    return env_vars

def compare_env_vars(deployment_env_vars, file_env_vars):
    mismatch_found = False
    print("\nComparison of environment variables:\n")
    for key, value in file_env_vars.items():
        if key in deployment_env_vars:
            if deployment_env_vars[key] != value:
                print(f"- Mismatch for variable '{key}':")
                print(f"  - Deployment value: '{deployment_env_vars[key]}'")
                print(f"  - File value: '{value}'")
                mismatch_found = True
        else:
            print(f"- Variable '{key}' is missing from deployment environment variables")
            mismatch_found = True
    
    if not mismatch_found:
        print("All environment variables match!")

def display_env_vars_all_deployments():
    # Initialize the API client
    apps_v1 = client.AppsV1Api()

    try:
        # List all deployments across all namespaces
        deployments = apps_v1.list_deployment_for_all_namespaces()

        if not deployments.items:
            print("No deployments found.")
            return
        
        print("\nEnvironment variables for all deployments across all namespaces:\n")
        for deployment in deployments.items:
            namespace = deployment.metadata.namespace
            deployment_name = deployment.metadata.name
            env_vars = get_env_vars_from_deployment(namespace, deployment_name)
            
            print(f"Deployment: {deployment_name} (Namespace: {namespace})")
            if env_vars:
                for name, value in env_vars.items():
                    print(f"  - {name}: {value}")
            else:
                print("  No environment variables found.")
            print("-" * 40)

    except ApiException as e:
        print(f"Exception when calling AppsV1Api->list_deployment_for_all_namespaces: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare deployment environment variables with a .env file.')
    parser.add_argument('-e', '--env', type=str, help='Path to .env file', default=None)
    parser.add_argument('--all', action='store_true', help='Display environment variables for all deployments across all namespaces')

    args = parser.parse_args()
    
    kubeconfig_path = input("Enter the path to kubeconfig file: ")
    load_kube_config(kubeconfig_path)
    
    if args.all:
        display_env_vars_all_deployments()
    else:
        deployment_name = input("Enter the deployment name: ")
        
        try:
            namespace = get_namespace_of_deployment(deployment_name)
            deployment_env_vars = get_env_vars_from_deployment(namespace, deployment_name)
            
            if deployment_env_vars:
                if args.env:
                    file_env_vars = parse_env_file(args.env)
                    compare_env_vars(deployment_env_vars, file_env_vars)
                else:
                    print(f"\nEnvironment variables in deployment '{deployment_name}' in namespace '{namespace}':\n")
                    for name, value in deployment_env_vars.items():
                        print(f"- {name}: {value}")
            else:
                print(f"No environment variables found in deployment '{deployment_name}' in namespace '{namespace}'.")
        
        except ValueError as e:
            print(e)

