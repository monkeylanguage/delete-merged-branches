import argparse
import subprocess
from typing import List, Tuple, Dict
import os
import sys


def init_args() -> Dict:

    parser = argparse.ArgumentParser(
        description="""Delete old branches, which are already merged""", formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-d",
        "--delete",
        help="Delete argument. Without this, its just a dry run for safety reasons",
        action="store_true",
    )
    return vars(parser.parse_args())


def main():
    args = init_args()
    git_list_args = ["git", "branch", "-r", "--merged", "master"]

    git_delete_args = ["git", "push", "origin", "--delete"]
    delete_branches = True if args.get("delete") else False

    git_list = subprocess.Popen(git_list_args, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
    old_branches = [branch.replace("origin/", "").strip() for branch in git_list.split("\n") if branch != ""]

    for old_branch in old_branches:
        if delete_branches:
            # running git push <remote_name> --delete <branch_name>
            subprocess.Popen(git_delete_args + [old_branch], stdout=subprocess.PIPE).stdout.read().decode("utf-8")
            print(f"{old_branch} - deleted")
        else:
            print(f"{old_branch} - could be deleted")

    print("Total:" + str(len(old_branches)))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye ;-)")
        sys.exit(0)
