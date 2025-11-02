"""Main application"""

import argparse
import matplotlib.pyplot as plt
from parser import parse_route_file
from visualizer import visualize_routing
from analyzer import analyze_routing, print_analysis


def main():
    parser = argparse.ArgumentParser(description="FPGA Route Visualizer")
    parser.add_argument("route_file", help="Path to .route file")
    parser.add_argument(
        "-v", "--visualize", action="store_true", help="Show visualization"
    )
    parser.add_argument("-a", "--analyze", action="store_true", help="Show analysis")
    parser.add_argument("-o", "--output", help="Save visualization to file")
    parser.add_argument(
        "--nets", nargs="+", type=int, help="Specific net IDs to visualize"
    )
    parser.add_argument(
        "--max-nets", type=int, default=10, help="Max nets to show (default: 10)"
    )

    args = parser.parse_args()

    # Parse file
    print(f"Parsing {args.route_file}...")
    try:
        data = parse_route_file(args.route_file)
        print(
            f"Parsed {data['width']}x{data['height']} FPGA with {len(data['nets'])} nets"
        )
    except Exception as e:
        print(f"Error: {e}")
        return 1

    # Analysis
    if args.analyze:
        stats = analyze_routing(data)
        print_analysis(stats)

    # Visualization
    if args.visualize or args.output:
        print("Generating visualization...")
        fig = visualize_routing(data, args.nets, args.max_nets)

        if args.output:
            fig.savefig(args.output, dpi=300, bbox_inches="tight")
            print(f"Saved to {args.output}")

        if args.visualize:
            plt.show()

    if not args.visualize and not args.analyze and not args.output:
        print("Use --help for usage information")
        return 1

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
