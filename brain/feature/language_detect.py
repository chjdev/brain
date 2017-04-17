#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy
import pycld2
from sklearn.base import TransformerMixin
import enum


def create_enum_type(to_string=True):
    members = dict((code, value) for value, code in pycld2.LANGUAGES)
    members['un'] = 'UNKNOWN'
    if to_string:
        return 'Enum(\'Lang\', %s)' % str(members)
    else:
        return enum.Enum('Lang', members)


def language_detect(text: str) -> str:
    """:return: the language short string detected in the text"""
    if isinstance(text, tuple):
        text = text[0]
    try:
        return pycld2.detect(text.replace('\x7f', '').replace('\b', ''))[2][0][1]
    except pycld2.error as err:
        print('couldn\'t process input:', text)
        print(err)


def is_english(text: str) -> bool:
    return language_detect(text) == 'en'


def is_german(text: str) -> bool:
    return language_detect(text) == 'de'


class LanguageTransformer(TransformerMixin):
    _vecfun = numpy.vectorize(language_detect)

    def transform(self, X: numpy.array, y=None, **transform_params):
        return self._vecfun(X)

    def fit(self, X: numpy.array, y=None, **fit_params):
        return self

    def get_params(self, deep=False):
        return {}

    def set_params(self, **_):
        pass


if __name__ == '__main__':
    print(create_enum_type())