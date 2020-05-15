from django.test import TestCase
from django.contrib.auth.models import User


class DetailsPageTest(TestCase):

    def test_page_slugify_on_save(self):
            user = User()
            user.save()

            # Create and save a new page to the test database.
            page = Page(title="Testing page", content="test", author=user)
            page.save()
            self.assertEqual(page.slug, "testing-page")


class PageListViewTests(TestCase):

    def test_multiple_pages(self):

        user = User.objects.create()
        Page.objects.create(title="Test Page", content="test", author=user)
        Page.objects.create(title="Another Test Page", content="test", author=user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        responses = response.context['pages']
        self.assertEqual(len(responses), 2)
        self.assertQuerysetEqual(
            responses,
            ['<Page: Test Page>', '<Page: Another Test Page>'],
            ordered=False
        )


class DetailsCreationTests(TestCase):

    def test_detail_page(self):
        user = User.objects.create()
        user.save()
        page = Page(title="Test Page", content="testing", author=user)
        page.save()

        self.assertEqual(page.slug, "test-page")

        response = self.client.get(f'/page/{page.slug}/')


        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testing")


    def test_page_edit(self):

        user = User.objects.create()
        user.save()
        page = Page(title="Test Page", content="testing", author=user)
        page.save()

        self.assertEqual(page.slug, "test-page")
        edit_info = {
            'title': 'A New Test',
            'content': 'Some New Test'
        }
        response = self.client.post(f'/page/{page.slug}/', edit_info)
        self.assertEqual(response.status_code, 302)
        page = Page.objects.get(id=1)
        self.assertEqual(page.title, 'A New Test')

    def test_creation(self):
        user = User.objects.create()
        user.username = 'mondale'
        user.password = 'isthegreatest'
        user.save()
        edit_info = {
            'title': 'A New Name',
            'content': 'Some New Contetnet'
        }

        
        self.client.force_login(user)
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/create/', edit_info)
        self.assertEqual(response.status_code, 302)
        page = Page.objects.get(author__username='admin')
        self.assertEqual(page.title, 'A New Name')