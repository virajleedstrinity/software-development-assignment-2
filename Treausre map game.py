import random
from collections import deque

class TreasureHunt:
    def __init__(self, grid_size=10):
        self.grid_size = grid_size
        self.grid = self.initialize_grid()
        self.player_pos = [0, 0]
        self.health = 100
        self.treasure_pos = self.place_treasure()
        self.rival_pos = [grid_size - 1, grid_size - 1]
        self.power_up_count = 0

    def initialize_grid(self):
        grid = [['E' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        # Add more traps
        for _ in range((self.grid_size * self.grid_size) // 3):  # Increase the number of traps
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            grid[x][y] = 'T'
        # Add obstacles
        for _ in range(self.grid_size // 3):
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            grid[x][y] = 'O'
        # Add power-ups
        for _ in range(self.grid_size // 4):
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            grid[x][y] = 'P'
        return grid

    def place_treasure(self):
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if self.grid[x][y] == 'E':  # Empty cell
                self.grid[x][y] = 'X'  # Mark treasure
                return [x, y]

    def display_grid(self, reveal=False):
        print("\nGrid:")
        for i in range(self.grid_size):
            row = ""
            for j in range(self.grid_size):
                if reveal or [i, j] == self.player_pos or [i, j] == self.rival_pos:
                    row += self.grid[i][j] + " "
                else:
                    row += ". "
            print(row)
        print()

    def move_player(self, direction):
        x, y = self.player_pos
        moves = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if direction in moves:
            dx, dy = moves[direction]
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                self.player_pos = [new_x, new_y]
                self.interact_with_cell(new_x, new_y)
            else:
                print("You can't move outside the grid!")

    def interact_with_cell(self, x, y):
        cell = self.grid[x][y]
        if cell == 'T':
            print("You stepped on a trap! Health -20.")
            self.health -= 20
        elif cell == 'P':
            print("You found a power-up! Health +10.")
            self.health += 10
            self.power_up_count += 1
        elif cell == 'X':
            print("Congratulations! You found the treasure!")
            exit()
        self.grid[x][y] = 'E'  # Clear the cell after interaction

    def bfs_pathfinding(self, start, goal):
        queue = deque([start])
        visited = set()
        visited.add(tuple(start))
        parent = {tuple(start): None}

        while queue:
            current = queue.popleft()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = parent[tuple(current)]
                return path[::-1]

            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.grid_size and 0 <= ny < self.grid_size and
                        (nx, ny) not in visited and self.grid[nx][ny] != 'O'):
                    queue.append([nx, ny])
                    visited.add((nx, ny))
                    parent[(nx, ny)] = current
        return None

    def rival_move(self):
        path = self.bfs_pathfinding(self.rival_pos, self.treasure_pos)
        if path and len(path) > 1:
            self.rival_pos = path[1]
            print("Rival moved closer to the treasure!")

    def run_game(self):
        print("Welcome to the Treasure Hunt!")
        while self.health > 0:
            self.display_grid()
            print(f"Health: {self.health}")
            print(f"Power-ups collected: {self.power_up_count}")
            move = input("Enter your move (w/a/s/d): ").lower()
            if move in ['w', 'a', 's', 'd']:
                self.move_player(move)
                self.rival_move()
                if self.rival_pos == self.treasure_pos:
                    print("The rival found the treasure before you! Game over.")
                    break
            else:
                print("Invalid move! Use 'w', 'a', 's', 'd' to move.")
        else:
            print("You ran out of health. Game over.")

if __name__ == "__main__":
    game = TreasureHunt(grid_size=10)
    game.run_game()
