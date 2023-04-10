class SoundUtil:
    
    @staticmethod
    def SILENT_SOUND_BASE64() -> str:
        str = "UklGRooWAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YWYW"
        i = len(str)
        while i < 7704:
            str += "A"
            i += 1
        return str