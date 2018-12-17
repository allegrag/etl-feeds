import decimal
import json
import os
import unittest
import csv
import sys


def cast_to_bool(value):
    if value.lower() not in ('true', 'false'):
        raise ValueError
    return bool(value)

TYPE_CAST_MAP = {
    'LONG': long,
    'BOOLEAN': cast_to_bool,
    'DECIMAL': decimal.Decimal,
    'STRING': str
}

TYPE_EXCEPTION_MAP = {
    'LONG': ValueError,
    'BOOLEAN': ValueError,
    'DECIMAL': decimal.InvalidOperation,
    'STRING': ValueError
}

FEED_PATH = os.path.abspath('data/feeds')


class ProductsTest(unittest.TestCase):
    PRODUCTS_PATH = os.path.join(FEED_PATH, 'products')

    def setUp(self):
        self.files = []
        self.config = {}
        for _, _, files in os.walk(self.PRODUCTS_PATH):
            for file_name in files:
                file_path = os.path.join(self.PRODUCTS_PATH, file_name)
                if file_name.endswith(".csv"):
                    self.files.append(file_path)
                elif file_name.endswith('config.json'):
                    self.config = json.loads(open(file_path).read())

    def test_product_columns(self):
        for file in self.files:
            print 'Checking {file}...'.format(file=file)
            with open(file, 'rb') as csvfile:
                for idx, row in enumerate(csv.DictReader(csvfile), start=1):
                    if idx == 1:
                        req_columns_present = set(row.keys()).issuperset(set(self.config['REQUIRED_COLUMNS']))
                        self.assertTrue(req_columns_present)

                    for field, value in row.items():
                        if field in TYPE_CAST_MAP:
                            try:
                                TYPE_CAST_MAP[field](value)
                            except TYPE_EXCEPTION_MAP[field]:
                                self.fail(('Type cast exception in row {row_number} for field {field}, value {value}. '
                                           'Expected value of type {type}.')
                                          .format(row_number=str(idx), field=field,
                                                  value=value, type=self.config['COLUMNS'][field]))

    def test_unique_columns(self):
        unique_field_set_map = {}

        for column in self.config.get('UNIQUE_COLUMNS', []):
            unique_field_set_map[column] = set()

        if not unique_field_set_map:
            self.skipTest('No unique columns found')

        for file in self.files:
            print 'Checking {file}...'.format(file=file)
            with open(file, 'rb') as csvfile:
                for idx, row in enumerate(csv.DictReader(csvfile), start=1):
                    if not row.get('field'):
                        self.skipTest('Missing unique column')
                    for field, field_set in unique_field_set_map.items():
                        self.assertTrue(row[field] not in field_set)
                        field_set.add(row[field])

if __name__ == '__main__':
    unittest.main()
