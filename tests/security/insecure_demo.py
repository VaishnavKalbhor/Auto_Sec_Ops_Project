# This file is INTENTIONALLY insecure. It exists to demonstrate that the
# SAST stage (Semgrep) in .github/workflows/security.yml actually catches
# real issues, and to document the fix in docs/security-findings.md.
#
# Do not copy this pattern into production code.
import subprocess


def unsafe_ping(host: str):
    """Vulnerable: shell=True with string concatenation allows shell injection
    if `host` is attacker-controlled, e.g. host = "8.8.8.8; rm -rf /"."""
    return subprocess.call("ping -c 1 " + host, shell=True)


def safer_ping(host: str):
    """Fixed: arguments passed as a list, no shell interpretation."""
    return subprocess.call(["ping", "-c", "1", host])
