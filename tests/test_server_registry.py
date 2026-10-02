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

    def test_valid_hostname_and_ipv4_forms(self):
        for host in ('localhost', 'EXAMPLE.invalid.', 'node-1.example.invalid',
                     'xn--bcher-kva.invalid', '192.0.2.1', '0.0.0.0', '255.255.255.255',
                     'a' * 63 + '.invalid', '.'.join(['a' * 63] * 3 + ['b' * 61])):
            with self.subTest(host=host):
                entry = dict(self.entry, ServerAddress=host, Port=7778, InfoPort=7777)
                original = copy.deepcopy(entry)
                self.assertEqual(validate_registry([entry]), 1)
                self.assertEqual(entry, original)

    def test_invalid_hostname_and_ipv4_forms(self):
        for host in ('example.invalid:7778', '192.0.2.1:7778', '[::1]', '::1',
                     'bad_name.invalid', '-bad.invalid', 'bad-.invalid', 'a..invalid',
                     '.example.invalid', 'example.invalid..', '.', 'host!invalid',
                     'a' * 64 + '.invalid', '.'.join(['a' * 63] * 4),
                     '256.0.0.1', '192.0.2', '127.1', '2130706433', '192.00.2.1',
                     '192.0.2.1.', '0x7f000001', '0x7f.0.0.1', 'host.123',
                     'example.invalid\\path', 'bücher.invalid'):
            with self.subTest(host=host), self.assertRaises(ValueError):
                validate_registry([dict(self.entry, ServerAddress=host)])

    def test_terminal_dns_dot_is_same_game_endpoint(self):
        with self.assertRaisesRegex(ValueError, 'duplicate game endpoint'):
            validate_registry([self.entry, dict(self.entry, ID='other',
                              ServerAddress='EXAMPLE.INVALID.', InfoPort=9999)])

    def test_terminal_dns_dot_with_distinct_game_port(self):
        self.assertEqual(validate_registry([self.entry, dict(self.entry, ID='other',
                         ServerAddress='EXAMPLE.INVALID.', Port=7778)]), 2)

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
