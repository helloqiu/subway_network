from generate_relative_position import relative_position
import svgwrite


def draw_map():
    pos = relative_position()
    dwg = svgwrite.Drawing('../picture/地铁位置图.svg', profile='tiny')
    for i in pos:
        dwg.add(svgwrite.shapes.Circle(
            center=(i['latitude'], i['longitude']),
            fill='#8fddff',
            r=5
        ))
    dwg.save()


if __name__ == '__main__':
    draw_map()
