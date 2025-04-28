import os
import math
from itertools import combinations

# Define a class to represent a circle
class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

# Function to read points from a file and store them in an array
def read_file_and_store_points(file_path):
    points = []
    with open(file_path, 'r') as file:
        n = int(file.readline())  # Read the number of points
        for _ in range(n):
            x, y = map(float, file.readline().split())

            points.append((x, y))
    return points

# Function to calculate the circle defined by two points (diameter endpoints)
def circle_from_two_points(p1, p2):
    # Compute the center
    cx = (p1[0] + p2[0]) / 2
    cy = (p1[1] + p2[1]) / 2

    # Compute the radius
    radius = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) / 2

    return Circle((cx, cy), radius)

# Function to calculate the circle defined by three points (on the circumference)
def circle_from_three_points(p1, p2, p3):
    A = p1[0] * (p2[1] - p3[1]) - p1[1] * (p2[0] - p3[0]) + p2[0] * p3[1] - p3[0] * p2[1]
    B = (p1[0]**2 + p1[1]**2) * (p3[1] - p2[1]) + (p2[0]**2 + p2[1]**2) * (p1[1] - p3[1]) + (p3[0]**2 + p3[1]**2) * (p2[1] - p1[1])
    C = (p1[0]**2 + p1[1]**2) * (p2[0] - p3[0]) + (p2[0]**2 + p2[1]**2) * (p3[0] - p1[0]) + (p3[0]**2 + p3[1]**2) * (p1[0] - p2[0])
    D = (p1[0]**2 + p1[1]**2) * (p3[0] * p2[1] - p2[0] * p3[1]) + (p2[0]**2 + p2[1]**2) * (p1[0] * p3[1] - p3[0] * p1[1]) + (p3[0]**2 + p3[1]**2) * (p2[0] * p1[1] - p1[0] * p2[1])

    if A == 0:
        return None  # Points are collinear, no circle can be formed

    center_x = B / (2 * A)
    center_y = -C / (2 * A)
    radius = math.sqrt((B**2 + C**2 - 4 * A * D) / (4 * A**2))
    return Circle((center_x, center_y), radius)

# Function to check if all points are inside or on the circle
def all_points_in_circle(circle, points):
    for point in points:
        distance_squared = (point[0] - circle.center[0])**2 + (point[1] - circle.center[1])**2
        if distance_squared > circle.radius**2 + 1e-6:  # Small tolerance for floating-point inaccuracies
            return False
    return True

# Two-Point Approach
def two_point_approach(points):
    smallest_circle = Circle((0, 0), float('inf'))

    for p1, p2 in combinations(points, 2):
        circle = circle_from_two_points(p1, p2)
        if all_points_in_circle(circle, points):
            if circle.radius < smallest_circle.radius:
                smallest_circle = circle

    return smallest_circle

# Three-Point Approach
def three_point_approach(points):
    smallest_circle = Circle((0, 0), float('inf'))

    for p1, p2, p3 in combinations(points, 3):
        circle = circle_from_three_points(p1, p2, p3)
        if circle and all_points_in_circle(circle, points):
            if circle.radius < smallest_circle.radius:
                smallest_circle = circle

    return smallest_circle

# Main function to process datasets
def main():
    dataset_folder = os.path.join(os.path.dirname(__file__), "..", "Datasets")
    dataset_files = [
        "circle_10.txt", "circle_20.txt","circle_40.txt" , "circle_100.txt", "circle_400.txt",
        "circle_800.txt", "circle_1000.txt", "circle_2000.txt", "circle_4000.txt",
        "circle_20000.txt", "circle_40000.txt", "circle_100000.txt", "circle_400000.txt",
        "circle_800000.txt"
    ]

    for file in dataset_files:
        file_path = os.path.join(dataset_folder, file)
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found!")
            continue

        points = read_file_and_store_points(file_path)
        print(f"Processing {file} with {len(points)} points...")

        # Two-Point Approach
        smallest_circle_two_point = two_point_approach(points)
        print(f"Two-Point Approach - Center: {smallest_circle_two_point.center}, Radius: {smallest_circle_two_point.radius}")

        # Three-Point Approach
        smallest_circle_three_point = three_point_approach(points)
        print(f"Three-Point Approach - Center: {smallest_circle_three_point.center}, Radius: {smallest_circle_three_point.radius}")
        print()

# Run the program
if __name__ == "__main__":
    main()