from elasticsearch import Elasticsearch
from dataclasses import dataclass


@dataclass
class Elasticsearcher:
    """
    This class implements the logic behind searching for a vector in elastic search.
    """
    client: Elasticsearch = Elasticsearch()
    index_name: str = 'covid-19'

    def __call__(self, vector: list):
        script_query = {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source":
                    "cosineSimilarity(params.query_vector, doc['title_abstract_embeddings']) + 1.0",
                    "params": {
                        "query_vector": vector
                    }
                }
            }
        }

        res = self.client.search(
            index=self.index_name,
            body={
                "size": 25,
                "query": script_query,
                "_source": {
                    "includes": ["title", "abstract"]
                }
            })

        return res
