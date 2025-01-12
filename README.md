# Google Cloud Function Samples

Google Cloud Function Samples is a collection of sample Google Cloud Functions showcasing different triggers like Http, Cloud Storage, and Pub/Sub. The project leverages several common patterns for configuring Cloud Functions, including local .env files, JSON/YAML configuration files, and centralised configuration management services like Google Storage, Google Secret

## Key Features

1. Multiple Trigger Types

   - HTTP Trigger – Demonstrates how to handle HTTP requests and responses.
   - Storage Trigger – Respond to events from Google Cloud Storage, such as file creation or deletion.
   - Pub/Sub Trigger – Process messages from Google Pub/Sub topics.

2. Centralized Configuration Management

   - Load and inject environment variables from a local `.env`, `config.json` or `config.yaml` file.
   - Load and inject environment variables from `Google Storage`, `Google Secret Manager` so that settings of application will be centralised

3. Dependency Management and Testing
   - UV is used for efficient dependency management and packaging.
   - Pytest provides a simple and flexible framework for writing and running tests, ensuring reliability and consistency of your Cloud Functions.

> Note: This project applies only to Cloud Run functions—formerly Cloud Functions (2nd gen). Find more details in [Cloud Run Function](https://cloud.google.com/functions/docs/create-deploy-http-python)

---

## Prerequisites

### Required Programs

Before setting up this project, ensure the following programs are installed:

### Xcode CLI

To use homebrew to install Python packages, you need a compiler

```bash
xcode-select --install
```

### Homebrew

Homebrew is a package manager for macOS, used to install other tools like `asdf` and `jq`.

Installation:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### jq

jq is a lightweight and flexible command-line JSON processor, used for automating JSON file generation.

Installation:

```bash
brew install jq
```

### asdf

asdf is a version manager for multiple runtimes like Python, Node.js, Java, Go, etc.

Installation:

```bash
brew install asdf
```

- Add asdf to your shell by adding the following lines to your shell configuration (~/.zshrc or ~/.bashrc):

  For `~/.zshrc`:

  ```bash
  echo '. $(brew --prefix asdf)/libexec/asdf.sh' >> ~/.zshrc
  ```

  For `~/.bashrc`:

  ```bash
  echo '. $(brew --prefix asdf)/libexec/asdf.sh' >> ~/.bashrc
  ```

- After adding the line, reload the shell configuration file for the changes to take effect:

  For `~/.zshrc`:

  ```bash
  source ~/.zshrc
  ```

  For `~/.bashrc`:

  ```bash
  source ~/.bashrc
  ```

### python

- Install the Python plugin and Python 3.12.7 using asdf:

  ```bash
  asdf plugin add python
  asdf install python 3.12.7
  asdf global python 3.12.7
  ```

- Verify the installation:

  ```bash
  python --version
  ```

### UV

- UV is a fast Python package installer and resolver, written in Rust. Install it using pip:

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Google Cloud CLI

- Install Google Cloud CLI running the following commands. Find more details in [gcloud CLI](https://cloud.google.com/sdk/docs/install)

  ```bash
  curl https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-darwin-arm.tar.gz -o GCLOUDCLI.tar.gz

  tar -xvf GCLOUDCLI.tar.gz

  ./google-cloud-sdk/install.sh
  ```

- To initialize the gcloud CLI, run gcloud init:

  ```bash
  ./google-cloud-sdk/bin/gcloud init
  ```

- Verify the installation:

  ```bash
  gcloud --version
  ```

- Update and install gcloud components with the following command:

  ```bash
  gcloud components update
  ```

### Automating VS Code Extensions Setup

- Install VSCode Default Extensions programatically.

  ```bash
  cat .vscode/extensions.json | jq -r '.recommendations[]' | xargs -n 1 code --install-extension
  ```

## Setting Up the Project

1. Clone the Repository:

   ```bash
   git clone <repository-url>
   cd google_cloud_function_samples
   ```

1. Create and Activate Virtual Environment:

   ```bash
   uv venv
   source .venv/bin/activate  # For Linux/Mac
   ```

1. Install Dependencies:

   ```bash
   # Install all dependencies including dev dependencies
   uv sync

   # Install/Reinstall pre-commit hooks
   rm -rf .git/hooks/*  # Remove all git hooks
   uv run pre-commit clean # Clean any existing pre-commit
   uv run pre-commit uninstall # Uninstall any remaining hooks
   uv run pre-commit install --overwrite  # Install hooks fresh
   ```

   or

   ```bash
   uv run setup
   ```

1. Run Tests: Run the tests using pytest:

   ```bash
   uv run pytest
   ```

1. Sync after team members update dependencies

   ```bash
   git pull # Get latest changes
   uv sync # Update environment from uv.lock
   ```

## Running Pre-commit hooks

- This command executes all the pre-commit hooks defined in your .pre-commit-config.yaml file on all files in your repository, regardless of whether they have been modified or staged for commit. It ensures that your entire codebase adheres to the standards and checks specified by your pre-commit hooks.

  ```bash
  # Run all pre-commit hooks
  uv run pre-commit run --all-files

  # OR

  # Run with verbose output
  uv run pre-commit run --all-files --verbose
  ```

- Additional Command Options

  ```bash
  # Run specific hooks
  uv run pre-commit run black --all-files
  uv run pre-commit run pretty-format-json --all-files
  uv run pre-commit run pretty-format-json --files config.json
  ```
