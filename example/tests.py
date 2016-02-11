from django.test import TestCase


from .models import Product, ProductCollection


class CorrectInTest(TestCase):

    maxDiff = None

    @classmethod
    def setUpClass(cls):
        super(CorrectInTest, cls).setUpClass()
        cls.collection1 = ProductCollection.objects.create(slug='one')
        cls.collection2 = ProductCollection.objects.create(slug='two')
        cls.collection3 = ProductCollection.objects.create(slug='three')

        cls.product1 = Product.objects.create(collection=cls.collection1)
        cls.product2 = Product.objects.create(collection=cls.collection1)
        cls.product3 = Product.objects.create(collection=cls.collection1)
        cls.product4 = Product.objects.create(collection=cls.collection2)

    def test_valid_query(self):
        """
        This test works on django 1.8 and 1.9
        Here are 2 queries to db.
        Both versions of django generate correct arguments for 'collection__in' argument.
        It means that django respects 'to_field' param in Product model
        """
        product_collections = ProductCollection.objects.filter(id__gte=0).order_by('id')
        products = Product.objects.filter(collection__in=list(product_collections))
        # products.query must look like this
        """SELECT "example_product"."id", "example_product"."collection_id" FROM "example_product" WHERE "example_product"."collection_id" IN (one, two, three)"""
        self.assertEqual(len(products), 4)

    def test_invalid_query(self):
        """
        Lets try to get the same data from db, but using subquery
        This is correct QuerySet which works correctly on Django 1.8.9 but fails on Django 1.9.2
        Difference between then is:
        1.8 produces (SELECT U0."slug" FROM ... in subquery, which is correct
        1.9 produces (SELECT U0."id" FROM ... in subquery, which is incorrect
        django 1.9 does not respect 'to_field' param in Product model
        """
        product_collections = ProductCollection.objects.filter(id__gte=0).order_by('-id')
        products = Product.objects.filter(collection__in=product_collections)
        # products.query must look like this
        reference_query = """SELECT "example_product"."id", "example_product"."collection_id" FROM "example_product" WHERE "example_product"."collection_id" IN (SELECT U0."slug" FROM "example_productcollection" U0 WHERE U0."id" >= 0)"""
        self.assertEqual(len(products), 4)
