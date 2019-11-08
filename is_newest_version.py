import json
import os
import sys
import urllib.request
from distutils.version import StrictVersion


from elb_log_tools import __version__

PACKAGE_NAME = "elb-log-tools"


def make_versions_request(package_name):
    repo_url = os.environ.get("PUBLIC_TWINE_REPOSITORY_URL", "https://pypi.org/simple")
    url = "{}/{}/json".format(repo_url, package_name)
    print(f"{url=}")
    username = os.environ.get("TWINE_USERNAME")
    password = os.environ.get("TWINE_PASSWORD")
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, repo_url, username, password)
    handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
    opener = urllib.request.build_opener(handler)

    with opener.open(url) as resp:
        content = resp.read()
    return json.loads(content)


def versions(package_name):
    try:
        response = make_versions_request(package_name)
    except urllib.error.HTTPError:
        return []
    # If the package is not found, an HTML page is returned
    if response.headers["content-type"] != "application/json":
        return []
    data = response.json()
    versions = list(data["releases"].keys())
    versions.sort(key=StrictVersion)
    return versions


if __name__ == "__main__":
    print(make_versions_request)
    CURRENT_VERSION = __version__  # noqa
    existing_versions = versions(PACKAGE_NAME)
    LATEST_PUBLISHED_VERSION = existing_versions[-1] if existing_versions else None
    if not LATEST_PUBLISHED_VERSION:
        print("Package is not yet published")
        sys.exit(0)

    if StrictVersion(CURRENT_VERSION) > StrictVersion(LATEST_PUBLISHED_VERSION):
        print("Version would be the newest version")
        sys.exit(0)
    print("Version would not be the newest version")
    sys.exit(1)
