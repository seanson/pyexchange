"""
(c) 2013 LinkedIn Corp. All rights reserved.
Licensed under the Apache License, Version 2.0 (the "License");?you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software?distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
"""
import unittest
import httpretty
from pytest import raises
from pyexchange import Exchange2010Service
from pyexchange.connection import ExchangeNTLMAuthConnection
from pyexchange.exceptions import *

from .fixtures import *


class Test_ParseRoomsFromRoomListResponseData(unittest.TestCase):
  roomLists = None

  @classmethod
  def setUpClass(cls):

    @httpretty.activate  # this decorator doesn't play nice with @classmethod
    def fake_room_request():
      cls.service = Exchange2010Service(
        connection=ExchangeNTLMAuthConnection(
          url=FAKE_EXCHANGE_URL,
          username=FAKE_EXCHANGE_USERNAME,
          password=FAKE_EXCHANGE_PASSWORD,
        )
      )

      httpretty.register_uri(
        httpretty.POST,
        FAKE_EXCHANGE_URL,
        body=GET_ROOMS_IN_ROOM_LIST_RESPONSE.encode('utf-8'),
        content_type='text/xml; charset=utf-8',
      )

      return cls.service.rooms().list_rooms(TEST_ROOM_LIST[0].email)

    cls.rooms = fake_room_request()

  def test_canary(self):
    assert self.rooms is not None

  def test_room_has_an_email(self):
    for room in self.rooms.rooms:
        assert room.get('email') == TEST_ROOM.email

  def test_room_has_a_name(self):
    for room in self.rooms.rooms:
        assert room.get('name') == TEST_ROOM.name

  def test_room_has_a_mailboxType(self):
    for room in self.rooms.rooms:
        assert room.get('mailboxType') == TEST_ROOM.mailboxType

  def test_room_has_a_routingType(self):
    for room in self.rooms.rooms:
        assert room.get('routingType') == TEST_ROOM.routingType

  @httpretty.activate
  def test_room_list_no_room_in_list(self):
    httpretty.register_uri(
      httpretty.POST,
      FAKE_EXCHANGE_URL,
      body=GET_ROOMS_IN_ROOM_LIST_ERROR_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    with raises(FailedExchangeException):
      self.service.rooms().list_rooms("test@test.com").rooms
