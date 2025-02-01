import pytest
from faq.serializers import FAQSerializer
from faq.tests.factories import FAQFactory

@pytest.mark.django_db
def test_faq_serializer():
    """Test FAQ serializer."""
    faq = FAQFactory()
    serializer = FAQSerializer(faq)

    assert serializer.data["question"] == faq.question
    assert serializer.data["answer"] == faq.answer
    assert serializer.data["default_language"] == faq.default_language