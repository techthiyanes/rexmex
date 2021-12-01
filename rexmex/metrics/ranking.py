import numpy as np
from scipy import stats


def reciprocal_rank(relevant_item: any, ranking: np.array) -> float:
    """
    Calculate the reciprocal rank (RR) of an item in a ranked list of items.

    Args:
        item (Object): an object in the list of items.
        ranking (array-like):  An N x 1 ranking of items.
    Returns:
        RR (float): The reciprocal rank of the item.
    """

    return 1.0 / (np.in1d(ranking, relevant_item).argmax() + 1)


def mean_reciprocal_rank(relevant_items: np.array, ranking: np.array):
    """
    Calculate the mean reciprocal rank (MRR) of items in a ranked list.

    Args:
        relevant_items (array-like): An N x 1 array of relevant items.
        ranking (array-like):  An N x 1 array of ordered items.
    Returns:
        MRR (float): The mean reciprocal rank of the relevant items in a ranking.
    """

    reciprocal_ranks = []
    for item in relevant_items:
        rr = reciprocal_rank(item, ranking)
        reciprocal_ranks.append(rr)

    return np.mean(reciprocal_ranks)


def average_percision_at_k(relevant_items: np.array, ranking: np.array, k=10):
    """
    Calculate the average percision at k (AP@K) of items in a ranked list.

    Args:
        relevant_items (array-like): An N x 1 array of relevant items.
        ranking (array-like):  An N x 1 array of ordered items.
        k (int): the number of items considered in the ranking.
    Returns:
        AP@K (float): The average percision @ k of a ranking.
    """

    if len(ranking) > k:
        ranking = ranking[:k]

    hits = np.in1d(ranking, relevant_items)
    ranks = np.arange(1, k + 1)
    p_at_ks = np.arange(1, len(ranks[hits]) + 1) / ranks[hits]
    return np.mean(p_at_ks)


def mean_average_percision_at_k(relevant_items: np.array, rankings: np.array, k=10):
    """
    Calculate the mean average percision at k (MAP@K) for a list of rankings.
    Each ranking should be paired with a list of relevant items. First ranking list is
    evaluated against the first list of relevant items, and so on.

    Example usage:
    .. code-block:: python

        import numpy as np
        from rexmex.metrics.ranking import mean_average_percision_at_k

        mean_average_percision_at_k(
            relevant_items=np.array(
                [
                    [1,2],
                    [2,3]
                ]
            ),
            rankings=np.array([
                [3,2,1],
                [2,1,3]
            ])
        )
        >>> 0.708333...

    Args:
        relevant_items (array-like): An M x N array of relevant items.
        rankings (array-like):  An M x N array of ranking arrays.
        k (int): the number of items considered in the rankings.
    Returns:
        MAP@K (float): The average percision @ k of a ranking.
    """

    aps = []
    for items, ranking in zip(relevant_items, rankings):
        ap = average_percision_at_k(items, ranking, k)
        aps.append(ap)

    return np.mean(aps)


def hits_at_k(relevant_items: np.array, ranking: np.array, k=10):
    """
    Calculate the number of hits of relevant items in a ranked list HITS@K.

    Args:
        relevant_items (array-like): An 1 x N array of relevant items.
        rankings (array-like):  An 1 x N array of ranking arrays
        k (int): the number of items considered in the ranking
    Returns:
        HITS@K (float):  The number of relevant items in the first k items in a ranking.
    """
    if len(ranking) > k:
        ranking = ranking[:k]

    hits = np.array(np.in1d(ranking, relevant_items), dtype=int).sum()
    return hits / len(ranking)


def spearmanns_rho(list_a: np.array, list_b: np.array):
    """
    Calculate the Spearmann's rank correlation coefficient (Spearmann's rho) between two arrays.

    Args:
        list_a (array-like): An 1 x N array of items.
        list_b (array-like):  An 1 x N array of items.
    Returns:
        Spearmann's rho (float): Spearmann's rho.
        p-value (float): two-sided p-value for null hypothesis that both rankings are uncorrelated.
    """
    return stats.spearmanr(list_a, list_b)


def kendall_tau(ranking_a: np.array, ranking_b: np.array):
    """
    Calculate the Kendall's tau, measuring the correspondance between two rankings.

    Args:
        ranking_a (array-like): An 1 x N array of items.
        ranking_b (array-like):  An 1 x N array of items.
    Returns:
        Kendall tau (float): The tau statistic.
        p-value (float): two-sided p-value for null hypothesis that there's no association between the rankings.
    """
    return stats.kendalltau(ranking_a, ranking_b)
