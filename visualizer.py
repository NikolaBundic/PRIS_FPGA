import matplotlib.pyplot as plt
import matplotlib.patches as patches


def visualize_routing(data, net_ids = None, max_nets = 10):
    #Visualization of FPGA routing
    fig, ax = plt.subplots(figsize=(12, 10))

    #Grid
    for x in range(data["width"] + 1):
        for y in range(data["height"] + 1):
            rect = patches.Rectangle(
                (x - 0.4, y - 0.4),
                0.8,
                0.8,
                facecolor = "lightgray",
                edgecolor = "gray",
                alpha = 0.5,
            )
            ax.add_patch(rect)

    #Nets
    nets = (
        data["nets"][:max_nets]
        if net_ids is None
        else [n for n in data["nets"] if n["id"] in net_ids]
    )
    colors = plt.cm.tab20(range(len(nets)))

    #Draw nets
    for i, net in enumerate(nets):
        coords = [(n["x"], n["y"]) for n in net["nodes"]]

        # Draw lines
        for j in range(len(coords) - 1):
            ax.plot(
                [coords[j][0], coords[j + 1][0]],
                [coords[j][1], coords[j + 1][1]],
                color = colors[i],
                linewidth = 2,
                alpha = 0.7,
                label = f"Net {net['id']}" if j == 0 else "",
            )

        #Draw source/sink
        for node in net["nodes"]:
            if node["type"] == "SOURCE":
                ax.scatter(
                    node["x"],
                    node["y"],
                    c = "green",
                    s = 100,
                    marker = "s",
                    edgecolors = "black",
                    zorder = 5
                )
            elif node["type"] == "SINK":
                ax.scatter(
                    node["x"],
                    node["y"],
                    c = "red",
                    s = 80,
                    marker = "o",
                    edgecolors = "black",
                    zorder = 5
                )

    ax.set_xlim(-0.5, data["width"] + 0.5)
    ax.set_ylim(-0.5, data["height"] + 0.5)
    ax.set_aspect("equal")
    ax.legend(bbox_to_anchor = (1.05, 1), loc = "upper left")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig