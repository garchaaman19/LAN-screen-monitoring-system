from socket import socket
from zlib import decompress
import cv2
import numpy
from PIL import Image


WIDTH = int(1366 / 1)
HEIGHT = int(768 / 1)


def recvall(conn, length):
    buf = b''
    while len(buf) < length:
        data = conn.recv(length - len(buf))
        if not data:
            return data
        buf += data
    return buf



def main(host='127.0.0.1', port=5000):
    watching = True

    sock = socket()
    sock.connect((host, port))
    try:
        while watching:
            size_len = int.from_bytes(sock.recv(1), byteorder='big')
            size = int.from_bytes(sock.recv(size_len), byteorder='big')
           
            bgra = decompress(recvall(sock, size))
            img = Image.frombytes("RGB", (WIDTH, HEIGHT), bgra, "raw", "BGRX")
            np_ar = numpy.array(img, dtype=numpy.uint8)
            
            np_ar = numpy.flip(np_ar[:, :, :3], 2)
            cv2.imshow("OpenCV show", np_ar)

            if cv2.waitKey(25) & 0xFF == ord("q"): ##escape key
                cv2.destroyAllWindows()#to jump out of window
                break
    finally:
        sock.close()


if __name__ == '__main__':
    main()
