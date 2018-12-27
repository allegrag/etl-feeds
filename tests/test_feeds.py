import decimal
import json
import os
import unittest
import csv
import re


def cast_to_bool(value):
    if value.lower() not in ('true', 'false'):
        raise ValueError
    return bool(value)


def cast_to_decimal(value):
    if re.search(r'[^0-9$.,]', value.strip()):
        raise decimal.InvalidOperation
    return decimal.Decimal(re.sub(r'[^\d\.]', '', value))


TYPE_CAST_MAP = {
    'LONG': long,
    'BOOLEAN': cast_to_bool,
    'DECIMAL': cast_to_decimal,
    'STRING': str
}

TYPE_EXCEPTION_MAP = {
    'LONG': ValueError,
    'BOOLEAN': ValueError,
    'DECIMAL': decimal.InvalidOperation,
    'STRING': ValueError
}

BASE_FEEDS_PATH = os.path.abspath('data/feeds')


class BaseFeedsTest(unittest.TestCase):
    def setUp(self):
        self.files = []
        self.config = {}

        if not self.FEEDS_DIR:
            self.skipTest('No feeds directory provided')

        self.FEEDS_PATH = os.path.join(BASE_FEEDS_PATH, self.FEEDS_DIR)

        if not os.path.isdir(self.FEEDS_PATH):
            self.fail('Provided feeds path {feeds_path} is not a directory'
                      .format(feeds_path=self.FEEDS_PATH))

        for _, _, files in os.walk(self.FEEDS_PATH):
            for file_name in files:
                file_path = os.path.join(self.FEEDS_PATH, file_name)
                if file_name.endswith(".csv"):
                    self.files.append(file_path)
                elif file_name.endswith('config.json'):
                    self.config = json.loads(open(file_path).read())

        if not self.config:
            self.fail('No config.json file found at feeds path {feeds_path}'
                      .format(feeds_path=self.FEEDS_PATH))

    def test_column_types(self):
        for file in self.files:
            print 'Checking {file}...'.format(file=file)
            with open(file, 'rb') as csvfile:
                for idx, row in enumerate(csv.DictReader(csvfile), start=1):
                    if idx == 1:
                        req_columns_present = set(row.keys()).issuperset(set(self.config['REQUIRED_COLUMNS']))
                        self.assertTrue(req_columns_present)

                    for field, value in row.items():
                        if field in self.config['COLUMNS']:
                            try:
                                TYPE_CAST_MAP[self.config['COLUMNS'][field]](value)
                            except TYPE_EXCEPTION_MAP[self.config['COLUMNS'][field]]:
                                self.fail(('Type cast exception in row {row_number} for field {field}, value {value}. '
                                           'Expected value of type {type}.')
                                          .format(row_number=str(idx), field=field,
                                                  value=value, type=self.config['COLUMNS'][field]))

    def test_unique_columns(self):
        unique_field_values_map = {}

        for column in self.config.get('UNIQUE_COLUMNS', []):
            unique_field_values_map[column] = {}

        if not unique_field_values_map:
            self.skipTest('No unique columns found')

        for file in self.files:
            print 'Checking {file}...'.format(file=file)
            with open(file, 'rb') as csvfile:
                for idx, row in enumerate(csv.DictReader(csvfile), start=1):
                    for field, values_map in unique_field_values_map.items():
                        if not row.get(field):
                            print 'Skipping, missing unique column'
                            continue
                        if row[field] in values_map:
                            self.fail(('Unique field {field} encountered duplicate '
                                       'value {value} at line {idx}')
                                      .format(field=field, value=row[field], idx=idx))
                        values_map.add(row[field])

    def test_column_name_formatting(self):
        for file in self.files:
            print 'Checking {file}...'.format(file=file)
            with open(file, 'rb') as csvfile:
                for field in csv.DictReader(csvfile).fieldnames:
                    if field.strip() != field:
                        self.fail('Error, field {field} contains trailing or leading whitespace'
                                  .format(field=field))


class SourceProductsTest(BaseFeedsTest):
    FEEDS_DIR = 'source_products'


class FilterProductsTest(BaseFeedsTest):
    FEEDS_DIR = 'filter_products'


class TagsTest(BaseFeedsTest):
    FEEDS_DIR = 'tags'

if __name__ == '__main__':
    unittest.main()
