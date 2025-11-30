"""クリック処理モジュール"""
def canvas_on_click(event):
    """キャンバスをクリックした時の処理"""  # --- (*1)
    if game["completed"]:
        return
    # クリックされた位置を取得 --- (*2)
    rect = canvas.getBoundingClientRect()
    x = int(event.clientX - rect.left)
    y = int(event.clientY - rect.top)
    # クリックされたセルを特定 --- (*3)
    row, col = y // CELL_SIZE, x // CELL_SIZE
    if (row >= GRID_SIZE) or (col >= GRID_SIZE):
        return
    game["selected"] = (row, col)
    draw_board()  # 再描画

def num_button_on_click(num):
    """数字ボタンをクリックした時の処理"""  # --- (*4)
    if game["selected"] is None:
        q_text("#title", "先にセルを選択してください")
        set_timeout(lambda: q_text("#title", "ナンバープレース"), 1000)
        return
    row, col = game["selected"]
    place_number(row, col, num)
    draw_board()

def eraser_button_click(event):
    """消しゴムボタンがクリックされた時の処理"""  # --- (*5)
    if game["selected"] is None:
        return
    row, col = game["selected"]
    if game["original"][row][col] != 0:
        return  # 元の数字は消せない
    game["board"][row][col] = 0
    draw_board()

# イベントリスナーの設定 --- (*6)
canvas.addEventListener("click", canvas_on_click)
q("#eraser").addEventListener("click", eraser_button_click)
# 数字ボタンのイベントリスナーを設定 --- (*7)
for i in range(1, 10):
    btn = q(f"#num{i}")
    btn.addEventListener("click",
        lambda e: num_button_on_click(int(e.target.textContent)))