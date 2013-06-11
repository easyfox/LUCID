#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import lucid
import base64
import numpy

def find_loop(b64_image_array_string, shape,zoom=0):
    a = numpy.fromstring(base64.b64decode(b64_image_array_string), numpy.uint8).astype("float32")
    a.shape = shape
    return lucid.find_loop(a,zoom)

def face_finder(b64_image_array_string, shape,zoom=0):
    a = numpy.fromstring(base64.b64decode(b64_image_array_string), numpy.uint8).astype("float32")
    a.shape = shape
    b = lucid.face_finder(a,zoom)
    return b

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("", 23640))
    server.register_introspection_functions()

    server.register_function(find_loop)
    server.register_function(face_finder)

    server.serve_forever()
