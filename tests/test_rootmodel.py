import os
import tempfile
import json
import unittest
from backend import RootModel

class TestRootModel(unittest.TestCase):
    def test_add_and_persist(self):
        with tempfile.TemporaryDirectory() as td:
            m = RootModel(data_dir=td)
            m.clear_history()
            m.add_result('TAI')
            m.add_result('XIU')
            m2 = RootModel(data_dir=td)
            self.assertEqual(m2.history[0], 'XIU')
            self.assertEqual(m2.history[1], 'TAI')

    def test_longest_run(self):
        m = RootModel(data_dir=tempfile.gettempdir())
        m.history = ['TAI', 'XIU', 'TAI', 'TAI']
        self.assertEqual(m.longest_run('TAI'), 2)
        self.assertEqual(m.longest_run('XIU'), 1)

    def test_predict_markov_basic(self):
        m = RootModel(data_dir=tempfile.gettempdir())
        m.history = ['TAI', 'XIU', 'TAI', 'TAI']
        probs = m.predict_markov_probs()
        self.assertIsNotNone(probs)
        p_tai, p_xiu = probs
        self.assertAlmostEqual(p_tai, 0.5)
        self.assertAlmostEqual(p_xiu, 0.5)

    def test_predict_markov_all_same(self):
        m = RootModel(data_dir=tempfile.gettempdir())
        m.history = ['TAI', 'TAI', 'TAI']
        probs = m.predict_markov_probs()
        self.assertAlmostEqual(probs[0], 1.0)
        self.assertAlmostEqual(probs[1], 0.0)

    def test_fallback_when_no_transitions(self):
        m = RootModel(data_dir=tempfile.gettempdir())
        m.history = ['XIU', 'TAI']
        probs = m.predict_markov_probs()
        self.assertAlmostEqual(probs[0], 0.5)
        self.assertAlmostEqual(probs[1], 0.5)

    def test_add_invalid_result_raises(self):
        with tempfile.TemporaryDirectory() as td:
            m = RootModel(data_dir=td)
            m.clear_history()
            with self.assertRaises(ValueError):
                m.add_result('INVALID')

    def test_export_json_creates_file(self):
        with tempfile.TemporaryDirectory() as td:
            m = RootModel(data_dir=td)
            m.clear_history()
            m.add_result('TAI')
            out = m.export_json()
            self.assertTrue(os.path.exists(out))
            with open(out, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.assertEqual(data, m.history)

    def test_predict_markov_none_when_insufficient(self):
        with tempfile.TemporaryDirectory() as td:
            m = RootModel(data_dir=td)
            m.clear_history()
            m.history = ['TAI']
            self.assertIsNone(m.predict_markov_probs())

if __name__ == '__main__':
    unittest.main()
