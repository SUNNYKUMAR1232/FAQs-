import pytest
from faq.models import FAQ
from faq.tests.factories import FAQFactory


@pytest.mark.django_db
def test_faq_creation():
    """Test FAQ creation."""
    faq = FAQFactory()
    assert faq.question == "What is Django?"
    assert faq.answer == "Django is a web framework."
    assert faq.default_language == "en"

@pytest.mark.django_db
def test_faq_translation():
    """Test FAQ translation."""
    faq = FAQFactory()
    faq.auto_translate()

    assert faq.question_hi is not None
    assert faq.question_bn is not None
    assert faq.answer_hi is not None
    assert faq.answer_bn is not None