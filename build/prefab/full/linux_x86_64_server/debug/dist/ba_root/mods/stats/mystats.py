import datetime
import babase
import os
import time
import threading
from typing import Any, List, Dict

from database.models.user import User
from database.manager import StatsManager
from dataclasses import asdict
from pymongo import UpdateOne
from efro.threadpool import ThreadPoolExecutorPlus
from concurrent.futures import wait



def earn(score: int, kills: int) -> int:
    return int(
        min(
            (int(score / 10) + kills * 5) / 2,
            70,
        )
    )


def update(score_set):
    stats = StatsManager()
    updates: dict[str, Any] = {}

    for p_entry in score_set.get_records().values():
        try:
            account_id = p_entry.player.get_v1_account_id()
            account_name = p_entry.player.inputdevice.get_v1_account_name(full=True)
            if not account_id:
                continue
        except Exception:
            continue


        entry = User(**stats.get_stats(account_id))


        entry.kills += p_entry.accum_kill_count
        entry.killed += p_entry.accum_killed_count
        entry.score += min(p_entry.accumscore, 250)
        entry.coins += earn(p_entry.accumscore, p_entry.accum_kill_count)
        entry.played += 1


        entry.character = p_entry.player.character
        entry.name = p_entry.getname(full=True)
        entry.ls = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


        entry.accounts = list(set(entry.accounts + [account_name]))


        updates[account_id] = asdict(entry)


    if updates:
        UpdateThread(updates, stats).start()


class UpdateThread(threading.Thread):
    def __init__(self, updates: Dict[str, Any], stats: StatsManager):
        super().__init__()
        self.stats = stats
        self.cache = self.stats.cache
        self.updates = updates
        self.bulk_updates: List[UpdateOne] = []

        self.cpu_count = os.cpu_count() or 2
        self.chunk_size = min(max(self.cpu_count * 10, 20), 500)
        self.workers = max(1, min(len(self.updates) // 10, self.cpu_count * 2))

    def run(self):
        with ThreadPoolExecutorPlus(max_workers=self.workers) as executor:
            executor.map(self.process_entry, self.updates.items())

        start = time.perf_counter()
        for chunk in self.chunk_generator(self.bulk_updates, self.chunk_size):
            self.process_bulk_updates(chunk)
        print(f"took: {time.perf_counter()- start:.4}")
    

    def process_entry(self, user_data):
        account_id, stats = user_data
        self.cache.update_from_cache(account_id, stats)
        print(f"{self.cache.get_from_cache(account_id)}")
        self.bulk_updates.append(UpdateOne({"_id": account_id}, {"$set": stats}, upsert=True))

    def process_bulk_updates(self, bulk: List[UpdateOne]):
        result = self.stats.update_from_bulk(bulk)
        print(f"Se han actualizado ({len(bulk)}) jugadores" if result.modified_count > 0 else "No hubo actualizaciones")

    @staticmethod
    def chunk_generator(items: List[Any], size: int):
        from itertools import islice
        itr = iter(items)
        while chunk := list(islice(itr, size)):
            yield chunk

