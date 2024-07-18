Here's the updated README to reflect the changes in the script, including the new functionality to display environment variables for all deployments across all namespaces:

---

# Kubernetes Deployment Environment Variables Checker

This script compares the environment variables of a Kubernetes deployment with those specified in a `.env` file, or displays the environment variables for all deployments across all namespaces.

## Usage

### Prerequisites

- Ensure you have a valid kubeconfig file to access your Kubernetes cluster. Ping @jragunanthan for cluster config files.
- Install the necessary Python packages:
  ```sh
  pip install kubernetes
  ```

### Running the Script

1. **Retrieve environment variables from a deployment:**

   ```sh
   python3 fetch_k3s_env_vars.py
   ```

   You will be prompted to enter the path to the kubeconfig file and the deployment name.

2. **Compare deployment environment variables with a `.env` file:**

   ```sh
   python3 fetch_k3s_env_vars.py -e path/to/your/envfile.env
   ```

   You will be prompted to enter the path to the kubeconfig file and the deployment name.

3. **Display environment variables for all deployments across all namespaces:**

   ```sh
   python3 fetch_k3s_env_vars.py --all
   ```

   You will be prompted to enter the path to the kubeconfig file.

### Examples

**Compare deployment environment variables with a `.env` file:**

```sh
python3 fetch_k3s_env_vars.py -e example.env
Enter the path to kubeconfig file: /mnt/c/Users/Ragunanthan/Downloads/IFF-DEV-DPP-IFRIC.yaml
Enter the deployment name: passport-creator-application-service
```

**Display environment variables for all deployments:**

```sh
python3 fetch_k3s_env_vars.py --all
Enter the path to kubeconfig file: /mnt/c/Users/Ragunanthan/Downloads/IFF-DEV-DPP-IFRIC.yaml
```

When prompted, enter the path to your kubeconfig file. The script will either display the comparison results or the environment variables for all deployments based on the chosen option.

---
