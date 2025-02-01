import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from faq.tests.factories import FAQFactory

@pytest.mark.django_db
def test_faq_list_view():
    """Test FAQ list view."""
    client = APIClient()
    FAQFactory.create_batch(3)  # Create 3 FAQs

    response = client.get(reverse("faq-list"))
    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_faq_create_view():
    """Test FAQ creation via API."""
    client = APIClient()
    data = {
        "question": "What is Python?",
        "answer": "Python is a programming language.",
        "default_language": "en",
    }

    response = client.post(reverse("faq-list"), data, format="json")
    assert response.status_code == 201
    assert response.data["question"] == "What is Python?"