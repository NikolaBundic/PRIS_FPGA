"""Parse .route files"""

import re


def parse_route_file(filename):
    """Parse route file and return dictionary with all data"""
    with open(filename, "r") as f:
        content = f.read()

    # Parse header
    size_match = re.search(r"Array size: (\d+) x (\d+)", content)
    width, height = int(size_match.group(1)), int(size_match.group(2))

    # Parse nets
    nets = []
    net_pattern = r"Net (\d+) \(([^)]+)\)(.*?)(?=Net \d+|\Z)"

    for net_match in re.finditer(net_pattern, content, re.DOTALL):
        net_id = int(net_match.group(1))
        net_name = net_match.group(2)
        net_content = net_match.group(3)

        # Parse nodes
        nodes = []
        node_pattern = r"Node:\s*\d+\s+(\w+)\s*\((\d+),(\d+),(\d+)\)"
        for node_match in re.finditer(node_pattern, net_content):
            nodes.append(
                {
                    "type": node_match.group(1),
                    "x": int(node_match.group(2)),
                    "y": int(node_match.group(3)),
                    "z": int(node_match.group(4)),
                }
            )

        nets.append({"id": net_id, "name": net_name, "nodes": nodes})

    return {"width": width, "height": height, "nets": nets}
    