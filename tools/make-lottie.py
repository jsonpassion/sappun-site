#!/usr/bin/env python3
"""사뿐 사이트 Lottie 생성기 — assets/lottie/*.json 재생성.
실행: 리포 루트에서 `python3 tools/make-lottie.py`
팔레트는 앱/아이콘과 동일: 앰버 · 웜그레이 · 크림 · 청회색."""
import json
import os

W = H = 300
FR = 30
OP = 90

AMBER = [0.937, 0.643, 0.243, 1]
DEEP = [0.855, 0.537, 0.153, 1]
CREAM = [0.96, 0.93, 0.84, 1]
GRAY = [0.55, 0.57, 0.63, 1]
BLUE = [0.42, 0.49, 0.62, 1]


def static(v):
    return {"a": 0, "k": v}


def kfs(frames):
    """frames: (t, value) 또는 (t, value, 'h'). value는 스칼라 또는 리스트."""
    keys = []
    for i, f in enumerate(frames):
        t, v = f[0], f[1]
        hold = len(f) > 2
        s = v if isinstance(v, list) else [v]
        k = {"t": t, "s": s}
        if hold:
            k["h"] = 1
        elif i < len(frames) - 1:
            dim = len(s)
            k["i"] = {"x": [0.42] * dim, "y": [1] * dim}
            k["o"] = {"x": [0.58] * dim, "y": [0] * dim}
        keys.append(k)
    return {"a": 1, "k": keys}


def transform():
    return {"ty": "tr", "p": static([0, 0]), "a": static([0, 0]),
            "s": static([100, 100]), "r": static(0), "o": static(100)}


def fill_group(shape, color):
    return {"ty": "gr", "it": [shape, {"ty": "fl", "c": static(color), "o": static(100)}, transform()]}


def stroke_group(shape, color, width):
    return {"ty": "gr", "it": [shape, {"ty": "st", "c": static(color), "o": static(100),
                                        "w": static(width), "lc": 2, "lj": 2}, transform()]}


def ellipse(w, h, p=(0, 0)):
    return {"ty": "el", "d": 1, "s": static([w, h]), "p": static(list(p))}


def rect(w, h, r=0, p=(0, 0)):
    return {"ty": "rc", "d": 1, "s": static([w, h]), "p": static(list(p)), "r": static(r)}


def path(points, closed=False):
    n = len(points)
    return {"ty": "sh", "d": 1, "ks": static({"i": [[0, 0]] * n, "o": [[0, 0]] * n,
                                              "v": points, "c": closed})}


def layer(name, shapes, ind, pos=None, o=None, s=None, a=None):
    return {
        "ddd": 0, "ind": ind, "ty": 4, "nm": name, "sr": 1,
        "ks": {
            "o": o if isinstance(o, dict) else static(100 if o is None else o),
            "r": static(0),
            "p": pos if isinstance(pos, dict) else static((pos or [150, 150]) + [0]),
            "a": static((a or [0, 0]) + [0]),
            "s": s if isinstance(s, dict) else static((s or [100, 100]) + [100]),
        },
        "ao": 0, "shapes": shapes, "ip": 0, "op": OP, "st": 0,
    }


def write(name, layers):
    doc = {"v": "5.7.4", "fr": FR, "ip": 0, "op": OP, "w": W, "h": H,
           "nm": name, "ddd": 0, "assets": [], "layers": layers}
    out = os.path.join("assets", "lottie", f"{name}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
    print("written:", out)


def footprint_shapes(color):
    """간략화한 사뿐 발자국: 발바닥 캡슐 + 엄지 + 발가락 둘"""
    return [
        fill_group(rect(46, 76, 23, (0, 0)), color),
        fill_group(ellipse(17, 20, (15, -52)), color),
        fill_group(ellipse(11, 12, (-2, -58)), color),
        fill_group(ellipse(8, 9, (-16, -50)), color),
    ]


# 1. hero-footprints — 사뿐사뿐 걷는 두 발자국
write("hero-footprints", [
    layer("step-left", footprint_shapes(DEEP), 1, pos=[112, 196],
          o=kfs([(0, 0), (12, 90), (55, 90, "h"), (58, 90), (80, 0), (90, 0, "h")]),
          s=kfs([(0, [92, 92, 100]), (12, [100, 100, 100])])),
    layer("step-right", footprint_shapes(AMBER), 2, pos=[192, 118],
          o=kfs([(0, 0, "h"), (28, 0), (40, 100), (68, 100, "h"), (71, 100), (88, 0)]),
          s=kfs([(0, [92, 92, 100], "h"), (28, [92, 92, 100]), (40, [100, 100, 100])])),
])

# 2. flow-night — 자기 전에 켜두면, 잠든 사이에도 측정
write("flow-night", [
    layer("moon", [fill_group(ellipse(26, 26), CREAM)], 1, pos=[226, 62], o=70),
    layer("phone", [stroke_group(rect(92, 158, 20), GRAY, 6)], 2, pos=[150, 170]),
    layer("dot", [fill_group(ellipse(16, 16), AMBER)], 3, pos=[150, 170],
          o=kfs([(0, 35), (45, 100), (90, 35)])),
    layer("ripple", [stroke_group(ellipse(150, 150), AMBER, 6)], 4, pos=[150, 170],
          o=kfs([(0, 60), (60, 0), (90, 0, "h")]),
          s=kfs([(0, [30, 30, 100]), (60, [100, 100, 100]), (90, [100, 100, 100], "h")])),
])

# 3. flow-morning — 아침에 확인하는 발생 패턴 (히트맵)
_cells = []
for row, y in enumerate([104, 140, 176]):
    for col, x in enumerate([96, 132, 168, 204]):
        _cells.append(fill_group(rect(28, 28, 7, (x - 150, y - 150)), GRAY))
_hot = [(168, 104), (204, 140), (168, 140), (132, 176)]
_hot_layers = [
    layer(f"hot{i}", [fill_group(rect(28, 28, 7), AMBER)], i + 2,
          pos=[x, y],
          o=kfs([(0, 0, "h"), (10 + i * 14, 0), (20 + i * 14, 100), (80, 100), (90, 0)]))
    for i, (x, y) in enumerate(_hot)
]
write("flow-morning", [layer("grid", _cells, 1, o=28)] + _hot_layers)

# 4. flow-note — 정중한 쪽지 한 장
write("flow-note", [
    layer("dot", [fill_group(ellipse(18, 18), AMBER)], 1,
          pos=kfs([(0, [150, 106, 0], "h"), (20, [150, 106, 0]), (58, [150, 62, 0]), (90, [150, 62, 0], "h")]),
          o=kfs([(0, 0, "h"), (20, 0), (32, 90), (58, 0), (90, 0, "h")])),
    layer("envelope", [
        stroke_group(rect(148, 98, 12), AMBER, 6),
        stroke_group(path([[-74, -49], [0, 8], [74, -49]]), AMBER, 6),
    ], 2, pos=kfs([(0, [150, 174, 0]), (45, [150, 163, 0]), (90, [150, 174, 0])])),
])

# 5. flow-report — 필요할 때 꺼내는 제출용 자료
_lines = [
    layer(f"line{i}", [fill_group(rect(76 - i * 10, 9, 4), GRAY)], i + 2,
          pos=[141 - i * 5, 128 + i * 26],
          o=kfs([(0, 0, "h"), (8 + i * 12, 0), (18 + i * 12, 85)]))
    for i in range(3)
]
write("flow-report", [
    layer("doc", [stroke_group(rect(128, 160, 14), GRAY, 6)], 1, pos=[145, 155]),
    *_lines,
    layer("badge", [fill_group(ellipse(52, 52), AMBER)], 5, pos=[204, 216],
          o=kfs([(0, 0, "h"), (52, 0), (60, 100)]),
          s=kfs([(0, [40, 40, 100], "h"), (52, [40, 40, 100]), (62, [112, 112, 100]), (70, [100, 100, 100])])),
    layer("check", [stroke_group(path([[-10, 1], [-3, 9], [12, -8]]), CREAM, 6)], 6, pos=[204, 216],
          o=kfs([(0, 0, "h"), (58, 0), (66, 100)])),
])

# 6. feature-judge — 기준선을 넘는 순간을 판정
write("feature-judge", [
    layer("limit", [fill_group(rect(150, 5, 2), GRAY)], 1, pos=[150, 118]),
    layer("bar", [fill_group(rect(40, 130, 10, (0, -65)), AMBER)], 2, pos=[150, 218],
          s=kfs([(0, [100, 24, 100]), (38, [100, 100, 100]), (60, [100, 100, 100], "h"),
                 (62, [100, 100, 100]), (90, [100, 24, 100])])),
    layer("pulse", [stroke_group(ellipse(60, 60), AMBER, 5)], 3, pos=[150, 118],
          o=kfs([(0, 0, "h"), (34, 0), (40, 80), (64, 0), (90, 0, "h")]),
          s=kfs([(0, [40, 40, 100], "h"), (34, [40, 40, 100]), (64, [110, 110, 100]), (90, [110, 110, 100], "h")])),
])

# 7. feature-quiet — 잦아드는 파동 (다시 조용해지는 것)
_waves = [
    layer(f"wave{i}", [stroke_group(ellipse(200, 200), AMBER, 8)], i + 2,
          pos=[150, 150],
          o=kfs([(0, 0, "h"), (i * 22, 0 if i else 70), (i * 22 + 1, 70), (i * 22 + 45, 0)] if i else [(0, 70), (45, 0), (90, 0, "h")]),
          s=kfs([(0, [10, 10, 100], "h"), (i * 22, [10, 10, 100]), (i * 22 + 45, [110, 110, 100])] if i else [(0, [10, 10, 100]), (45, [110, 110, 100]), (90, [110, 110, 100], "h")]))
    for i in range(3)
]
write("feature-quiet", [layer("dot", [fill_group(ellipse(18, 18), GRAY)], 1, pos=[150, 150])] + _waves)

# 8. feature-private — 소리는 수치만 남고 사라진다
write("feature-private", [
    layer("bar-a", [fill_group(rect(12, 64, 6), AMBER)], 1, pos=[118, 150],
          s=kfs([(0, [100, 55, 100]), (12, [100, 100, 100]), (24, [100, 45, 100]), (36, [100, 80, 100]),
                 (48, [100, 55, 100]), (62, [100, 8, 100], "h"), (90, [100, 8, 100])])),
    layer("bar-b", [fill_group(rect(12, 96, 6), AMBER)], 2, pos=[150, 150],
          s=kfs([(0, [100, 80, 100]), (12, [100, 50, 100]), (24, [100, 100, 100]), (36, [100, 60, 100]),
                 (48, [100, 80, 100]), (62, [100, 6, 100], "h"), (90, [100, 6, 100])])),
    layer("bar-c", [fill_group(rect(12, 64, 6), AMBER)], 3, pos=[182, 150],
          s=kfs([(0, [100, 70, 100]), (12, [100, 40, 100]), (24, [100, 90, 100]), (36, [100, 100, 100]),
                 (48, [100, 70, 100]), (62, [100, 8, 100], "h"), (90, [100, 8, 100])])),
    layer("digit", [fill_group(rect(18, 18, 5), CREAM)], 4, pos=[150, 150],
          o=kfs([(0, 0, "h"), (60, 0), (72, 100), (84, 100), (90, 0)])),
])

print("done — 8 animations")
