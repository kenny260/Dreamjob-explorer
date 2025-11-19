"""
cache.py
Simple in-memory caching for DreamJob Explorer.
Stores API responses or computed results for a configurable TTL.
"""

import time
from typing import Any, Optional
from ..config import CACHE_TTL_SECONDS
from ..logger import get_logger

logger = get_logger(__name__)


class SimpleCache:
    """
    A basic key-value in-memory cache with expiration.
    """

    def __init__(self, ttl: int = CACHE_TTL_SECONDS):
        self.ttl = ttl
        self.store = {}

    def set(self, key: str, value: Any):
        """
        Store a value in the cache with the current timestamp.
        """
        self.store[key] = {"value": value, "timestamp": time.time()}
        logger.debug(f"Cache set for key: {key}")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the cache.
        Returns None if key is missing or expired.
        """
        item = self.store.get(key)
        if not item:
            logger.debug(f"Cache miss for key: {key}")
            return None

        if (time.time() - item["timestamp"]) > self.ttl:
            logger.debug(f"Cache expired for key: {key}")
            self.store.pop(key)
            return None

        logger.debug(f"Cache hit for key: {key}")
        return item["value"]

    def clear(self):
        """
        Clear the entire cache.
        """
        self.store.clear()
        logger.debug("Cache cleared")

