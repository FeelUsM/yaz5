from sys import stdin
input = stdin.readline


DEBUG = True

grid = []
def debug(*args):
    if DEBUG:
        print(*args)


class Word:
    x = y = -1
    def __init__(self, text, size):
        self.text = text
        self.size = size

    def prespace(self):
        self.text = " " + self.text

    def display(self):
        l = len(self)
        debug(f"text l:{l} ({self.text}) x:{self.x} y:{self.y} end:{self.size + self.x}")


    def __len__(self):
        return len(self.text)

    def set(self, x, y):
        self.x = x
        self.y = y

        if not DEBUG:
            return
        for col in range(x, x + self.size):
            col += 1
            row = self.y
            if grid[row][col] != ".":
                1/0
            grid[row][col] = "T"

def make_word(arr, charl):
    return Word("".join(arr), len(arr) * charl)


class Pad:
    def __init__(self, size):
        self.size = size
    def display(self):
        debug(f"Pad:{self.size}")


    def set(self, x, y):
        self.x = x
        self.y = y
        if not DEBUG:
            return

        for col in range(x, x + self.size):
            col += 1
            row = self.y
            if grid[row][col] != ".":
                grid[row][col] = "!"
                continue
                1/0
            grid[row][col] = "p"

class Blocked:
    x = y = -1
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def display(self):
        debug(f"Blocked:{self.start}-{self.end}")


SURR = "surrounded"
FLOAT = "floating"
EMB = "embedded"



def intercept(start1, end1, start2, end2):
    intervals = [[start1, end1], [start2, end2]]
    intervals.sort()
    result = []
    for start, end in intervals:
        if not result or result[-1][1] < start:
            result.append([start, end])
        else:
            result[-1][1] = max(result[-1][1], end)

    return len(result) == 1

class Line:
    def __init__(self, cfg, num, offset, blocks):
        self.blocks = blocks
        self.offset = offset
        self.num = num
        self.frags = []
        self.cfg = cfg
        self.width = 0
        self.height = cfg.line_height


    def display(self):
        debug(
            f"line {self.num}: off:{self.offset} w:{self.width} h:{self.height}, frags:{self.frags}"
        )
        debug(f'...blocks {self.blocks}')
        for obj in self.frags:
            obj.display()
        debug("...")

    def add_word(self, word):
        need = len(word) * self.cfg.char_width
        padding = 0
        floatless = []
        for x in self.frags:
            if not isinstance(x, Blocked):
                if not isinstance(x, Image) or x.layout != FLOAT:
                    floatless.append(x)
        if floatless and (isinstance(floatless[-1], Word) or  floatless[-1].layout == EMB):
            padding = self.cfg.char_width

        blocked = 0
        for start, end, _ in self.blocks:

            if padding and (self.width <= start <= self.width + padding or self.width <= end <= self.width + padding):
                padding = 0
                blocked = end  - self.width + 1
            if intercept(start, end, self.width + padding + blocked, self.width + need + padding + blocked - 1):
                padding = 0
                blocked = end  - self.width + 1
                self.frags.append(Blocked(start, end))
            # elif self.width <= end <= self.width + padding + blocked:
            #     blocked = end - self.width - 1
            #     padding = 0

        if self.width + need + padding + blocked > self.cfg.page_width:
            return False

        word.set(self.width + padding + blocked, self.offset)

        if padding:
            pad = Pad(self.cfg.char_width)
            pad.set(self.width, self.offset)
            self.frags.append(pad)

        self.width += need + padding + blocked

        self.frags.append(word)
        return True

    def add_image(self, image):
        block = None
        need = 0
        if image.layout != FLOAT:
            need = image.width

        padding = 0

        if image.layout == EMB:
            floatless = []
            for x in self.frags:
                if not isinstance(x, Blocked):
                    if not isinstance(x, Image) or x.layout != FLOAT:
                        floatless.append(x)


            if floatless and (isinstance(floatless[-1], Word) or  floatless[-1].layout == EMB):
                padding = self.cfg.char_width

        blocked = 0
        for start, end, _ in self.blocks:
            if padding and (self.width <= start <= self.width + padding or self.width <= end <= self.width + padding):
                debug("RESETTING padding", self.offset, self.width, end, padding, image.display(True))
                debug("BLOCKS", self.blocks)
                padding = 0
                blocked = end  - self.width + 1
            if intercept(start, end, self.width + padding + blocked, self.width + need + padding + blocked - 1):
                debug("BLOCKED", image.display(True),"|", padding, (start, end), (self.width + padding + blocked, self.width + need + padding + blocked))

                padding = 0
                blocked = end  - self.width + 1
                self.frags.append(Blocked(start, end))
            # elif self.width <= end <= self.width + padding + blocked:
            #     blocked = end - self.width - 1
            #     padding = 0


        if self.width + need + padding + blocked> self.cfg.page_width:
            return False

        if padding:
            pad = Pad(self.cfg.char_width)
            pad.set(self.width, self.offset)

            self.frags.append(pad)

        self.width += padding + blocked

        if image.layout == FLOAT:
            prev = [x for x in self.frags if isinstance(x, Image) or isinstance(x, Word)]
            if not prev or not isinstance(prev[-1], Image):
                image.set(self.width, self.offset)
            else:
                prev_img = prev[-1]
                prev_img_x = prev_img.x + prev_img.width
                prev_img_y = prev_img.y
                image.set(prev_img_x, prev_img_y)
            if image.x < 0:
                image.x = 0
            if image.x + image.width > self.cfg.page_width:
                image.x = self.cfg.page_width - image.width
        else:
            image.set(self.width, self.offset)

        if image.layout == EMB:
            self.height = max(self.height, image.height)


        self.width += need
        self.frags.append(image)

        return True




class Image:
    """
    (image layout=surrounded width=25 height=58)
    and word is
    (image layout=floating dx=18 dy=-15 width=25 height=20)
    here new
    (image layout=embedded width=20 height=22)
    another
    """
    x = y = 0
    def __init__(self, layout=None, width=None, height=None, dx=None, dy=None):
        self.layout=layout
        self.width=int(width)
        self.height=int(height)
        if dx:
            self.x = int(dx)
        if dy:
            self.y = int(dy)
        self.dx=dx
        self.dy=dy

    def display(self, txt=False):
        data = f"image layout:{self.layout} width:{self.width} height:{self.height} dx:{self.dx} dy:{self.dy} x:{self.x} y:{self.y} end:{self.x + self.width}"
        if txt:
            return data
        debug(
            data
        )

    def set(self, x, y):
        self.x += x
        self.y += y

        if not DEBUG:
            return

        if self.layout != FLOAT:
            for col in range(self.x, self.x + self.width):
                col += 1
                for row in range(self.y, self.y + self.height):
                    if grid[row][col] != ".":
                        #1/0
                        let = "?"

                    elif self.layout == EMB:
                        let = "E"
                    else:
                        let = "S"
                    grid[row][col] = let



def make_image(arr):
    data = "".join(arr).split()
    if data[0] != "image":
        1/0
    args = {}
    for line in data[1:]:
        param, val = line.split("=")
        args[param] = val

    return Image(**args)



class Config:
    def __init__(self):
        self.page_width, self.line_height, self.char_width = map(int, input().split())

        if DEBUG:

            for _ in range(200):
                grid.append(["."] * (self.page_width + 1))

            debug("CFG", self.page_width, self.line_height, self.char_width)


class Processor:
    def __init__(self):
        self.cfg = Config()

        paragraphs = []
        curr = []
        for line in stdin:
            line = line.strip()
            if line:
                curr.append(line)
            else:
                paragraphs.append(curr[:])
                curr.clear()

        if curr:
            paragraphs.append(curr[:])

        self.parags = paragraphs

    def parag2objects(self, parag):
        parag = " ".join(parag).replace("/n", " ").replace("  ", " ") + " "
        objects = []
        pos = 0
        word = []
        image = []
        need_image = False
        valid = set(".,:;!?-'")
        for letter in parag:
            if need_image and letter != ")":
                image.append(letter)
            elif letter == ")":
                if not need_image:
                    1/0
                objects.append(make_image(image))
                need_image = False
                image.clear()
            elif letter in valid or letter.isalnum():
                word.append(letter)
            elif letter == "(":
                need_image = True
                if word:
                    objects.append(make_word(word, self.cfg.char_width))
                    word.clear()
            elif letter.isspace():
                if word:
                    objects.append(make_word(word, self.cfg.char_width))
                    word.clear()
            else:
                1/0

        debug("...")
        return objects

    def objects2lines(self, objects, num, offset):
        lines = []
        blocks = []
        new_blocks = []
        line = Line(self.cfg, num, offset, blocks)
        debug("...placing", objects)

        def new_line():
            nonlocal num, offset, blocks, new_blocks
            if DEBUG:
                grid[line.offset][0] = "*"
            lines.append(line)
            line.display()
            offset += line.height
            blocks = [
                [x, width, height - line.height]
                for x, width, height in blocks + new_blocks
                if height - line.height > 0]
            blocks.sort()
            new_blocks.clear()
            num += 1
            return Line(self.cfg, num, offset, blocks)


        for obj in objects:
            if isinstance(obj, Word):
                while not line.add_word(obj):
                    line = new_line()
            else:  # image
                while not line.add_image(obj):
                    line = new_line()

                if obj.layout == SURR:
                    block = [obj.x, obj.x + obj.width - 1, obj.height]
                    new_blocks.append(block)


        new_line()
        debug("...lines end")
        max_block = 0
        for _, _, it in blocks:
            max_block = max(max_block, it)
        if max_block:
            debug("hanging", max_block, blocks)

        return lines, offset + max_block

    def parse(self):
        offset = linenum = 0
        images = []
        for parag in self.parags:
            objects = self.parag2objects(parag)
            for obj in objects:
                if isinstance(obj, Image):
                    images.append(obj)
            lines, offset = self.objects2lines(objects, linenum, offset)
            linenum += len(lines)

        debug("...done")
        if DEBUG:
            digit = ["."] * (len(grid[0] ) + 3)
            sub = ["."]
            for num in range(len(grid[0])):

                if num % 10 == 0:
                    digit[len(sub):len(sub) + len(str(num))] = str(num)
                sub.append(str(num % 10))



            debug("".join(digit))
            debug("".join(sub))

            for row, line in enumerate(grid):
                line.append(str(row % 10))
                if row % 10 == 0:
                    line.append(".")
                    line.append(str(row))
                debug("".join(line))

        for img in images:
            #print(*[img.layout, img.x, img.y])
            print(*[img.x, img.y])


def solve():
    it = Processor()
    it.parse()


solve()
