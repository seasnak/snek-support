import re

def find_user_id(user: str) -> int:
    # Returns the User ID given the user mention.
    match_user: re.Match|None = re.match(r"<@!?(\d+)>", user)
    return -1 if match_user == None else int(match_user.group(1))


