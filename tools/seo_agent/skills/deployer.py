
import os
import subprocess
import sys

def deploy_to_git(file_path: str, commit_message: str) -> bool:
    """
    Commits and pushes the generated file to the git repository.
    """
    try:
        # Get directory of the file
        cwd = os.path.dirname(file_path)
        # Actually proper CWD should be the repo root
        repo_root = os.path.abspath(os.path.join(cwd, "../../..")) # Adjust based on depth
        
        print(f"Deploying from {repo_root}...")
        
        subprocess.run(["git", "add", file_path], cwd=repo_root, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_root, check=True)
        # subprocess.run(["git", "push"], cwd=repo_root, check=True) # Commented out for safety in development
        print("Git commit successful. Push skipped for safety.", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    pass
