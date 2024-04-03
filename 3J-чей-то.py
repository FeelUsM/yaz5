from collections import defaultdict
from sys import stdin
input = stdin.readline


def debug(*args):
    if False:
        print(*args)


def solve():
    device_cnt, part_cnt = map(int, input().split())
    devices = [set() for _ in range(device_cnt)]
    devices[0] = set(range(part_cnt))
    seen_parts = [1] * part_cnt
    result = [0] * (device_cnt - 1)
    likes = [defaultdict(int) for _ in range(device_cnt)]
    done = 1
    step = 0
    while done != device_cnt:
        debug("step", step, done)
        queries = defaultdict(list)
        # prepare queries
        for device_id in range(1, device_cnt):
            device_parts = devices[device_id]
            debug("Q", device_id, device_parts, len(device_parts) ,  part_cnt)

            if len(device_parts) != part_cnt:
                # what part we ask
                # Перед каждым таймслотом для каждой части обновления определяется, на
                # скольких устройствах сети скачана эта часть. Каждое устройство выбирает
                # отсутствующую на нем часть обновления, которая встречается в сети реже
                # всего. Если таких частей несколько, то выбирается отсутствующая на
                # устройстве часть обновления с наименьшим номером.
                min_part_cnt = float('inf')
                min_part = -1
                for part_id, seen_part_cnt in enumerate(seen_parts):
                    if part_id not in device_parts and seen_part_cnt < min_part_cnt:
                        min_part_cnt = seen_part_cnt
                        min_part = part_id

                # whom we ask for part
                # После этого устройство делает запрос выбранной части обновления у
                # одного из устройств, на котором такая часть обновления уже скачана.
                # Если таких устройств несколько — выбирается устройство, на котором
                # скачано наименьшее количество частей обновления. Если и таких устройств
                # оказалось несколько — выбирается устройство с минимальным номером.
                min_ask_cnt = float('inf')
                min_ask_device_id = -1
                for ask_device_id, ask_device_parts in enumerate(devices):
                    if min_part in ask_device_parts and len(ask_device_parts) < min_ask_cnt:
                        min_ask_cnt = len(ask_device_parts)
                        min_ask_device_id = ask_device_id

                queries[min_ask_device_id].append((min_part, device_id))
        debug("queries", dict(queries))

        # process queries
        # Устройство A удовлетворяет тот запрос, который поступил от наиболее ценного для A устройства.
        # Ценность устройства B для устройства A определяется как количество частей обновления,
        # ранее полученных устройством A от устройства B.
        # Если на устройство A пришло несколько запросов от одинаково ценных устройств,
        # то удовлетворяется запрос того устройства, на котором меньше всего скачанных частей
        # обновления. Если и таких запросов несколько, то среди них выбирается устройство с наименьшим номером.
        gives = []
        for device, asks in queries.items():
            min_likes = (float('inf'), float('inf'))
            give_to = None
            for ask_part, asker_device_id in asks:
                like = (-likes[device][asker_device_id], len(devices[asker_device_id]))
                if like < min_likes:
                    min_likes = like
                    give_to = device, ask_part, asker_device_id

            debug("giving", give_to, asks)
            gives.append(give_to)

        for device_from, part, device_to in gives:
            likes[device_to][device_from] += 1
            seen_parts[part] += 1
            devices[device_to].add(part)
            if len(devices[device_to]) == part_cnt:
                result[device_to - 1] = step + 1
                done += 1

        step += 1

    return result


print(*solve())
