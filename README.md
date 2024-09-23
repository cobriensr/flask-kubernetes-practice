# Flask Kubernetes Practice Application

A small Flask app to practice Kubernetes deployments

## Vulnerabilities

### CVE-2018-20225 (pip vulnerability)

Our project uses Poetry for dependency management, which significantly mitigates the risk associated with CVE-2018-20225, a high-severity vulnerability in pip (all versions).

**Nature of the Vulnerability:**
This vulnerability could potentially allow an attacker to trick pip into installing a malicious package when using the `--extra-index-url` option.

**Our Mitigation:**

1. We use Poetry as our primary package manager, which provides enhanced security features and dependency resolution.
2. Poetry's lockfile system and improved package management significantly reduce the risk of this vulnerability.
3. We avoid using additional package sources unless absolutely necessary, and when used, ensure they are trusted and use HTTPS.

**Note to Reviewers:**
While vulnerability scanners may still flag this issue due to pip's presence in the Python environment, our use of Poetry as the primary package manager substantially reduces the actual risk. We continue to monitor for updates and best practices in Python package management security.
