from babushkin_arch import *
from unittest import TestCase
from StringIO import StringIO as sio


class TestBabArch(TestCase):
    
    def try_compress_decompress(self, data):
        source = sio(data)
        dest = sio()
        encode_file(source, dest)
        dest.seek(0)
        
        decoded = sio()
        decode_file(dest, decoded)

        decoded_data = decoded.getvalue()
        self.assertEqual( len(data), len(decoded_data))
        self.assertEqual( data, decoded_data )
        
    def test_hello_world(self):
        """Test that data is decoded correctly"""
        self.try_compress_decompress( "hello world" )
        self.try_compress_decompress( "hello world world world world" )
        
    def test_random_data(self):
        from random import random, randint
        for i in xrange(1000):
            #make random string
            n = randint(1, 1000)
            s = "".join( chr(randint(0,255)) for _ in xrange(n))            
            self.try_compress_decompress(s)

