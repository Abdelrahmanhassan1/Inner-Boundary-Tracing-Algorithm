import matplotlib.pyplot as plt
import numpy as np
import copy
import cv2
image = [
    [0, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 0],
    [1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0]
]


# image = cv2.imread("./image.png", 0)
# rows, cols = image.shape
rows, cols = 6, 7
# new_image = np.zeros(image.shape)
new_image = np.zeros((6, 7))
dir = 3
left_most_value = [0, 0]
next_point = [0, 0]
boundary_points = []


def find_left_most():
    for col in range(cols+1):
        for row in range(col+1):
            if image[row][col-row] == 1:
                left_most_value = [row, col - row]
                boundary_points.append(left_most_value)
                return left_most_value


left_most_value = find_left_most()

while(True):
    row_left_most = left_most_value[0]
    column_left_most = left_most_value[1]
    dir = (dir + 3) % 4

    while(True):
        if dir == 0:

            next_point[0] = row_left_most
            next_point[1] = column_left_most + 1

            if next_point[1] > cols - 1:
                dir = (dir + 1) % 4
            elif(image[next_point[0]][next_point[1]]) == 1:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 4

        elif dir == 1:
            # go up
            next_point[0] = row_left_most - 1
            next_point[1] = column_left_most

            if next_point[0] < 0:
                dir = (dir + 1) % 4
            elif(image[next_point[0]][next_point[1]]) == 1:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 4

        elif dir == 2:
            # go left
            next_point[0] = row_left_most
            next_point[1] = column_left_most - 1

            if next_point[1] < 0:
                dir = (dir + 1) % 4

            elif(image[next_point[0]][next_point[1]]) == 1:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)

                break
            else:
                dir = (dir + 1) % 4

        elif dir == 3:
            # go down

            next_point[0] = row_left_most + 1
            next_point[1] = column_left_most

            if next_point[0] > rows - 1:
                dir = (dir + 1) % 4
            elif(image[next_point[0]][next_point[1]]) == 1:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 4

    if len(boundary_points) >= 4:
        if boundary_points[-1] == boundary_points[1]:
            if boundary_points[-2] == boundary_points[0]:
                break


for boundary in boundary_points:
    new_image[boundary[0]][boundary[1]] = 1
    print(boundary)

plt.imshow(new_image, cmap="gray")
plt.show()
