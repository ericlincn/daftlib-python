import time

class SnowflakeID:

    def __init__(self, machine_id):
        # machine_id 0 ~ 1023
        self.machine_id_bits = 10
        # sequence 0 ~ 4095
        self.sequence_bits = 12
        # start timestamp
        magic_date = time.strptime('2023-05-18 18:56:00', "%Y-%m-%d %H:%M:%S")
        self.twepoch = int(time.mktime(magic_date) * 1000)

        self.max_machine_id = -1 ^ (-1 << self.machine_id_bits)
        self.max_sequence = -1 ^ (-1 << self.sequence_bits)
        
        if machine_id > self.max_machine_id:
            raise ValueError("Machine ID exceeds the maximum value.")
        
        self.__machine_id = machine_id

        self.__sequence = 0
        self.__last_timestamp = -1

    def _current_timestamp(self):
        return int(time.time() * 1000)

    def _wait_next_millisecond(self, last_timestamp):
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp

    def generate_id(self):
        timestamp = self._current_timestamp()

        if timestamp < self.__last_timestamp:
            raise ValueError("Clock moved backwards. Refusing to generate ID.")

        # In same millisecond
        if timestamp == self.__last_timestamp:
            self.__sequence = (self.__sequence + 1) & self.max_sequence
            # 4096 sequence_id are sold out, wait for next millisecond
            if self.__sequence == 0:
                timestamp = self._wait_next_millisecond(self.__last_timestamp)
        else:
            # New millisecond
            self.__sequence = 0

        # Saving last timestamp
        self.__last_timestamp = timestamp

        snowflake_id = (((timestamp - self.twepoch) << (self.machine_id_bits + self.sequence_bits)) |
                        (self.__machine_id << self.sequence_bits) |
                        self.__sequence)

        return snowflake_id