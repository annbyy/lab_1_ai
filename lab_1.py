import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QTextEdit, QInputDialog
from PyQt5.QtGui import QFont

class WorldCube:
    def __init__(self, world_length, world_width):
        self.world_length = world_length
        self.world_width = world_width
        self.matrix = [['0' for _ in range(world_width)] for _ in range(world_length)]
        self.log = []
        self.block_counter = 0

    def display_world(self):
        world_state = ""
        for row in self.matrix:
            world_state += ' '.join(row) + '\n'
        return world_state

    def place_block(self, row_index, column_index):
        if 0 <= row_index < self.world_length and 0 <= column_index < self.world_width:
            # если выбранный столбец уже заполнен, нужно найти следующий доступный столбец
            while self.matrix[0][column_index] != '0':
                column_index = (column_index + 1) % self.world_width

            for level in range(self.world_length - 1, -1, -1):
                if self.matrix[level][column_index] == '0':
                    self.block_counter += 1
                    block_name = f"{self.block_counter}"
                    self.matrix[level][column_index] = block_name
                    self.log.append(f"Placed {block_name} at ({level}, {column_index})")
                    return
        else:
            self.log.append(f"Invalid coordinates: ({row_index}, {column_index})")

    def move_block(self, block_name, dest_row, dest_column):
        if 0 <= dest_row < self.world_length and 0 <= dest_column < self.world_width:
            if self.matrix[dest_row][dest_column] == '0':
                for row_index in range(self.world_length):
                    for column_index in range(self.world_width):
                        if self.matrix[row_index][column_index] == block_name:
                            self.matrix[dest_row][dest_column] = block_name
                            self.matrix[row_index][column_index] = '0'
                            self.log.append(f"Moved {block_name} to ({dest_row}, {dest_column})")
                            self.save_logs("D:/Anna/utm/3 year/ai/lab_1/log.txt")
                            return True
                self.log.append(f"Block {block_name} not found.")
                return False
            else:
                self.log.append(f"Target position at ({dest_row}, {dest_column}) is occupied.")
                return False
        else:
            self.log.append(f"Invalid destination coordinates: ({dest_row}, {dest_column})")
            return False

    def grasp_block(self, block_name):
        for row_index in range(self.world_length):
            for column_index in range(self.world_width):
                if self.matrix[row_index][column_index] == block_name:
                    current_row, current_column = row_index, column_index
                    self.block_to_move = (current_row, current_column)
                    self.log.append(f"Grasped {block_name} from ({current_row}, {current_column})")
                    self.save_logs("D:/Anna/utm/3 year/ai/lab_1/log.txt")
                    return current_row, current_column
        self.log.append(f"Failed to grasp {block_name}")
        self.save_logs("D:/Anna/utm/3 year/ai/lab_1/log.txt")
        return None, None

    def put_on(self, block_name, dest_row, dest_column):
        current_row, current_column = self.grasp_block(block_name)
        if current_row is not None and current_column is not None:
            if self.move_block(block_name, dest_row, dest_column):
                self.matrix[current_row][current_column] = '0'
                self.log.append(f"Successfully put {block_name} on ({dest_row}, {dest_column})")
                self.save_logs("D:/Anna/utm/3 year/ai/lab_1/log.txt")
                return True
            else:
                self.log.append(f"Failed to put {block_name} on ({dest_row}, {dest_column})")
        return False

    def save_logs(self, file_path):
        with open(file_path, 'w') as f:
            for entry in self.log:
                f.write(entry + '\n')

class WorldCubeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.world = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('World Cube')

        self.setStyleSheet("background-color: #ffc0bc;")

        self.layout = QVBoxLayout()

        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Enter the length of the world")
        self.length_input.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.length_input)

        self.width_input = QLineEdit()
        self.width_input.setPlaceholderText("Enter the width of the world")
        self.width_input.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.width_input)

        self.blocks_input = QLineEdit()
        self.blocks_input.setPlaceholderText("How many blocks to place?")
        self.blocks_input.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.blocks_input)

        self.place_button = QPushButton('Place Blocks')
        self.place_button.clicked.connect(self.place_blocks)
        self.place_button.setStyleSheet("background-color: #e3a5b0;")
        self.place_button.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.place_button)

        self.move_button = QPushButton('Move Block')
        self.move_button.clicked.connect(self.move_block_ui)
        self.move_button.setStyleSheet("background-color: #e3a5b0;")
        self.move_button.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.move_button)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.log_display)

        self.setLayout(self.layout)
        self.setGeometry(100, 100, 600, 400)

    def place_blocks(self):
        length = int(self.length_input.text())
        width = int(self.width_input.text())
        n_blocks = int(self.blocks_input.text())

        if n_blocks > length * width:
            self.update_log("Warning: The number of blocks exceeds the size of the matrix.")
            return

        self.world = WorldCube(length, width)

        for i in range(n_blocks):
            row_index, ok1 = QInputDialog.getInt(self, f"Block {i+1}", f"Enter row index for block {i+1}:")
            column_index, ok2 = QInputDialog.getInt(self, f"Block {i+1}", f"Enter column index for block {i+1}:")
            if ok1 and ok2:
                self.world.place_block(row_index, column_index)
                self.update_log(f"World state after adding Block {self.world.block_counter}:")
                self.update_log(self.world.display_world())

        self.update_log("Final world state:")
        self.update_log(self.world.display_world())
        self.world.save_logs("D:/Anna/utm/3 year/ai/lab_1/log.txt")

    def move_block_ui(self):
        block_name, ok = QInputDialog.getText(self, "Move Block", "Enter block name:")
        if ok:
            dest_row, ok1 = QInputDialog.getInt(self, "Move Block", "Enter destination row:")
            dest_column, ok2 = QInputDialog.getInt(self, "Move Block", "Enter destination column:")
            if ok1 and ok2:
                self.world.put_on(block_name, dest_row, dest_column)
                self.update_log(f"World state after moving Block {block_name}:")
                self.update_log(self.world.display_world())

    def update_log(self, message):
        self.log_display.append(message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = WorldCubeGUI()
    gui.show()
    sys.exit(app.exec_())
