from typing import List, Dict

def rank_candidates(results: List[Dict]) -> List[Dict]:
    """
    Sort candidates by final_score in descending order.
    Assigns rank to each candidate.
    """
    sorted_results = sorted(results, key=lambda x: x.get('final_score', 0), reverse=True)

    for i, candidate in enumerate(sorted_results):
        candidate['rank'] = i + 1

    return sorted_results
