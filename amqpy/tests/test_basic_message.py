from __future__ import absolute_import, division, print_function

__metaclass__ = type
from datetime import datetime
from decimal import Decimal
import pickle

from .. import Message


class TestBasicMessage:
    def check_proplist(self, msg):
        """Check roundtrip processing of a single object
        """
        raw_properties = msg.serialize_properties()

        new_msg = Message()
        new_msg.load_properties(raw_properties)
        new_msg.body = msg.body

        assert msg == new_msg

    def test_eq(self):
        msg = Message('hello', content_type='text/plain')
        assert msg

        # Make sure that something that looks vaguely like a Message doesn't raise an Attribute
        # error when compared to a Message, and instead returns False
        class FakeMsg:
            pass

        fake_msg = FakeMsg()
        fake_msg.properties = {'content_type': 'text/plain'}

        assert msg != fake_msg

    def test_pickle(self):
        msg = Message(
            'some body' * 200000,
            content_type='text/plain',
            content_encoding='utf-8',
            application_headers={'foo': 7, 'bar': 'baz', 'd2': {'foo2': 'xxx', 'foo3': -1}},
            delivery_mode=1,
            priority=7,
        )

        msg2 = pickle.loads(pickle.dumps(msg, -1))
        assert msg == msg2

    def test_roundtrip(self):
        """Check round-trip processing of content-properties
        """
        self.check_proplist(Message())
        self.check_proplist(Message(content_type='text/plain'))
        self.check_proplist(Message(
            content_type='text/plain',
            content_encoding='utf-8',
            application_headers={'foo': 7, 'bar': 'baz', 'd2': {'foo2': 'xxx', 'foo3': -1}},
            delivery_mode=1,
            priority=7,
        ))

        self.check_proplist(Message(
            application_headers={
                'regular': datetime(2007, 11, 12, 12, 34, 56),
                'dst': datetime(2007, 7, 12, 12, 34, 56),
            },
        ))

        n = datetime.now()
        # AMQP only does timestamps to 1-second resolution
        n = n.replace(microsecond=0)
        self.check_proplist(Message(application_headers={'foo': n}))
        self.check_proplist(Message(application_headers={'foo': Decimal('10.1')}))
        self.check_proplist(Message(application_headers={'foo': Decimal('-1987654.193')}))
        self.check_proplist(Message(timestamp=datetime(1980, 1, 2, 3, 4, 6)))
