import math as m
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

input_list = []  # 입력 리스트
seg_tree = []  # 세그먼트 트리

# 세그먼트 트리의 크기 설정하는 함수
def seg_tree_const(list, n):
    global seg_tree
    height = m.ceil(m.log2(n))
    t_size = 2 * 2 ** height - 1
    seg_tree = [0] * t_size
    construct_tree(list, 0, n-1, seg_tree, 0)
    return seg_tree


# 입력 리스트를 세그먼트 트리의 리스트에 넣어서 구성하는 함수
def construct_tree(list, start, end, seg_tree, current):
    if start == end:
        seg_tree[current] = list[start]
        return list[start]
    
    mid = (start + end) // 2
    child = 2 * current
    seg_tree[current] = (construct_tree(list, start, mid, seg_tree, child + 1) + 
                         construct_tree(list, mid + 1, end, seg_tree, child + 2))
    return seg_tree[current]


# 질의 범위의 해당하는 값 반환하는 함수
def get_query(seg_tree, n, q_s, q_e):
    if q_s < 0 or q_e > n-1 or q_s > q_e: return -1

    return query_sum(seg_tree, 0, n-1, q_s, q_e, 0)


# 범위에 해당하는 값들을 더해서 반환하는 함수
def query_sum(seg_tree, start, end, q_s, q_e, current):
    if end < q_s or start > q_e: return 0
    if q_s <= start and q_e >= end: return seg_tree[current]
    
    mid = (start + end) // 2
    child = 2 * current
    return (query_sum(seg_tree, start, mid, q_s, q_e, child + 1) + 
            query_sum(seg_tree, mid + 1, end, q_s, q_e, child + 2))


# 입력 리스트의 변경에 따른 세그먼트 트리를 갱신하는 함수
def seg_tree_update(seg_tree, start, end, index, diff_val, current):
    if index < start or index > end: return
    
    seg_tree[current] = seg_tree[current] + diff_val
    if start != end:
        mid = (start + end) // 2
        child = 2 * current
        seg_tree_update(seg_tree, start, mid, index, diff_val, child + 1)
        seg_tree_update(seg_tree, mid + 1, end, index, diff_val, child + 2)


# main 함수
def main():
    print()
    print("1.입력 리스트 초기화  |  2.구간 합 질의  |  3.입력 리스트 변경  |  4.출력  |  5.종료")
    print("번호 입력 : ", end = "")
    menu = int(input())

    global input_list
    global seg_tree

    if menu == 1:
        print("입력 리스트 : ", end = "")
        input_list = list(map(int, input().split()))
        seg_tree = seg_tree_const(input_list, len(input_list))
        print(f'세그먼트 트리 : {seg_tree}')

    elif menu == 2:
        if len(seg_tree) == 0: 
            print("tree empty!!")
            return False
        
        print("시작 인덱스 : ", end = "")
        q_s = int(input())
        print("끝 인덱스 : ", end = "")
        q_e = int(input())

        sum = get_query(seg_tree, len(input_list), q_s, q_e)
        
        if sum < 0:
            print("range error!!")
            return False
        else:
            print(f'구간 합 : {sum}')

    elif menu == 3:
        print("변경할 인덱스(위치) : ", end = "")
        index = int(input())
        print("변경 값 : ", end = "")
        value = int(input())
        if input_list[index] > value:
            diff_val = input_list[index] - value
        else:
            diff_val = value - input_list[index]

        print(f'갱신 전 세그먼트 트리 : {seg_tree}')
        seg_tree_update(seg_tree, 0, len(input_list) - 1, index, diff_val, 0)
        print(f'갱신 후 세그먼트 트리 : {seg_tree}')

    elif menu == 4:
        print(seg_tree)
    elif menu == 5:
        return False
    else:
        print("menu error!!")
        return False


while True:
    if main() == False: break