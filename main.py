# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
import random
import math
import time

# 定数
GRID_WIDTH = 50 # 1マスの幅
BOARD_X0 = 150 # 盤面の描画位置(X座標)
BOARD_Y0 = 20  # 盤面の描画位置(Y座標)
BLACK = 1
WHITE = -1
SPACE = 0
SENTINEL = 3
KOMI = 6.5

GRID = 9
BOARD_MAX = (GRID + 2) * (GRID + 2)

DIR4 = [1, -1, GRID + 2, -(GRID + 2)] # 右左下上
PASS = 0

# 打った結果
SUCCESS = 0
ILLIGAL = 1
KO = 2
EYE = 3

# UCB用定数
FPU = 5 # First Play Urgency
C = 0.31
THR = 1

PLAYOUT_MAX = 300

# 盤初期化 9×9  二次元配列でやったらよくない？
def create_board():
	board = [0 for i in range((9+2)*(9+2))]
	#上下の壁(3)を作る
	for x in range(9+2):
		board[x] = 3
		board[x+(9+2)*(9+1)] = 3
	#左右の壁を作る
	for y in range(1,9+2):
		board[(9+2)*y] = 3
		board[(9+1) + (GRID+2)*y] = 3
	return board
'''
# x, y座標をboardのインデックスに変換
def get_xy(x, y):
    return x + (GRID+2) * y

def get_x_y(xy):
    return xy % (GRID+2),  xy / (GRID+2)
'''

'''
def capture(board, xy, color):
    board[xy] = SPACE
    for d in DIR4:
        if board[xy + d] == color:
            capture(board, xy + d, color)
'''


# メインウィンドウ
class MainWindow(QtGui.QWidget):

    # 初期化
    def __init__(self):
        super(MainWindow, self).__init__()
        self.app = app

        # 盤初期化
        self.board = create_board()

        # コウ
        #self.ko = Ko()

        # 思考ルーチン一覧
        '''
        self.player_lists = []
        self.player_lists.append(MCTSSample)
        self.player_lists.append(Human)
        '''


        # プレイヤー選択
        #self.selectedPlayer = []
        # Black
        '''
        self.selectedPlayer.append(self.player_lists[0])
        self.cmbPlayer = []
        self.labelBlack = QtGui.QLabel(self)
        self.labelBlack.setText("Black:")
        self.labelBlack.move(10, 10)
        self.cmbPlayer.append(QtGui.QComboBox(self))
        self.cmbPlayer[0].activated.connect(self.onActivatedBalack)
        self.cmbPlayer[0].move(10, 30)
        '''

        # White
        '''
        self.selectedPlayer.append(self.player_lists[0])
        x_white = BOARD_X0 + GRID_WIDTH * 10 + 10
        self.labelWhite = QtGui.QLabel(self)
        self.labelWhite.setText("White:")
        self.labelWhite.move(x_white, 10)
        self.cmbPlayer.append(QtGui.QComboBox(self))
        self.cmbPlayer[1].activated.connect(self.onActivatedWhite)
        self.cmbPlayer[1].move(x_white, 30)

        for player in self.player_lists:
            for cmb in self.cmbPlayer:
                cmb.addItem(player.__name__)

        self.current_player = None
        '''

        # 開始ボタン
        '''
        self.btnStart = QtGui.QPushButton(self)
        self.btnStart.setText("Start")
        self.btnStart.resize(GRID_WIDTH * 3, GRID_WIDTH)
        self.btnStart.clicked.connect(self.start)
        self.btnStart.move(BOARD_X0 + GRID_WIDTH * (GRID / 2 - 0.5), BOARD_Y0 + GRID_WIDTH * GRID / 2)
        '''

        # ウィンドウサイズ
        self.resize(BOARD_X0 * 2 + GRID_WIDTH * (GRID + 1), BOARD_Y0 * 2 + GRID_WIDTH * (GRID + 1))

    # 描画
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setBrush(QtGui.QColor(190, 160, 60))
        painter.drawRect(BOARD_X0, BOARD_Y0, GRID_WIDTH * 10, GRID_WIDTH * (GRID + 1))

        # 盤面
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 2))
        for x in range(1, GRID + 1):
            painter.drawLine(BOARD_X0 + GRID_WIDTH * x, BOARD_Y0 + GRID_WIDTH,
                                BOARD_X0 + GRID_WIDTH * x, BOARD_Y0 + GRID_WIDTH * GRID)
        for y in range(1, GRID + 1):
            painter.drawLine(BOARD_X0 + GRID_WIDTH, BOARD_Y0 + GRID_WIDTH * y,
                                BOARD_X0 + GRID_WIDTH * GRID, BOARD_Y0 + GRID_WIDTH * y)

        # 石
        '''
        for x in range(GRID):
            for y in range(GRID):
                xy = get_xy(x + 1, y + 1)
                c = self.board[xy]
                if c != SPACE:
                    if c == BLACK:
                        painter.setBrush(QtCore.Qt.black)
                    else:
                        painter.setBrush(QtCore.Qt.white)
                    painter.drawEllipse(BOARD_X0 + GRID_WIDTH * (x+0.5), BOARD_Y0 + GRID_WIDTH * (y+0.5), GRID_WIDTH, GRID_WIDTH)
		'''
        # 位置ごとの勝率を表示
        '''
        if isinstance(self.current_player, MCTSSample):
            painter.setPen(QtCore.Qt.red)
            for child in self.current_player.root.child:
                x, y = get_x_y(child.xy)
                text = "{0:^3}/{1:^3}".format(child.win_num, child.playout_num)
                painter.drawText(BOARD_X0 + GRID_WIDTH * (x-0.35), BOARD_Y0 + GRID_WIDTH * y, text)

        painter.end()
        '''
	'''
    # コンボボックス選択(Black)
    def onActivatedBalack(self, number):
        self.selectedPlayer[0] = self.player_lists[number]

    # コンボボックス選択(White)
    def onActivatedWhite(self, number):
        self.selectedPlayer[1] = self.player_lists[number]
	'''
    # Start
    '''
    def start(self):
        self.btnStart.hide()

        players = {BLACK : self.selectedPlayer[0](BLACK), WHITE : self.selectedPlayer[1](WHITE)}

        color = BLACK
        pre_xy = -1
        while True:
            # 局面コピー
            board_tmp = self.board[:]
            ko_tmp = self.ko.copy()

            # 手を選択
            start = time.time()

            self.current_player = players[color]
            xy = self.current_player.select_move(board_tmp, ko_tmp)

            elapsed_time = time.time() - start
            print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"

            # 石を打つ
            err = move(self.board, self.ko, xy, color)

            if err != SUCCESS:
                print "error {0},{1}".format(get_x_y(xy))
                break

            if xy == PASS and pre_xy == PASS:
                # 終局
                print "end"
                break

            # 描画更新
            self.update()
            QtCore.QCoreApplication.processEvents()

            pre_xy = xy
            color = -color
    '''

    # マウスクリック
    '''
    def mousePressEvent(self, event):
        if isinstance(self.current_player, Human):
            if event.button() == QtCore.Qt.LeftButton:
                x = (event.pos().x() - BOARD_X0 + GRID_WIDTH/2) / GRID_WIDTH
                y = (event.pos().y() - BOARD_Y0 + GRID_WIDTH/2) / GRID_WIDTH
                self.current_player.set_xy(x, y)
            elif event.button() == QtCore.Qt.RightButton:
                self.current_player.set_xy(0, 0)
    '''
    # 閉じる
    def closeEvent(self, event):
        QtCore.QCoreApplication.quit()
        sys.exit()


if __name__=='__main__':
	#if len(sys.argv) >= 2:
	#	PLAYOUT = int(sys.argv[1])
	app = QtGui.QApplication(sys.argv)
	mainwnd = MainWindow()
	mainwnd.show()
	sys.exit(app.exec_())