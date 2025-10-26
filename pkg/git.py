import subprocess

def get_diff():
    result = subprocess.run(
        ["git", "diff"], 
        capture_output=True,
        text=True,
        check=False
    )
    return result.stdout