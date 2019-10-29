#!/usr/bin/env python
# _*_ coding:utf-8 _*_


# 棋盘
class Board(object):
    def __init__(self):
        self._board = ['-' for _ in range(9)]

    # 按指定动作，放入棋子
    def move(self, action, take):
        if self._board[action] == '-':
            self._board[action] = take

    # 撤销动作，拿走棋子
    def revert(self, action):
        self._board[action] = '-'

    # 取棋盘上的合法走法
    def get_legal_actions(self):
        return [i for i in range(9) if self._board[i] == '-']

    # 判断走法是否合法
    def is_legal_action(self, action):
        return self._board[action] == '-'

    # 终止检测
    def terminate(self):
        lines = self._get_lines()
        return ['X'] * 3 in lines or ['O'] * 3 in lines or '-' not in self._board

    # 胜负检查
    def get_winner(self):
        lines = self._get_lines()
        return 0 if ['X'] * 3 in lines else 1 if ['O'] * 3 in lines else 2

    def _get_lines(self):
        board = self._board
        return [board[0:3], board[3:6], board[6:9], board[0::3], board[1::3], board[2::3], board[0::4], board[2:7:2]]

    # 打印棋盘
    def show_board(self):
        board = self._board
        for i in range(len(board)):
            print(board[i], end='')
            if (i + 1) % 3 == 0:
                print()


# 玩家
class Player(object):
    """
        玩家只做两件事：思考、落子
        1. 思考 --> 得到走法
        2. 落子 --> 执行走法，改变棋盘
    """

    def __init__(self, take='X'):  # 默认执的棋子为 take = 'X'
        self.take = take

    def think(self, board):
        pass

    def move(self, board, action):
        board.move(action, self.take)


# 人类玩家
class HumanPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        while True:
            action = input('Please input a num in 1-9:')
            if len(action) == 1 and action in '123456789' and board.is_legal_action(int(action)):
                return int(action) - 1


# 电脑玩家
class AIPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        print('AI is thinking ...')
        take = ['X', 'O'][self.take == 'X']
        player = AIPlayer(take)  # 假想敌！！！
        _, action = self.min_max(board, player)
        return action

    # 极大极小法搜索，α-β剪枝
    def min_max(self, board, player, depth=0):
        """参考：https://stackoverflow.com/questions/44089757/minimax-algorithm-for-tic-tac-toe-python"""

        best_val = -10 if self.take == "O" else 10
        best_action = None

        if board.terminate():
            if board.get_winner() == 0:
                return -10 + depth, None
            elif board.get_winner() == 1:
                return 10 - depth, None
            elif board.get_winner() == 2:
                return 0, None

        for action in board.get_legal_actions():  # 遍历合法走法
            board.move(action, self.take)
            val, _ = player.min_max(board, self, depth + 1)  # 切换到 假想敌！！！
            board.revert(action)  # 撤销走法，回溯

            if self.take == "O":
                if val > best_val:
                    best_val, best_action = val, action
            else:
                if val < best_val:
                    best_val, best_action = val, action

        return best_val, best_action


# 游戏
class Game(object):
    def __init__(self):
        self.board = Board()
        self.current_player = None

    # 生成玩家
    @staticmethod
    def mk_player(p, take='X'):  # p in [0,1]
        return HumanPlayer(take) if p == 0 else AIPlayer(take)

    # 切换玩家
    def switch_player(self, player1, player2):
        return player1 if self.current_player is None else [player1, player2][self.current_player == player1]

    # 运行游戏
    def run(self):
        ps = input("Please select two player's type:\n\t0.Human\n\t1.AI\nSuch as:0 0\n")
        p1, p2 = [int(p) for p in ps.split(' ')]
        player1, player2 = self.mk_player(p1, 'X'), self.mk_player(p2, 'O')  # 先手执X，后手执O

        print('\nGame start!\n')
        self.board.show_board()  # 显示棋盘
        while True:
            self.current_player = self.switch_player(player1, player2)  # 切换当前玩家

            action = self.current_player.think(self.board)  # 当前玩家对棋盘进行思考后，得到招法

            self.current_player.move(self.board, action)  # 当前玩家执行招法，改变棋盘

            self.board.show_board()  # 显示当前棋盘

            if self.board.terminate():  # 根据当前棋盘，判断棋局是否终止
                winner = self.board.get_winner()  # 得到赢家 0,1,2
                break

        # 打印赢家 winner in [0,1,2]
        print(['Winner is player1\n', 'Winner is player2\n', 'Draw\n'][winner])
        print('Game over!\n')


if __name__ == '__main__':
    Game().run()
