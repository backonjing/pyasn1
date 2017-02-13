#
# This file is part of pyasn1 software.
#
# Copyright (c) 2005-2017, Ilya Etingof <etingof@gmail.com>
# License: http://pyasn1.sf.net/license.html
#
import sys
from pyasn1.type import univ, tag
from pyasn1 import error


class AbstractCharacterString(univ.OctetString):

    if sys.version_info[0] <= 2:
        def __str__(self):
            try:
                return self._value.encode(self._encoding)
            except UnicodeEncodeError:
                raise error.PyAsn1Error(
                    'Can\'t encode string \'%s\' with \'%s\' codec' % (self._value, self._encoding)
                )

        def __unicode__(self):
            return self._value

        def prettyIn(self, value):
            if isinstance(value, unicode):
                return value
            elif isinstance(value, str):
                return value.decode(self._encoding)
            elif isinstance(value, (tuple, list)):
                try:
                    return self.prettyIn(''.join([chr(x) for x in value]))
                except ValueError:
                    raise error.PyAsn1Error(
                        'Bad %s initializer \'%s\'' % (self.__class__.__name__, value)
                    )
            else:
                try:
                    return unicode(value)
                except (LookupError, UnicodeDecodeError):
                    raise error.PyAsn1Error(
                        'Can\'t decode string \'%s\' with \'%s\' codec' % (value, self._encoding)
                    )

        def asOctets(self, padding=True):
            return str(self)

        def asNumbers(self, padding=True):
            return tuple([ord(x) for x in str(self)])

    else:
        def __str__(self):
            return self._value

        def __bytes__(self):
            try:
                return self._value.encode(self._encoding)
            except UnicodeEncodeError:
                raise error.PyAsn1Error(
                    'Can\'t encode string \'%s\' with \'%s\' codec' % (self._value, self._encoding)
                )

        def prettyIn(self, value):
            if isinstance(value, str):
                return value
            elif isinstance(value, bytes):
                try:
                    return value.decode(self._encoding)
                except UnicodeDecodeError:
                    raise error.PyAsn1Error(
                        'Can\'t decode string \'%s\' with \'%s\' codec' % (value, self._encoding)
                    )
            elif isinstance(value, (tuple, list)):
                try:
                    return self.prettyIn(bytes(value))
                except ValueError:
                    raise error.PyAsn1Error(
                        'Bad %s initializer \'%s\'' % (self.__class__.__name__, value)
                    )
            else:
                try:
                    return str(value)
                except UnicodeDecodeError:
                    raise error.PyAsn1Error(
                        'Can\'t decode string \'%s\' with \'%s\' codec' % (value, self._encoding)
                    )

        def asOctets(self, padding=True):
            return bytes(self)

        def asNumbers(self, padding=True):
            return tuple(bytes(self))

    def prettyOut(self, value):
        return value


class NumericString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 18)
    )


class PrintableString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 19)
    )


class TeletexString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 20)
    )


class T61String(TeletexString):
    pass


class VideotexString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 21)
    )


class IA5String(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 22)
    )


class GraphicString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 25)
    )


class VisibleString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 26)
    )


class ISO646String(VisibleString):
    pass


class GeneralString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 27)
    )


class UniversalString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 28)
    )
    encoding = "utf-32-be"


class BMPString(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 30)
    )
    encoding = "utf-16-be"


class UTF8String(AbstractCharacterString):
    tagSet = AbstractCharacterString.tagSet.tagImplicitly(
        tag.Tag(tag.tagClassUniversal, tag.tagFormatSimple, 12)
    )
    encoding = "utf-8"
