import unittest
from zope import component, interface, testing

from ..interfaces import ITable, ISource


class MockTable(object):
    interface.implements(ITable)

class MockSource(object):
    interface.implements(ISource)
    component.adapts(ITable)
    def __init__(self, context): pass


class StoragesVocabularyTest(testing.cleanup.CleanUp, unittest.TestCase):
    def _availableTableStorages(self):
        from ..table import availableTableStorages
        return availableTableStorages(MockTable())

    def testNoRegistrations(self):
        vocab = self._availableTableStorages()
        self.assertEqual(len(vocab), 0)

    def testRegistrations(self):
        class SourceOne(MockSource):
            title = u'Source One'
        component.provideAdapter(SourceOne, name='source1')

        class SourceTwo(MockSource):
            title = u'Source Two'
        component.provideAdapter(SourceTwo, name='source2')

        class SourceThree(MockSource):
            title = u'Source Three'
        component.provideAdapter(SourceThree, name='source3')

        vocab = self._availableTableStorages()
        self.assertEqual(len(vocab), 3)

        # Note that the sources are sorted by title, Three comes before Two
        self.assertEqual([t.value for t in vocab],
            [u'source1', u'source3', u'source2'])
        self.assertEqual([t.title for t in vocab], 
            [u'Source One', 'Source Three', 'Source Two'])


def test_suite():
    import sys
    return unittest.findTestCases(sys.modules[__name__])
