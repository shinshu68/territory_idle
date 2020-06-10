import numpy as np
import os
import toml


def green(txt):
    GREEN = '\033[32m'
    END = '\033[0m'
    return GREEN + txt + END


# 各種データ
HOME = os.getenv('HOME')
with open(f'{HOME}/workspace/territory_idle/tile_calc_by_surveyors/data.toml') as f:
    data = toml.load(f)

base_tile_cost = data['cost']['tile']
surveyors_cost = data['cost']['surveyors']
russia_empire = data['empire']['russia']
tile_max = data['max']['tile']
surveyors_max = data['max']['surveyors']

# タイルのコスト倍率を数値で保存
tile_cost_ratio = 9 if russia_empire else 10

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
r = surveyors_max + 1
c = tile_max + 1
a = np.zeros((r, c))

# surveyorが0回の時を計算
for i in range(0, c):
    a[0][i] = sum(base_tile_cost * tile_cost_ratio**x for x in range(0, i))

# surveyorが1回以上の時を計算
for i in range(1, r):
    # i回surveyorした時のコスト合計
    n = sum((x**2 - 2 * x + 2) * (2**((x - 1) // 10)) for x in range(surveyors_times, surveyors_times + i))

    # i回surveyorしてj枚のタイルを買った時のコスト合計を計算
    for j in range(0, c):
        cost_cut = 2**i
        a[i][j] = n + sum(base_tile_cost * (tile_cost_ratio**x) / cost_cut for x in range(0, j))


# タイル枚数の見出し表示
axis_row = ['↓ S \\ T →'] + list(range(0, c))
for i in axis_row:
    print(f'{i:^9}', end='')
print()

# 各コストを表示
for i in range(r):
    print(f'{i:<9}', end='')
    for j in range(c):
        # 表示桁数が多いものは表示しない
        if a[i][j] > 1e6:
            break

        # 各枚数で最もコストが少ないものを緑色で表示
        if (i == 0 and a[i + 1][j] > a[i][j]) or \
           (i == r - 1 and a[i - 1][j] > a[i][j]) or \
           (a[i - 1][j] > a[i][j] and a[i + 1][j] > a[i][j]):
            print(green(f'{a[i][j]:>8.1f} '), end='')
        else:
            print(f'{a[i][j]:>8.1f} ', end='')
    print()

# print(a)
