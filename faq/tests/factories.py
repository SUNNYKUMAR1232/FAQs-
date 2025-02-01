import factory
from faq.models import FAQ

class FAQFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FAQ

    question = "What is Django?"
    answer = "Django is a web framework."
    default_language = "en"