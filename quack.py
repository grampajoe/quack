"""
Quack

Mock and SQLAlchemy but not horrible.
"""
import mock
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query


class MockSession(mock.MagicMock):
    """A mock SQLAlchemy session.

    The query method returns a special mock Query.
    """
    query = mock.MagicMock()
    _mock_queries = []

    def __init__(self, spec=Session, *args, **kwargs):
        """Use Session as the default spec."""
        super(MockSession, self).__init__(spec=spec, *args, **kwargs)

        def _query(*args, **kwargs):
            """Return a MockQuery only if query's return value is not set."""
            if self.query._mock_return_value is mock.DEFAULT:
                query = MockQuery()
                self._mock_queries.append(query)

                return query
            else:
                return self.query.return_value

        self.query.side_effect = _query

    @property
    def mock_queries(self):
        return self._mock_queries


class MockQuery(mock.MagicMock):
    """A mock SQLAlchemy query.

    All methods return the query to allow chaining.
    """
    def __init__(self, spec=Query, *args, **kwargs):
        """Use Query as the default spec."""
        super(MockQuery, self).__init__(spec=spec, *args, **kwargs)

    def __getattr__(self, name):
        """Get attributes that return self when called.

        This can be overridden by setting the attribute's return_value.
        """
        attr = super(MockQuery, self).__getattr__(name)

        if attr._mock_return_value is mock.DEFAULT:
            attr.return_value = self

        return attr
