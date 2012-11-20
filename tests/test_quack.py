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
