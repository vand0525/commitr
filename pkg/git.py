import subprocess

def get_unstaged_diff():
    result = subprocess.run(
        ["git", "diff"], capture_output=True, text=True, check=False
    )
    return result.stdout


def get_staged_diff():
    result = subprocess.run(
        ["git", "diff", "--cached"], capture_output=True, text=True, check=False
    )
    return result.stdout


def get_unstaged_paths():
    tracked_result = subprocess.run(
        ["git", "diff", "--name-only", "-z"],
        capture_output=True,
        text=False,
        check=True,
    )
    tracked = [p.decode() for p in tracked_result.stdout.split(b"\x00") if p]

    untracked_result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        capture_output=True,
        text=False,
        check=True,
    )
    untracked = [p.decode() for p in untracked_result.stdout.split(b"\x00") if p]
    return list(dict.fromkeys(tracked + untracked))

def stage(paths: list[str]):
    subprocess.run(["git", "add", *paths])


def unstage_all():
    subprocess.run(["git", "reset"], check=True, stdout=subprocess.DEVNULL,)


def do_commit(message: str):
    subprocess.run(["git", "commit", "-m", message])
