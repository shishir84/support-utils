from neo4j import GraphDatabase
from core import settings

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )
    return _driver


def run_query(query: str, params: dict | None = None):
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, params or {})
        return list(result)
