import time
import math
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
            if ind_i==ind_j:
                continue
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
    min_support = math.ceil(len(dataset)*min_support)
    # print(f"Min suopp {min_support}")
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
    min_support = math.ceil(len(dataset)*min_support)
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
    timestart = time.time()
    frequent_one_itemset,support_count =  oneItemset(filename,min_support)
    timeend = time.time()
    
    totalTime = timeend - timestart
    sum = 0
    
    L = frequent_one_itemset
    print(f"1 Itemset total elements {len(L)} time needed {totalTime}")
    sum+=len(L)
    # for ind,ele in enumerate(L):
    #     print(ele, support_count[ind])
        
    i = 2
    while (len(L)!=0):
        timestart = time.time()
        C = join(L)
        pruned_C = prune(C,L)
        L,support_count = finalL(filename,pruned_C,min_support)
        timeend = time.time()
    
        totalTime = timeend - timestart
        print(f"{i} Itemset Candidate {len(pruned_C)}")
        print(f"{i} Frequent Itemset total elements {len(L)} time needed {totalTime}")
        sum+=len(L)
        
        # for ind,ele in enumerate(L):
        #     print(ele, support_count[ind])
            
        i+=1
        
    print(sum)
    
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
    
    
    
    
overallTimeStart = time.time()
apriori("mushroom",0.30)
overallTimeEnd = time.time()



print(f"Total time needed {overallTimeEnd - overallTimeStart}")

# print(readDataset("data3"))    

# dataset = readDataset("data2")
# # print(dataset)
# C = join(dataset)

# C_pruned = prune(C,dataset)
# print(C_pruned)
        
                             
                
            
        
    
    
