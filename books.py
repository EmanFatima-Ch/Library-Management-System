members = []


def register_member(member_id, name):
    """Register a new member. Returns True if added, False if the ID already exists."""
    for member in members:
        if member["id"] == member_id:
            print("A member with this ID already exists.")
            return False

    members.append({"id": member_id, "name": name})
    print(f"Member '{name}' registered.")
    return True


def view_members():
    """Print all registered members."""
    if not members:
        print("No members registered.")
        return

    print("\n--- Registered Members ---")
    for member in members:
        print(f"ID: {member['id']} | Name: {member['name']}")
