from manger import Manger
from driver import init
from store import Store
from snapshot import MarketSnapshot

store = Store("data.json")
manger = Manger(init(), store)
manger.start()
