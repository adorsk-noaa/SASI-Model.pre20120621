"""
Utility functions for working with mapserver.
"""
from cStringIO import StringIO
import mapscript

def ms_img_to_buffer(ms_img): return StringIO(ms_img.getBytes())


