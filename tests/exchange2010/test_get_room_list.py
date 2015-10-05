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


class Test_ParseRoomListResponseData(unittest.TestCase):
  roomLists = None

  @classmethod
  def setUpClass(cls):

    @httpretty.activate  # this decorator doesn't play nice with @classmethod
    def fake_roomList_request():
      service = Exchange2010Service(
        connection=ExchangeNTLMAuthConnection(
          url=FAKE_EXCHANGE_URL,
          username=FAKE_EXCHANGE_USERNAME,
          password=FAKE_EXCHANGE_PASSWORD,
        )
      )

      httpretty.register_uri(
        httpretty.POST,
        FAKE_EXCHANGE_URL,
        body=GET_ROOM_LIST_RESPONSE.encode('utf-8'),
        content_type='text/xml; charset=utf-8',
      )

      return service.rooms().list_room_lists()

    cls.roomLists = fake_roomList_request()

  def test_canary(self):
    assert self.roomLists is not None

  def test_room_list_has_an_email(self):
    for roomList in self.roomLists.roomLists:
        assert roomList.get('email') == TEST_ROOM_LIST[0].email