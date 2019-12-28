from typing import List

from day11.part1 import paint, Panel


def get_panel_color_by_position(robot_path: List[Panel], x: int, y: int) -> bool:
    color = False
    for p in robot_path:
        if p == Panel(x, y):
            color = p.color
            break
    return color


def main():
    robot_path = paint(starting_color=True)
    print(f"Robot path length: {len(robot_path)}")

    # Determine grid size to print
    x_list = [p.x for p in robot_path]
    y_list = [p.y for p in robot_path]

    x_size = max(x_list) - min(x_list) + 1
    y_size = max(y_list) - min(y_list) + 1

    print("Identifier:")
    for y in range(max(y_list), max(y_list) - y_size, -1):
        line = ""
        for x in range(min(x_list), min(x_list) + x_size):
            line += "X" if get_panel_color_by_position(robot_path, x, y) else " "
        print(line)


if __name__ == "__main__":
    main()
