#!/usr/bin/env python

import datetime
from unittest import TestCase

from mock import patch

from awscurl.awscurl import make_request

__author__ = 'iokulist'


def my_mock_get():
    class Object():
        pass

    def ss(*args, **kargs):
        print("in mock")
        response = Object()
        response.status_code = 200
        response.text = 'some text'
        return response

    return ss


def my_mock_send_request():
    class Object():
        pass

    def ss(*args, **kargs):
        print("in mock")
        response = Object()
        response.status_code = 200
        response.text = 'some text'
        return response

    return ss


def my_mock_utcnow():
    class Object():
        pass

    def ss(*args, **kargs):
        print("in mock")
        return datetime.datetime.utcfromtimestamp(0)

    return ss


class TestMakeRequest(TestCase):
    @patch('requests.get', new_callable=my_mock_get)
    @patch('awscurl.awscurl.send_request', new_callable=my_mock_send_request)
    @patch('awscurl.awscurl.now', new_callable=my_mock_utcnow)
    def test_make_request(self, *args, **kvargs):
        headers = {}
        params = {'method': 'GET',
                  'service': 'ec2',
                  'region': 'region',
                  'uri': 'https://user:pass@host:123/path/?a=b&c=d',
                  'headers': headers,
                  'data': '',
                  'access_key': '',
                  'secret_key': '',
                  'security_token': ''}
        make_request(**params)

        expected = {'x-amz-date': '19700101T000000Z',
                    'Authorization': 'AWS4-HMAC-SHA256 Credential=/19700101/region/ec2/aws4_request, SignedHeaders=host;x-amz-date, Signature=cabc851aa1139c804beabf1ae27961845d8f6b10b333a996254369bfc526ba21',
                    'x-amz-security-token': ''}

        self.assertEqual(expected, headers)

        pass
