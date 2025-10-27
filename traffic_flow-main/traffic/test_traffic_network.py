import unittest
import traffic_network
import networkx as nx

class TestTrafficNetwork(unittest.TestCase):

    def test_max_vehicule_sans_ville(self):
        """Test du débit maximal sans contrainte sur les villes (Q1)"""
        flow, flow_dict = traffic_network.max_vehicule()
        self.assertEqual(flow, 18)  

    def test_max_vehicule_avec_ville(self):
        """Test du débit maximal avec contraintes sur les villes (Q2)"""
        flow, flow_dict = traffic_network.max_vehicule_avec_flux()
        self.assertEqual(flow, 16)  
        
        # Vérification que les contraintes villes sont respectées
        G = traffic_network.crea_graph_ville_cap()
        for ville in traffic_network.ville_cap:
            self.assertLessEqual(
                flow_dict[f"{ville}_in"][f"{ville}_out"],
                G[f"{ville}_in"][f"{ville}_out"]["capacity"]
            )

    def test_graphe_sans_ville_complet(self):
        """Test complet de la structure du graphe sans contraintes"""
        G = traffic_network.crea_traffic_graph()
        
        # Test des noeuds
        expected_nodes = {"E", "a", "b", "c", "d", "e", "f", "g", "S"}
        self.assertEqual(set(G.nodes), expected_nodes)
        
        # Test des capa
        self.assertEqual(G["E"]["a"]["capacity"], 5)
        self.assertEqual(G["g"]["S"]["capacity"], 10)   

    def test_graphe_avec_ville_structure(self):
        """Test complet de la structure avec contraintes"""
        G = traffic_network.crea_graph_ville_cap()
        
        # Vérification du split des villes
        for ville in traffic_network.ville_cap:
            self.assertIn(f"{ville}_in", G.nodes)
            self.assertIn(f"{ville}_out", G.nodes)
            self.assertIn((f"{ville}_in", f"{ville}_out"), G.edges)
            self.assertEqual(
                G[f"{ville}_in"][f"{ville}_out"]["capacity"],
                traffic_network.ville_cap[ville]
            )
        
        # Vérification des connexions entrantes/sortantes
        self.assertIn(("E", "a_in"), G.edges)
        self.assertIn(("b_out", "c_in"), G.edges)
        self.assertIn(("g_out", "S"), G.edges)

    def test_noeuds_inexistants(self):
        """Test avec source/destination inexistantes"""
        with self.assertRaises(nx.NetworkXError):
            traffic_network.max_vehicule(source="X", sink="Y")
        
        with self.assertRaises(nx.NetworkXError):
            traffic_network.max_vehicule_avec_flux(source="X", sink="Y")

if __name__ == "__main__":
    unittest.main()
