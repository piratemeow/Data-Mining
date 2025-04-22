import time
import math

from collections import deque


def tree_traversal(root,table):
    queue = deque()
    
    level = 1
    current_level = 0
    queue.append((root,level))
    while (queue):
        node,level = queue.popleft()
        item = node.item
        if item in table and table[item]==None:
            table[item] = ListNode()
            table[item].treeNode = node
        elif item in table:
            f = table[item]
            while(f.next!=None):
                f = f.next
                        
            f.next = ListNode()
            f.next.treeNode = node
        
        if level > current_level:
            current_level = level
            # print(f"\nLevel {current_level}:")
            
        for key,value in node.children.items():
            # print(value.item, value.count)
            queue.append((value,level+1))
        

def table_traversal(table):
    
    for key,value in table.items():
        print(key)
        i = value
        while(i!=None):
            print(i.treeNode.item, i.treeNode.count)
            i = i.next    
            
class TreeNode:
    def __init__(self,item, count):
        self.item = item
        self.count = count
        self.parent = None
        self.children = {}
        
class ListNode:
    def __init__(self):
        self.treeNode = None
        self.next = None

def readDataset(filename):
    with open(filename, 'r') as file:
        dataset = [sorted(map(int, line.strip().split())) for line in file if line.strip()] 
    # dataset.sort()
    
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
            frequent_one_itemset.append(i[0])
            support_count.append(count)
            
    frequent_one_itemset_with_support_count = [list(pair) for pair in zip(frequent_one_itemset,support_count)]
    frequent_one_itemset_with_support_count = sorted(frequent_one_itemset_with_support_count,key = lambda x:x[1],reverse=True)
            
    return frequent_one_itemset_with_support_count
    
    
def fp_growth_tree(filename, min_support):
    frequent_one_itemset_with_support_count = oneItemset(filename,min_support)
    table = {item[0]: None for item in frequent_one_itemset_with_support_count}
    
    root = TreeNode(-1,-1)
    dataset = readDataset(filename)
    
    for trans in dataset:
        map = {item[0]:0 for item in frequent_one_itemset_with_support_count}
        node = root
        for item in trans:
            map[item]+=1
            
        for i in frequent_one_itemset_with_support_count:
            if map[i[0]]>=1:
                if i[0] in node.children:
                    node.children[i[0]].count+=1
                else:
                    new_node = TreeNode(i[0],1)
                    node.children[i[0]] = new_node
                
                node.children[i[0]].parent = node
                node = node.children[i[0]]
                
                # if table[i[0]]==None:
                #     table[i[0]] = ListNode()
                #     table[i[0]].treeNode = node
                # else:
                #     f = table[i[0]]
                    
                #     while(f.next!=None):
                #         f = f.next
                        
                #     f.next = ListNode()
                #     f.next.treeNode = node
                    
                        
    tree_traversal(root,table)    
    table_traversal(table)
                
    
    # print(map)    
    # tree_traversal(root=root)
    
    return 
    
x = oneItemset("book_data",2)
print(x)


fp_growth_tree("book_data",2)

    
    
