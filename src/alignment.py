
def alignment(config, x='', y=''):

    log = {
        'cost': 0,
        'matches': 0,
        'mismatches': [],
        'x_gaps': 0,
        'y_gaps': 0
    }
    
    costs = [[(0, 'Match')]] # Memoization matrix

    for i in range(1, len(x)+1):
        costs.append([(costs[i-1][0][0] + config['gap_weight'], 'Gap em Y')])
    for j in range(1, len(y)+1):
        costs[0].append((costs[0][j-1][0] + config['gap_weight'], 'Gap em X'))

    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            costs[i].append(min(
                ((costs[i-1][j-1][0] + config['mism_weight'], 'Mismatch') if x[i-1]!=y[j-1] else (costs[i-1][j-1][0] + 0, 'Match')),
                (costs[i-1][j][0] + config['gap_weight'], 'Gap em Y'),
                (costs[i][j-1][0] + config['gap_weight'], 'Gap em X'),
                key=lambda a: (a[0], config['priority'].index(a[1]))
            ))

    #for i in range(len(x)+1): print(costs[i]) # Debug

    i, j = len(x), len(y)
    a, b = '', ''
    
    while i or j:
        if costs[i][j][1] == 'Gap em X':
            log['cost'] += config['gap_weight']; log['x_gaps'] += 1
            a = '□' + a; b = y[j-1] + b; j -= 1
        elif costs[i][j][1] == 'Gap em Y':
            log['cost'] += config['gap_weight']; log['y_gaps'] += 1
            b = '□' + b; a = x[i-1] + a; i -= 1
        else:
            if costs[i][j][1] == 'Match':
                log['matches'] += 1
            elif costs[i][j][1] == 'Mismatch':
                log['mismatches'].append(len(b))
                log['cost'] += config['mism_weight']
            
            a = x[i-1] + a; b = y[j-1] + b
            i -= 1; j -= 1

    return a, b, log

# gap char: □ (U+25A1)