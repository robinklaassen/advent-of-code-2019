from day10.asteroid import Asteroid
from day10.parser import parse_input


def main():
    asteroids = parse_input('puzzle_input.txt')
    print(f"Total number of asteroids: {len(asteroids)}")

    # Results from part 1
    laser_x = 20
    laser_y = 18

    # Shift so that laser it at center
    for asteroid in asteroids:
        asteroid.x -= laser_x
        asteroid.y -= laser_y

    # Remove laser asteroid (now in center) from list
    asteroids.remove(Asteroid(0, 0))

    # Make a sorted list of all unique angles
    angles = [a.relative_angle_in_radians for a in asteroids]
    unique_angles = list(set(angles))
    unique_angles.sort()
    print(f"Total number of unique angles: {len(unique_angles)}")

    # Make a dictionary using these angles as keys and the asteroids as value
    angle_counts = {}
    for angle in unique_angles:
        angle_counts[angle] = [a for a in asteroids if a.relative_angle_in_radians == angle]

    # Now lets shoot some of these mofo's
    asteroid_shooting_order = []
    while len(asteroid_shooting_order) < len(asteroids):
        for angle, target_asteroids in angle_counts.items():
            # Skip if there are no targets
            if len(target_asteroids) == 0:
                continue

            # Shoot closest one
            target_asteroid = min(target_asteroids, key=lambda a: a.distance)
            asteroid_shooting_order.append(target_asteroid)
            target_asteroids.remove(target_asteroid)
            angle_counts[angle] = target_asteroids

    assert len(asteroid_shooting_order) == len(asteroids)

    # Get the info of the 200th asteroid
    output_asteroid = asteroid_shooting_order[199]
    print(output_asteroid)

    # Transform back to original coordinates
    output_asteroid.x += laser_x
    output_asteroid.y += laser_y

    print(f"Submit value: {output_asteroid.x * 100 + output_asteroid.y}")


if __name__ == "__main__":
    main()
