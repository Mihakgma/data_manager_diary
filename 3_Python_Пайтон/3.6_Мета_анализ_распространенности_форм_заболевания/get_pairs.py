from itertools import combinations
from random import seed
# import seet


def get_all_pairs(my_list, pairs_value=2):
  """Возвращает список всех комбинаций пар из заданного списка."""
  seed(42)
  return list(combinations(my_list, pairs_value))
