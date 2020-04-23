def func1(a):
    print("func1", a)
def func2(a):
    print("func2",a)
def func3(a):
    print("func3",a)
def func4(a):
    print("func4",a)


def call_func(n, a):
    # if n== 1:
    #     func1()
    # elif n == 2:
    #     func2()
    # elif n == 3:
    #     func3()
    # elif n == 4:
    #     func4()
    branch_table = {
        1: func1,
        2: func2,
        3: func3,
        4: func4
    }
    # bt[n]()
    f = branch_table[n]
    f(a)
call_func(1, "hello")
call_func(2, " world")
call_func(3, "ha")
call_func(4, "ha")