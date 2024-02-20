import os
import json
from snapshot import MarketSnapshot


class Store:
    path: str

    def __init__(self, path: str) -> None:
        self.path = path
        self.create_store()

    def create_store(self):
        if os.path.isfile(self.path):
            return

        with open(self.path, 'w') as f:
            f.write('[]')

    def load(self) -> list[MarketSnapshot]:
        with open(self.path, 'r') as f:
            snapshots: list[dict] = json.loads(f.read())
            return [MarketSnapshot.from_dict(snapshot) for snapshot in snapshots]

    def save(self, snapshots: list[MarketSnapshot]) -> 'Store':
        with open(self.path, 'w') as f:
            json.dump(snapshots, f)

        return self

    def append(self, snapshot: MarketSnapshot) -> 'Store':
        snapshots = self.load()
        snapshots.append(snapshot)
        self.save(snapshots)
        return self
