"""
Quack tests.
"""
import unittest
import mock
import quack
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query


class TestMockSession(unittest.TestCase):
    """Tests for the MockSession class."""
    def test_init(self):
        """Test that MockSession uses Session as its spec."""
        session = quack.MockSession()

        self.assertIsInstance(session, Session)

    @mock.patch('quack.MockQuery')
    def test_query(self, mock_query):
        """Test that the query method returns a MockQuery."""
        session = quack.MockSession()

        self.assertIs(session.query(), mock_query.return_value)

    def test_query_multiple(self):
        """Test that the same MockQuery is returned for every query call."""
        session = quack.MockSession()

        self.assertIsNot(session.query(), session.query())

    def test_query_return_value(self):
        """Test overriding query's return value."""
        session = quack.MockSession()

        session.query.return_value = 'test'

        self.assertIs(session.query(), 'test')

    def test_mock_queries(self):
        """Test getting all queries performed with the session."""
        session = quack.MockSession()

        query1 = session.query()
        query2 = session.query()

        self.assertSequenceEqual(session.mock_queries, (query1, query2))


class TestMockQuery(unittest.TestCase):
    """Tests for the MockQuery class."""
    def test_init(self):
        """Test that MockQuery uses Query as its spec."""
        query = quack.MockQuery()

        self.assertIsInstance(query, Query)

    def test_call(self):
        """Test that MockQuery returns itself when methods are called."""
        query = quack.MockQuery()

        self.assertIs(query.filter(), query)
        self.assertIs(query.options(), query)
        self.assertIs(query.having(), query)
        self.assertIs(query.join(), query)

    def test_set_return_value(self):
        """Test setting the return value of a query method."""
        query = quack.MockQuery()

        query.one.return_value = 'test'

        self.assertIs(query.one(), 'test')

    def test_model_class(self):
        """Test setting the model class."""
        query = quack.MockQuery('test')

        self.assertIs(query._mock_model_class, 'test')

    def test_all_no_model_class(self):
        """Test calling query.all with no model class."""
        query = quack.MockQuery()

        items = query.all()

        self.assertIs(items, query.all.return_value)

    def test_all_override(self):
        """Test overriding all."""
        query = quack.MockQuery()

        query.all.return_value = 'fart'

        self.assertIs(query.all(), 'fart')


class TestClass(object):
    """A dummy class."""


class TestQueryEndpoints(unittest.TestCase):
    """Tests for query endpoint methods."""
    def setUp(self):
        self.query = quack.MockQuery(TestClass)

    def test_all(self):
        """Test calling query.all."""
        items = self.query.all()

        self.assertGreater(len(items), 0)
        for item in items:
            self.assertIsInstance(item, TestClass)


class Overridden(mock.MagicMock):
    """A class with an overridable method."""
    @quack.overridable
    def test(self):
        return 'test'


class TestOverridable(unittest.TestCase):
    def test_override(self):
        """Test overriding an overridable property."""
        instance = Overridden()

        self.assertIsInstance(instance.test, mock.Mock)
        self.assertIs(instance.test(), 'test')

        instance.test.return_value = 'fart'

        self.assertIs(instance.test(), 'fart')

    def test_multiple_instances(self):
        """Test getting new overridable method mocks for every instance."""
        first = Overridden()
        second = Overridden()

        self.assertIsNot(first.test, second.test)
