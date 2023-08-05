statuses = {
    "Alice": "online",
    "Bob": "offline",
    "Eve": "online",
}


def online_count(s: dict):
    count = 0
    for value in statuses.values():
        if value == "online":
            count = count + 1
    return count


get_count = online_count(statuses)
print(get_count)
