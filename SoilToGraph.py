import re
import EdgeToAdjacency

class Pair(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type

# Function to convert an instance in the SOIL (USE format) to a graph
def soilToGraph(text):

    entity_map = {}     # Maps entity names to their IDs and types
    node_labels = {}    # Stores node labels as {id: entity_type}
    edges = []          # Stores edges as [(edgei1, edgej1), (edgei2, edgej2), ...]
    current_id = 0

    regex_labels = r"!new\s+(\w+)\s*\(\s*'([^']+)'\s*\)"
    pattern_labels = re.compile(regex_labels)

    regex_edges = r"!insert\s+\(([^)]+)\)\s+into\s+\w+"
    pattern_edges = re.compile(regex_edges)

    for line in text.split("\n"):
        matcher_labels = pattern_labels.search(line)
        matcher_edges = pattern_edges.search(line)

        if matcher_labels:
            entity_type = matcher_labels.group(1)
            entity_name = matcher_labels.group(2)
            entity_map[entity_name] = Pair(current_id, entity_type)

            # Add to node_labels dictionary
            node_labels[current_id] = entity_type

            current_id += 1
            continue

        if matcher_edges:
            edges_str = matcher_edges.group(1)
            split_edges = edges_str.split(",")
            source = split_edges[0].strip()
            target = split_edges[1].strip()

            # Get IDs of source and target entities
            edgei = entity_map[source].id
            edgej = entity_map[target].id

            # Add to edges list
            edges.append((edgei, edgej))

    # Results
    adgency_matrix = EdgeToAdjacency.convert_to_adjacency_matrix(edges, len(node_labels))
    
    return adgency_matrix, node_labels, edges



if __name__ == "__main__":
    text = """
    !new Bank('bank2')
    !bank2.country := 'India'
    !bank2.name := 'Bharat Bank'
    !bank2.bic := 'INBBINBB'

    !new Person('person2')
    !person2.age := 45
    !person2.firstName := 'Raj'
    !person2.lastName := 'Kumar'

    !new Account('account2')
    !account2.iban := 'IN0212450000001234567890'
    !account2.balance := 1000000000

    !new Account('account3')
    !account3.iban := 'IN0212450000009876543210'
    !account3.balance := 500000000

    !new Person('person3')
    !person3.age := 32
    !person3.firstName := 'Priya'
    !person3.lastName := 'Kapoor'

    !insert (person2, account2) into Ownership
    !insert (person2, account3) into Ownership
    !insert (person2, account2) into Use
    !insert (person3, account2) into Use
    !insert (person3, account3) into Use
    !insert (bank2, account2) into AccountOfBanks
    !insert (bank2, account3) into AccountOfBanks
    """

    adgency_matrix, node_labels, edges = soilToGraph(text)
    
    print("Edges: "), 
    print(edges)
    print("Adjacency matrix: "), 
    print(adgency_matrix)
    print("Node labels: "), 
    print(node_labels)