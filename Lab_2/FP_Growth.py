from collections import defaultdict, namedtuple
import math
# --- Data Structures ---

class FPNode:
    """
    A node in the FP-tree.
    """
    def __init__(self, item, count, parent):
        self.item = item          # Item stored in this node
        self.count = count        # Number of transactions passing through this node
        self.parent = parent      # Parent node
        self.children = {}        # Dictionary of child nodes {item: FPNode}
        self.node_link = None     # Link to the next node with the same item name (for header table)

    def increment(self, count):
        """Increment the count for this node."""
        self.count += count

    def display(self, indent=1):
        """Helper function to display the tree (for debugging)."""
        print('  ' * indent, self.item, ':', self.count)
        for child in self.children.values():
            child.display(indent + 1)

# --- Helper Functions ---

def find_frequent_items(transactions, min_support):
    """
    Scans the transaction database to find frequent one items meeting minimum support.
    Args:
        transactions (list of lists): The transaction database.
        min_support (int): The minimum support count threshold.
    Returns:
        dict: A dictionary of {item: support_count} for frequent items,
              sorted by frequency in descending order.
    """
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1

    # Filter items below min_support
    frequent_items = {item: count for item, count in item_counts.items() if count >= min_support}

    # Sort frequent items by frequency (descending) for efficient tree building
    sorted_frequent_items = dict(sorted(frequent_items.items(), key=lambda item: item[1], reverse=True))

    return sorted_frequent_items

def construct_ordered_transactions(transactions, frequent_items_order):
    """
    Filters and orders items in each transaction based on frequent item order.
    Args:
        transactions (list of lists): The transaction database.
        frequent_items_order (list): List of frequent items sorted by frequency desc.
    Returns:
        list: List of transactions, each containing only frequent items
              sorted according to frequent_items_order.
    """
    ordered_transactions = []
    item_order_map = {item: i for i, item in enumerate(frequent_items_order)}

    for transaction in transactions:
        # Filter out non-frequent items
        frequent_in_tx = [item for item in transaction if item in item_order_map]
        # Sort items based on the global frequency order
        frequent_in_tx.sort(key=lambda item: item_order_map[item])
        if frequent_in_tx:
            ordered_transactions.append(frequent_in_tx)
    return ordered_transactions

def update_header_table(item, target_node, header_table):
    """
    Updates the header table to link nodes with the same item.
    Args:
        item: The item of the node being added.
        target_node (FPNode): The node to add to the linked list.
        header_table (dict): The header table {item: [count, head_node]}.
    """
    head_node_info = header_table[item] # [count, node_pointer]
    current_node = head_node_info[1]

    if current_node is None:
        # First node for this item
        head_node_info[1] = target_node
    else:
        # Traverse the linked list to the end and append
        while current_node.node_link is not None:
            current_node = current_node.node_link
        current_node.node_link = target_node

def update_tree(items, node, header_table, count):
    """
    Recursively updates the FP-tree with a transaction (or conditional pattern base path).
    Args:
        items (list): The ordered list of items in the transaction/path.
        node (FPNode): The current node in the FP-tree to process from.
        header_table (dict): The header table.
        count (int): The count associated with this path (usually 1 for transactions).
    """
    if not items:
        return

    first_item = items[0]
    remaining_items = items[1:]

    # Check if a child exists for the first item
    if first_item in node.children:
        # Increment count of existing child
        child_node = node.children[first_item]
        child_node.increment(count)
    else:
        # Create a new child node
        new_node = FPNode(item=first_item, count=count, parent=node)
        node.children[first_item] = new_node
        # Update the header table link
        update_header_table(first_item, new_node, header_table)
        child_node = new_node

    # Recursively call for remaining items
    if remaining_items:
        update_tree(remaining_items, child_node, header_table, count)


def build_fp_tree(ordered_transactions_with_counts, frequent_items):
    """
    Builds the FP-tree from ordered transactions.
    Args:
        ordered_transactions_with_counts (list of tuples):
            List of (ordered_transaction, count).
        frequent_items (dict): Dictionary of {item: support_count}.
    Returns:
        tuple: (root_node, header_table)
            root_node (FPNode): The root of the FP-tree.
            header_table (dict): The header table {item: [count, head_node]}.
    """
    root = FPNode(item=None, count=1, parent=None)
    # Initialize header table: {item: [total_count, head_node_pointer]}
    header_table = {item: [count, None] for item, count in frequent_items.items()}

    for transaction, count in ordered_transactions_with_counts:
        update_tree(transaction, root, header_table, count)

    return root, header_table

# --- Mining Functions ---

def ascend_tree(node):
    """
    Ascends from a node up to the root, collecting items in the path (excluding the start node's item).
    Args:
        node (FPNode): The starting node.
    Returns:
        list: The list of items in the prefix path.
    """
    path = []
    while node.parent is not None and node.parent.item is not None:
        path.append(node.parent.item)
        node = node.parent
    # The path items are collected bottom-up, reverse them
    return path[::-1]


def find_prefix_paths(base_item, header_table):
    """
    Finds all conditional prefix paths for a given item.
    Args:
        base_item: The item for which to find prefix paths.
        header_table (dict): The header table of the current FP-tree.
    Returns:
        list: A list of tuples (prefix_path, count), representing the
              conditional pattern base.
    """
    conditional_patterns = []
    # Start from the head node link in the header table
    current_node = header_table[base_item][1]

    while current_node is not None:
        prefix_path = ascend_tree(current_node)
        if prefix_path:
            conditional_patterns.append((prefix_path, current_node.count))
        # Follow the node link to the next node with the same item
        current_node = current_node.node_link

    return conditional_patterns


def mine_frequent_itemsets(header_table, min_support, prefix, frequent_itemsets):
    """
    Recursively mines the FP-tree or conditional FP-tree.
    Args:
        header_table (dict): The header table of the current tree.
        min_support (int): The minimum support count.
        prefix (set): The current prefix pattern being explored.
        frequent_itemsets (dict): Dictionary to store discovered frequent itemsets {itemset_tuple: support}.
    """
    # Sort items in header table by frequency (ascending) - process less frequent first
    sorted_items = sorted(header_table.keys(), key=lambda item: header_table[item][0])

    for base_item in sorted_items:
        # Current frequent pattern = prefix U {base_item}
        new_frequent_set = prefix.copy()
        new_frequent_set.add(base_item)

        # Store the new frequent itemset with its support (total count from header table)
        support = header_table[base_item][0]
        frequent_itemsets[tuple(sorted(list(new_frequent_set)))] = support

        # --- Construct Conditional FP-Tree ---
        # 1. Find Conditional Pattern Base
        conditional_pattern_base = find_prefix_paths(base_item, header_table)

        # 2. Calculate frequent items in the conditional base
        conditional_transactions = []
        for path, count in conditional_pattern_base:
             # Each path acts like a transaction weighted by count
             for _ in range(count):
                 conditional_transactions.append(path)

        # Calculate frequent items ONLY within this conditional base
        conditional_frequent_items = find_frequent_items(conditional_transactions, min_support)

        if conditional_frequent_items:
            # Order the conditional transactions based on conditional frequent items
            conditional_frequent_order = list(conditional_frequent_items.keys())
            ordered_cond_transactions = construct_ordered_transactions(
                conditional_transactions, conditional_frequent_order
            )

            # Need counts for building the conditional tree (handle weights from original paths)
            # Re-aggregate counts for the *ordered* paths within the conditional base
            cond_transactions_with_counts = defaultdict(int)
            for path, original_count in conditional_pattern_base:
                # Filter and order the path according to *conditional* frequency
                ordered_path = [item for item in path if item in conditional_frequent_items]
                ordered_path.sort(key=lambda item: conditional_frequent_order.index(item))
                if ordered_path:
                    cond_transactions_with_counts[tuple(ordered_path)] += original_count

            # Convert back to list of tuples format expected by build_fp_tree
            cond_transactions_list = list(cond_transactions_with_counts.items())


            # 3. Build Conditional FP-Tree
            conditional_tree_root, conditional_header = build_fp_tree(
                cond_transactions_list, conditional_frequent_items
            )

            # 4. Recursively mine the conditional tree
            if conditional_header: # Check if the conditional tree is not empty
                 mine_frequent_itemsets(conditional_header, min_support, new_frequent_set, frequent_itemsets)


# --- Main FP-Growth Function ---

def fp_growth(transactions, min_support):
    """
    Performs the FP-Growth algorithm.
    Args:
        transactions (list of lists): The transaction database. Each inner list is a transaction.
        min_support (int): The minimum support count threshold.
    Returns:
        dict: A dictionary of frequent itemsets {itemset_tuple: support_count}.
    """
    # 1. First Scan: Find frequent 1-itemsets and their order
    frequent_items = find_frequent_items(transactions, min_support)
    frequent_items_order = list(frequent_items.keys()) # Already sorted by frequency desc

    if not frequent_items_order:
        return {} # No frequent items found

    # 2. Second Scan: Construct ordered transactions
    ordered_transactions = construct_ordered_transactions(transactions, frequent_items_order)
    # Prepare data for building the initial FP-tree (each transaction has count 1 initially)
    initial_transactions_with_counts = [(tx, 1) for tx in ordered_transactions]


    # 3. Build the initial FP-Tree
    root_node, header_table = build_fp_tree(initial_transactions_with_counts, frequent_items)

    # (Optional) Display the initial tree for debugging
    # print("Initial FP-Tree Structure:")
    # root_node.display()
    # print("\nHeader Table:", {item: info[0] for item, info in header_table.items()}) # Show item counts


    # 4. Mine the FP-Tree
    frequent_itemsets = {}
    mine_frequent_itemsets(header_table, min_support, set(), frequent_itemsets)

    return frequent_itemsets


# --- Example Usage ---

if __name__ == "__main__":
    # Example dataset from the original paper
    transactions_data = [
        ['R', 'Z', 'H', 'J', 'P'],
        ['Z', 'Y', 'X', 'W', 'V', 'U', 'T', 'S'],
        ['Z'],
        ['R', 'X', 'N', 'O', 'S'],
        ['Y', 'R', 'X', 'Z', 'Q', 'T', 'P'],
        ['Y', 'Z', 'X', 'E', 'Q', 'S', 'T', 'M'],
    ]

    filename = input()
    with open(filename, 'r') as file:
        dataset = [sorted(map(str, line.strip().split())) for line in file if line.strip()] 
    transactions_data = dataset
    # print(transactions_data)
    min_support_count = math.ceil(0.30*len(dataset))

    print(f"Running FP-Growth with min_support = {min_support_count}")
    print("Dataset 1 (Original Paper):")
    frequent_patterns = fp_growth(transactions_data, min_support_count)
    print("Frequent Itemsets Found:")
    # Sort by support for better readability
    sorted_patterns = sorted(frequent_patterns.items(), key=lambda item: item[1], reverse=True)
    
    total = 0
    for itemset, support in sorted_patterns:
        total+=1
        print(f"  {list(itemset)} : {support}")

    print(f'Total {total}')

    