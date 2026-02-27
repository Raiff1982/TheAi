# ModelLab CLI

## Prerequisites

Make sure Python and pip are available in your system's environment PATH.

## Recommendation

It is recommended to use the Command Line (cmd) instead of PowerShell to install ModelLab CLI. PowerShell may cause issues with Python environment paths or command registration, which can result in the `modellab` command being unavailable or unrecognized.

## Installation

1. Open a command line terminal
2. Navigate to the current directory:
```bash
cd <path-to-this-directory>
```
3. Using pipx to Install the package:
```bash
python -m pip install pipx
python -m pipx install .
```
- To uninstall the ModelLab CLI, run:
```bash
python -m pipx uninstall modellab
```

## Usage

After installation, you can use the `modellab` command from anywhere. The command is installed in your system Python's scripts directory, so you don't need to keep the installation folder.

### Command Usage Notes

- For commands like `createworkspace` that do **not** require a workspace path, you can run them from any directory.
- For commands like addmodel that do require a workspace path, you can either cd to the root directory of the target workspace before running the command, or add --path <workspace-path> to specify the workspace directly.
