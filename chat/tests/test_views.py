from django.test import TestCase
from django.urls import reverse

from chat.models import Block


class ViewTest(TestCase):
    def setUp(self):
        self.block = Block.objects.create(name='Backend View')
        self.block.slug = 'backend-view'
        self.block.save()

    def test_blocks_view(self):
        response = self.client.get(reverse('blocks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name')
        self.assertTemplateUsed(response, 'chat/blocks.html')

    '''
    def test_block_groups(self):
        response = self.client.get(reverse('block_group', args=[self.block.slug]))
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'detail')
        #self.assertTemplateUsed(response, 'chat/group_block.html')
    '''
