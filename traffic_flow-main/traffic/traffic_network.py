"""
    Ce module modélise un réseau routier et calcule le débit maximal de véhicules entre deux points (E et S),
    avec ou sans contraintes de capacité sur les villes (nœuds).

    Questions abordées :
    - Question 1 : Débit maximal avec seulement les capacités des routes.
    - Question 2 : Débit maximal avec capacités sur les routes et sur les villes.
"""

import networkx as nx

## Question 1

"""
    Crée le graphe orienté représentant le réseau routier sans contrainte sur les villes.
"""
def crea_traffic_graph():
    G = nx.DiGraph()

    arete = [
        ("E", "a", 5),
        ("E", "b", 10),
        ("E", "e", 8),
        ("a", "c", 7),
        ("a", "d", 10),
        ("b", "c", 8),
        ("b", "d", 2),
        ("b", "e", 1),
        ("c", "g", 7),
        ("d", "g", 4),
        ("d", "f", 2),
        ("d", "S", 6),
        ("e", "f", 4),
        ("f", "S", 6),
        ("g", "S", 10),
    ]

    for u, v, cap in arete:
        G.add_edge(u, v, capacity=cap)

    return G

"""
    Calcule le débit maximal entre deux points dans le graphe sans contrainte sur les villes.
"""
def max_vehicule(source="E", sink="S"):
    G = crea_traffic_graph()
    flow_value, flow_dict = nx.maximum_flow(G, source, sink, flow_func=nx.algorithms.flow.edmonds_karp)
    return flow_value, flow_dict

## Question 2 et 3

ville_cap = {
    "a": 6,
    "b": 7,
    "c": 8,
    "d": 6,
    "e": 6,
    "f": 5,
    "g": 9,
}

"""
    Crée le graphe orienté représentant le réseau routier avec contrainte sur les villes.
"""
def crea_graph_ville_cap():
    H = nx.DiGraph()

    arete = [
        ("E", "a", 5),
        ("E", "b", 10),
        ("E", "e", 8),
        ("a", "c", 7),
        ("a", "d", 10),
        ("b", "c", 8),
        ("b", "d", 2),
        ("b", "e", 1),
        ("c", "g", 7),
        ("d", "g", 4),
        ("d", "f", 2),
        ("d", "S", 6),
        ("e", "f", 4),
        ("f", "S", 6),
        ("g", "S", 10),
    ]

    for ville, cap in ville_cap.items():
        H.add_edge(f"{ville}_in", f"{ville}_out", capacity=cap)

    for u, v, cap in arete:
        u_ = f"{u}_out" if u in ville_cap else u
        v_ = f"{v}_in" if v in ville_cap else v
        H.add_edge(u_ , v_, capacity=cap)

    return H

"""
    Calcul le débit maximal de véhicules entre la source et la destination
    en tenant compte des limites de capacité des villes.
"""
def max_vehicule_avec_flux(source="E", sink="S"):
    G = crea_graph_ville_cap()
    flow_value, flow_dict = nx.maximum_flow(G, source, sink, flow_func=nx.algorithms.flow.edmonds_karp)
    return flow_value, flow_dict


## Question 4
"""
    Analyse  de la variation du débit maximal lorsque la capacité de la ville d varie
"""
def variation_d(plage=range(2, 10), source="E", sink="S"):
    resultats = {}

    for cap_d in plage:
        ville_cap_modif = ville_cap.copy()
        ville_cap_modif["d"] = cap_d

        G = nx.DiGraph()

        for ville, cap in ville_cap_modif.items():
            G.add_edge(f"{ville}_in", f"{ville}_out", capacity=cap)

        arete = [
            ("E", "a", 5),
            ("E", "b", 10),
            ("E", "e", 8),
            ("a", "c", 7),
            ("a", "d", 10),
            ("b", "c", 8),
            ("b", "d", 2),
            ("b", "e", 1),
            ("c", "g", 7),
            ("d", "g", 4),
            ("d", "f", 2),
            ("d", "S", 6),
            ("e", "f", 4),
            ("f", "S", 6),
            ("g", "S", 10),
        ]

        for u, v, cap in arete:
            u_ = f"{u}_out" if u in ville_cap_modif else u
            v_ = f"{v}_in" if v in ville_cap_modif else v
            G.add_edge(u_, v_, capacity=cap)

        flow_value, _ = nx.maximum_flow(G, source, sink, flow_func=nx.algorithms.flow.edmonds_karp)
        resultats[cap_d] = flow_value

    return resultats
