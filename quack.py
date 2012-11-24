"""
Quack

Mock and SQLAlchemy but not horrible.
"""
import mock
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.attributes import InstrumentedAttribute


def overridable(func):
    """Decorator used to create overridable methods.
    
    Creates a property that returns a MagicMock. When called, the mock
    returns either the result of calling the decorated method or
    mock.return_value if it was overridden.
    """
    instances = {}

    @property
    def prop(self):
        """Property that associates mocks with instances."""
        try:
            return instances[self]
        except KeyError:
            attr = mock.MagicMock()

            def wrapper(*args, **kwargs):
                """Either call the decorated method or return reuturn_value."""
                if attr._mock_return_value is mock.DEFAULT:
                    return func(self, *args, **kwargs)
                else:
                    return mock.DEFAULT

            attr.side_effect = wrapper
            instances[self] = attr

            return attr

    return prop


class MockSession(mock.MagicMock):
    """A mock SQLAlchemy session.

    The query method returns a special mock Query.
    """
    query = mock.MagicMock()
    _mock_queries = []

    def __init__(self, spec=Session, *args, **kwargs):
        """Use Session as the default spec."""
        super(MockSession, self).__init__(spec=spec, *args, **kwargs)

    @overridable
    def query(self):
        query = MockQuery()
        self._mock_queries.append(query)

        return query

    @property
    def mock_queries(self):
        return self._mock_queries


class MockQuery(mock.MagicMock):
    """A mock SQLAlchemy query.

    All methods return the query to allow chaining.
    """
    def __init__(self, model_class=None, spec=Query, *args, **kwargs):
        """Use Query as the default spec."""
        super(MockQuery, self).__init__(spec=spec, *args, **kwargs)

        if isinstance(model_class, InstrumentedAttribute):
            model_class = model_class.class_

        self._mock_model_class = model_class

    def __getattr__(self, name):
        """Get attributes that return self when called.

        This can be overridden by setting the attribute's return_value.
        """
        attr = super(MockQuery, self).__getattr__(name)

        if attr._mock_return_value is mock.DEFAULT:
            attr.return_value = self

        return attr

    @overridable
    def all(self):
        """Get a list of all items."""
        if not self._mock_model_class:
            return self.all.return_value

        return [mock.MagicMock(spec=self._mock_model_class)
                for i in range(10)]

    @overridable
    def first(self):
        """Get the first item from a query result."""
        if not self._mock_model_class:
            return self.first.return_value

        return mock.MagicMock(spec=self._mock_model_class)

    @overridable
    def get(self, pk):
        """Get a single item by its primary key."""
        if not self._mock_model_class:
            return self.get.return_value

        return mock.MagicMock(spec=self._mock_model_class)

    @overridable
    def one(self):
        """Get a single item."""
        if not self._mock_model_class:
            return self.one.return_value

        return mock.MagicMock(spec=self._mock_model_class)
