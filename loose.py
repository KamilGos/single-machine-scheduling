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
import operator
import sys
from itertools import permutations
from typing import List


class TreeNode:
    def __init__(self, tasks, seq, curr=0, low_bound=sys.maxsize):
        self.tasks = tasks  # 所有的任务
        self.seq = seq  # 已经确定的路径
        self.remain_tasks = [t for t in tasks if t[0] not in seq]  # 未完成的任务
        self.seq_tasks = []  # 已经完成的任务
        for i in seq:
            for j in tasks:
                if j[0] == i:
                    self.seq_tasks.append(j)
        self.curr = curr  # 当前运行到的时间
        self.low_bound = low_bound  # 可中断情况下的下界 1 | r_{j},prmp | min(L_{max})
        self.obj_val = sys.maxsize  # search the min of Lmax
        self.child = []  # 所有的子节点

    def add_child(self, node):
        self.child.append(node)
        return self

    def get_obj_val(self):
        # 计算已经排程部分的目标值
        if len(self.seq) == 0:
            return sys.maxsize
        release = []
        process = []
        due = []
        for j in self.seq_tasks:
            release.append(j[1])
            process.append(j[2])
            due.append(j[3])
        finish = [0] * len(release)
        if len(self.seq) == 1:
            late = release[0] + process[0] - due[0]
        else:
            for i in range(len(self.seq)):
                finish[i] = max(finish[i - 1], release[i]) + process[i]
            late = max([f - d for d, f in zip(due, finish)])
        late = max(0, late)
        return late

    def compute(self):
        # 计算未排程部分
        temp_seq = self.seq
        temp_curr = self.curr
        task_num = len(self.remain_tasks)  # 剩余task数量
        edd_tasks = sorted(self.remain_tasks, key=operator.itemgetter(3))  # EDD rule

        while len(temp_seq) < task_num:
            unscheduled_tasks = edd_tasks  # unscheduled task
            if unscheduled_tasks[0][1] <= temp_curr:  # earliest due date of task's release time is achieve
                # directly compute the first task
                temp_seq.append(unscheduled_tasks[0][0])
                temp_curr = max(unscheduled_tasks[0][1], temp_curr)
                temp_curr += unscheduled_tasks[0][2]
            else:
                # compute the part/whole min release time of task
                min_release_task1 = sorted(unscheduled_tasks, key=operator.itemgetter(1))[0]
                ix = unscheduled_tasks.index(min_release_task1)
                temp_curr = max(temp_curr, min_release_task1[1])  # 结合release time获取此时的开始时间
                if ix == 0:
                    # EDD第一单就是release time最小，直接加工
                    temp_seq.append(min_release_task1[0])
                    temp_curr += min_release_task1[2]
                else:
                    # 比最小release time的due date还小的里面，找到最小release time
                    min_release_task2 = sorted(unscheduled_tasks[:ix], key=operator.itemgetter(1))[0]
                    available_process_time = (
                        min_release_task2[1] - min_release_task1[1]
                    )  # 两个release time的差即为最小release time task需要加工的时间
                    if available_process_time < min_release_task1[2]:
                        # compute part of min release time of task
                        temp_curr += available_process_time
                        min_release_task1[2] -= available_process_time  # 该task消耗部分加工时间
                    else:
                        # compute whole of min release time of task
                        temp_seq.append(min_release_task1[0])
                        temp_curr += min_release_task1[2]
        print(self.seq, temp_seq, temp_curr)
        # self.low_bound = temp_curr


def traversal(root: TreeNode) -> TreeNode:
    all_tasks = root.tasks

    def dfs(curr_node):
        curr_node.compute()
        if len(curr_node.remain_tasks) == 0:
            print(curr_node.get_obj_val())
            return
        tasks = [t for t in curr_node.tasks if t[0] not in curr_node.seq]
        for t in tasks:
            # child_task = [j for j in tasks if j[0] != t[0]]
            child_seq = curr_node.seq + [t[0]]
            child_curr = max(curr_node.curr, t[1]) + t[2]
            child_node = TreeNode(all_tasks, child_seq, child_curr)
            curr_node.add_child(child_node)
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
    print("low bound:", root.low_bound)
    print("seq of low bound:", root.seq)


def EDD_rule():
    m = Machine("machine1", [0, 1, 3, 5], [4, 2, 6, 5], [8, 12, 11, 10])
    m.output()
    root = TreeNode(m.tasks, [])
    root.compute()
    print("low bound:", root.low_bound)
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
