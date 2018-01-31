import unittest
import os

from resource_manager.parser import Parser
from resource_manager.tokenizer import tokenize


def standardize(source):
    tokens = tokenize(source)
    result = ''
    definitions, parents, imports = Parser(tokens).parse()
    if parents:
        result += 'import ' + ' '.join(f'{repr(x)}' for x in parents) + '\n'
    result += ''.join(imp.to_str(0) for imp in imports)
    for definition in definitions:
        result += definition.to_str(0) + '\n'
    return result


class TestParser(unittest.TestCase):
    def test_idempotency(self):
        folder = os.path.dirname(__file__)

        for root, _, files in os.walk(folder):
            for filename in files:
                if filename.endswith('.config'):
                    path = os.path.join(root, filename)
                    with self.subTest(filename=filename):
                        with open(path, 'r') as file:
                            source = file.read()
                        temp = standardize(source)
                        self.assertEqual(temp, standardize(temp))

    def test_token(self):
        with self.assertRaises(SyntaxError):
            tokenize('''
            # unrecognized token:
            &
            ''')
