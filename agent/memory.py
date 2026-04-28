
from collections import defaultdict, deque

memory_store = defaultdict(lambda: deque(maxlen=5))

def add_message(user_id, role, content):
    memory_store[user_id].append({"role": role, "content": content})

def get_history(user_id):
    return list(memory_store[user_id])