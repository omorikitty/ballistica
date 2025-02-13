import os
import itertools
import time
import random
from dataclasses import asdict
from pymongo import UpdateOne
from efro.threadpool import ThreadPoolExecutorPlus
from database.manager import StatsManager
from database.models import User

cpu_count = os.cpu_count() or 1
handle_stats_manager = StatsManager()

def load_cache_from_db():
    return {
        user["_id"]: {key: user[key] for key in user}
        for user in handle_stats_manager.find({})
    }

def generate_users(max_users: int = 5) -> dict[str, User]:
    return {
        f"pb-id_{i}": User(_id=f"pb-id_{i}", kills=0, killed=0, played=0, score=0, name=f"Player_{i}")
        for i in range(max_users)
    }

def batch_dict(data: dict[str, User], batch_size: int):
    it = iter(data.items())
    while batch := dict(itertools.islice(it, batch_size)):
        yield batch

def process_batch(batch: dict[str, User], cache: dict, changed_users: set):
    """Procesa un batch de usuarios y actualiza MongoDB solo si hubo cambios."""
    bulk = []
    
    for user_id, user_instance in batch.items():
        if user_id not in changed_users:  
            continue  

        new_stats = asdict(user_instance) 
        bulk.append(UpdateOne({"_id": user_id}, {"$set": new_stats}, upsert=True))
        cache[user_id] = new_stats  

    if bulk:
        start = time.perf_counter()
        handle_stats_manager.update_from_bulk(bulk)
        elapsed = time.perf_counter() - start
        print(f"Actualizados {len(bulk)} usuarios en {elapsed:.4f} segundos.")

def bulk_insert_threads(data: dict[str, User], cache: dict, workers: int, batch_size: int, changed_users: set):
    """Ejecuta la actualización en MongoDB con múltiples hilos."""
    if not changed_users:
        print("🔹 No hay cambios en esta ronda, omitiendo actualización.")
        return

    start_time = time.perf_counter()
    with ThreadPoolExecutorPlus(workers) as executor:
        executor.map(lambda batch: process_batch(batch, cache, changed_users), batch_dict(data, batch_size))
    
    print(f"⌛ Tiempo total de batch: {time.perf_counter() - start_time:.4f} segundos")

def simulate_round(users_data: dict[str, User], round_number: int, changed_users: set):
    """Simula una ronda de juego y marca los usuarios que cambiaron."""
    print(f"\n🏆 --- RONDA {round_number} --- 🏆")
    
    for user in users_data.values():
        prev_state = (user.kills, user.killed, user.score, user.played)
        
        user.kills += random.randint(0, 5)
        user.killed += random.randint(0, 3)
        user.score += random.randint(10, 50)
        user.played += 1 
        
        new_state = (user.kills, user.killed, user.score, user.played)
        
        if prev_state != new_state:  
            changed_users.add(user._id)  

def run_game():
    users_data = generate_users(max_users=1000)  
    cache_data = load_cache_from_db()  
    changed_users = set()  

    batch_size = max(100, (len(users_data) // cpu_count))
    max_workers = min(cpu_count, max(1, len(users_data) // (batch_size * 2)))

    for round_num in range(1, 6):
        simulate_round(users_data, round_num, changed_users)  

        if round_num % 2 == 0:  
            bulk_insert_threads(users_data, cache_data, max_workers, batch_size, changed_users)  
            changed_users.clear()  

#run_game()
