import time
import math
import os
import psutil
from collections import defaultdict

process = psutil.Process(os.getpid())

def readDataset(filename):
    with open(filename, 'r') as file:
        dataset = [set(line.strip().split()) for line in file if line.strip()] 
    return dataset

def join(L):
    C = []
    for ind_i, i in enumerate(L):
        for j in L[ind_i+1:]:
            if i[:-1] == j[:-1]:
                new_item = sorted(set(i) | set(j))
                if new_item not in C:
                    C.append(new_item)
    return C

def generate_subsets(lst, length):
    from itertools import combinations
    return list(map(list, combinations(lst, length)))

def prune(C, L_pre):
    L_pre_sets = list(map(set, L_pre))
    C_pruned = []
    for itemset in C:
        subsets = generate_subsets(itemset, len(itemset) - 1)
        if all(set(sub) in L_pre_sets for sub in subsets):
            C_pruned.append(itemset)
    return C_pruned

def finalL(dataset, C, min_support_count):
    counts = defaultdict(int)
    for transaction in dataset:
        for candidate in C:
            if set(candidate).issubset(transaction):
                counts[tuple(candidate)] += 1

    frequent_k_itemsets = []
    support_counts = []
    for candidate, count in counts.items():
        if count >= min_support_count:
            frequent_k_itemsets.append(list(candidate))
            support_counts.append(count)
    return frequent_k_itemsets, support_counts

def oneItemset(dataset, min_support_count):
    item_counts = defaultdict(int)
    for transaction in dataset:
        for item in transaction:
            item_counts[item] += 1

    frequent_one_itemsets = []
    support_counts = []
    for item, count in item_counts.items():
        if count >= min_support_count:
            frequent_one_itemsets.append([item])
            support_counts.append(count)

    return frequent_one_itemsets, support_counts

def apriori(filename, min_support):
    print("Apriori Starts")
    dataset = readDataset(filename)
    min_support_count = math.ceil(len(dataset) * min_support)
    print(f'Running Apriori with min_support count = {min_support_count}')

    overall_start = time.time()
    L, support_counts = oneItemset(dataset, min_support_count)
    print(f"1-itemset: {len(L)} frequent itemsets found")
    total_frequent = len(L)

    k = 2
    while L:
        C = join(L)
        C = prune(C, L)
        L, support_counts = finalL(dataset, C, min_support_count)
        print(f"{k}-itemset: {len(L)} frequent itemsets found")
        total_frequent += len(L)
        k += 1

    overall_end = time.time()
    print(f"Total frequent itemsets: {total_frequent}")
    # print(f"Total time: {overall_end - overall_start:.2f} seconds")

filename = input("Filename?\n")
min_support_percent = float(input("Min support percentage?\n")) / 100

overallTimeStart = time.time()
mem_before = process.memory_info().rss

apriori(filename, min_support_percent)

mem_after = process.memory_info().rss
overallTimeEnd = time.time()

print(f"Total time needed: {overallTimeEnd - overallTimeStart:.2f} sec")
print(f"Total memory used: {(mem_after - mem_before) / 1024 ** 2:.2f} MB")
