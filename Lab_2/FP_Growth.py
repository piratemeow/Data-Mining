import time
import math
def readDataset(filename):
    with open(filename, 'r') as file:
        dataset = [sorted(map(int, line.strip().split())) for line in file if line.strip()] 
    dataset.sort()
    
    return dataset


def oneItemset(filename,min_support):
    dataset = readDataset(filename)
    # min_support = math.ceil(len(dataset)*min_support)
    def unique_elements(lst_of_lists):
        unique_set = set()
        for sublist in lst_of_lists:
            for item in sublist:
                unique_set.add(item)  
                      
        lis = list(unique_set)
        
        items = []
        
        for i in lis:
            c = [i]
            items.append(c)
        return items
        
    
    items = unique_elements(dataset)
    # print(items)
    # print(items)
    support_count = []    # for the count of frequent one iteset
    frequent_one_itemset = []      # for frequent one itemset
    frequent_one_itemset_with_support_count = {}
    for i in items:
        count = 0
        for j in dataset:
            if all(item in j for item in i):
                
                count+=1
        if count>=min_support:
            # frequent_one_itemset_with_support_count[i] = count
            frequent_one_itemset.append(i)
            support_count.append(count)
            
    frequent_one_itemset_with_support_count = [list(pair) for pair in zip(frequent_one_itemset,support_count)]
    frequent_one_itemset_with_support_count = sorted(frequent_one_itemset_with_support_count,key = lambda x:x[1],reverse=True)
            
    return frequent_one_itemset_with_support_count
    
    
x = oneItemset("book_data",2)
print(x)
