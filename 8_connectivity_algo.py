
import cv2
import copy
import numpy as np
import matplotlib.pyplot as plt
# image = [
#     [0, 1, 1, 0, 0, 0, 0],
#     [1, 0, 0, 1, 1, 1, 1],
#     [1, 0, 1, 1, 1, 0, 1],
#     [1, 0, 0, 0, 1, 1, 1],
#     [1, 1, 0, 1, 0, 0, 0],
#     [0, 0, 1, 1, 0, 0, 0]
# ]
image = cv2.imread("./images/image 5.png", 0)
rows, cols = image.shape
# rows = 6
# cols = 7

new_image = np.zeros(image.shape)
dir = 7
left_most_value = [0, 0]
next_point = [0, 0]
boundary_points = []


def find_left_most():
    for col in range(cols+1):
        for row in range(col+1):
            if image[row][col-row] == 255:
                left_most_value = [row, col - row]
                boundary_points.append(left_most_value)
                return left_most_value


left_most_value = find_left_most()

while(True):
    row_left_most = left_most_value[0]
    column_left_most = left_most_value[1]
    # even
    if dir % 2 == 0:
        dir = (dir + 7) % 8
    # odd
    else:
        dir = (dir + 6) % 8

    while(True):
        if dir == 0:
            # go right
            next_point[0] = row_left_most
            next_point[1] = column_left_most + 1

            if next_point[1] > cols - 1:
                dir = (dir + 1) % 8
            elif(image[next_point[0]][next_point[1]]) == 255:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 8

        elif dir == 1:

            next_point[0] = row_left_most - 1
            next_point[1] = column_left_most + 1

            if (next_point[1] > cols - 1) or (next_point[0] < 0):
                dir = (dir + 1) % 8
            elif(image[next_point[0]][next_point[1]]) == 255:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 8

        elif dir == 2:
            # go up
            next_point[0] = row_left_most - 1
            next_point[1] = column_left_most

            if next_point[0] < 0:
                dir = (dir + 1) % 8
            elif(image[next_point[0]][next_point[1]]) == 255:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 8

        elif dir == 3:
            next_point[0] = row_left_most - 1
            next_point[1] = column_left_most - 1

            if (next_point[0] < 0) or (next_point[1] < 0):
                dir = (dir + 1) % 8
            elif(image[next_point[0]][next_point[1]]) == 255:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 8

        elif dir == 4:
            # go left
            next_point[0] = row_left_most
            next_point[1] = column_left_most - 1

            if next_point[1] < 0:
                dir = (dir + 1) % 8

            elif(image[next_point[0]][next_point[1]]) == 255:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)

                break
            else:
                dir = (dir + 1) % 8

        elif dir == 5:
            next_point[0] = row_left_most + 1
            next_point[1] = column_left_most - 1

            if (next_point[0] > rows - 1) or (next_point[1] < 0):
                dir = (dir + 1) % 8

            elif(image[next_point[0]][next_point[1]]) == 255:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)

                break
            else:
                dir = (dir + 1) % 8

        elif dir == 6:
            # go down

            next_point[0] = row_left_most + 1
            next_point[1] = column_left_most

            if next_point[0] > rows - 1:
                dir = (dir + 1) % 8
            elif(image[next_point[0]][next_point[1]]) == 255:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 8

        elif dir == 7:
            next_point[0] = row_left_most + 1
            next_point[1] = column_left_most + 1

            if (next_point[0] > rows - 1) or (next_point[1] > cols - 1):
                dir = (dir + 1) % 8
            elif(image[next_point[0]][next_point[1]]) == 255:
                left_most_value = copy.deepcopy(next_point)
                boundary_points.append(left_most_value)
                break
            else:
                dir = (dir + 1) % 8

    if len(boundary_points) >= 4:
        if boundary_points[-1] == boundary_points[1]:
            if boundary_points[-2] == boundary_points[0]:
                break


for boundary in boundary_points:
    new_image[boundary[0]][boundary[1]] = 255

# print(boundary_points)
plt.imshow(new_image, cmap="gray")
plt.show()
