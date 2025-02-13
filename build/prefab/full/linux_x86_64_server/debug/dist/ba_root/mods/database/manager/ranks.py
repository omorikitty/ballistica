from abc import ABC, abstractmethod
from functools import wraps
from database import stats


tops = []

def rank_cache(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global tops
        
        result = func(*args, **kwargs)
        if result != tops: 
            tops = result if isinstance(result, list) else list(result)

        return tops 
    
    return wrapper


class UpdateRanks:
    
    def get_ranks(self):
        return tops if tops else []

    @rank_cache
    def update(self):
        return stats.aggregate(
            [
                {"$sort": {"kills": -1, "score": -1}},
                {"$limit": 10},
                {"$project": {"_id": 0, "kills": 1, "score": 1, "name": 1}},
            ]
        )
