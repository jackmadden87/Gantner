__author__ = 'Jack Madden'

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
        self.session = Session(self.skt)

    def tcp_connect(self):
        """Attempt connection to TCP port 8001"""
        port = Egate.ports.get('high_speed_port_TCP')

        try:
            self.skt.connect((self.address, port))
        except socket.error:
            print "Failed to connect to " + self.address + ":" + str(port)


class Session(object):
    """Egate Request - Response handling"""

    def __init__(self, skt):
        """Initialisation"""
        self.skt = skt

    def send_request(self, request=""):
        try:
            self.skt.sendall(request)
        except socket.error:
            print "Unable to send request, is connection active?"

    def get_response(self):
        pass


class RequestGenerator(object):

    def __init__(self, command=0, offset_write=0, length_write=0, data_write=None, offset_read=0, length_read=0):
        """init"""
        self.command = command
        self.offset_write = offset_write
        self.length_write = length_write
        self.data_write = data_write
        self.offset_read = offset_read
        self.length_read = length_read

    @staticmethod
    def print_request_format():
        """print out a set of strings to show how to build a request"""
        print "Could not pack this request"
        print "Request must be a dict of format"
        print "KEY\t\t\t\tBYTES"
        print "'command':\t\t\t1"
        print "'offset_write':\t\t2"
        print "'length_write':\t\t2"
        print "'data_write'\t\tn"
        print "'offset_read:'\t\t2"
        print "'length_read':\t\t2"

    @staticmethod
    def pack(request):
        """Calculate frame length and pack up a request
           ready for sending to the egate.
           Method expects Dict with format as defined in
           RequestGenerator.print_request_format()"""
        try:
            command = request.get('command')
            offset_write = request.get('offset_write')
            length_write = request.get('length_write')
            data_write = request.get('data_write')
            offset_read = request.get('offset_read')
            length_read = request.get('length_read')

            # get length of the data to head the request
            if data_write is None:
                frame_length = 9
            else:
                frame_length = 9 + len(data_write)

            packing_format = ["H", "b", "H", "H", "H", "H"]
            data_to_pack = [frame_length, command, offset_write, length_write, offset_read, length_read]
            packed_request = ""

            for fmt, data in zip(packing_format, data_to_pack):
                packed_request += struct.pack(">" + fmt, data)

            print struct.unpack(">HbHHHH", packed_request)
            return packed_request

        except AttributeError:
            RequestGenerator.print_request_format()
        except ValueError:
            RequestGenerator.print_request_format()

    def request_variable(self):
        pass

    def request_state(self, command=1, length_read=65535):
        """Returns a dict containing the request parameters for a State
        Request from an egate"""

        request = {"command": command,
                   "offset_write": self.offset_write,
                   "length_write": self.length_write,
                   "data_write": self.data_write,
                   "offset_read": self.offset_read,
                   "length_read": length_read}
        return request

    def request_clock(self, command=2, clk=None):
        """Return a dict containing the request parameters for a Clock
           Request from an egate. Method defaults to 'get'. To 'set'
           the clock, pass parameters to 'clk' variable"""

        if clk is None:
            # Build a request to GET the Real Time Clock.

            request = {"command": command,
                       "offset_write": self.offset_write,
                       "length_write": 0,
                       "data_write": self.data_write,
                       "offset_read": self.offset_read,
                       "length_read": 65535}

            return request
        else:
            # Build a request to SET the Real Time Clock

            request = {"command": command,
                       "offset_write": self.offset_write,
                       "length_write": 9,
                       "data_write": clk,
                       "offset_read": self.offset_read,
                       "length_read": 0}

            return request

    def request_circlebuffer(self):
        pass

    def request_filetransfer(self):
        pass

    def request_diagnostics(self, command=9):
        """Return a dict containing the request parameters for a Diagnostic
           Request from an egate"""
        request = {"command": command,
                   "offset_write": self.offset_write,
                   "length_write": self.length_write,
                   "data_write": self.data_write,
                   "offset_read": self.offset_read,
                   "length_read": 65535}
        return request

    def request_logger(self):
        pass


if __name__ == '__main__':

    r = RequestGenerator()
    r.pack(r.request_state())
    r.pack(r.request_diagnostics())
    r.pack(r.request_clock())