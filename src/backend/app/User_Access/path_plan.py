import json
from . import robots

def scope_plan(position):
    scopes = []
    for i in range(1, 10):
            if len(robots['UAV']) <= i ** 2:
                scope_cnt = i 
                break

    scope_left_low = {
        'lat': position['lat'] - 1 / 111 / 2,
        'lng': position['lng'] - 0.01 / 2
    }
    mash_unit = {
        'lat': 1 / 111 / scope_cnt,
        'lng': 0.01 / scope_cnt
    }

    for i in range(scope_cnt):
        for j in range(scope_cnt):
            scope = [
                {'lat': scope_left_low['lat'] + mash_unit['lat'] * i, 'lng': scope_left_low['lng'] + mash_unit['lng'] * j},
                {'lat': scope_left_low['lat'] + mash_unit['lat'] * (i + 1), 'lng': scope_left_low['lng'] + mash_unit['lng'] * j},
                {'lat': scope_left_low['lat'] + mash_unit['lat'] * (i + 1), 'lng': scope_left_low['lng'] + mash_unit['lng'] * (j + 1)},
                {'lat': scope_left_low['lat'] + mash_unit['lat'] * i, 'lng': scope_left_low['lng'] + mash_unit['lng'] * (j + 1)}
            ]
            scopes.append(scope)
    
    return scopes 
