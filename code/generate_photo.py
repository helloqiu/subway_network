from generate_relative_position import relative_position
import svgwrite


def draw_map():
    pos = relative_position()
    dwg = svgwrite.Drawing('../picture/地铁位置图.svg', profile='full', size=('4000', '4000'))
    for i in pos:
        dwg.add(svgwrite.shapes.Circle(
            center=(i['latitude'], i['longitude']),
            fill='#8fddff',
            r=5
        ))
        dwg.add(svgwrite.text.Text(
            text=i['name'],
            insert=(i['latitude'], i['longitude']),
            font_size="5",
            font_family="黑体",
            style="text-anchor: middle; dominant-baseline: central;"
        ))
    dwg.save()


if __name__ == '__main__':
    draw_map()
