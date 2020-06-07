import numpy as np

# 各種入力
base_tile_cost = float(input('Tile Cost? (M) '))
surveyors_cost = int(input('Surveyors Cost? (M) '))
russia_empire = input('Russia Empire? [y/n] ')
while russia_empire not in ['y', 'n']:
    print(f'Russia Empire Value is Invalid {russia_empire}')
    russia_empire = input('Try Again: Russia Empire? [y/n] ')

# タイルのコスト倍率を数値で保存
tile_cost_ratio = 9 if russia_empire == 'y' else 10

# surveyorsの回数を計算
surveyors_times = None
for x in range(1, 11):
    n = (x**2 - 2 * x + 2) * (2**((x - 1) // 10))
    if surveyors_cost == n:
        surveyors_times = x
        break

    if surveyors_cost < n:
        print(f'Maybe Not Right Surveyors Cost Value ({surveyors_cost})')
        exit()

# 配列の大きさ指定
r = 11
c = 9 
a = np.zeros((r, c))

# surveyorが0回の時を計算
for i in range(0, c):
    a[0][i] = sum(base_tile_cost * tile_cost_ratio**x for x in range(0, i))

# surveyorが1回以上の時を計算
for i in range(1, r):
    # n回surveyorした時のコスト合計
    n = sum((x**2 - 2 * x + 2) * (2**((x - 1) // 10)) for x in range(surveyors_times, surveyors_times + i))
    for j in range(0, c):
        cost_cut = 2**i
        a[i][j] = n + sum(base_tile_cost * (tile_cost_ratio**x) / cost_cut for x in range(0, j))


axis_row = ['Tile →', 0, 1, 2, 3, 4, 5, 6, 7, 8]
for i in axis_row:
    print(f'{i:^9}', end='')

print()
print('Surveyor ↓')
for i, li in enumerate(a):
    print(f'{i:>9}', end='')
    for x in li:
        if x > 1e6:
            break
        print(f'{x:>8.1f} ', end='')
    print()

# print(a)
