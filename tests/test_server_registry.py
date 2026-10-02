import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from validate_server_registry import DEFAULT_REGISTRY, load_registry, unique_object, validate_registry


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.entry = {'ID': 'synthetic', 'ServerAddress': 'example.invalid'}

    def test_shipped_registry_and_upstream_port_fix(self):
        entries = load_registry(DEFAULT_REGISTRY)
        server = next(e for e in entries if e['ID'] == 'xmutantson 0')
        self.assertEqual((server['Port'], server['InfoPort']), (7778, 7778))

    def test_omitted_ports_and_optional_properties(self):
        self.assertEqual(validate_registry([self.entry]), 1)

    def test_port_boundaries(self):
        for port in (1, 65535):
            self.assertEqual(validate_registry([dict(self.entry, Port=port, InfoPort=port)]), 1)

    def test_invalid_ports(self):
        for field in ('Port', 'InfoPort'):
            for port in (0, -1, 65536, True, None, '7778', 7778.5):
                with self.subTest(field=field, port=port), self.assertRaises(ValueError):
                    validate_registry([dict(self.entry, **{field: port})])

    def test_duplicate_id(self):
        with self.assertRaisesRegex(ValueError, 'duplicate ID'):
            validate_registry([self.entry, dict(self.entry, Port=7778)])

    def test_duplicate_default_endpoint_case_insensitive(self):
        with self.assertRaisesRegex(ValueError, 'duplicate game endpoint'):
            validate_registry([self.entry, dict(self.entry, ID='other', ServerAddress='EXAMPLE.INVALID', Port=7777)])

    def test_distinct_ports_same_host(self):
        self.assertEqual(validate_registry([self.entry, dict(self.entry, ID='other', Port=7778)]), 2)

    def test_invalid_shapes(self):
        for entries in ({}, [], None, [None], ['server']):
            with self.subTest(entries=entries), self.assertRaises(ValueError):
                validate_registry(entries)

    def test_required_strings(self):
        for field in ('ID', 'ServerAddress'):
            for value in ('', ' ', ' padded ', None, 42):
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    validate_registry([dict(self.entry, **{field: value})])

    def test_url_and_whitespace_are_not_hosts(self):
        for host in ('https://example.invalid', 'example.invalid/path', 'example .invalid'):
            with self.subTest(host=host), self.assertRaises(ValueError):
                validate_registry([dict(self.entry, ServerAddress=host)])

    def test_optional_types_and_typos(self):
        for extra in ({'Hidden': 'true'}, {'ValidatesLoadout': 1}, {'Region': []}, {'Infoport': 7778}):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                validate_registry([dict(self.entry, **extra)])

    def test_duplicate_json_properties(self):
        with self.assertRaisesRegex(ValueError, 'duplicate JSON property'):
            json.loads('{"Port":7777,"Port":7778}', object_pairs_hook=unique_object)

    def test_validation_does_not_mutate(self):
        original = copy.deepcopy(self.entry)
        validate_registry([self.entry])
        self.assertEqual(self.entry, original)


if __name__ == '__main__':
    unittest.main()
