from typeguard.importhook import install_import_hook
import unittest

with install_import_hook('utilities.functional.dict'):
    from ..functional.dict import FunctionalDict, dmap, dzip, merge_dicts, rmerge_dicts


class FuncDictTest(unittest.TestCase):
    def test_subset_keys(self):
        fd = FunctionalDict({'foo': 'hello',
                             'bar': 'world',
                             'baz': 'spam',
                             'moo': 'polly',
                             'myon': 'ni'})
        self.assertEqual({'foo': 'hello',
                          'bar': 'world'},
                         fd.copy_subset(whitelist=('foo', 'bar', 'baz', 'fyon'),
                                        blacklist=('baz', 'moo', 'nargle')))
        self.assertEqual({'bar': 'world',
                          'moo': 'polly'},
                         fd.only_keys({'bar', 'moo', 'fyon'}))
        self.assertEqual({'foo': 'hello',
                          'baz': 'spam',
                          'myon': 'ni'},
                         fd.without_keys(['bar', 'moo', 'fyon']))

    def test_map(self):
        d1 = {'foo': 7,
              'bar': 'spam',
              'baz': [0, 1, 2]}
        self.assertEqual({'foofoo': 7,
                          'barbar': 'spam',
                          'bazbaz': [0, 1, 2]},
                         dmap(lambda x: x * 2, d1, mapvalues=False))
        self.assertEqual({'foo': 14,
                          'bar': 'spamspam',
                          'baz': [0, 1, 2, 0, 1, 2]},
                         dmap(lambda x: x * 2, d1, mapkeys=False))
        self.assertEqual({'foofoo': ('foo', 7),
                          'barbar': ('bar', 'spam'),
                          'bazbaz': ('baz', [0, 1, 2])},
                         dmap(lambda k, v: (k * 2, (k, v)), d1))
        with self.assertRaises(ValueError):
            dmap(lambda x: x, d1, mapkeys=False, mapvalues=False)

        d2 = {'foo': 2,
              'moo': 4}
        self.assertEqual({'foo': 5},
                         dmap(lambda x, y: x - y, d1, d2, mapkeys=False))

        # Incorrect number of inputs
        with self.assertRaises(TypeError):
            dmap(lambda x: x, d1, d1, mapkeys=False)

    def test_zip(self):
        d1 = {'foo': 1,
              'bar': 2,
              'baz': 3}
        self.assertEqual({'foo': (1, 1, 1),
                          'bar': (2, 2, 2),
                          'baz': (3, 3, 3)},
                         dzip(d1, d1, d1))
        self.assertEqual({}, dzip(d1, {}))

        d2 = {'foo': 10,
              'bar': 11,
              'myon': 12}
        d3 = {'foo': 'a',
              'bar': 'b',
              'fru': 'c'}
        self.assertEqual({'foo': (1, 10, 'a'),
                          'bar': (2, 11, 'b')},
                         dzip(d1, d2, d3))

        d4 = {'hello': 'goodbye',
              'global': 'local'}
        self.assertEqual({}, dzip(d1, d4))

    def test_merge(self):
        # Common subset with rmerge_dicts()
        d1 = {'foo': 1,
              'bar': 2}
        d2 = {'foo': 1,
              'baz': 3}
        self.assertEqual({'foo': 1, 'bar': 2, 'baz': 3}, merge_dicts(d1, d2))

        d3 = {'foo': 5,
              'moo': 4}
        with self.assertRaises(ValueError):
            merge_dicts(d1, d3)

        d4 = {'foo': 1,
              'bar': {'hello': 'abcd',
                      'world': 'dcba'}}
        d5 = {'bar': {'hello': 'abcd',
                      'world': 'dcba'},
              'baz': 3}
        d6 = {'bar': {'moo': 'xyzzy',
                      'myon': 'syzygy'},
              'baz': 3}
        self.assertEqual({'foo': 1,
                          'bar': {'hello': 'abcd',
                                  'world': 'dcba'},
                          'baz': 3}, merge_dicts(d4, d5))

        # Differing behaviour with rmerge_dicts()
        with self.assertRaises(ValueError):
            merge_dicts(d4, d6)

    def test_rmerge(self):
        # Common subset with merge_dicts()
        d1 = {'foo': 1,
              'bar': 2}
        d2 = {'foo': 1,
              'baz': 3}
        self.assertEqual({'foo': 1, 'bar': 2, 'baz': 3}, rmerge_dicts(d1, d2))

        d3 = {'foo': 5,
              'moo': 4}
        with self.assertRaises(ValueError):
            rmerge_dicts(d1, d3)

        d4 = {'foo': 1,
              'bar': {'hello': 'abcd',
                      'world': 'dcba'}}
        d5 = {'bar': {'hello': 'abcd',
                      'world': 'dcba'},
              'baz': 3}
        d6 = {'bar': {'moo': 'xyzzy',
                      'myon': 'syzygy'},
              'baz': 3}
        self.assertEqual({'foo': 1,
                          'bar': {'hello': 'abcd',
                                  'world': 'dcba'},
                          'baz': 3}, merge_dicts(d4, d5))

        # Differing behaviour with merge_dicts()
        self.assertEqual({'foo': 1,
                          'bar': {'hello': 'abcd',
                                  'world': 'dcba',
                                  'moo': 'xyzzy',
                                  'myon': 'syzygy'},
                          'baz': 3}, rmerge_dicts(d4, d6))

        d7 = {'bar': {'hello': 'something'}}
        with self.assertRaises(ValueError):
            rmerge_dicts(d4, d7)

        d8 = {'bar': {'hello': 'abcd'},
              'baz': 3,
              'fru': 'orchid'}
        d9 = {'foo': 1,
              'baz': 3}
        self.assertEqual({'foo': 1,
                          'bar': {'hello': 'abcd',
                                  'world': 'dcba',
                                  'moo': 'xyzzy',
                                  'myon': 'syzygy'},
                          'baz': 3,
                          'fru': 'orchid'}, rmerge_dicts(d4, d6, d8, d9))


if __name__ == '__main__':
    unittest.main()
