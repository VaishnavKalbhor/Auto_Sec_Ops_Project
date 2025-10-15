# Security Findings

This document records security issues found during development of AutoSecureOps
and how they were addressed. It follows the same pattern a real DevSecOps
pipeline would use: a scanner flags something, the finding is triaged, and the
fix (and reasoning) is documented.

## Finding 1: Shell Injection Risk (SAST — Semgrep)

**Location:** `tests/security/insecure_demo.py` (intentional demo file, not
production code)

**Detected by:** Semgrep (`p/security-audit`, `p/python` rulesets), also
flagged by CodeQL's python security queries.

### Risk

`unsafe_ping()` builds a shell command by concatenating an untrusted `host`
string and executes it with `subprocess.call(..., shell=True)`. If `host`
came from user input (e.g. a vehicle ID or API parameter), an attacker could
inject additional shell commands — for example a host value like
`8.8.8.8; rm -rf /` would run a second, attacker-controlled command.

### Fix

Replaced the shell string with an argument list and removed `shell=True`
(`safer_ping()`). Passing arguments as a list means the OS executes `ping`
directly with fixed arguments — there is no shell to interpret injected
metacharacters.

### Learning

This demonstrated how SAST tools catch insecure coding patterns (like
`shell=True` + string concatenation) before the code ever reaches a running
service, which is exactly the kind of automotive-relevant risk (an
attacker-influenced diagnostic string executing arbitrary commands on a
backend host) that a real DevSecOps gate exists to catch early.
