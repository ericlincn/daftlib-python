import re
import random
import math

class StringUtil:

    BG2312:str = "gb2312" # chinese, CN-GB, csGB2312, csGB231280, csISO58GB231280, GB_2312-80, GB231280, GB2312-80, GBK, iso-ir-58
    BIG5:str = "big5" # cn-big5, csbig5, x-x-big5
    GBK:str = "gbk"
    UNICODE:str = "unicode" # utf-16
    UTF8:str = "utf-8" # unicode-1-1-utf-8, unicode-2-0-utf-8, x-unicode-2-0-utf-8

    @staticmethod
    def encodeByCharset(source:str, charset:str) -> bytes:
        encoded = source.encode(charset)
        return encoded

    @staticmethod
    def isURL(source:str) -> bool:
        source = StringUtil.trim(source).lower()
        pattern = re.compile('^https?://[a-z0-9]+\.[a-z0-9]+[\/=\?%\-&_~`@[\]\':+!]*([^<>\"\"])*$')
        result = pattern.match(source)
        if result is None:
            return False
        return True

    @staticmethod
    def isEmail(source:str) -> bool:
        pattern = re.compile('^[A-Z0-9._%+-]+@(?:[A-Z0-9-]+\.)+[A-Z]{2,4}$', re.IGNORECASE)
        return pattern.match(source) is not None

    @staticmethod
    def isNumber(source:str) -> bool:
        try:
            float(source)
            return True
        except ValueError:
            return False

    @staticmethod
    def trim(source:str) -> str:
        return StringUtil.rtrim(StringUtil.ltrim(source))

    @staticmethod
    def ltrim(source:str) -> str:
        pattern = re.compile('^\s*')
        return pattern.sub('', source)

    @staticmethod
    def rtrim(source:str) -> str:
        pattern = re.compile('\s*$')
        return pattern.sub('', source)

    @staticmethod
    def initialCap(source:str) -> str:
        return source[0].upper() + source[1:].lower()

    @staticmethod
    def removeWhitespace(source:str) -> str:
        pattern = re.compile(r'[ \n\t\r]')
        return pattern.sub('', source)

    @staticmethod
    def getNumbersFromString(source:str) -> str:
        pattern = re.compile(r'[^0-9]')
        return pattern.sub('', source)

    @staticmethod
    def getLettersFromString(source:str) -> str:
        pattern = re.compile(r'[^A-Za-z]')
        return pattern.sub('', source)

    @staticmethod
    def replace(source:str, remove:str, replace:str) -> str:
        pattern = re.compile(remove)
        return pattern.sub(replace, source)

    @staticmethod
    def substitute(source:str, *rest) -> str:
        if source is None:
            return ''
        args = rest[0] if len(rest) == 1 and isinstance(rest[0], list) else rest
        for i, arg in enumerate(args):
            source = source.replace("{" + str(i) + "}", str(arg))
        return source
    
    @staticmethod
    def substituteProperty(source:str, obj) -> str:
        if source == None:
            return ''

        for key in obj:
            source = re.sub('\\{' + key + '\\}', str(obj[key]), source, flags=re.MULTILINE)

        return source

    @staticmethod
    def removeExtension(source:str) -> str:
        extensionIndex = source.rfind('.')
        if extensionIndex == -1:
            return source
        else:
            return source[:extensionIndex]

    @staticmethod
    def getExtension(source:str) -> str:
        extensionIndex = source.rfind('.')
        if extensionIndex == -1:
            return None
        else:
            return source[extensionIndex + 1:].lower()

    @staticmethod
    def getRandomString(length:int) -> str:
        chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678' # 默认去掉了容易混淆的字符oOLl,9gq,Vv,Uu,I1
        out = ''
        for i in range(length):
            out += random.choice(chars)
        return out
    
    @staticmethod
    def getRandomCode(length:int) -> str:
        digits = [str(random.randint(0, 9)) for _ in range(length)]
        code = ''.join(digits)
        return code
    
    @staticmethod
    def containsChinese(source:str) -> bool:
        for c in source:
            code = ord(c)
            if (code >= 0x4e00) and (code <= 0x9fbb):
                return True
        return False

    @staticmethod
    def containsNonEnglish(source:str) -> bool:
        for c in source:
            code = ord(c)
            if code > 255 or code < 0:
                return True
        return False

    @staticmethod
    def getFormattedNumber(value) -> str:
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
    
    @staticmethod
    def getTextInsideBrackets(source:str) -> str:
        pattern = r'\[(.*?)\]'
        match = re.search(pattern, source)
        if match:
            return match.group(1)
        else:
            return None
    
    @staticmethod
    def sanitizeFilename(filename:str) -> str:
        forbidden_chars = r'[<>:"/\\|?*\x00-\x1F\x7F]'
        sanitized_filename = re.sub(forbidden_chars, '', filename)
        return sanitized_filename