#!/usr/bin/env python
# _*_ coding:utf-8 _*_


class Game:
    def __init__(self, size: int = 3):
        self.size = size
        self.board = ['-' for _ in range(size * size)]
        self.current_tag = None

    def fall(self):
        while True:
            action = input('Please input line and column,Such as:0 0\n')
            line, column = [int(p) for p in action.split(' ')]
            action = (line - 1) * self.size + (column - 1)
            if self.board[action] == '-':
                return action

    def run(self):
        self.show()  # 显示棋盘
        while True:
            self.current_tag = 'X' if not self.current_tag else ['X', 'O'][self.current_tag == 'X']  # 切换当前玩家
            action = self.fall()  # 落子
            self.board[action] = self.current_tag
            self.show()  # 显示当前棋盘
            lines = list()
            for i in range(self.size):
                lines.append(self.board[(i * self.size):(i * self.size + self.size)])
                lines.append(self.board[i::self.size])
            lines.append(self.board[0::(self.size + 1)])
            lines.append(self.board[(self.size - 1):(self.size * self.size - 2):(self.size - 1)])
            if ['X'] * self.size in lines or ['O'] * self.size in lines or '-' not in self.board:  # 判断棋局是否终止
                index = 0 if ['X'] * self.size in lines else 1 if ['O'] * self.size in lines else 2
                return ['Winner is player1', 'Winner is player2', 'Draw'][index]  # 得到赢家

    def show(self):
        for i in range(len(self.board)):
            print(self.board[i], end='')
            if (i + 1) % self.size == 0:
                print()


if __name__ == '__main__':
    print('Game start!')
    print(Game(3).run())
    print('Game over!')
