---

# GitHub Actions Pipeline Status Check Script

## Usage

### Prerequisites

- Ensure Python 3.x is installed.
- Install necessary Python packages:
  ```sh
  pip install requests
  ```

### Running the Script

1. **Retrieve all available Pipeline Statuses:**

   ```sh
   python3 PipelineStatus.py
   ```

2. **Retrieve specific Pipeline Status:**

   ```sh
   python3 PipelineStatus.py <Pipeline Name>
   ```

   Example:
   ```sh
   python3 PipelineStatus.py fleet
   ```

### How to Create a GitHub Token

1. Go to [GitHub Token Settings](https://github.com/settings/tokens).
2. Click "Generate new token".
3. Select the appropriate scopes (e.g., `repo`, `workflow`).
4. Click "Generate token" and save it securely.

### Exporting GitHub Token

Before running the script, export your GitHub token in the terminal:

```sh
export GITHUB_TOKEN='your_generated_token_here'
```

Replace `'your_generated_token_here'` with your actual GitHub token.

