import re


def get_users(passwd: str) -> dict:
    """Split password output by newline,
      extract user and name (1st and 5th columns),
      strip trailing commas from name,
      replace multiple commas in name with a single space
      return dict of keys = user, values = name.
    """
    users = dict()
    for line in passwd.split('\n'):
        if line.strip():
            columns = line.split(':')
            (id, name) = (columns[0], columns[4])
            name = re.sub(',+', ' ', name).strip()
            name = name if name else 'unknown'
            users[id] = name
    return users
