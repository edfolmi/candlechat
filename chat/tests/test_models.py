from django.test import TestCase
from django.contrib.auth.models import User

from chat.models import Block, PrivateBlock, GroupBlock


class BlockTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test_user', password='test12345')
        self.user2 = User.objects.create_user(username='test_user2', password='#test12345')
        self.user3 = User.objects.create_user(username='test_user3', password='@test12345')
        self.block = Block.objects.create(name='Backend Block')

    def test_block_creation(self):
        self.block.slug = 'backend-block'
        self.block.save()

        self.assertEqual(str(self.block), 'Backend Block')
        self.assertEqual(self.block.slug, 'backend-block')

    def test_block_online_users(self):
        self.block.online.set([self.user1.id, self.user2.id, self.user3.id])
        self.assertEqual(self.block.online.count(), 3)

        self.block.online.add(self.user1, self.user2, self.user3)
        self.assertEqual(self.block.online_users(), 3)

    def test_block_connect_disconnect(self):
        self.block.connect(self.user1)
        self.assertEqual(self.block.online_users(), 1)

        self.block.disconnect(self.user1)
        self.assertEqual(self.block.online_users(), 0)

        self.block.connect(self.user3)
        self.assertEqual(self.block.online_users(), 1)

        self.block.connect(self.user2)
        self.assertEqual(self.block.online_users(), 2)

        self.block.connect(self.user1)
        self.assertEqual(self.block.online_users(), 3)

        self.block.disconnect(self.user1)
        self.assertEqual(self.block.online_users(), 2)

    def test_block_get_absolute_url(self):
        self.block.slug = Block.objects.get(id=1)
        self.assertEqual('/block/group/backend-block/', self.block.slug.get_absolute_url())


class GroupBlockTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test_user', password='test12345')
        self.user2 = User.objects.create_user(username='test_user2', password='#test12345')
        self.block1 = Block.objects.create(name='Backend Block')
        self.block2 = Block.objects.create(name='Frontend Block')

    def test_string_representation(self):
        group_block = GroupBlock(user=self.user1, block=self.block1, content='Test Hello')
        self.assertEqual(str(group_block), 'test_user')

    def test_ordering(self):
        group_block_message1 = GroupBlock(user=self.user1, block=self.block1, content='Test Hello by 1')
        group_block_message2 = GroupBlock(user=self.user2, block=self.block2, content='Test Hello by 2')
        group_block_message3 = GroupBlock(user=self.user1, block=self.block2, content='Test Hello by 1')

        group_block_message1.save()
        group_block_message2.save()
        group_block_message3.save()

        expected_order = [group_block_message3, group_block_message2, group_block_message1]
        self.assertEqual(list(GroupBlock.objects.all()), expected_order)


class PrivateBlockTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test_user', password='test12345')
        self.user2 = User.objects.create_user(username='test_user2', password='#test12345')

    def test_string_representaion(self):
        private_block = PrivateBlock(user=self.user1, message='hello good day', block_thread='test_thread_1_2')
        self.assertEqual(str(private_block), 'test_thread_1_2')

    def test_ordering(self):
        group_block_message1 = PrivateBlock(user=self.user1, message='hello here', block_thread='test_thread_1')
        group_block_message2 = PrivateBlock(user=self.user2, message='hello here', block_thread='test_thread_2')
        group_block_message3 = PrivateBlock(user=self.user1, message='hello here', block_thread='test_thread_3')

        group_block_message1.save()
        group_block_message2.save()
        group_block_message3.save()

        expected_order = [group_block_message3, group_block_message2, group_block_message1]
        self.assertEqual(list(PrivateBlock.objects.all()), expected_order)
