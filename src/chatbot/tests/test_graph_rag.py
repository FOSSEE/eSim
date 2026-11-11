import unittest
from chatbot.graph_rag import eSimGraphRAG

class TestGraphRAG(unittest.TestCase):
    def setUp(self):
        self.graph_rag = eSimGraphRAG()

    def test_lm741_topology_extraction(self):
        query = "How do I wire an LM741 operational amplifier in eSim?"
        context = self.graph_rag.get_topology_context(query)
        self.assertIn("LM741", context)
        self.assertIn("Dual_Power_Supply", context)
        self.assertIn("LM741.sub", context)

    def test_bc547_base_resistor_rule(self):
        query = "Why is my BC547 transistor simulation burning out?"
        context = self.graph_rag.get_topology_context(query)
        self.assertIn("BC547", context)
        self.assertIn("Base_Resistor", context)

    def test_irrelevant_query(self):
        query = "What is the capital of France?"
        context = self.graph_rag.get_topology_context(query)
        self.assertEqual(context, "")

if __name__ == '__main__':
    unittest.main()
