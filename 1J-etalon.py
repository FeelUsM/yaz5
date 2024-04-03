from __future__ import annotations

from bisect import insort_left
from collections import deque
from dataclasses import dataclass
from enum import IntEnum


class ImageType(IntEnum):
    EMBEDDED = 0
    SURROUNDED = 1
    FLOATING = 2


@dataclass
class Image:
    width: int
    height: int
    dx: int
    dy: int
    type: ImageType


class Fragment:
    def __init__(self, width: int, dx: int):
        self.remain_width: int = width
        self.width: int = width
        self.dx: int = dx
        self.is_first = True
        self.right_corner_x: int = dx
        self.right_corner_y: int = 0

    def checkCapacity(self, token_width: int, is_surrounded: int) -> bool:
        if self.is_first or is_surrounded:
            return token_width <= self.remain_width
        return token_width + char_w <= self.remain_width

    def addWord(self, token_width: int):
        if self.is_first:
            self.remain_width -= token_width
            self.is_first = False
        else:
            self.remain_width -= token_width + char_w
        self.right_corner_x = self.dx + self.width - self.remain_width
        self.right_corner_y = 0

    def addEmbeddedImage(self, image: Image):
        if self.is_first:
            image.dx = self.dx + self.width - self.remain_width
            self.remain_width -= image.width
            self.is_first = False
        else:
            image.dx = self.dx + self.width - self.remain_width + char_w
            self.remain_width -= image.width + char_w
        self.right_corner_x = self.dx + self.width - self.remain_width
        self.right_corner_y = 0

    def addSurroundedImage(self, image: Image):
        image.dx = self.dx + self.width - self.remain_width
        self.remain_width -= image.width
        self.is_first = True
        self.right_corner_x = self.dx + self.width - self.remain_width
        self.right_corner_y = 0

    def addFloatingImage(self, image: Image, absolute_dy: int):
        if self.right_corner_x + image.dx >= 0:
            if self.right_corner_x + image.dx + image.width <= file_width:
                image.dx = self.right_corner_x + image.dx
            else:
                shift: int = self.right_corner_x + image.dx + image.width - file_width
                image.dx = self.right_corner_x + image.dx - shift
        else:
            image.dx = 0

        self.right_corner_x = image.dx + image.width
        self.right_corner_y = image.dy + self.right_corner_y
        image.dy = absolute_dy + self.right_corner_y


class FileString:
    def __init__(self, images: list[Image]):
        self.height: int = file_height
        self.fragments: deque[Fragment] = deque()
        self.createFragments(images)

    def createFragments(self, images: list[Image]):
        if images:
            if images[0].dx != 0:
                self.fragments.append(Fragment(images[0].dx, 0))
            for i in range(len(images) - 1):
                new_width: int = images[i + 1].dx - images[i].dx - images[i].width
                if new_width != 0:
                    self.fragments.append(Fragment(new_width, images[i].dx + images[i].width))

            right_corner: int = images[-1].dx + images[-1].width
            if right_corner != file_width:
                self.fragments.append(Fragment(file_width - right_corner, right_corner))
        else:
            self.fragments.append(Fragment(file_width, 0))

    def addWord(self, width) -> bool:
        while self.fragments:
            cur_fragment: Fragment = self.fragments[0]
            if cur_fragment.checkCapacity(width, False):
                cur_fragment.addWord(width)
                return True
            self.fragments.popleft()

        return False

    def addEmbeddedImage(self, image: Image):
        while self.fragments:
            cur_fragment: Fragment = self.fragments[0]
            if cur_fragment.checkCapacity(image.width, False):
                cur_fragment.addEmbeddedImage(image)
                self.height = max(self.height, image.height)
                return True
            self.fragments.popleft()

        return False

    def addSurroundedImage(self, image: Image):
        while self.fragments:
            cur_fragment: Fragment = self.fragments[0]
            if cur_fragment.checkCapacity(image.width, True):
                cur_fragment.addSurroundedImage(image)
                return True
            self.fragments.popleft()

        return False

    def addFloatingImage(self, image: Image, absolute_dy: int):
        self.fragments[0].addFloatingImage(image, absolute_dy)


class Paragraph:
    def __init__(self, dy: int):
        self.height: int = 0
        self.dy: int = dy
        self.images: list[Image] = []
        self.strings: list[FileString] = [FileString(self.images)]

    def addString(self):
        self.height += self.strings[-1].height
        self.refreshImages()
        self.strings.append(FileString(self.images))

    def refreshImages(self):
        new_images: list[Image] = []
        for image in self.images:
            if self.dy + self.height < image.dy + image.height:
                new_images.append(image)
        self.images = new_images

    def addWord(self, width):
        while not self.strings[-1].addWord(width):
            self.addString()

    def addImage(self, image: Image):
        match image.type:
            case ImageType.EMBEDDED:
                while not self.strings[-1].addEmbeddedImage(image):
                    self.addString()
                image.dy = self.dy + self.height

            case ImageType.SURROUNDED:
                while not self.strings[-1].addSurroundedImage(image):
                    self.addString()
                image.dy = self.dy + self.height
                insort_left(self.images, image, key=lambda elem: elem.dx)

            case ImageType.FLOATING:
                self.strings[-1].addFloatingImage(image, self.dy + self.height)

        print(image.dx, image.dy)

    def endParagraph(self):
        self.addString()
        if self.images:
            max_h: Image = max(self.images, key=lambda elem: elem.dy + elem.height)
            diff: int = max_h.dy + max_h.height - self.height
            if diff > 0:
                self.height += diff


class File:
    def __init__(self):
        self.height: int = 0
        self.paragraphs: list[Paragraph] = [Paragraph(0)]

    def parseString(self, string: str):
        token_w: int = 0
        is_empty: bool = True
        i: int = 0
        while i < len(string):
            if string[i] not in " \t\n":
                is_empty = False
                if string[i] != "(":
                    token_w += char_w
                    i += 1
                else:
                    new_i = string.find(")", i + 1)
                    image = self.parseString2Image(string, i + 1, new_i)
                    self.paragraphs[-1].addImage(image)
                    i = new_i + 1

            else:
                if token_w != 0:
                    self.paragraphs[-1].addWord(token_w)
                    token_w = 0
                i += 1

        if token_w != 0:
            self.paragraphs[-1].addWord(token_w)

        if is_empty:
            self.paragraphs[-1].endParagraph()
            self.height += self.paragraphs[-1].height
            self.paragraphs.append(Paragraph(self.height))

    def parseString2Image(self, string: str, start: int, end: int) -> Image:
        image_arr: list[str] = string[start:end].split()[1:]

        key_val = [elem.split("=") for elem in image_arr]
        dx = dy = 0
        for key, val in key_val:
            match key:
                case "layout":
                    if val == "embedded":
                        image_type = ImageType.EMBEDDED
                    elif val == "surrounded":
                        image_type = ImageType.SURROUNDED
                    else:
                        image_type = ImageType.FLOATING
                case "width":
                    width = int(val)
                case "height":
                    height = int(val)
                case "dx":
                    dx = int(val)
                case "dy":
                    dy = int(val)

        return Image(width, height, dx, dy, image_type)


with open("input.txt", "r") as fin:
    file_width, file_height, char_w = map(int, fin.readline().split())
    file: File = File()
    lines: list[str] = []

    cur_line: str = ""
    for line in fin:
        if not line.rstrip():
            lines.append(cur_line)
            lines.append("")
            cur_line = ""
        else:
            cur_line += " " + line.rstrip()
    lines.append(cur_line)

    for line in lines:
        file.parseString(line)
