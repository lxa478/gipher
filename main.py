import struct

HEADER_BLOCK = b'\x47\x49\x46\x38\x39\x61' #GIF89a

class Gipher(object):
    def __init__(self, width, height, background=(255, 255, 255)):
        self.width = width
        self.height = height
        self.background_color = background
        self.frames = []
        self.colors = set()

    def line(self, start, end, fill=(0, 0, 0)):
        self.colors.add(fill)

    def rectangle(self, start, end, fill=(0, 0, 0), stroke=None):
        if not stroke:
            stroke = fill

        self.colors.add(fill)
        self.colors.add(stroke)

    def get_header_block(self):
        header_block = b'\x47\x49\x46\x38\x39\x61'
        return header_block

    def get_logical_screen_descriptor(self, global_color_flag=True, color_resolution=7, sort_color_table=False):
        canvas_width = self.width.to_bytes(2, byteorder='little', signed=False)
        canvas_height = self.height.to_bytes(2, byteorder='little', signed=False)

        global_color_table_flag = 1
        color_resolution = 1
        sort_flag = 0
        size_of_global_color_table = 1

        packed_field = 0
        packed_field = (packed_field << 1) | global_color_table_flag
        packed_field = (packed_field << 3) | color_resolution
        packed_field = (packed_field << 1) | sort_flag
        packed_field = (packed_field << 3) | size_of_global_color_table

        background_color_index = 0
        pixel_aspect_ratio = 0

        bt = bytearray()
        bt.extend(canvas_width)
        bt.extend(canvas_height)
        bt.extend(bytearray([packed_field, background_color_index, pixel_aspect_ratio]))

        return bt

    def get_global_color_table(self):
        colors = [
            (255, 255, 255),
            (255, 0, 0),
            (0, 0, 255),
            (0, 0, 0)
        ]

        color_bytes = bytearray(list(sum(colors, ())))
        return color_bytes

    def get_graphics_control_extension(self):
        return []

    def get_image_descriptor(self):
        lt, rt = 0, 0

        image_seperator = b'\x2c'
        image_left = lt.to_bytes(2, byteorder='little', signed=False)
        image_right = rt.to_bytes(2, byteorder='little', signed=False)
        image_width = self.width.to_bytes(2, byteorder='little', signed=False)
        image_height = self.height.to_bytes(2, byteorder='little', signed=False)
        packed_field = b'\x00'

        bt = bytearray()
        bt.extend(image_seperator)
        bt.extend(image_left)
        bt.extend(image_right)
        bt.extend(image_width)
        bt.extend(image_height)
        bt.extend(packed_field)

        return bt

    def get_image_data(self):
        image_data = b'\x02\x16\x8C\x2D\x99\x87\x2A\x1C\xDC\x33\xA0\x02\x75\xEC\x95\xFA\xA8\xDE\x60\x8C\x04\x91\x4C\x01\x00'
        return image_data

    def get_plain_text_extension(self):
        return []

    def get_application_extension(self):
        return []

    def get_comment_extension(self):
        return []

    def get_trailer(self):
        trailer = b'\x3B'
        return trailer

    def save(self, file_name):
        image = bytearray()
        image.extend(self.get_header_block())
        image.extend(self.get_logical_screen_descriptor())
        image.extend(self.get_global_color_table())
        image.extend(self.get_graphics_control_extension())
        image.extend(self.get_image_descriptor())
        image.extend(self.get_image_data())
        image.extend(self.get_plain_text_extension())
        image.extend(self.get_application_extension())
        image.extend(self.get_comment_extension())
        image.extend(self.get_trailer())

        print([hex(b) for b in image])

        with open(file_name, "wb") as file:
            file.write(image)


def execute():
    print(type(HEADER_BLOCK))
    print(HEADER_BLOCK)

    gipher = Gipher(10, 10)

    gipher.rectangle((4, 4), (6, 6), fill=(255, 0, 0))
    gipher.line((0, 0), (9, 9), fill=(0, 0, 0))

    gipher.save("my_image.gif")


if __name__ == '__main__':
    execute()