from os import listdir
from os.path import isfile, join
from unittest import TestCase

from td2 import Parser, parse_course, SearchEngine

COURSE_PATH = '02/sample'
FILES = [join(COURSE_PATH, f) for f in listdir(COURSE_PATH) if isfile(join(COURSE_PATH, f))]


class TestUtils(TestCase):
    def test_parse_course(self):
        self.assertTupleEqual(('Langages de script',
                               "Caracteristiques des langages de script. Principaux langages et dom"
                               "aines d'application. Programmation avec un langage de script : synt"
                               "axe, structures de controle, structures de donnees, communication i"
                               "nterprocessus et communication avec une base de donnees, modules cl"
                               "ients et serveurs."),
                              parse_course(path=join(COURSE_PATH,'INF8007.txt')), msg="usual case")
        not_found_error = False
        try:
            parse_course(path='foobar')
        except FileNotFoundError:
            not_found_error = True

        self.assertTrue(not_found_error, msg="bad acronym")


class TestParser(TestCase):
    parser = Parser('french')

    def test_tokenise(self):
        self.assertEqual(['foo'], self.parser.tokenise('foo\n'), msg='string cleaning')
        self.assertEqual('jean va à la fontaine'.split(),
                         self.parser.tokenise('Jean va à la fontaine', False, False),
                         msg='normal use')
        self.assertEqual(['siffl'], self.parser.tokenise('sifflement', False, True), msg='stemming')

        self.assertEqual('jean va fontaine'.split(),
                         self.parser.tokenise('Jean va à la fontaine', True, False),
                         msg='removing stopwords')

        self.assertEqual('jean va fontain'.split(),
                         self.parser.tokenise('Jean va à la fontaine', True, True),
                         msg='removing stopwords and stemming')

    def test_count_terms(self):
        self.assertEqual(dict(foo=2, bar=1), self.parser.count_terms('foo foo bar'.split()))


class TestSearchEngine(TestCase):
    engine = SearchEngine(language='french', files=FILES)

    def test_search(self):
        print(self.engine.search('INF0330'))
