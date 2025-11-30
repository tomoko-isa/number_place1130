"""ナンバープレース描画モジュール (draw.py)"""
# キャンバスとコンテキストの取得 --- (*1)
canvas = q("#canvas")
context = canvas.getContext("2d")

def draw_board():
    """ボードを描画する"""  # --- (*2)
    draw_background()  # 背景を白で塗りつぶし
    draw_grid()  # グリッド線を描画
    draw_numbers()  # 数字を描画

def draw_background():
    """背景を描画する"""  # --- (*3)
    context.clearRect(0, 0, canvas.width, canvas.height) # 画面クリア
    context.fillStyle = "#ffffff"
    context.fillRect(0, 0, canvas.width, canvas.height)
    # 選択中のセルがあればハイライトする --- (*4)
    if not game["selected"]:
        return
    # 選択中のセルの背景を描画
    sel_c, sel_r = game["selected"][0], game["selected"][1]
    xx = sel_r * CELL_SIZE
    yy = sel_c * CELL_SIZE
    context.fillStyle = "rgba(230, 230, 80, 0.1)"
    for row in range(GRID_SIZE):  # 行全体
        y = row * CELL_SIZE
        context.fillRect(xx ,y, CELL_SIZE, CELL_SIZE)
    for col in range(GRID_SIZE):  # 列全体
        x = col * CELL_SIZE
        context.fillRect(x ,yy, CELL_SIZE, CELL_SIZE)
    # 選択中のセルを描画
    context.fillStyle = "rgba(255, 255, 0, 0.5)"
    context.fillRect(xx ,yy, CELL_SIZE, CELL_SIZE)

def draw_line(x1, y1, x2, y2, width=1, color="black"):
    """線を描画する"""  # --- (*5)
    context.strokeStyle = color
    context.lineWidth = width
    context.beginPath()
    context.moveTo(x1, y1)
    context.lineTo(x2, y2)
    context.stroke()

def draw_grid():
    """グリッド線を描画する"""  # --- (*6)
    # 細い線（セル境界）
    for i in range(GRID_SIZE + 1):
        x, y = i * CELL_SIZE, i * CELL_SIZE
        draw_line(x, 0, x, GRID_SIZE * CELL_SIZE, 1)
        draw_line(0, y, GRID_SIZE * CELL_SIZE, y, 1)
    # 太い線（3x3のボックス境界）
    for i in range(0, GRID_SIZE + 1, BOX_SIZE):
        x, y = i * CELL_SIZE, i * CELL_SIZE
        draw_line(x, 0, x, GRID_SIZE * CELL_SIZE, 3)
        draw_line(0, y, GRID_SIZE * CELL_SIZE, y, 3)

def draw_numbers():
    """数字を描画する"""  # --- (*7)
    context.textAlign = "center"
    context.textBaseline = "middle"
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            num = game["board"][row][col]
            if num == 0:
                continue
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2
            # 固定数字と入力数字で色を変える --- (*8)
            if game["original"][row][col] != 0:
                # 問題として与えられた数字（黒）
                context.fillStyle = "#000000"
                context.font = "bold 20px Arial"
            else:
                # ユーザーが入力した数字（青） --- (*9)
                context.fillStyle = "#0066cc"
                context.font = "18px Arial"
            context.fillText(str(num), x, y)