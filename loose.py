"""
@project:RL-task-Shop-Scheduling
@author: fxz
@contact: fxz.fzu@gmail.com
@file:loose.py
@version: alpha
@time:2022/3/6 10:48
@desc:
    创建者请写入文件说明
"""
import copy
import operator
import sys
from itertools import permutations
from typing import List

cnt = 0
lower_bound = sys.maxsize  # 可中断情况下的下界 1 | r_{j},prmp | min(L_{max})
upper_bound = sys.maxsize  # 可行解的结果来更新


class TreeNode:
    def __init__(self, tasks, seq, curr=0):
        self.tasks = tasks  # 所有的任务
        self.task_dict = dict()
        for i in tasks:
            self.task_dict[i[0]] = i
        self.seq = []  # 已经确定的路径
        self.curr = 0  # 当前运行到的时间
        self.set_seq(seq)
        self.remain_tasks = [t for t in tasks if t[0] not in self.seq]  # 未完成的任务
        self.obj_val = self.get_obj_val()  # search the min of Lmax
        self.child = []  # 所有的子节点

    def set_seq(self, seq):
        self.seq = seq
        curr = 0
        for s in self.seq:
            t = self.task_dict[s]
            curr = max(curr, t[1]) + t[2]
        self.curr = curr

    def add_child(self, node):
        self.child.append(node)
        return self

    def get_obj_val(self, seq=None):
        if seq is None:
            seq = self.seq
        # 计算已经排程部分的目标值
        if len(seq) == 0:
            return 0
        release = []
        process = []
        due = []
        for s in seq:
            t = self.task_dict[s]
            release.append(t[1])
            process.append(t[2])
            due.append(t[3])
        finish = [0] * len(release)
        if len(seq) == 1:
            late = release[0] + process[0] - due[0]
        else:
            for i in range(len(seq)):
                finish[i] = max(finish[i - 1], release[i]) + process[i]
            late = max([f - d for d, f in zip(due, finish)])
        # late = max(0, late)
        return late

    def compute(self):
        # 计算未排程部分
        temp_seq = copy.copy(self.seq)
        temp_curr = self.curr
        task_num = len(self.remain_tasks)  # 剩余task数量
        edd_tasks = copy.deepcopy(sorted(self.remain_tasks, key=operator.itemgetter(3)))  # EDD rule
        lateness_time = [self.get_obj_val()]
        while len(temp_seq) < task_num:
            unscheduled_tasks = [i for i in edd_tasks if i[0] not in temp_seq]  # unscheduled task
            if unscheduled_tasks[0][1] <= temp_curr:  # earliest due date of task's release time is achieve
                # directly compute the first task
                temp_seq.append(unscheduled_tasks[0][0])
                temp_curr = max(unscheduled_tasks[0][1], temp_curr)
                temp_curr += unscheduled_tasks[0][2]
                lateness_time.append(temp_curr - unscheduled_tasks[0][3])
            else:
                need_time = unscheduled_tasks[0][1] - temp_curr
                # 尝试从后面找时间填充它
                while need_time > 0:
                    no_change = 0
                    for j in unscheduled_tasks[1:]:
                        # 找到可以填充的工单
                        if j[1] <= temp_curr:
                            if j[2] > need_time:  # compute part of min release time of task
                                temp_curr += need_time
                                for t in range(len(edd_tasks)):
                                    if edd_tasks[t][0] == j[0]:
                                        edd_tasks[t][2] -= need_time
                                need_time = 0
                            else:  # compute whole of min release time of task
                                temp_seq.append(j[0])
                                temp_curr += j[2]
                                lateness_time.append(temp_curr - j[3])
                                need_time -= j[2]
                        # 找不到可以填充的工单
                        else:
                            no_change += 1
                    if no_change == len(unscheduled_tasks[1:]):
                        # 没有办法填充，只能idle
                        temp_curr += need_time
                        need_time = 0
        # global cnt
        # cnt += 1
        # print(cnt, ":", self.seq, temp_seq, temp_curr)
        lb = max(lateness_time)
        return lb  # 下界
        # self.low_bound = temp_curr


def traversal(root: TreeNode) -> TreeNode:
    all_tasks = root.tasks
    # 直接构造可行解作为，上界
    all_tasks = sorted(all_tasks, key=operator.itemgetter(3))  # EDD sorted
    feasible_node = copy.deepcopy(root)
    seq = [t[0] for t in all_tasks]
    feasible_node.set_seq(seq)
    global upper_bound
    upper_bound = feasible_node.get_obj_val()
    print("feasible solution(upper bound):", upper_bound)

    def dfs(curr_node):
        curr_node.compute()
        if len(curr_node.remain_tasks) == 0:
            # 产生可行解
            print(
                f"feasible solution:{curr_node.get_obj_val()}, LB:{curr_node.compute()}, UB:{upper_bound},seq:{curr_node.seq}"
            )
            return
        tasks = [t for t in curr_node.tasks if t[0] not in curr_node.seq]
        for t in tasks:
            # child_task = [j for j in tasks if j[0] != t[0]]
            child_seq = curr_node.seq + [t[0]]
            child_curr = max(curr_node.curr, t[1]) + t[2]
            child_node = TreeNode(all_tasks, child_seq, child_curr)
            curr_node.add_child(child_node)
            print(
                f"obj value:{curr_node.get_obj_val()}, LB:{curr_node.compute()}, UB:{upper_bound},seq:{curr_node.seq}"
            )
            dfs(child_node)

    dfs(root)
    return root


class Machine:
    def __init__(self, i, r, p, d):
        self.i = i  # id
        # self.r = r  # release time list
        # self.p = p  # process time list
        # self.d = d  # due date list
        self.s = []  # solution
        assert len(r) == len(p) == len(d), "data length error"
        self.tasks = []
        for i in range(len(r)):
            self.tasks.append([i, r[i], p[i], d[i]])

    def output(self):
        print("{:<15}{:<15}{:<15}{:<15}".format("job id", "release time", "process time", "due date"))  # 左对齐
        for i in self.tasks:
            print("{:<15}{:<15}{:<15}{:<15}".format(i[0], i[1], i[2], i[3]))

    def solve(self):
        self.tasks = sorted(self.tasks, key=operator.itemgetter(3))  # EDD Rule
        root = TreeNode([], [])
        traversal(root)


def singleMachinePermutation(machine):
    # 1 r_j L_max
    # direct permutation
    lateness = {}
    tasks = machine.tasks
    tasks_id = [i[0] for i in tasks]
    tasks_dict = dict()
    for seq in permutations(tasks_id):
        release = [tasks_dict[j][1] for j in seq]
        due = [tasks_dict[j][3] for j in seq]
        finish = [0] * len(release)
        for i, j in enumerate(seq):
            finish[i] = max(finish[i - 1], release[i]) + tasks_dict[j][2]
        late = max([f - d for d, f in zip(due, finish)])
        lateness[seq] = late
    node_seq, late = min(lateness.items(), key=lambda x: x[1])
    return late, node_seq


def deep_first_search():
    m = Machine("machine1", [0, 1, 3, 5], [4, 2, 6, 5], [8, 12, 11, 10])
    m.output()
    root = TreeNode(m.tasks, [])
    traversal(root)
    print("low bound:")
    print("seq of low bound:", root.seq)


def EDD_rule():
    m = Machine("machine1", [0, 1, 3, 5], [4, 2, 6, 5], [8, 12, 11, 10])
    m.output()
    root = TreeNode(m.tasks, [])
    root.compute()
    print("low bound:")
    print("seq of low bound:", root.seq)
    assert root.low_bound == 17

    m = Machine("machine2", [5, 2, 1, 10], [4, 2, 6, 5], [8, 12, 11, 10])
    m.output()
    root = TreeNode(m.tasks, [])
    root.compute()
    print("low bound:", root.low_bound)
    print("seq of low bound:", root.seq)
    assert root.low_bound == 18

    m = Machine("machine2", [5, 3, 1, 5], [1, 3, 5, 5], [10, 2, 1, 10])
    m.output()
    root = TreeNode(m.tasks, [])
    root.compute()
    print("low bound:", root.low_bound)
    print("seq of low bound:", root.seq)
    assert root.low_bound == 15

    m = Machine("machine2", [30, 11, 10, 2, 5], [23, 11, 3, 5, 5], [3, 10, 2, 1, 10])
    m.output()
    root = TreeNode(m.tasks, [])
    root.compute()
    print("low bound:", root.low_bound)
    print("seq of low bound:", root.seq)
    assert root.low_bound == 53


if __name__ == "__main__":
    deep_first_search()
