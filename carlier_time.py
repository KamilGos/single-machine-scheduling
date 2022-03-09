import sys
from heapq import heappush, heapify, nlargest
from copy import deepcopy
from timeit import default_timer as timer

"""
some thing wrong
the result of carlier_data5 is 3618
"""
new_pi = 0
LB = 0
UB = sys.maxsize


class RPQ:
    @staticmethod
    def sortR(tab):
        data = tab.copy()
        order_by_access_time = data.copy()
        order_by_access_time.sort(key=lambda x: x[0])
        return order_by_access_time

    @staticmethod
    def start(tab):
        data = tab.copy()
        max_time_q = data[0][0] + data[0][1] + data[0][2]  # the current time of delivery of the low_bound
        time = data[0][0] + data[0][1]
        C = []
        C.append(time)
        for t in range(1, len(data)):
            if time > data[t][0]:
                time = time + data[t][1]
            else:
                time = data[t][0] + data[t][1]

            time_q = data[t][2] + time
            max_time_q = max(max_time_q, time_q)
            if max_time_q in C:
                C.append(time_q)
            else:
                C.append(max_time_q)
        return C

    @staticmethod
    def find_max_C(data):
        max_C = data[0]
        for i in range(0, len(data)):
            if data[i] > max_C:
                max_C = data[i]
        return max_C

    @staticmethod
    def heap(data):
        q = [(x[2], x) for x in data]
        heapify(q)
        max = nlargest(1, q)
        max_q = max[0][0]
        max_el = max[0][1]
        p = max[0][1][1]
        return max_q, max_el, p

    @staticmethod
    def schrage(tab):
        N = tab.copy()
        pi = []
        # n, N = RPQ.read(data)  # loads data from a file
        k = 1
        G = []
        sorted = RPQ.sortR(N)
        min_r = sorted[0][0]
        time = sorted[0][0]  # take the smallest time R (sorting by R)
        while len(N) != 0 or len(G) != 0:
            while len(N) != 0 and (min_r <= time):
                el = sorted[0]
                heappush(G, el)  # add an element to G
                N.remove(el)  # remove an element from N
                sorted.remove(el)
                if len(sorted) != 0:
                    min_r = sorted[0][0]
            if len(G) != 0:
                max_q, el_2, p = RPQ.heap(G)
                G.remove(el_2)  # remove this element from G
                time += p  # add the execution time to the start time
                k += 1
                pi.append(el_2)
            else:
                time = sorted[0][0]
        return pi

    @staticmethod
    def schrage_pmtn(tab):
        # n, N = RPQ.read(data)  # loads data from a file

        N = deepcopy(tab)
        G = []
        sorted = RPQ.sortR(N)
        min_r = sorted[0][0]
        time = 0  # take the smallest time R (sorting by R)
        C_max = 0
        el_l = [0, 0, 1000000]
        while len(N) != 0 or len(G) != 0:
            while len(N) != 0 and min_r <= time:
                el = sorted[0]
                heappush(G, el)  # add an element to G
                N.remove(el)  # remove an element from N
                sorted.remove(el)
                if len(sorted) != 0:
                    min_r = sorted[0][0]
                if el[2] > el_l[2]:
                    el_l[1] = time - el[0]
                    time = el[0]
                    if el_l[1] > 0:
                        heappush(G, el_l)
            if len(G) == 0:
                time = sorted[0][0]
            else:
                max_q, el_2, p = RPQ.heap(G)  # search for the largest time q
                G.remove(el_2)  # remove this element from G
                el_l = el_2
                time += p  # add the execution time to the start time
                C_max = max(C_max, time + max_q)
        return C_max

    @staticmethod
    def schrage_pmtn_deepcopy(tab):
        # n, N = RPQ.read(data)  #loads data from a file

        N = deepcopy(tab)
        G = []
        sorted = RPQ.sortR(N)
        min_r = sorted[0][0]
        time = 0  # take the smallest time R (sorting by R)
        C_max = 0
        el_l = [0, 0, 1000000]
        while len(N) != 0 or len(G) != 0:
            while len(N) != 0 and min_r <= time:
                el = sorted[0]
                heappush(G, el)  # add an element to G
                N.remove(el)  # remove an element from N
                sorted.remove(el)
                if len(sorted) != 0:
                    min_r = sorted[0][0]
                if el[2] > el_l[2]:
                    el_l[1] = time - el[0]
                    time = el[0]
                    if el_l[1] > 0:
                        heappush(G, el_l)
            if len(G) == 0:
                time = sorted[0][0]
            else:
                max_q, el_2, p = RPQ.heap(G)  # search for the largest time q
                G.remove(el_2)  # remove this element from G
                el_l = el_2
                time += p  # add the execution time to the start time
                C_max = max(C_max, time + max_q)
        return C_max, tab

    @staticmethod
    def find_max_b(data_b, C_max):
        for i in range(len(data_b) - 1, 0, -1):
            if data_b[i] == C_max:
                return data_b.index(data_b[i])

    @staticmethod
    def find_min_a(data, C_max, b):
        sum_p = 0
        for i in range(0, len(data)):
            for j in range(i, b + 1):
                sum_p += data[j][1]
            r = data[i][0]
            q = data[b][2]
            C_max_pom = data[i][0] + sum_p + data[b][2]
            if C_max_pom == C_max:
                return i
            sum_p = 0

    @staticmethod
    def find_max_c(data, a, b):
        for i in range(b, a - 1, -1):
            if data[i][2] < data[b][2]:
                return i

    @staticmethod
    def find_new_rpq(c, b, data):
        new_p = 0
        new_r = sys.maxsize
        # min_q = sys.maxsize
        new_q = sys.maxsize
        for i in range(c + 1, b + 1):
            if data[i][0] < new_r:
                new_r = data[i][0]
            if data[i][2] < new_q:
                new_q = data[i][2]
            new_p += data[i][1]
        return new_r, new_p, new_q

    @staticmethod
    def carlier_test(arrays):
        arrays_copy = arrays.copy()
        arrays_schrage = RPQ.schrage(arrays_copy)
        arrays_start = RPQ.start(arrays_schrage)
        U = RPQ.find_max_C(arrays_start)
        old_pi = RPQ.find_max_C(arrays_start)
        C_max = RPQ.find_max_C(arrays_start)
        start = timer()
        # UB = sys.maxsize
        global UB
        global new_pi
        if U < UB:
            UB = U
            new_pi = old_pi
        b = RPQ.find_max_b(arrays_start, C_max)
        a = RPQ.find_min_a(arrays_schrage, C_max, b)
        c = RPQ.find_max_c(arrays_schrage, a, b)
        if c is None:
            end = timer()
            return end - start
        new_r, new_p, new_q = RPQ.find_new_rpq(c, b, arrays_schrage)
        r_c = arrays_schrage[c][0]
        arrays_schrage[c][0] = max(arrays_schrage[c][0], new_r + new_p)
        # t = arrays_schrage.copy()
        global LB
        LB, original_schrage = RPQ.schrage_pmtn_deepcopy(arrays_schrage)
        if LB < UB:
            RPQ.carlier_test(original_schrage)
        original_schrage[c][2] = r_c
        q_c = original_schrage[c][2]
        original_schrage[c][2] = max(original_schrage[c][2], new_q + new_p)
        LB, more_original_schrage = RPQ.schrage_pmtn_deepcopy(original_schrage)
        if LB < UB:
            RPQ.carlier_test(more_original_schrage)
        more_original_schrage[c][2] = q_c
        end = timer()
        return end - start


def read_file(filepath):
    data = []
    with open(filepath) as f:
        n, columns = [int(x) for x in next(f).split()]
        data = [[int(x) for x in line.split()] for line in f]
        data = data[:n]
    return data


# print(RPQ.carlier_test(read('data500.txt')))

if __name__ == "__main__":
    time_result = 0
    for i in range(100):
        time_result = time_result + RPQ.carlier_test(read_file("data/carlier_data5.txt"))
    print(time_result / 100)
    print(LB, UB, new_pi)

    # data = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    # get_data_file = lambda x: "data/carlier_data" + str(x) + ".txt"
    # result_schrage = []
    # result_schrage_pmtn = []
    # result_carlier = []
    # result_UB = []
    # result_pi = []
    # for i in range(9):
    #     new_pi = 0
    #     LB = 0
    #     UB = sys.maxsize
    #     data10 = read_file(get_data_file(i))
    #     result_schrage.append(RPQ.find_max_C(RPQ.start(RPQ.schrage(data10))))
    #     result_schrage_pmtn.append(RPQ.schrage_pmtn(data10))
    #     result_carlier.append((RPQ.carlier_test(data10)))
    #     result_UB.append(UB)
    #     result_pi.append(new_pi)
    #
    # print(result_schrage)
    # print(result_schrage_pmtn)
    # print(result_carlier)
    # print(result_UB)
    # print(result_pi)
