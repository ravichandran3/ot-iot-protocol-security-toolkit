# cable.py - landing-station reachability: flat network, zoning, OOB bypass, broker.
import networkx as nx

CRITICAL = ["slte_data", "slte_mgmt", "pfe", "pfe_mgmt", "scada"]


def flat() -> nx.Graph:
    G = nx.Graph()
    G.add_edges_from([
        ("internet", "web"), ("internet", "noc"),
        ("web", "corp"), ("noc", "corp"),
        ("corp", "station"), ("corp", "oob"),
        ("station", "scada"), ("station", "slte_data"),
        ("scada", "pfe"),
        ("oob", "slte_mgmt"), ("oob", "pfe_mgmt"),
        ("slte_mgmt", "slte_data"), ("pfe_mgmt", "pfe"),
    ])
    return G


def reachable(G, src="internet", blocked=()):
    seen, stack = {src}, [src]
    while stack:
        cur = stack.pop()
        for nxt in G[cur]:
            if nxt in blocked or nxt in seen:
                continue
            seen.add(nxt)
            stack.append(nxt)
    return seen


def report(label, G, blocked=()):
    seen = reachable(G, blocked=blocked)
    crit = [c for c in CRITICAL if c in seen]
    try:
        path = nx.shortest_path(G, "internet", "pfe")
        hops, route = len(path) - 1, "->".join(path)
    except nx.NetworkXNoPath:
        hops, route = None, "-"
    print(f"{label:<38} critical {len(crit)}/5 hops_to_pfe {str(hops):>4}  {route}")
    return seen


if __name__ == "__main__":
    base = flat()
    print("nodes", base.number_of_nodes(), "edges", base.number_of_edges())
    report("flat network", base)

    cut_station = base.copy()
    cut_station.remove_edge("corp", "station")
    report("cut corp->station only", cut_station)

    cut_both = cut_station.copy()
    cut_both.remove_edge("corp", "oob")
    report("+ cut corp->oob", cut_both)

    nocpath = cut_both.copy()
    nocpath.add_edge("noc", "station")
    report("+ sanctioned NOC->station path", nocpath)

    broker = nocpath.copy()
    broker.remove_edge("noc", "station")
    broker.add_edges_from([("noc", "broker"), ("broker", "station")])
    report("+ broker, unauthenticated", broker, blocked={"broker"})
    report("+ broker, authenticated", broker)

    print("min edge cut internet->slte_data", sorted(nx.minimum_edge_cut(base, "internet", "slte_data")))
    print("min edge cut internet->pfe      ", sorted(nx.minimum_edge_cut(base, "internet", "pfe")))
    for n in ("corp", "oob", "station"):
        rest = base.copy()
        rest.remove_node(n)
        alive = [c for c in CRITICAL if nx.has_path(rest, "internet", c)]
        print(f"remove node {n:<8} critical still reachable {len(alive)}/5")
