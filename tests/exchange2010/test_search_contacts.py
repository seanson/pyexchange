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


class Test_ParseSearchedContacts(unittest.TestCase):
  contacts = None

  @classmethod
  def setUpClass(cls):

    @httpretty.activate  # this decorator doesn't play nice with @classmethod
    def fake_contact_request():
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
        body=GET_CONTACTS_IN_CONTACTS_SEARCH.encode('utf-8'),
        content_type='text/xml; charset=utf-8',
      )

      return cls.service.contacts().search_contacts(TEST_CONTACT.name)
    
    cls.contacts = fake_contact_request()

  def test_canary(self):
    assert self.contacts is not None

  def test_contact_has_an_email(self):
    for contact in self.contacts.contacts:
        assert contact.get('email') == TEST_CONTACT.email

  def test_contact_has_a_name(self):
    for contact in self.contacts.contacts:
        assert contact.get('name') == TEST_CONTACT.name

  def test_contact_has_a_displayName(self):
    for contact in self.contacts.contacts:
        assert contact.get('displayName') == TEST_CONTACT.displayName

  def test_contact_has_a_contactSource(self):
    for contact in self.contacts.contacts:
        assert contact.get('contactSource') == TEST_CONTACT.contactSource

  def test_contact_has_a_mailboxType(self):
    for contact in self.contacts.contacts:
        assert contact.get('mailboxType') == TEST_CONTACT.mailboxType

  def test_contact_has_a_routingType(self):
    for contact in self.contacts.contacts:
        assert contact.get('routingType') == TEST_CONTACT.routingType

  @httpretty.activate
  def test_contact_list_no_contact_found(self):
    httpretty.register_uri(
      httpretty.POST,
      FAKE_EXCHANGE_URL,
      body=GET_CONTACTS_IN_CONTACTS_SEARCH_ERROR_RESPONSE.encode('utf-8'),
      content_type='text/xml; charset=utf-8',
    )

    with raises(FailedExchangeException):
      self.service.contacts().search_contacts("test@test.com")
