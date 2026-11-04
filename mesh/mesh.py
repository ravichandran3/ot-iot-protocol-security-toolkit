# mesh.py - bedside-monitor mesh: sybil route attraction vs signed next-hop allowlist.
import networkx as nx

MONITORS = [f"m{i}" for i in range(8)]
STATION, ATTACKER, CORE = "station", "x", "core"


def topology(sybil: bool) -> nx.Graph:
    G = nx.Graph()
    G.add_edges_from([(f"m{i}", "r0") for i in range(4)])
    G.add_edges_from([(f"m{i}", "r1") for i in range(4, 8)])
    G.add_edges_from([("r0", "r1"), ("r0", CORE), ("r1", CORE), (CORE, STATION)])
    if sybil:
        G.add_edges_from([(m, ATTACKER) for m in MONITORS] + [(ATTACKER, STATION)])
    return G


def route(G, src, dst, allowed):
    path, cur = [src], src
    for _ in range(12):
        if cur == dst:
            return path
        hops = [n for n in G[cur] if n != cur]
        hops.sort(key=lambda n: nx.shortest_path_length(G, n, dst)
                  if nx.has_path(G, n, dst) else 99)
        nxt = next((n for n in hops if n in allowed), None)
        if nxt is None:
            return None
        path.append(nxt)
        cur = nxt
    return None


def deliver(G, allowed, blackhole=None):
    ok, hops = 0, []
    for m in MONITORS:
        path = route(G, m, STATION, allowed)
        if path and not (blackhole and blackhole in path):
            ok += 1
            hops.append(len(path) - 1)
    return ok, (sum(hops) / len(hops) if hops else 0.0)


if __name__ == "__main__":
    legit = topology(sybil=False)
    every = set(legit)
    ok, mean = deliver(legit, every)
    print(f"baseline  delivered {ok}/8 mean_hops {mean:.1f}")

    attacked = topology(sybil=True)
    every = set(attacked)
    ok, mean = deliver(attacked, every, blackhole=ATTACKER)
    path = route(attacked, "m0", STATION, every)
    print(f"sybil     delivered {ok}/8 mean_hops {mean:.1f} path {'->'.join(path)}")

    signed = set(attacked) - {ATTACKER}
    ok, mean = deliver(attacked, signed, blackhole=ATTACKER)
    path = route(attacked, "m0", STATION, signed)
<<<<<<< HEAD
    print(f"allowlist delivered {ok}/8 mean_hops {mean:.1f} path {'->'.join(path)}")
=======
    print(f"allowlist delivered {ok}/8 mean_hops {mean:.1f} path {'->'.join(path)}")
>>>>>>> d160e37 (Add toolkit files)
