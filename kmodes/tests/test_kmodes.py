"""
Tests for k-modes clustering algorithm
"""

import pickle
import unittest

import numpy as np
from sklearn.utils.testing import assert_equal

from kmodes import kmodes


SOYBEAN = np.array([
[4,0,2,1,1,1,0,1,0,2,1,1,0,2,2,0,0,0,1,0,3,1,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[5,0,2,1,0,3,1,1,1,2,1,1,0,2,2,0,0,0,1,1,3,0,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[3,0,2,1,0,2,0,2,1,1,1,1,0,2,2,0,0,0,1,0,3,0,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[6,0,2,1,0,1,1,1,0,0,1,1,0,2,2,0,0,0,1,1,3,1,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[4,0,2,1,0,3,0,2,0,2,1,1,0,2,2,0,0,0,1,0,3,1,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[5,0,2,1,0,2,0,1,1,0,1,1,0,2,2,0,0,0,1,1,3,1,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[3,0,2,1,0,2,1,1,0,1,1,1,0,2,2,0,0,0,1,1,3,0,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[3,0,2,1,0,1,0,2,1,2,1,1,0,2,2,0,0,0,1,0,3,0,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[6,0,2,1,0,3,0,1,1,1,1,1,0,2,2,0,0,0,1,0,3,1,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[6,0,2,1,0,1,0,1,0,2,1,1,0,2,2,0,0,0,1,0,3,1,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[6,0,0,2,1,0,2,1,0,0,1,1,0,2,2,0,0,0,1,1,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[4,0,0,1,0,2,3,1,1,1,1,1,0,2,2,0,0,0,1,0,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[5,0,0,2,0,3,2,1,0,2,1,1,0,2,2,0,0,0,1,0,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[6,0,0,1,1,3,3,1,1,0,1,1,0,2,2,0,0,0,1,0,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[3,0,0,2,1,0,2,1,0,1,1,1,0,2,2,0,0,0,1,0,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[4,0,0,1,1,1,3,1,1,1,1,1,0,2,2,0,0,0,1,1,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[3,0,0,1,0,1,2,1,0,0,1,1,0,2,2,0,0,0,1,0,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[5,0,0,2,1,2,2,1,0,2,1,1,0,2,2,0,0,0,1,1,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[6,0,0,2,0,1,3,1,1,0,1,1,0,2,2,0,0,0,1,0,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[5,0,0,2,1,3,3,1,1,2,1,1,0,2,2,0,0,0,1,0,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[0,1,2,0,0,1,1,1,1,1,1,0,0,2,2,0,0,0,1,0,1,1,0,1,1,0,0,3,4,0,0,0,0,0,0,'D3'],
[2,1,2,0,0,3,1,2,0,1,1,0,0,2,2,0,0,0,1,0,1,1,0,1,0,0,0,3,4,0,0,0,0,0,0,'D3'],
[2,1,2,0,0,2,1,1,0,2,1,0,0,2,2,0,0,0,1,0,1,1,0,1,1,0,0,3,4,0,0,0,0,0,0,'D3'],
[0,1,2,0,0,0,1,1,1,2,1,0,0,2,2,0,0,0,1,0,1,1,0,1,0,0,0,3,4,0,0,0,0,0,0,'D3'],
[0,1,2,0,0,2,1,1,1,1,1,0,0,2,2,0,0,0,1,0,1,1,0,1,0,0,0,3,4,0,0,0,0,0,0,'D3'],
[4,0,2,0,1,0,1,2,0,2,1,1,0,2,2,0,0,0,1,1,1,1,0,1,1,0,0,3,4,0,0,0,0,0,0,'D3'],
[2,1,2,0,0,3,1,2,0,2,1,0,0,2,2,0,0,0,1,0,1,1,0,1,1,0,0,3,4,0,0,0,0,0,0,'D3'],
[0,1,2,0,0,0,1,1,0,1,1,0,0,2,2,0,0,0,1,0,1,1,0,1,0,0,0,3,4,0,0,0,0,0,1,'D3'],
[3,0,2,0,1,3,1,2,0,1,1,0,0,2,2,0,0,0,1,1,1,1,0,1,1,0,0,3,4,0,0,0,0,0,0,'D3'],
[0,1,2,0,0,1,1,2,1,2,1,0,0,2,2,0,0,0,1,0,1,1,0,1,0,0,0,3,4,0,0,0,0,0,0,'D3'],
[2,1,2,1,1,3,1,2,1,2,1,1,0,2,2,0,0,0,1,0,2,2,0,1,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[0,1,1,1,0,1,1,1,0,0,1,1,0,2,2,0,0,0,1,0,1,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[3,1,2,0,0,1,1,2,1,0,1,1,0,2,2,0,0,0,1,0,2,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[2,1,2,1,1,1,1,2,0,2,1,1,0,2,2,0,0,0,1,0,1,2,0,1,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[1,1,2,0,0,3,1,1,1,2,1,1,0,2,2,0,0,0,1,0,2,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[1,1,2,1,0,0,1,2,1,1,1,1,0,2,2,0,0,0,1,0,2,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[0,1,2,1,0,3,1,1,0,0,1,1,0,2,2,0,0,0,1,0,1,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[2,1,2,0,0,1,1,2,0,0,1,1,0,2,2,0,0,0,1,0,1,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[3,1,2,0,0,2,1,2,1,1,1,1,0,2,2,0,0,0,1,0,2,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[3,1,1,0,0,2,1,2,1,2,1,1,0,2,2,0,0,0,1,0,2,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[0,1,2,1,1,1,1,1,0,0,1,1,0,2,2,0,0,0,1,0,1,2,0,1,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[1,1,2,1,1,3,1,2,0,1,1,1,0,2,2,0,0,0,1,1,1,2,0,1,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[1,1,2,0,0,0,1,2,1,0,1,1,0,2,2,0,0,0,1,0,2,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[1,1,2,1,1,2,3,1,1,1,1,1,0,2,2,0,0,0,1,0,2,2,0,1,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[2,1,1,0,0,3,1,2,0,2,1,1,0,2,2,0,0,0,1,0,1,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[0,1,1,1,1,2,1,2,1,0,1,1,0,2,2,0,0,0,1,1,2,2,0,1,0,0,0,3,4,0,0,0,0,0,1,'D4'],
[0,1,2,1,0,3,1,1,0,2,1,1,0,2,2,0,0,0,1,0,1,2,0,0,0,0,0,3,4,0,0,0,0,0,1,'D4'],
])
# Drop target column
SOYBEAN = SOYBEAN[:, :35]

SOYBEAN2 = np.array([
[4,0,2,1,1,1,0,1,0,1,1,1,0,2,2,0,0,0,1,0,3,0,1,1,0,0,0,0,4,0,0,0,0,0,0,'D1'],
[7,0,0,2,1,0,2,1,0,0,1,1,0,2,2,0,0,0,1,1,0,3,0,0,0,2,1,0,4,0,0,0,0,0,0,'D2'],
[0,1,2,0,0,1,1,1,1,2,1,0,0,2,2,0,0,0,1,0,1,1,0,1,0,0,0,3,4,0,0,0,0,0,0,'D3'],
[2,1,2,1,1,3,1,2,1,1,1,1,0,2,2,0,0,0,1,1,1,2,0,1,0,0,0,3,4,0,0,0,0,0,1,'D4'],
])
# Drop target column
SOYBEAN2 = SOYBEAN2[:, :35]


class TestKModes(unittest.TestCase):

    def test_pickle(self):
        obj = kmodes.KModes()
        s = pickle.dumps(obj)
        assert_equal(type(pickle.loads(s)), obj.__class__)

    def test_kmodes_huang_soybean(self):
        np.random.seed(42)
        kmodes_huang = kmodes.KModes(n_clusters=4, n_init=2, init='Huang', verbose=2)
        result = kmodes_huang.fit_predict(SOYBEAN)
        expected = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1,
                             2, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 1])
        np.testing.assert_array_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint8))

    def test_kmodes_cao_soybean(self):
        kmodes_cao = kmodes.KModes(n_clusters=4, init='Cao', verbose=2)
        result = kmodes_cao.fit_predict(SOYBEAN)
        expected = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
                             1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        np.testing.assert_array_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint8))

    def test_kmodes_predict_soybean(self):
        kmodes_cao = kmodes.KModes(n_clusters=4, init='Cao', verbose=2)
        kmodes_cao = kmodes_cao.fit(SOYBEAN)
        result = kmodes_cao.predict(SOYBEAN2)
        expected = np.array([2, 1, 3, 0])
        np.testing.assert_array_equal(result, expected)
        self.assertTrue(result.dtype == np.dtype(np.uint8))

    def test_kmodes_predict_unfitted(self):
        kmodes_cao = kmodes.KModes(n_clusters=4, init='Cao', verbose=2)
        with self.assertRaises(AssertionError):
            kmodes_cao.predict(SOYBEAN)
        with self.assertRaises(AttributeError):
            kmodes_cao.cluster_centroids_

    def test_kmodes_random_soybean(self):
        kmodes_random = kmodes.KModes(n_clusters=4, init='random', verbose=2)
        result = kmodes_random.fit(SOYBEAN)
        self.assertIsInstance(result, kmodes.KModes)

    def test_kmodes_init_soybean(self):
        init_vals = np.array(
            [[0, 1, 2, 1, 0, 3, 1, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2,
              0, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 0, 1],
             [4, 0, 0, 1, 1, 1, 3, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 0, 3,
              0, 0, 0, 2, 1, 0, 4, 0, 0, 0, 0, 0, 0],
             [3, 0, 2, 1, 0, 2, 0, 2, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 0,
              1, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
             [3, 0, 2, 0, 1, 3, 1, 2, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1,
              0, 1, 1, 0, 0, 3, 4, 0, 0, 0, 0, 0, 0]])
        kmodes_init = kmodes.KModes(n_clusters=4, init=init_vals, verbose=2)
        result = kmodes_init.fit_predict(SOYBEAN)
        expected = np.array([2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1,
                             1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        np.testing.assert_array_equal(result, expected)

        # 5 initial centroids, 4 n_clusters
        init_vals = np.array(
            [[0, 1],
             [4, 0],
             [4, 0],
             [3, 0],
             [3, 0]])
        kmodes_init = kmodes.KModes(n_clusters=4, init=init_vals, verbose=2)
        with self.assertRaises(AssertionError):
            kmodes_init.fit(SOYBEAN)

        # wrong number of attributes
        init_vals = np.array(
            [0, 1, 2, 3])
        kmodes_init = kmodes.KModes(n_clusters=4, init=init_vals, verbose=2)
        with self.assertRaises(AssertionError):
            kmodes_init.fit(SOYBEAN)

    def test_kmodes_empty_init_cluster_soybean(self):
        # Check if the clustering does not crash in case of an empty cluster.
        init_vals = np.array(
            [[0, 1, 2, 1, 0, 3, 1, 1, 0, 2, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 1, 2,
              0, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 0, 1],
             [4, 0, 0, 1, 1, 1, 3, 1, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 1, 0, 3,
              0, 0, 0, 2, 1, 0, 4, 0, 0, 0, 0, 0, 0],
             [3, 0, 2, 1, 0, 2, 0, 2, 1, 1, 1, 1, 0, 2, 2, 0, 0, 0, 1, 0, 3, 0,
              1, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0],
             [3, 0, 2, 0, 1, 3, 1, 2, 0, 1, 1, 0, 0, 2, 2, 0, 0, 0, 1, 1, 1, 1,
              0, 1, 1, 0, 0, 3, 4, 0, 0, 0, 0, 0, 0]])
        kmodes_init = kmodes.KModes(n_clusters=4, init=init_vals, verbose=2)
        result = kmodes_init.fit(SOYBEAN)
        self.assertIsInstance(result, kmodes.KModes)

    def test_kmodes_unknowninit_soybean(self):
        with self.assertRaises(NotImplementedError):
            kmodes.KModes(n_clusters=4, init='nonsense', verbose=2).fit(SOYBEAN)

    def test_kmodes_nunique_nclusters(self):
        data = np.array([
            [0, 1],
            [0, 1],
            [0, 1],
            [0, 2],
            [0, 2],
            [0, 2]
        ])
        np.random.seed(42)
        kmodes_cao = kmodes.KModes(n_clusters=6, init='Cao', verbose=2)
        result = kmodes_cao.fit_predict(data, categorical=[1])
        expected = np.array([0, 0, 0, 1, 1, 1])
        np.testing.assert_array_equal(result, expected)
        np.testing.assert_array_equal(kmodes_cao.cluster_centroids_,
                                      np.array([[0, 1],
                                                [0, 2]]))


if __name__ == '__main__':
    unittest.main()
