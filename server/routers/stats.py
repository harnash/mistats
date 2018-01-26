from prometheus_client.exposition import generate_latest
from prometheus_client import REGISTRY


def generate_stats():
    return generate_latest(REGISTRY).decode('utf8')
