#!/usr/bin/env python3
"""
Version management script for flask-react-ssr
"""
import subprocess
import sys
import argparse


def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, shell=True, check=check, capture_output=True, text=True
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def bump_version(bump_type):
    """Bump version using bump2version."""
    print(f"Bumping {bump_type} version...")

    # Install bump2version if not available
    try:
        subprocess.run(["bump2version", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Installing bump2version...")
        run_command("pip install bump2version")

    # Bump version
    stdout, stderr = run_command(f"bump2version {bump_type}")
    print("Version bumped successfully!")

    # Get new version
    import configparser

    config = configparser.ConfigParser()
    config.read(".bumpversion.cfg")
    new_version = config["bumpversion"]["current_version"]

    print(f"New version: {new_version}")
    return new_version


def main():
    parser = argparse.ArgumentParser(description="Manage flask-react-ssr versions")
    parser.add_argument(
        "bump_type", choices=["patch", "minor", "major"], help="Type of version bump"
    )
    parser.add_argument(
        "--push", action="store_true", help="Push changes to remote repository"
    )

    args = parser.parse_args()

    new_version = bump_version(args.bump_type)

    if args.push:
        print("Pushing changes to remote...")
        run_command("git push origin main")
        run_command(f"git push origin v{new_version}")
        print("Changes pushed successfully!")
    else:
        print("Changes made locally. Use --push to push to remote repository.")
        print(f"Or run: git push origin main && git push origin v{new_version}")


if __name__ == "__main__":
    main()
