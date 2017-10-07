from django.test import TestCase
from infty.core.models import Topic, Comment, Transaction
from infty.api.v1.serializers import *
from rest_framework.test import APIClient, APITestCase
from rest_framework.request import Request
from rest_framework import status
from django.core.urlresolvers import reverse
from rest_framework.authtoken.models import Token
from infty.api.v1.views import *
from infty.users.models import User
import json
from decimal import Decimal
import pdb


class APITestCaseAuthorizedUser(APITestCase):

    def setUp(self):

        self.username = "testuser"
        self.email = "test@test.com"
        self.password = "password_for_test"
        self.testuser = User.objects.create_user(self.username, self.email,
            is_superuser=False, is_staff=False)
        self.testuser.set_password(self.password)
        self.testuser.save()

        self.client.force_authenticate(user=User.objects.first())

        self.topic = Topic.objects.create(
            title='Test topic 1',
            owner=self.testuser,
        )
        self.topic_url = reverse('topic-detail', kwargs={'pk':self.topic.pk})

        self.comment = Comment(
            topic=self.topic,
            text='Test comment text',
            owner=self.testuser
        )
        self.comment.save()
        self.comment_url = reverse('comment-detail', kwargs={'pk':self.comment.pk})

        self.snapshot = self.comment.create_snapshot()

        self.usd = Currency(label='usd'); self.usd.save()

        self.hprice = HourPriceSnapshot(
            name='FRED',
            base=self.usd,
            data=json.loads("""
{"realtime_start":"2017-07-28","realtime_end":"2017-07-28","observation_start":"1600-01-01","observation_end":"9999-12-31","units":"lin","output_type":1,"file_type":"json","order_by":"observation_date","sort_order":"desc","count":136,"offset":0,"limit":1,"observations":[{"realtime_start":"2017-07-28","realtime_end":"2017-07-28","date":"2017-06-01","value":"26.25"}]}"""),
            endpoint='https://api.stlouisfed.org/fred/series/observations?series_id=CES0500000003&api_key=0a90ca7b5204b2ed6e998d9f6877187e&limit=1&sort_order=desc&file_type=json',
        )
        self.hprice.save()

        self.cprice = CurrencyPriceSnapshot(
            name='FIXER',
            base=self.usd,
            data=json.loads("""
{"base":"EUR","date":"2017-07-28","rates":{"AUD":1.4732,"BGN":1.9558,"BRL":3.7015,"CAD":1.4712,"CHF":1.1357,"CNY":7.9087,"CZK":26.048,"DKK":7.4364,"GBP":0.89568,"HKD":9.1613,"HRK":7.412,"HUF":304.93,"IDR":15639.0,"ILS":4.1765,"INR":75.256,"JPY":130.37,"KRW":1317.6,"MXN":20.809,"MYR":5.0229,"NOK":9.3195,"NZD":1.5694,"PHP":59.207,"PLN":4.2493,"RON":4.558,"RUB":69.832,"SEK":9.5355,"SGD":1.5947,"THB":39.146,"TRY":4.1462,"USD":1.1729,"ZAR":15.281}}"""),
            endpoint='https://api.fixer.io/latest?base=eur',
        )
        self.cprice.save()

        self.transaction = Transaction(
            comment = self.comment,
            snapshot = self.snapshot,
            hour_price = self.hprice,
            currency_price = self.cprice,
            payment_amount = Decimal(10),
            payment_currency = self.usd,
            payment_recipient = self.testuser,
            payment_sender = self.testuser,
            hour_unit_cost = (1)
        )
        self.transaction.save()


class GetAPIRoot(APITestCaseAuthorizedUser):

    def test_can_access_api_root(self):
        response = self.client.get(reverse('topic-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateTopicList(APITestCaseAuthorizedUser):

    def setUp(self):

        super(CreateTopicList, self).setUp()

        self.topic_data = {
            'title': 'Test topic 1'
            }

        self.response = self.client.post(
            reverse('topic-list'),
            self.topic_data,
            format="json")

    def test_can_create_topic(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class CreateTopicList(APITestCase):

    # Unauthorized user cannot create a topic

    def setUp(self):

        self.topic_data = {
            'title': 'Test topic 1'
            }

        self.response = self.client.post(
            reverse('topic-list'),
            self.topic_data,
            format="json")

    def test_cannot_create_topic(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)


class CreateCommentList(APITestCaseAuthorizedUser):

    def setUp(self):

        super(CreateCommentList, self).setUp()

        self.comment_data = {
            'topic': self.topic_url,
            'text': 'Test comment text',
            'claimed_hours': 1.5,
            'assumed_hours': 6.5,
            }

        self.response = self.client.post(
            reverse('comment-list'),
            self.comment_data,
            format="json")

    def test_can_create_comment(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class CreateTransactionList(APITestCaseAuthorizedUser):

    def setUp(self):

        super(CreateTransactionList, self).setUp()

        self.transaction_data = {
            'comment': self.comment_url,
            'snapshot': self.snapshot.pk,
            'hour_price': self.hprice.pk,
            'currency_price': self.cprice.pk,
            'payment_amount': 10,
            'payment_currency': self.usd.pk,
            'payment_recipient': self.testuser.pk,
            'payment_sender': self.testuser.pk,
            'hour_unit_cost': 1,
            'donated_hours': 1,
            'matched_hours': 1
            }

        self.response = self.client.post(
            reverse('transaction-list'),
            self.transaction_data,
            format="json")

    def test_can_create_comment(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)


class GetTopicList(APITestCaseAuthorizedUser):

    def test_get_all_topics(self):

        self.response = self.client.get(reverse('topic-list'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class GetCommentList(APITestCaseAuthorizedUser):

    def test_get_all_comments(self):

        self.response = self.client.get(reverse('comment-list'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class GetTransactionList(APITestCaseAuthorizedUser):

    def test_get_all_transactions(self):

        self.response = self.client.get(reverse('transaction-list'))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)


class GetTopicDetail(APITestCaseAuthorizedUser):

    def test_get_valid_single_topic(self):
        self.response = self.client.get(reverse('topic-detail', kwargs={'pk': self.topic.pk}))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_topic(self):
        self.response = self.client.get(
            reverse('topic-detail', kwargs={'pk': 30}))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)


class GetCommentDetail(APITestCaseAuthorizedUser):

    def test_get_valid_single_comment(self):
        self.response = self.client.get(reverse('comment-detail', kwargs={'pk': self.comment.pk}))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_commment(self):
        self.response = self.client.get(
            reverse('comment-detail', kwargs={'pk': 30}))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)


class GetTransactionDetail(APITestCaseAuthorizedUser):

    def test_get_valid_single_transaction(self):
        self.response = self.client.get(reverse('transaction-detail', kwargs={'pk': self.transaction.pk}))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_transaction(self):
        self.response = self.client.get(
            reverse('transaction-detail', kwargs={'pk': 30}))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateTopic(APITestCaseAuthorizedUser):

    def test_valid_update_topic(self):

        valid_info = {
            'title': 'Test topic 1',
            "body": "Updated body"
        }

        self.response = self.client.put(
            reverse('topic-detail', kwargs={'pk':self.topic.pk}),
            valid_info,
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_invalid_update_channel(self):

        invalid_info = {
            'title': 'Test topic 1',
            "body": "Updated body",
            'type': 'Invalid type',
        }

        self.response = self.client.put(
            reverse('topic-detail', kwargs={'pk': self.topic.pk}),
            invalid_info,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateComment(APITestCaseAuthorizedUser):

    def test_valid_update_comment(self):

        valid_info = {
            'topic': self.topic_url,
            "text": "Updated text",
            'claimed_hours': 1.5,
            'assumed_hours': 6.5,
        }

        self.response = self.client.put(
            reverse('comment-detail', kwargs={'pk':self.comment.pk}),
            valid_info,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_invalid_update_comment(self):

        invalid_info = {
            'topic': self.topic_url,
            "text": "Updated text",
            'claimed_hours': 'Invalid claimed hours',
            'assumed_hours': 6.5,
        }

        self.response = self.client.put(
            reverse('comment-detail', kwargs={'pk': self.comment.pk}),
            invalid_info,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateTransaction(APITestCaseAuthorizedUser):

    def test_valid_update_transaction(self):

        valid_info = {
            'comment': self.comment_url,
            'snapshot': self.snapshot.pk,
            'hour_price': self.hprice.pk,
            'currency_price': self.cprice.pk,
            'payment_amount': 10,
            'payment_currency': self.usd.pk,
            'payment_recipient': self.testuser.pk,
            'payment_sender': self.testuser.pk,
            "hour_unit_cost": 5,
            'donated_hours': 1,
            'matched_hours': 1
        }

        self.response = self.client.put(
            reverse('transaction-detail', kwargs={'pk':self.transaction.pk}),
            valid_info,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_invalid_update_transaction(self):

        invalid_info = {
            'comment': self.comment_url,
            'snapshot': self.snapshot.pk,
            'hour_price': self.hprice.pk,
            'currency_price': self.cprice.pk,
            'payment_amount': 10,
            'payment_currency': self.usd.pk,
            'payment_recipient': self.testuser.pk,
            'payment_sender': self.testuser.pk,
            'hour_unit_cost': 'Invalid hour unit cost',
            'donated_hours': 1,
            'matched_hours': 1
        }

        self.response = self.client.put(
            reverse('transaction-detail', kwargs={'pk': self.transaction.pk}),
            invalid_info,
            format="json")

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
