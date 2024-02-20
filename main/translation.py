from modeltranslation.translator import translator, TranslationOptions
from main.models import Category, Wallet


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class WalletTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Category, CategoryTranslationOptions)
translator.register(Wallet, WalletTranslationOptions)
