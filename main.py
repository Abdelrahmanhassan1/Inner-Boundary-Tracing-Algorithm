from math import sin, cos, radians, sqrt, pow
import numpy as np
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import cv2
import copy
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from sympy import EX
from maingui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.browse_button.clicked.connect(self.browse)
        self.ui.apply_button.clicked.connect(
            self.check_algorithm_selected)

        # variables
        self.original_image_figure = Figure()
        self.original_canvas_figure = FigureCanvas(self.original_image_figure)
        self.ui.verticalLayout.addWidget(self.original_canvas_figure)

        self.final_image_figure = Figure()
        self.final_canvas_figure = FigureCanvas(self.final_image_figure)
        self.ui.verticalLayout_2.addWidget(self.final_canvas_figure)

        self.left_most_value = [0, 0]
        self.next_point = [0, 0]
        self.boundary_points = []

    def browse(self):
        try:
            imported_image = QFileDialog.getOpenFileName(
                filter="image (*.png *.jbg *.jbeg)")[0]
            self.image = cv2.imread(imported_image, 0)
            self.rows, self.cols = self.image.shape
            self.new_image = np.zeros(self.image.shape)
            self.show_original_image()
        except Exception as e:
            print(e)

    def apply_algorithm_4_connectivity(self):
        try:
            self.boundary_points = []
            self.find_left_most()
            self.dir = 3
            while(True):
                row_left_most = self.left_most_value[0]
                column_left_most = self.left_most_value[1]
                self.dir = (self.dir + 3) % 4
                while(True):
                    if self.dir == 0:

                        self.next_point[0] = row_left_most
                        self.next_point[1] = column_left_most + 1

                        if self.next_point[1] > self.cols - 1:
                            self.dir = (self.dir + 1) % 4
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 4

                    elif self.dir == 1:
                        # go up
                        self.next_point[0] = row_left_most - 1
                        self.next_point[1] = column_left_most

                        if self.next_point[0] < 0:
                            self.dir = (self.dir + 1) % 4
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 4

                    elif self.dir == 2:
                        # go left
                        self.next_point[0] = row_left_most
                        self.next_point[1] = column_left_most - 1

                        if self.next_point[1] < 0:
                            self.dir = (self.dir + 1) % 4

                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)

                            break
                        else:
                            self.dir = (self.dir + 1) % 4

                    elif self.dir == 3:
                        # go down

                        self.next_point[0] = row_left_most + 1
                        self.next_point[1] = column_left_most

                        if self.next_point[0] > self.rows - 1:
                            self.dir = (self.dir + 1) % 4
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 4

                if len(self.boundary_points) >= 4:
                    if self.boundary_points[-1] == self.boundary_points[1]:
                        if self.boundary_points[-2] == self.boundary_points[0]:
                            break
            for boundary in self.boundary_points:
                self.new_image[boundary[0]][boundary[1]] = 255
            self.show_final_image()
        except Exception as e:
            print(e)

    def apply_algorithm_8_connectivity(self):
        try:

            self.boundary_points = []
            self.find_left_most()
            self.dir = 7

            while(True):
                row_left_most = self.left_most_value[0]
                column_left_most = self.left_most_value[1]
                # even
                if self.dir % 2 == 0:
                    self.dir = (self.dir + 7) % 8
                # odd
                else:
                    self.dir = (self.dir + 6) % 8

                while(True):

                    if self.dir == 0:
                        # go right
                        self.next_point[0] = row_left_most
                        self.next_point[1] = column_left_most + 1

                        if self.next_point[1] > self.cols - 1:
                            self.dir = (self.dir + 1) % 8
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 8

                    elif self.dir == 1:

                        self.next_point[0] = row_left_most - 1
                        self.next_point[1] = column_left_most + 1

                        if (self.next_point[1] > self.cols - 1) or (self.next_point[0] < 0):
                            self.dir = (self.dir + 1) % 8
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 8

                    elif self.dir == 2:
                        # go up
                        self.next_point[0] = row_left_most - 1
                        self.next_point[1] = column_left_most

                        if self.next_point[0] < 0:
                            self.dir = (self.dir + 1) % 8
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 8

                    elif self.dir == 3:
                        self.next_point[0] = row_left_most - 1
                        self.next_point[1] = column_left_most - 1

                        if (self.next_point[0] < 0) or (self.next_point[1] < 0):
                            self.dir = (self.dir + 1) % 8
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 8

                    elif self.dir == 4:
                        # go left
                        self.next_point[0] = row_left_most
                        self.next_point[1] = column_left_most - 1

                        if self.next_point[1] < 0:
                            self.dir = (self.dir + 1) % 8

                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)

                            break
                        else:
                            self.dir = (self.dir + 1) % 8

                    elif self.dir == 5:
                        self.next_point[0] = row_left_most + 1
                        self.next_point[1] = column_left_most - 1

                        if (self.next_point[0] > self.rows - 1) or (self.next_point[1] < 0):
                            self.dir = (self.dir + 1) % 8

                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)

                            break
                        else:
                            self.dir = (self.dir + 1) % 8

                    elif self.dir == 6:
                        # go down

                        self.next_point[0] = row_left_most + 1
                        self.next_point[1] = column_left_most

                        if self.next_point[0] > self.rows - 1:
                            self.dir = (self.dir + 1) % 8
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 8

                    elif self.dir == 7:
                        self.next_point[0] = row_left_most + 1
                        self.next_point[1] = column_left_most + 1

                        if (self.next_point[0] > self.rows - 1) or (self.next_point[1] > self.cols - 1):
                            self.dir = (self.dir + 1) % 8
                        elif(self.image[self.next_point[0]][self.next_point[1]]) == 255:
                            self.left_most_value = copy.deepcopy(
                                self.next_point)
                            self.boundary_points.append(self.left_most_value)
                            break
                        else:
                            self.dir = (self.dir + 1) % 8

                if len(self.boundary_points) >= 4:
                    if self.boundary_points[-1] == self.boundary_points[1]:
                        if self.boundary_points[-2] == self.boundary_points[0]:
                            break

            for boundary in self.boundary_points:
                self.new_image[boundary[0]][boundary[1]] = 255
            self.show_final_image()

        except Exception as e:
            print(e)

    def check_algorithm_selected(self):
        algo_index = self.ui.comboBox.currentIndex()
        if algo_index == 0:
            self.apply_algorithm_4_connectivity()
        elif algo_index == 1:
            self.apply_algorithm_8_connectivity()

    def find_left_most(self):
        for col in range(self.cols+1):
            for row in range(col+1):
                if self.image[row][col-row] == 255:
                    self.left_most_value = [row, col - row]
                    self.boundary_points.append(self.left_most_value)
                    return self.left_most_value

    def show_original_image(self):
        self.original_image_figure.clear()
        figure_axes = self.original_image_figure.gca()
        figure_axes.imshow(self.image, cmap='gray')
        figure_axes.set_xticks([])
        figure_axes.set_yticks([])
        figure_axes.set_aspect('equal')
        figure_axes.set_frame_on(False)
        self.original_canvas_figure.draw()
        self.original_canvas_figure.flush_events()

    def show_final_image(self):
        self.final_image_figure.clear()
        figure_axes = self.final_image_figure.gca()
        figure_axes.imshow(self.new_image, cmap='gray')
        figure_axes.set_xticks([])
        figure_axes.set_yticks([])
        self.final_canvas_figure.draw()
        self.final_canvas_figure.flush_events()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
