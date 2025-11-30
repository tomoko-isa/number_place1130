"""ナンバープレースのメインロジック"""
# 定数の定義 --- (*1)
GRID_SIZE = 9  # 9x9のグリッド
BOX_SIZE = 3   # 3x3のボックス
CELL_SIZE = 43  # セルのサイズ (387 / 9 = 43)
EMPTY = 0  # 空のセルを表す値
# グローバル変数 --- (*2)
game = {
    "board": [],  # ボードデータ (9x9の2次元リスト)
    "original": [],  # 問題として与えられた初期ボード
    "selected": None,  # 選択中のセル (行, 列) または None
    "completed": False  # ゲームクリアしたかどうか
}  # ゲーム状態を表す

def game_start():
    """ゲームを開始する"""  # --- (*3)
    global game
    board = get_puzzle_data()  # 問題データを取得
    game = {
        "selected": None,
        "completed": False,
        "board": board,
        "original": [row[:] for row in board]  # コピーを保存
    }
    # ゲーム変数の初期化
    q_text("#title", "ナンバープレース")
    draw_board()

def get_puzzle_data():
    """ナンバープレース問題をを取得"""  # --- (*4)
    board = [
        [0, 0, 5, 0, 3, 0, 6, 0, 0],
        [8, 0, 0, 4, 0, 0, 3, 0, 0],
        [4, 0, 0, 0, 0, 9, 0, 2, 0],
        [0, 0, 0, 0, 0, 0, 9, 0, 6],
        [0, 0, 0, 1, 0, 0, 0, 8, 0],
        [7, 0, 0, 0, 0, 8, 0, 0, 0],
        [3, 0, 0, 5, 0, 0, 8, 0, 0],
        [2, 0, 1, 0, 7, 3, 0, 0, 0],
        [0, 9, 0, 0, 1, 2, 0, 0, 0]
    ]  # 問題データ
    return board

def can_place_number(board, row, col, num):
    """指定位置に数字を置けるかチェック"""  # --- (*5)
    # 行のチェック --- (*5a)
    for c in range(GRID_SIZE):
        if board[row][c] == num:
            return False
    # 列のチェック --- (*5b)
    for r in range(GRID_SIZE):
        if board[r][col] == num:
            return False
    # 3x3ボックスのチェック --- (*5c)
    box_row = (row // BOX_SIZE) * BOX_SIZE
    box_col = (col // BOX_SIZE) * BOX_SIZE
    for r in range(box_row, box_row + BOX_SIZE):
        for c in range(box_col, box_col + BOX_SIZE):
            if board[r][c] == num:
                return False
    return True

def place_number(row, col, num):
    """指定位置に数字を配置する"""  # --- (*6)
    if game["completed"]:
        return
    # 元の問題で固定されたセルは変更不可
    if game["original"][row][col] != 0:
        return
    # 数字を配置 --- (*7)
    if can_place_number(game["board"], row, col, num):
        game["board"][row][col] = num
        # 完成チェック
        if check_completion():
            game["completed"] = True
            q_text("#title", "おめでとう★ ナンバープレース完成！")
        else:
            q_text("#title", "ナンバープレース")
    else:
        # 無効な配置の場合、一時的にメッセージを表示 --- (*8)
        q_text("#title", "その数字は置けません")
        set_timeout(lambda: q_text("#title", "ナンバープレース"), 1000)

def check_completion():
    """パズルが完成しているかチェック"""  # --- (*9)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if game["board"][row][col] == 0:
                return False
    return True