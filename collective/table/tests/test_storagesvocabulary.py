import unittest
from zope import component, interface, testing
from Products.Archetypes.interfaces import IBaseObject

from ..interfaces import ITableField, ISource


class MockContent(object):
    interface.implements(IBaseObject)


class MockSource(object):
    interface.implements(ISource)
    component.adapts(ITableField, IBaseObject)
    def __init__(self, field, instance): pass


class StoragesVocabularyTest(testing.cleanup.CleanUp, unittest.TestCase):
    def _availableTableStorages(self):
        from ..field_widget import availableTableStorages
        return availableTableStorages(MockContent())

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
