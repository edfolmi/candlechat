from django.test import TestCase
from django.contrib.auth.models import User

from chat.models import Block
from chat.admin import BlockAdmin


class BlockAdminTest(TestCase):
    def test_online_users_count(self):
        user = User.objects.create_user(username='test_user', password='test12345')
        block = Block.objects.create(name='Backend Block')
        block.online.add(user)

        block_admin = BlockAdmin(model=Block, admin_site=None)
        online_users = block_admin.online_users_count(block)

        self.assertEqual(online_users, 1)
