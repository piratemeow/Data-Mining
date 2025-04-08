def readDataset(filename):
    with open(filename, 'r') as file:
        dataset = [sorted(map(int, line.strip().split())) for line in file if line.strip()] 
    dataset.sort()
    
    # print(dataset)
    return dataset


def join(L):
    C = []
    for ind_i,i in enumerate(L):
        for ind_j,j in enumerate(L[ind_i+1:],start=(ind_i+1)):
            # print(ind_i, ind_j)
            flag = True
            for k in range((len(i)-1)):
                if i[k]!=j[k]:
                    flag = False
                    break
            if (flag):
                new_lis = i[:-1]
                new_lis.append(i[-1])
                new_lis.append(j[-1])
                C.append(new_lis)
                
    return C

def generate_subsets(lst, length):
    subsets = []
    def backtrack(start, current_subset):
        if len(current_subset) == length:
            subsets.append(current_subset[:])  
            return
        
        for i in range(start, len(lst)):
            current_subset.append(lst[i])
            backtrack(i + 1, current_subset)
            current_subset.pop()  
    
    backtrack(0, [])
    return subsets


def prune(C,L_pre):
    C_pruned = []
    for itemset in C:
        subsets = generate_subsets(itemset,len(itemset)-1)
        flag = True
        for i in subsets:
            if i not in L_pre:
                flag = False
        if flag:
            C_pruned.append(itemset)
            
    # print(subsets)
    return C_pruned

def finalL(filename, C,min_support):
    dataset = readDataset(filename=filename)
    support_count = []
    frequent_k_itemset = []
    frequent_k_itemset_with_support_count = {}
    # print(dataset)
    for i in C:
        count = 0
        for j in dataset:
            f = all(item in j for item in i)
            if f:
                # print(i,j)
                count+=1
        if count>=min_support:
            # print(i)
            # frequent_one_itemset_with_support_count[i] = count
            frequent_k_itemset.append(i)
            support_count.append(count)
    
    return frequent_k_itemset, support_count
        
    
def oneItemset(filename,min_support):
    dataset = readDataset(filename)
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
    support_count = []
    frequent_one_itemset = []
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
            
    return frequent_one_itemset, support_count
    
  

    
    
def apriori(filename,min_support):
    print("Apriori Starts")
    
    frequent_one_itemset,support_count =  oneItemset(filename,min_support)
    L = frequent_one_itemset
    print("1 Itemset")
    print(frequent_one_itemset,support_count)
    i = 2
    while (len(L)!=0):
        print(f"{i} Itemset")
        C = join(L)
        pruned_C = prune(C,L)
        L,support_count = finalL(filename,pruned_C,min_support)
        
        print(L, support_count)
        i+=1
        
    
    
    # print()
    # print()
    # print()
    # C = join(frequent_one_itemset)
    # C = prune(C,frequent_one_itemset)
    # L = finalL(filename,C,min_support)
    
    # # print(C)
    # print()
    # print()
    # print()
    # print(L)
    
    
    
    
    
apriori("data3",100000)

# print(readDataset("data3"))    

# dataset = readDataset("data2")
# # print(dataset)
# C = join(dataset)

# C_pruned = prune(C,dataset)
# print(C_pruned)
        
                             
                
            
        
    
    
