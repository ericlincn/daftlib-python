import re
import random
import math

class StringUtil:

    BG2312:str = "gb2312" # chinese, CN-GB, csGB2312, csGB231280, csISO58GB231280, GB_2312-80, GB231280, GB2312-80, GBK, iso-ir-58
    BIG5:str = "big5" # cn-big5, csbig5, x-x-big5
    GBK:str = "gbk"
    UNICODE:str = "unicode" # utf-16
    UTF8:str = "utf-8" # unicode-1-1-utf-8, unicode-2-0-utf-8, x-unicode-2-0-utf-8

    def encodeByCharset(source:str, charset:str) -> bytes:
        encoded = source.encode(charset)
        return encoded

    def isURL(source):
        source = StringUtil.trim(source).lower()
        pattern = re.compile('^https?://[a-z0-9]+\.[a-z0-9]+[\/=\?%\-&_~`@[\]\':+!]*([^<>\"\"])*$')
        result = pattern.match(source)
        if result is None:
            return False
        return True

    def isEmail(source):
        pattern = re.compile('^[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}$', re.IGNORECASE)
        return pattern.match(source) is not None

    def isNumber(source):
        try:
            float(source)
            return True
        except ValueError:
            return False

    def trim(source):
        return StringUtil.rtrim(StringUtil.ltrim(source))

    def ltrim(source):
        pattern = re.compile('^\s*')
        return pattern.sub('', source)

    def rtrim(source):
        pattern = re.compile('\s*$')
        return pattern.sub('', source)

    def initialCap(source):
        return source[0].upper() + source[1:].lower()

    def removeWhitespace(source):
        pattern = re.compile(r'[ \n\t\r]')
        return pattern.sub('', source)

    def getNumbersFromString(source):
        pattern = re.compile(r'[^0-9]')
        return pattern.sub('', source)

    def getLettersFromString(source):
        pattern = re.compile(r'[^A-Za-z]')
        return pattern.sub('', source)

    def replace(source, remove, replace):
        pattern = re.compile(remove)
        return pattern.sub(replace, source)

    def substitute(source, *rest):
        if source is None:
            return ''
        args = rest[0] if len(rest) == 1 and isinstance(rest[0], list) else rest
        for i, arg in enumerate(args):
            source = source.replace("{" + str(i) + "}", str(arg))
        return source
    
    def substituteProperty(source, obj):
        if source == None:
            return ''

        for key in obj:
            source = re.sub('\\{' + key + '\\}', str(obj[key]), source, flags=re.MULTILINE)

        return source

    def removeExtension(source):
        extensionIndex = source.rfind('.')
        if extensionIndex == -1:
            return source
        else:
            return source[:extensionIndex]

    def getExtension(source):
        extensionIndex = source.rfind('.')
        if extensionIndex == -1:
            return None
        else:
            return source[extensionIndex + 1:].lower()

    def getRandomString(length):
        chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678' # 默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1
        out = ''
        for i in range(length):
            out += random.choice(chars)
        return out
    
    def containsChinese(source):
        for c in source:
            code = ord(c)
            if (code >= 0x4e00) and (code <= 0x9fbb):
                return True
        return False

    def containsNonEnglish(source):
        for c in source:
            code = ord(c)
            if code > 255 or code < 0:
                return True
        return False

    def getFormattedNumber(value):
        if math.isnan(value):
            return "NaN"
        if value == float('inf'):
            return "Infinity"
        if value == float('-inf'):
            return "-Infinity"

        thousandsSeparator = ","
        decimalSeparator = "."
        strValue = str(value)
        pieces = strValue.split('.')
        before = list(pieces[0])
        after = pieces[1] if len(pieces) > 1 else ''

        beforeFormatted = []
        for i in range(len(before)):
            if i % 3 == 0 and i != 0:
                beforeFormatted.insert(0, thousandsSeparator)
            beforeFormatted.insert(0, before[len(before) - 1 - i])
        result = ''.join(beforeFormatted)
        if len(after) > 0:
            result += decimalSeparator + after

        return result