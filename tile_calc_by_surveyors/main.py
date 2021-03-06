import numpy as np
import os
import toml


def green(txt):
    GREEN = '\033[32m'
    END = '\033[0m'
    return GREEN + txt + END


def white_black(txt):
    WHITE_BLACK = '\033[30;47m'
    END = '\033[0m'
    return WHITE_BLACK + txt + END


_, lines = os.get_terminal_size()
# 各種データ
HOME = os.getenv('HOME')
with open(f'{HOME}/workspace/territory_idle/tile_calc_by_surveyors/data.toml') as f:
    data = toml.load(f)

base_tile_cost = data['cost']['tile']
surveyors_cost = data['cost']['surveyors']
russia_empire = data['empire']['russia']
tile_max = data['max']['tile']

# タイルのコスト倍率を数値で保存
tile_cost_ratio = 9 if russia_empire else 10

# surveyorsの回数を計算
surveyors_times = None
i = 1
while True:
    # surveyorsのcostの計算
    n = (i**2 - 2 * i + 2) * (2**((i - 1) // 10))

    if surveyors_cost == n:
        surveyors_times = i
        break

    if surveyors_cost < n:
        print(f'Maybe Not Right Surveyors Cost Value ({surveyors_cost})')
        a = i - 1
        n2 = (a**2 - 2 * a + 2) * (2**((a - 1) // 10))
        print(f'Maybe {n} or {n2}')
        exit()

    i += 1

# 配列の大きさ指定
c = tile_max
a = np.zeros(c)

# 各タイル購入で最適なコスト保存用配列 適当な値で初期化
best_costs = np.full(c, 1e9)

# surveyorが0回の時を計算
for i in range(1, c + 1):
    a[i - 1] = sum(base_tile_cost * tile_cost_ratio**x for x in range(0, i))

# surveyorが1回以上の時を計算
i = 1
while True:
    f = False
    a = np.vstack((a, np.zeros(c)))

    # i回surveyorした時のコスト合計
    n = sum((x**2 - 2 * x + 2) * (2**((x - 1) // 10)) for x in range(surveyors_times, surveyors_times + i))

    # i回surveyorしてj枚のタイルを買った時のコスト合計を計算
    for j in range(1, c + 1):
        cost_cut = 2**i
        a[i][j - 1] = n + sum(base_tile_cost * (tile_cost_ratio**x) / cost_cut for x in range(0, j))

        if best_costs[j - 1] > a[i][j - 1]:
            best_costs[j - 1] = a[i][j - 1]
            f = True

    i += 1
    if not f:
        break

# タイル枚数の見出し表示
axis_row = ['↓ S \\ T →'] + list(range(1, c + 1))
for i in range(c + 1):
    if i == 0:
        print(white_black(f'{axis_row[i]:^11}'), end='')
    else:
        print(white_black(f'{axis_row[i]:^9}'), end='')
print()

for i in range(len(a)):
    # surveyorsの回数と各コストを表示
    print(white_black(f'{i:<3}'), end='')
    x = surveyors_times + i - 1
    n = (x**2 - 2 * x + 2) * (2**((x - 1) // 10))
    if i == 0:
        print(white_black(f'{0:>7}') + ' ', end='')
    elif n < 1e6:
        print(white_black(f'{n:>7}') + ' ', end='')
    else:
        print(white_black(f'{" ":>7}') + ' ', end='')

    # タイルのコストとSurveyorsのコストの合計
    for j in range(c):
        # 桁数が多いものは表示しない
        if a[i][j] > 1e6:
            break

        # 各枚数で最もコストが少ないものを緑色で表示
        if (i == 0 and a[i + 1][j] > a[i][j]) or \
           (i == len(a) - 1 and a[i - 1][j] > a[i][j]) or \
           (a[i - 1][j] > a[i][j] and a[i + 1][j] > a[i][j]):
            print(green(f'{a[i][j]:>8.1f}') + ' ', end='')
        else:
            print(f'{a[i][j]:>8.1f}' + ' ', end='')
    print()

cost_rario = np.zeros(c - 1)
for i in range(c - 1):
    cost_rario[i] = best_costs[i + 1] / best_costs[i]

print(f'{"cost_ratio":^11}', end='')
print(f'{" ":^9}', end='')
for i in range(c - 1):
    print(f'{cost_rario[i]:>8.3f}' + ' ', end='')
print()

