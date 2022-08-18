# encoding: utf-8

from __future__ import absolute_import, division, print_function

import logging
import xml.etree.ElementTree as ET

from .constants import MIME_TYPE
from .image import BaseImageHeader

from ..shared import Inches, Cm, Emu, Mm, Pt


def convert_raw_input_to_pixels(measure_input):
    """
    >>> convert_raw_input_to_pixels('300.00pt')


    # See https://www.w3.org/TR/SVG11/struct.html#NewDocument
    """
    if isinstance(measure_input, str):
        if measure_input.lower().endswith('pt'):
            document_picture_measure = Pt(float(measure_input[:-2]))
        elif measure_input.lower().endswith('px'):
            document_picture_measure = Inches(float(measure_input[:-2]) / 96)
        # TODO: To add 'em' support we need to know the "Base size (px)".
        # If Base size is 16px then it will equivalent to 1em and 100%.
        # elif measure_input.endswith('em'):
        #     document_picture_measure = Emu(float(measure_input[:-2]))
        elif measure_input.lower().endswith('cm'):
            document_picture_measure = Cm(float(measure_input[:-2]))
        elif measure_input.lower().endswith('mm'):
            document_picture_measure = Mm(float(measure_input[:-2]))
        elif measure_input.lower().endswith('in'):
            document_picture_measure = Inches(float(measure_input[:-2]))
        elif measure_input.lower().endswith('pc'):
            document_picture_measure = Pt(float(measure_input[:-2]) / 12)
        else:
            logging.warning("Assume size in pixels")
            document_picture_measure = Inches(float(measure_input) / 96)
    elif isinstance(measure_input, (int, float)):
        logging.warning("Assume size in pixels")
        document_picture_measure = Inches(float(measure_input) / 96)
    else:
        raise TypeError(f"Unsupported width input type {type(measure_input)}")
    return document_picture_measure.inches * 96


class Svg(BaseImageHeader):
    """
    Image header parser for SVG images.
    """

    @classmethod
    def from_stream(cls, stream):
        """
        Return |Svg| instance having header properties parsed from SVG image
        in *stream*.
        """
        px_width, px_height = cls._dimensions_from_stream(stream)
        return cls(px_width, px_height, 72, 72)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/svg+xml` for
        SVG images.
        """
        return MIME_TYPE.SVG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'svg' for SVG images.
        """
        return "svg"

    @classmethod
    def _dimensions_from_stream(cls, stream):
        stream.seek(0)
        data = stream.read()
        root = ET.fromstring(data)
        width = int(convert_raw_input_to_pixels(root.attrib["width"]))
        height = int(convert_raw_input_to_pixels(root.attrib["height"]))
        return width, height
