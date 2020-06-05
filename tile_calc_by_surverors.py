
base_tile_cost = float(input('tile cost? (M) '))
surveyors_cost = int(input('surveyors cost? (M) '))
russia_empire = input('russia empire? [y/n] ')

surveyors_times = None
for x in range(1, 11):
    n = (x**2 - 2 * x + 2) * (2**((x - 1) // 10))
    if surveyors_cost == n:
        surveyors_times = x
        break

    if surveyors_cost < n:
        print(f'Maybe Not Right Surveyors Cost Value ({surveyors_cost})')
        exit()

