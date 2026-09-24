"""红黑树测试：随机操作 + 性质自检。"""
import random

import pytest

from rbtree import RBTree


def build_random(keys):
    t = RBTree()
    for k in keys:
        t.insert(k)
    return t


def test_insert_100_random_validate():
    rng = random.Random(42)
    keys = [rng.randint(0, 10000) for _ in range(100)]
    t = build_random(keys)
    t.validate()
    assert t.inorder() == sorted(set(keys))


def test_insert_sorted_1000_validate():
    t = build_random(range(1000))
    t.validate()
    assert t.inorder() == list(range(1000))


def test_search_present_and_absent():
    t = build_random([5, 3, 8, 1, 9, 2, 7])
    for k in (5, 3, 8, 1, 9, 2, 7):
        assert t.search(k) is True
    for k in (0, 4, 6, 10, -1, 100):
        assert t.search(k) is False


def test_delete_evens_validate():
    t = build_random(range(100))
    for k in range(0, 100, 2):
        t.delete(k)
    t.validate()
    assert t.inorder() == list(range(1, 100, 2))


def test_delete_odds_validate():
    t = build_random(range(100))
    for k in range(1, 100, 2):
        t.delete(k)
    t.validate()
    assert t.inorder() == list(range(0, 100, 2))


def test_delete_all_validate():
    t = build_random(range(50))
    for k in range(50):
        t.delete(k)
    t.validate()
    assert t.inorder() == []


def test_delete_missing_is_noop():
    t = build_random([1, 2, 3])
    t.delete(999)
    t.validate()
    assert t.inorder() == [1, 2, 3]


def test_delete_root_and_extremes():
    t = build_random([10, 5, 15, 3, 7, 12, 18, 1, 4, 6, 8, 11, 13, 16, 20])
    for k in (10, 1, 20):  # 根、最小值、最大值
        t.delete(k)
        t.validate()
    assert t.inorder() == sorted([5, 15, 3, 7, 12, 18, 4, 6, 8, 11, 13, 16])


def test_mixed_ops_1000_validate():
    """1000 次随机插入/删除后，性质与有序性保持。"""
    rng = random.Random(7)
    t = RBTree()
    live = set()
    for _ in range(1000):
        k = rng.randint(0, 500)
        if rng.random() < 0.6 or k not in live:
            t.insert(k)
            live.add(k)
        else:
            t.delete(k)
            live.discard(k)
        t.validate()
    assert t.inorder() == sorted(live)


def test_duplicate_insert_ignored():
    t = build_random([1, 1, 1, 2, 2])
    t.validate()
    assert t.inorder() == [1, 2]
