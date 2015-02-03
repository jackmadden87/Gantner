__author__ = 'jackmadden87'

import socket
import struct


class Egate(object):
    """e.gate Object"""
    ports = {
        'ftp_port': 21,                 # TCP
        'e.con': 1234,                  # UDP
        'broadcast_ASCII': 5565,        # UDP
        'high_speed_port_UDP': 8000,    # UDP
        'high_speed_port_TCP': 8001,    # TCP
        'UART0': 8010,                  # TCP
        'UART1': 8011,                  # TCP
        'UART2': 8012,                  # TCP
        'UART3': 8013,                  # TCP
        'data_port': 10000,
        }

    def __init__(self, address="192.168.222.100"):
        """Initialise egate with ip address"""
        self.address = address
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def tcp_connect(self):
        """Attempt connection to TCP port 8001"""
        port = Egate.ports.get('high_speed_port_TCP')

        try:
            self.skt.connect((self.address, port))
        except socket.error:
            print "Failed to connect to " + self.address + ":" + str(port)


class Session(object):
    """Egate Request - Response handling"""

    def __init__(self, skt, request=""):
        """Initialisation"""
        self.skt = skt
        self.request = request

    def send_request(self):
        try:
            self.skt.sendall(self.request)
        except socket.error:
            print "Unable to send request, is connection active?"

    def get_response(self):
        pass


class Request(object):

    def __init__(self, command=0, offset_write=0, length_write=0, data_write=None, offset_read=0, length_read=0):
        """Initialisation of Dummy request"""
        self.frameLength = [self.get_frame_length(), 'H']    # 2 byte int
        self.command = [command, 'b']                        # 1 Byte Int
        self.offsetWrite = [offset_write, 'H']               # 2 Byte Int
        self.lengthWrite = [length_write, 'H']               # 2 Byte Int
        self.dataWrite = data_write                          # n Bytes
        self.offsetRead = [offset_read, 'H']                 # 2 Byte Int
        self.lengthRead = [length_read, 'H']                 # 2 Byte Int

    def get_frame_length(self):
        """Returns the length of the frame(minus this component), taking into account the length
           of the data to be sent"""
        if self.dataWrite is None:
            return 9
        else:
            return 9 + len(self.dataWrite)

    def pack_frame(self):
        """Pack the request into hex data ready for transmission"""
        request = ""

        for data in [self.frameLength, self.command, self.offsetWrite,
                     self.lengthWrite, self.dataWrite, self.offsetRead, self.lengthRead]:
            if data is not None:
                request += struct.pack(">" + data[1], data[0])

        return request


class StateRequest(Request):

    def __init__(self):
        super(StateRequest, self).__init__(command=1, length_read=65535)


class ClockRequest(Request):
    """Read and Write the RealTimeClock"""
    def __init__(self, cmd="read", time="None"):
        self.cmd = cmd
        self.time = time
        super(ClockRequest, self).__init__(command=2, length_read=self.read_write())

    def read_write(self):
        if self.cmd == "read":
            return 0
        elif self.cmd == "write":
            return 9
        else:
            print "Unknown RealTimeClock command, using 'Read' mode"
            return 0  # todo Handle this as an exception

    def gen_clock(self):
        pass