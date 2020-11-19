"""
协议序列号:
    格式： 0 - 46位时间戳  - 17位序列号

直接调用 nextId()
"""
import time


def getNewStamp():
    current_seconds = time.time()
    return int(current_seconds * 1000)


# value 秒级时间戳
def timestamp_datetime(value):
    _format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(value)
    dt = time.strftime(_format, value)
    return dt


class GetSeqNo(object):
    sequence = 0
    lastStamp = 0

    # 2018-01-01 08:00:00,000
    START_STAMP = 1514764800000
    SEQUENCE_BIT = 17
    MAX_SEQUENCE = -1 ^ (-1 << SEQUENCE_BIT)
    TIMESTAMP_LEFT = SEQUENCE_BIT

    def __init__(self):
        self.sequence = 0
        self.lastStamp = 0

    def nextId(self):
        curr_stamp = getNewStamp()
        if curr_stamp == self.lastStamp:
            self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
            if self.sequence == 0:
                curr_stamp = self.getNextMill()
        else:
            self.sequence = 0

        self.lastStamp = curr_stamp
        return (curr_stamp - self.START_STAMP) << self.TIMESTAMP_LEFT | self.sequence

    def getNextMill(self):
        mill = getNewStamp()
        while mill <= self.lastStamp:
            mill = getNewStamp()
        return mill

    def getTimeMills(self, _id):
        self.isRangeID(_id)
        return (_id >> self.TIMESTAMP_LEFT) + self.START_STAMP

    def getSequence(self, _id):
        self.isRangeID(_id)
        return _id & self.MAX_SEQUENCE

    @staticmethod
    def isRangeID(_id):
        if _id < 0:
            raise RuntimeError("id range error.")


if __name__ == "__main__":
    seq = GetSeqNo()
    msg_id = seq.nextId()
    print(msg_id)
    print(timestamp_datetime(seq.getTimeMills(msg_id) / 1000))
    print(seq.getSequence(msg_id))
