import os
import json
from typing import List, Dict

class ChatStore:
    def __init__(self) -> None:
        self.file_path: str = "data/chat_history.json"
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump({}, f)

    def _load(self) -> Dict[str, Dict]:
        with open(self.file_path, "r") as f:
            return json.load(f)

    def _save(self, data: Dict[str, Dict]) -> None:
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def fetch(self, chat_id: str) -> Dict:
        return self._load().get(chat_id, {})

    def update(self, chat_id: str, messages: Dict) -> None:
        data = self._load()
        data[chat_id] = messages
        self._save(data)

    def delete(self, chat_id: str) -> None:
        data = self._load()
        data[chat_id] = {}
        self._save(data)

if __name__ == "__main__":
    store = ChatStore()
    store.update("user1", {"messages": ["hi"], "filters": {}})
    print("Fetch user1:", store.fetch("user1"))
    store.delete("user1")
    print("Fetch after delete:", store.fetch("user1"))
    os.remove("data/chat_history.json")
