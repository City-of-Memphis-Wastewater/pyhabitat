import os
import sys

__all__ = [
    "is_likely_ci_or_non_interactive"
]

def is_likely_ci_or_non_interactive() -> bool:
    """
    Heuristic: are we probably in a CI/CD pipeline or non-interactive container?
    Returns True if we should avoid prompts (require all args instead).
    """
    # 1. Basic TTY check (fast fail if no tty)
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        return True  # definitely non-interactive

    # 2. Common CI env var fingerprints (high confidence)
    ci_markers = [
        "GITHUB_ACTIONS",     # == "true"
        "GITLAB_CI",          # == "true"
        "CIRCLECI",           # == "true"
        "TRAVIS",             # == "true"
        "JENKINS_URL",        # non-empty
        "TF_BUILD",           # Azure Pipelines
        "CI",                 # generic (many set to "true")
        "BUILD_ID",           # Jenkins, some others
        "CODEBUILD_BUILD_ID", # AWS
        "BITBUCKET_BUILD_NUMBER",
    ]

    for var in ci_markers:
        val = os.getenv(var)
        if val and val.lower() not in ("", "false", "0", "no"):
            return True

    # 3. Optional: Docker/container detection (if relevant for your tool)
    #    - File-based (classic, works in most Docker images)
    if os.path.exists("/.dockerenv"):
        return True

    #    - cgroup-based (more reliable in modern Docker / containerd / podman)
    try:
        with open("/proc/1/cgroup", "r") as f:
            if "docker" in f.read() or "kubepods" in f.read() or "containerd" in f.read():
                return True
    except Exception:
        pass  # ignore if /proc not available (e.g. non-Linux)

    # If none of the above → probably real interactive terminal
    return False

"""
# Usage in your CLI logic:
if is_likely_ci_or_non_interactive():
    # Require all required args (e.g. value must be positional)
    if value is None:
        raise typer.BadParameter("Value required in non-interactive/CI mode")
else:
    # Safe to prompt
    value = typer.prompt("Secret value", hide_input=True)
"""
