# import datetime
from datetime import datetime, timedelta, timezone

class TimeUtil:

    MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    DAYS_EN = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    MONTHS_CN = ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"]
    DAYS_CN = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"]

    # Parses W3CDTF Time stamps eg 1994-11-05T13:15:30Z, 1997-07-16T19:20:30.45+01:00
    @staticmethod
    def parseW3CDTF(time:str) -> datetime:
        if not time:
            return None
        if time[-1] == 'Z':
            return datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        else:
            timezone_str = time[-6:]
            offset = int(timezone_str[1:3]) * 60 + int(timezone_str[4:6])
            if timezone_str[0] == '-':
                offset = -offset
            return datetime.strptime(time[:-6], '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone(timedelta(minutes=offset)))

    @staticmethod
    def getFormattedDateEN(date:datetime) -> str:
        s = ""
        s += TimeUtil.DAYS_EN[date.weekday()] + ", "
        s += TimeUtil.MONTHS_EN[date.month - 1] + " "
        s += str(date.day) + ", "
        s += str(date.year)
        s += " " + str(TimeUtil.__getShortHour(date)) + ":" + (date.minute < 10 and "0" or "") + str(date.minute) + TimeUtil.getAMPM(date)
        return s

    @staticmethod
    def getFormattedDateCN(date:datetime) -> str:
        s = ""
        s += TimeUtil.__numberToChinese(date.year) + "年, "
        s += TimeUtil.MONTHS_CN[date.month - 1]
        s += TimeUtil.__numberToChinese(date.day) + "日, "
        s += TimeUtil.DAYS_CN[date.weekday()] + ", "
        s += (TimeUtil.getAMPM(date) == "pm" and "下午" or "上午") + TimeUtil.__numberToChinese(TimeUtil.__getShortHour(date)) + "点" + TimeUtil.__numberToChinese(date.minute)
        return s

    @staticmethod
    def getAMPM(date:datetime) -> str:
        return "pm" if date.hour > 11 else "am"

    @staticmethod
    def getClockTime(milliseconds:int, showHour:bool = True) -> str:
        seconds, milliseconds = divmod(milliseconds, 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if showHour:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            if hours > 0:
                return f"{hours:02}:{minutes:02}:{seconds:02}"
            else:
                return f"{minutes:02}:{seconds:02}"

    @staticmethod
    def __fixNumber(number:int) -> str:
        addzero = str(number + 100)[1:2]
        return addzero

    @staticmethod
    def __getShortHour(date:datetime) -> int:
        h = date.hour
        if h == 0 or h == 12:
            return 12
        elif h > 12:
            return h - 12
        else:
            return h

    @staticmethod
    def __numberToChinese(number:int) -> str:
        arr = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]
        s = str(number)

        if number > 1000:
            return arr[int(s[0])] + arr[int(s[1])] + arr[int(s[2])] + arr[int(s[3])]
        if number < 10:
            return arr[number]
        if number < 100:
            return (arr[int(number / 10)] if int(number / 10) > 1 else "十") + (arr[number % 10] if number % 10 else "十")
        return None