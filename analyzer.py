from collections import defaultdict

def analyze_routing(data):
    nets = data["nets"]

    # Net statistics
    net_sizes = [len(net["nodes"]) for net in nets]

    # Node type counts
    node_types = defaultdict(int)
    for net in nets:
        for node in net["nodes"]:
            node_types[node["type"]] += 1

    # Count CHANX/CHANY usage per location
    congestion = defaultdict(int)
    for net in nets:
        for node in net["nodes"]:
            if node["type"] in ["CHANX", "CHANY"]:
                congestion[(node["x"], node["y"])] += 1

    congested = sum(1 for v in congestion.values() if v > 1)

    return {
        "total_nets": len(nets),
        "min_nodes": min(net_sizes),
        "max_nodes": max(net_sizes),
        "avg_nodes": sum(net_sizes) / len(net_sizes),
        "node_types": dict(node_types),
        "total_routing_locations": len(congestion),
        "congested_locations": congested,
        "max_congestion": max(congestion.values()) if congestion else 0,
    }


def print_analysis(stats):
    print("\n" + "=" * 50)
    print("ROUTING ANALYSIS")
    print("=" * 50)

    print("\nNet Statistics:")
    print(f"  Total nets: {stats['total_nets']}")
    print(f"  Nodes per net: {stats['min_nodes']} - {stats['max_nodes']}")
    print(f"  Average nodes: {stats['avg_nodes']:.2f}")

    print("\nNode Types:")
    for node_type, count in sorted(stats["node_types"].items()):
        print(f"  {node_type}: {count}")

    print("\nCongestion:")
    print(f"  Routing locations: {stats['total_routing_locations']}")
    print(f"  Congested: {stats['congested_locations']}")
    print(f"  Max congestion: {stats['max_congestion']}")
