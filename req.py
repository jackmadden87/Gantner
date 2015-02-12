__author__ = 'jack'
import struct


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
    def pack(request):
        """HbHHnHH"""
        try:
            command = request.get('command')
            offset_write = request.get('offset_write')
            length_write = request.get('length_write')
            data_write = request.get('data_write')
            offset_read = request.get('offset_read')
            length_read = request.get('length_read')

            print(command, offset_write, length_write, data_write, offset_read, length_read)

        except AttributeError:
            print "Could not pack this request"
            print "Request must be a dict of format"
            print "KEY\t\t\t\tBYTES"
            print "'command':\t\t\t1"
            print "'offset_write':\t\t2"
            print "'length_write':\t\t2"
            print "'data_write'\t\tn"
            print "'offset_read:'\t\t2"
            print "'length_read':\t\t2"
        except struct.error:
            print "you fucked up!"


    def state_request(self, command=1, length_read=65535):
        """Returns a dict containing the request params for a state
        Request from an egate"""

        request = {"command": command,
                   "offset_write": self.offset_write,
                   "length_write": self.length_write,
                   "data_write": self.data_write,
                   "offset_read": self.offset_read,
                   "length_read": length_read}
        return request


if __name__ == '__main__':

    r = RequestGenerator()
    r.pack("asdfaf")