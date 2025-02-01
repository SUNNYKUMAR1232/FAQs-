from django.db import models
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _
from googletrans import Translator


class FAQ(models.Model):
    """
    FAQ Model
    This model stores frequently asked questions (FAQs) with support for multilingual content.
    Each FAQ has a question and answer, with translations for Hindi and Bengali.
    """

    # Original question and answer (in English)
    question = models.TextField(verbose_name=_("Question"))
    answer = RichTextField(verbose_name=_("Answer"))

    # Translated questions and answers
    question_hi = models.TextField(
        verbose_name=_("Question (Hindi)"), blank=True, null=True
    )
    question_bn = models.TextField(
        verbose_name=_("Question (Bengali)"), blank=True, null=True
    )
    answer_hi = RichTextField(
        verbose_name=_("Answer (Hindi)"), blank=True, null=True
    )
    answer_bn = RichTextField(
        verbose_name=_("Answer (Bengali)"), blank=True, null=True
    )

    # Timestamps for tracking creation and updates
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At")
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At")
    )

    # Status field to enable/disable FAQs
    is_active = models.BooleanField(
        default=True, verbose_name=_("Is Active")
    )

    # Default language for the FAQ
    language_choices = [
        ("en", _("English")),
        ("hi", _("Hindi")),
        ("bn", _("Bengali")),
    ]
    default_language = models.CharField(
        max_length=2,
        choices=language_choices,
        default="en",
        verbose_name=_("Default Language"),
    )

    def __str__(self):
        return self.question

    def get_translated_question(self, lang=None):
        lang = lang or self.default_language
        translation_map = {
            "hi": self.question_hi,
            "bn": self.question_bn,
            "en": self.question,
        }
        return translation_map.get(lang, self.question)

    def get_translated_answer(self, lang=None):

        lang = lang or self.default_language
        translation_map = {
            "hi": self.answer_hi,
            "bn": self.answer_bn,
            "en": self.answer,
        }
        return translation_map.get(lang, self.answer)

    def auto_translate(self):
        """
        Automatically translate the question and answer into Hindi and Bengali using googletrans.
        Translations are saved to the respective fields if they are not already populated.
        """
        translator = Translator()

        # Translate questions
        if not self.question_hi:
            self.question_hi = translator.translate(
                self.question, dest="hi"
            ).text
        if not self.question_bn:
            self.question_bn = translator.translate(
                self.question, dest="bn"
            ).text

        # Translate answers (preserving rich text)
        if not self.answer_hi:
            self.answer_hi = translator.translate(
                self.answer, dest="hi"
            ).text
        if not self.answer_bn:
            self.answer_bn = translator.translate(
                self.answer, dest="bn"
            ).text

        self.save()

    def save(self, *args, **kwargs):
        """
        Override the save method to trigger auto-translation when a new FAQ is created.
        """
        is_new = self.pk is None  # Check if the FAQ is being created
        super().save(*args, **kwargs)

        if is_new:
            self.auto_translate()  # Trigger auto-translation for new FAQs

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ["-created_at"]  # Order FAQs by creation date (newest first)