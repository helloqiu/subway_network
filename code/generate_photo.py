from generate_relative_position import relative_position
import svgwrite
from graph import subway_graph, nodes_by_data
from datetime import datetime

pos = relative_position()


def draw_map():
    dwg = svgwrite.Drawing('../picture/地铁位置图.svg', profile='full', size=('2000', '3000'))
    for i in pos:
        dwg.add(svgwrite.shapes.Circle(
            center=(i['latitude'], i['longitude']),
            fill='#8fddff',
            r=8,
            fill_opacity="0.5"
        ))
        dwg.add(svgwrite.text.Text(
            text=i['name'],
            insert=(i['latitude'], i['longitude']),
            font_size="5",
            font_family="黑体",
            style="text-anchor: middle; dominant-baseline: central;"
        ))
    g = subway_graph()
    for e in g.edges.data():
        pos_a = get_location(e[0], pos)
        pos_b = get_location(e[1], pos)
        dwg.add(svgwrite.path.Path(
            stroke_width="1",
            stroke_opacity="0.5",
            stroke="#ffaa5c",
            d="M {},{} L {},{}".format(pos_a[0], pos_a[1], pos_b[0], pos_b[1])
        ))
        dwg.add(svgwrite.text.Text(
            text=e[2]['weight'],
            font_size="5",
            font_family="黑体",
            style="text-anchor: middle; dominant-baseline: central;",
            insert=((pos_a[0] + pos_b[0]) / 2, (pos_a[1] + pos_b[1]) / 2)
        ))
    dwg.save()


def get_location(name, p):
    for i in p:
        if i['name'] == name:
            return i['latitude'], i['longitude']


def draw(stations, name):
    pos = relative_position(stations)
    dwg = svgwrite.Drawing('../picture/{}.svg'.format(name), profile='full', size=('2000', '3000'))
    for i in pos:
        dwg.add(svgwrite.shapes.Circle(
            center=(i['latitude'], i['longitude']),
            fill='#8fddff',
            r=8,
            fill_opacity="0.5"
        ))
        dwg.add(svgwrite.text.Text(
            text=i['name'],
            insert=(i['latitude'], i['longitude']),
            font_size="5",
            font_family="黑体",
            style="text-anchor: middle; dominant-baseline: central;"
        ))
    g = subway_graph()
    for e in g.edges.data():
        if (e[0] not in stations) or (e[1] not in stations):
            continue
        pos_a = get_location(e[0], pos)
        pos_b = get_location(e[1], pos)
        dwg.add(svgwrite.path.Path(
            stroke_width="1",
            stroke_opacity="0.5",
            stroke="#ffaa5c",
            d="M {},{} L {},{}".format(pos_a[0], pos_a[1], pos_b[0], pos_b[1])
        ))
        dwg.add(svgwrite.text.Text(
            text=e[2]['weight'],
            font_size="5",
            font_family="黑体",
            style="text-anchor: middle; dominant-baseline: central;",
            insert=((pos_a[0] + pos_b[0]) / 2, (pos_a[1] + pos_b[1]) / 2)
        ))
    dwg.save()


def draw_map_by_date():
    data = nodes_by_data()
    temp = list()
    for key in data.keys():
        temp = temp + data[key]
        draw(temp, key.strftime("%Y-%m-%d"))


if __name__ == '__main__':
    draw_map_by_date()
