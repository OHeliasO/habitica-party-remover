import requests
from datetime import datetime, timedelta, timezone
from config import API_USER_ID, API_TOKEN, API_GROUP_ID, API_CLIENT

GROUP_URL = f"https://habitica.com/api/v4/groups/{API_GROUP_ID}"
GROUP_MEMBERS_URL = f"{GROUP_URL}/members?includeAllPublicFields=true"
REMOVE_MEMBER_URL = f"https://habitica.com/api/v4/groups/{API_GROUP_ID}/removeMember"

headers = {
    "x-api-user": API_USER_ID,
    "x-api-key": API_TOKEN,
    "x-client": API_CLIENT,
    "Content-Type": "application/json"
}

# Settings
INACTIVITY_LIMIT = timedelta(days=14)
LOG_FILE = "removed_members.log"


def fetch_group_info():
    resp = requests.get(GROUP_URL, headers=headers)
    resp.raise_for_status()
    return resp.json().get("data", {})

def fetch_group_members():
    """Fetch all members of the group."""
    resp = requests.get(GROUP_MEMBERS_URL, headers=headers)
    resp.raise_for_status()
    return resp.json().get("data", [])


def remove_member(memberId, username=None):
    """Remove a member from the group."""
    url = f"{REMOVE_MEMBER_URL}/{memberId}"

    body = {"message": f"You have been removed from the party due to inactivity ({INACTIVITY_LIMIT.days} days). If you believe this is in error, please contact an OHeliasO."}
    print("Message:", body)
    # resp = requests.post(url, headers=headers, json=body)
    # if resp.ok:
    #     msg = f"🗑️ Removed {username or user_id} ({user_id}) due to inactivity."
    #     print(msg)
    #     log_removal(msg)
    # else:
    #     print(f"❌ Failed to remove {username or user_id} ({user_id}): {resp.status_code} - {resp.text}")


def check_and_remove_inactive():
    group_info = fetch_group_info()
    leader_id = group_info.get("leader").get("id")

    members = fetch_group_members()
    now = datetime.now(timezone.utc)

    print(f"Checking {len(members)} party members...")

    for m in members:
        uid = m.get("_id")
        username = m.get("auth", {}).get("local", {}).get("username", uid)

        # 🚫 Skip the group leader
        if uid == leader_id:
            print(f"👑 Skipping {username} ({uid}), group leader.")
            continue

        last_login_str = m.get("auth", {}).get("timestamps", {}).get("loggedin")
        if not last_login_str:
            print(f"⚠️ {username} ({uid}) has no login record. Skipping.")
            continue

        try:
            last_login = datetime.fromisoformat(last_login_str.replace("Z", "+00:00"))
        except Exception:
            print(f"⚠️ Could not parse last login for {username} ({uid}): {last_login_str}")
            continue

        inactive_time = now - last_login
        if inactive_time > INACTIVITY_LIMIT:
            print(f"🚪 {username} inactive for {inactive_time.days} days.")
            remove_member(uid, username)
        else:
            print(f"✅ {username} active ({inactive_time.days} days since last login).")

def log_removal(message):
    """Log removals to a file with timestamp."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.utcnow().isoformat()}] {message}\n")


def main_loop():
    try:
        check_and_remove_inactive()
    except Exception as e:
        print(f"⚠️ Error: {e}")


if __name__ == "__main__":
    main_loop()
