"""Validate the shipped registry without importing BLREdit or contacting servers."""
import argparse
import ipaddress
import json
import re
from pathlib import Path


DEFAULT_REGISTRY = Path(__file__).resolve().parents[1] / 'Resources' / 'ServerList.json'
FIELDS = {'ID', 'ServerAddress', 'Port', 'InfoPort', 'Hidden', 'Region', 'ValidatesLoadout'}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON property: {key}')
        result[key] = value
    return result


def canonical_host(address):
    """Validate an ASCII DNS hostname or strict dotted-decimal IPv4, without DNS I/O."""
    host = address.removesuffix('.')
    labels = host.split('.')
    # Numeric/hex address spellings must not slip through as hostnames. IPv4Address
    # rejects shorthand, integer, octal/leading-zero and hexadecimal alternatives.
    if all(re.fullmatch(r'(?:[0-9]+|0[xX][0-9a-fA-F]+)', label) for label in labels):
        return str(ipaddress.IPv4Address(address))
    if (len(host) > 253 or not host
            or re.fullmatch(r'[0-9]+', labels[-1])
            or any(not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?', label)
                   for label in labels)):
        raise ValueError('ServerAddress must be a DNS hostname or dotted-decimal IPv4; use separate port fields')
    return host.lower()


def validate_registry(entries):
    if not isinstance(entries, list) or not entries:
        raise ValueError('registry must be a non-empty array')
    ids = set()
    endpoints = set()
    for index, entry in enumerate(entries):
        prefix = f'entry {index}'
        if not isinstance(entry, dict):
            raise ValueError(f'{prefix}: expected an object')
        unknown = entry.keys() - FIELDS
        if unknown:
            raise ValueError(f'{prefix}: unknown properties: {sorted(unknown)}')
        for field in ('ID', 'ServerAddress'):
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip() or value != value.strip():
                raise ValueError(f'{prefix}: {field} must be a non-empty, trimmed string')
        if entry['ID'] in ids:
            raise ValueError(f'{prefix}: duplicate ID {entry["ID"]!r}')
        ids.add(entry['ID'])
        try:
            address = canonical_host(entry['ServerAddress'])
        except ValueError as error:
            raise ValueError(f'{prefix}: invalid ServerAddress: {error}') from error
        for field in ('Port', 'InfoPort'):
            # Match BLRServer's omitted-port defaults; bool is not a JSON integer port.
            port = entry.get(field, 7777)
            if type(port) is not int or not 1 <= port <= 65535:
                raise ValueError(f'{prefix}: {field} must be an integer from 1 to 65535')
        endpoint = (address, entry.get('Port', 7777))
        if endpoint in endpoints:
            raise ValueError(f'{prefix}: duplicate game endpoint {endpoint}')
        endpoints.add(endpoint)
        for field in ('Hidden', 'ValidatesLoadout'):
            if field in entry and type(entry[field]) is not bool:
                raise ValueError(f'{prefix}: {field} must be a boolean')
        if 'Region' in entry and not isinstance(entry['Region'], str):
            raise ValueError(f'{prefix}: Region must be a string')
    return len(entries)


def load_registry(path):
    with open(path, encoding='utf-8-sig') as source:
        entries = json.load(source, object_pairs_hook=unique_object)
    validate_registry(entries)
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', type=Path, default=DEFAULT_REGISTRY)
    args = parser.parse_args()
    try:
        entries = load_registry(args.path)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Invalid registry: {error}\n')
    print(f'Validated {len(entries)} server entries (offline).')


if __name__ == '__main__':
    main()
