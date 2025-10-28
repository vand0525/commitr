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
    result = subprocess.run(
        ["git", "diff", "--name-only", "-z"],
        capture_output=True,
        text=False,
        check=True,
    )
    items = result.stdout.split(b"\x00")
    return [i.decode() for i in items if i]


def stage(paths: list[str]):
    subprocess.run(["git", "add", *paths])


def unstage_all():
    subprocess.run(["git", "reset"], check=True, stdout=subprocess.DEVNULL,)


def do_commit(message: str):
    subprocess.run(["git", "commit", "-m", message])
