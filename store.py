import os
import json
from snapshot import MarketSnapshot


def create_store(path: str):
    if os.path.isfile(path):
        return

    with open(path, 'w') as f:
        f.write('[]')


def read(path) -> str:
    with open(path) as f:
        return f.read()


def save(path: str, data: str):
    with open(path, 'w') as f:
        f.write(data)

# todo: should be renamed


class Store:
    path: str

    def __init__(self, path: str) -> None:
        self.path = path
        create_store(path)

    def create_store(self):
        if os.path.isfile(self.path):
            return

        with open(self.path, 'w') as f:
            f.write('[]')

    def load(self) -> list[MarketSnapshot]:
        snapshots: list[dict] = json.loads(read(self.path))
        return [MarketSnapshot.from_dict(snapshot) for snapshot in snapshots]

    def save(self, snapshots: list[MarketSnapshot]) -> 'Store':
        with open(self.path, 'w') as f:
            json.dump([snapshot.as_dict() for snapshot in snapshots], f)

        return self

    def append(self, snapshot: MarketSnapshot) -> 'Store':
        snapshots = self.load()
        snapshots.append(snapshot)
        self.save(snapshots)
        return self


class UserStore:
    path: str

    def __init__(self, path: str) -> None:
        self.path = path
        create_store(path)

    def load(self) -> list[int]:
        users: list[int] = json.loads(read(self.path))
        return users

    def save(self, users: list[int]) -> 'UserStore':
        save(self.path, json.dumps(users))
        return self

    def add(self, user: int) -> 'UserStore':
        users = self.load()
        users.append(user)
        self.save(users)

        return self

    def add_unique(self, user: int) -> 'UserStore':
        users = self.load()
        if user not in users:
            users.append(user)
            self.save(users)
        return self
