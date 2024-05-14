from itertools import permutations
def next_bigger(n):
    s_n = str(n)
    v = 9
    for i in s_n:
        if int(i) <= v:
            v = int(i)
        else:
            return solve_bigger(s_n)
    return -1

def solve_bigger(s_n):
    permutation = [''.join(p) for p in permutations(s_n)]
    int_perm = list(map(int, permutation))
    int_perm.sort()
    print(int_perm)
    i = int_perm.index(int(s_n))
    count = int_perm.count(int(s_n))
    return int_perm[i + count]