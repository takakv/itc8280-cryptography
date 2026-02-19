import os
from urllib.parse import quote_plus

import requests
from dotenv import load_dotenv
from requests import JSONDecodeError

load_dotenv()

GITLAB_URL = os.environ.get("GITLAB_URL", "https://gitlab.cs.taltech.ee").rstrip("/")
TOKEN = os.environ["GITLAB_TOKEN"]
GROUP_ID = os.environ["GROUP_ID"]

if not TOKEN or not GROUP_ID:
    raise ValueError("GITLAB_TOKEN and GROUP_ID must be set in .env")

HEADERS = {
    "PRIVATE-TOKEN": TOKEN,
    "Content-Type": "application/json"
}

ACCESS_LEVELS = {
    0: "No access",
    5: "Minimal access",
    10: "Guest",
    20: "Reporter",
    30: "Developer",
    40: "Maintainer",
    50: "Owner"
}

DEVELOPER_ACCESS = 30
MAINTAINER_ACCESS = 40
PROTECTED_NAMES = {"Group management", "Taaniel Kraavi"}
PROTECTED_BRANCH = "main"


def list_group_projects(group_id):
    projects = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITLAB_URL}/api/v4/groups/{group_id}/projects"
        params = {"page": page, "per_page": per_page, "with_shared": True}

        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()

        if not data:
            break

        projects.extend(data)

        if len(data) < per_page:
            break

        page += 1

    return projects


def list_project_members(project_id):
    members = []
    page = 1
    per_page = 100

    while True:
        url = f"{GITLAB_URL}/api/v4/projects/{project_id}/members/all"
        params = {"page": page, "per_page": per_page}

        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()

        if not data:
            break

        members.extend(data)

        if len(data) < per_page:
            break

        page += 1

    return members


def update_project(project_id):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}"
    payload = {
        "merge_method": "rebase_merge",
        "only_allow_merge_if_pipeline_succeeds": True
    }

    r = requests.put(url, headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()


def set_member_to_developer(project_id, user_id):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/members/{user_id}"
    payload = {
        "access_level": DEVELOPER_ACCESS
    }

    r = requests.put(url, headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()


def project_has_branch(project_id, branch_name):
    branch_escaped = quote_plus(branch_name)
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/branches/{branch_escaped}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return True
    if r.status_code == 404:
        return False
    r.raise_for_status()
    return False


def branch_is_protected(project_id, branch_name):
    branch_escaped = quote_plus(branch_name)
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/protected_branches/{branch_escaped}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return True, r.json()
    if r.status_code == 404:
        return False, None
    r.raise_for_status()
    return False, None


def protect_branch(project_id, branch_name, push_access_level=DEVELOPER_ACCESS, merge_access_level=MAINTAINER_ACCESS):
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/protected_branches"
    payload = {
        "name": branch_name,
        "push_access_level": push_access_level,
        "merge_access_level": merge_access_level
    }

    r = requests.post(url, headers=HEADERS, json=payload)
    if r.status_code in (201, 200):
        return r.json()
    else:
        try:
            body = r.json()
        except JSONDecodeError:
            body = r.text

        print(body)
        r.raise_for_status()
        return None


def main():
    projects = list_group_projects(GROUP_ID)
    print(f"Found {len(projects)} projects")

    for p in projects:
        pid = p["id"]
        name = p["path_with_namespace"]

        print(f"Processing project: {name}")
        try:
            members = list_project_members(pid)
        except Exception as e:
            print(f"  Failed to fetch members: {e}\n")
            continue

        for m in members:
            member_name = m.get("name")
            user_id = m.get("id")
            current_access = m.get("access_level")

            if member_name in PROTECTED_NAMES:
                continue

            if current_access == DEVELOPER_ACCESS:
                continue

            try:
                set_member_to_developer(pid, user_id)
                print(f"  Updated {member_name} to Developer")
            except Exception as e:
                print(f"  Failed to update {member_name}: {e}")

        try:
            if not project_has_branch(pid, PROTECTED_BRANCH):
                print(f"  Branch '{PROTECTED_BRANCH}' does not exist in {name}")
            else:
                protected, _ = branch_is_protected(pid, PROTECTED_BRANCH)
                if not protected:
                    try:
                        protect_branch(pid, PROTECTED_BRANCH,
                                       push_access_level=DEVELOPER_ACCESS,
                                       merge_access_level=DEVELOPER_ACCESS)
                    except Exception as e:
                        print(f"  Failed to protect branch for {name}: {e}")

        except Exception as e:
            print(f"  Failed to query {name}: {e}")

        try:
            update_project(pid)
        except Exception as e:
            print(f"  Failed to update {name}: {e}")


if __name__ == "__main__":
    main()
