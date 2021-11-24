import copy
import operator

def read_data_2list(filename):
    file = open(filename, "r")
    tasks_val, columns_val = file.readline().split()
    tasks_val = int(tasks_val)
    columns_val = int(columns_val)
    tasks = []
    values = []
    for val in file.read().split():
        values.append(float(val))

    for a in range(0, len(values), 3):
        tmp_tab = []
        for b in range(0,3):
            tmp_tab = tmp_tab + [values[a+b]]
        tasks.append(tmp_tab)
    print("Number of tasks: ", tasks_val)
    print("Number of columns: ", columns_val)
    print("Tasks: \n", tasks)
    file.close()
    return tasks_val, columns_val, tasks


################################################## CLASSICAL APPROACH #################################################
def Schrage(tasks):
    sigma = []   
    Ng = [] 
    Nn = copy.deepcopy(tasks)
    t = min(Nn)[0]  
    Cmax = 0

    while (Ng !=[] or Nn!=[]):
        while(Nn !=[] and min(Nn)[0] <=t):
            j = Nn.index(min(Nn))
            Ng.append(Nn[j])
            Nn.pop(j)
        if Ng == []:
            t = min(Nn)[0]
        else:
            j = Ng.index(max(Ng, key=operator.itemgetter(2)))
            tmp = Ng[j]
            Ng.pop(j)
            sigma.append(tmp)
            t = t + tmp[1]
            Cmax = max(Cmax, t+tmp[2])
    return  sigma, Cmax


################################################### SCHRAGE WITH TASKS DIVISION #######################################
def Schrage_pmtn(tasks):
    sigma = [] 
    Ng = []  
    Nn = copy.deepcopy(tasks)  
    t = 0
    Cmax = 0
    l = [0, 0, 0]

    while (Ng != [] or Nn != []):
        while (Nn != [] and min(Nn)[0] <= t):
            j = Nn.index(min(Nn))
            tmp = Nn[j]
            Ng.append(tmp)
            Nn.pop(j)
            if tmp[2] > l[2]:
                l[1] = t-tmp[0]
                t = tmp[0]
                if l[1] > 0:
                    Ng.append(l)
        if Ng == []:
             t = min(Nn)[0]
        else:
            i = Ng.index(max(Ng, key=operator.itemgetter(2)))
            j = Ng[i]
            Ng.pop(i)
            sigma.append(j)
            l = j
            t = t + j[1]
            Cmax = max(Cmax, t + j[2])
    return sigma, Cmax

## just run the code...
if __name__=="__main__":
    test_nr = 0

    while (test_nr != 5):

        print("----------------------------")
        print("Which test would you like to use?")
        print(" 1. in50 \r\n 2. in100 \r\n 3. in200 \r\n 4. FULL(sum) \r\n 5. Escape ")
        test_nr = int(input("Enter your choose: "))

        if test_nr == 1:
            tasks_val, columns_val, tasks = read_data_2list("data/schrage_in50.txt")
            print(tasks)
            sigma50, Cmax50 = Schrage(tasks)
            print("-------SCHRAGE--------")
            print("Correct result for in50 test is 1513")
            print("Your result is: ", Cmax50)
            if Cmax50 == 1513: print("CORRECT!")

            sigma50_pmtn, Cmax50_pmtn = Schrage_pmtn(tasks)
            # sigma50_pmtn, Cmax50_pmtn = schragepmtn(tasks)
            print("-----SCHRAGE_PMTN------")
            print("Correct result for in50 test is 1492")
            print("Your result is: ", Cmax50_pmtn)
            if Cmax50_pmtn == 1492: print("CORRECT!")

        elif test_nr == 2:
            tasks_val, columns_val, tasks = read_data_2list("data/schrage_in100.txt")
            sigma100, Cmax100 = Schrage(tasks)
            print("Correct result for in100 test is 3070")
            print("Your result is: ", Cmax100)
            if Cmax100 == 3070: print("CORRECT!")

            sigma100_pmtn, Cmax100_pmtn = Schrage_pmtn(tasks)
            print("-----SCHRAGE_PMTN------")
            print("Correct result for in100 test is 1492")
            print("Your result is: ", Cmax100_pmtn)
            if Cmax100_pmtn == 1492: print("CORRECT!")

        elif test_nr == 3:
            tasks_val, columns_val, tasks = read_data_2list("data/schrage_in200.txt")
            sigma200, Cmax200 = Schrage(tasks)
            print("Correct result for in200 test is 6416")
            print("Your result is: ", Cmax200)
            if Cmax200 == 6416: print("CORRECT!")

            sigma200_pmtn, Cmax200_pmtn = Schrage_pmtn(tasks)
            print("-----SCHRAGE_PMTN------")
            print("Correct result for in200 test is 6398")
            print("Your result is: ", Cmax200_pmtn)
            if Cmax200_pmtn == 6398: print("CORRECT!")

        elif test_nr == 4:
            results = []
            results_pmtn = []
            tests = ["data/schrage_in50.txt", "data/schrage_in100.txt", "data/schrage_in200.txt"]
            for test_file in tests:
                tasks_val, columns_val, tasks = read_data_2list(test_file)
                sigma, Cmax = Schrage(tasks)
                sigma_pmtn, Cmax_pmtn = Schrage_pmtn(tasks)
                results.append(Cmax)
                results_pmtn.append(Cmax_pmtn)
            print("=== Schrage === \r\n Correst result is: [1513.0, 3076.0, 6416.0]")
            print("Your result is:", results)
            print("=== Schrage Pmtn === \r\n Correst result is: [1492.0, 3070.0, 6398.0]")
            print("Your result is:", results_pmtn)