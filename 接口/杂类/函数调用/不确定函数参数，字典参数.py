# 如果我们不确定要往函数中传入多少个参数，或者我们想往函数中以列表和元组的形式传参数时，那就使要用*args；
# 如果我们不知道要往函数中传入多少个关键词参数，或者想传入字典的值作为关键词参数时，那就要使用**kwargs。
def args(*args):
    for i in args:
        print(i)

#
args([1, 2, 3, 4, 8, 7],[1,2])
# args(1)

def demo(**kwargs):
    for i in kwargs:
        print(i)
myDict = {'a':'a', 'b':'b'}
myDict2 = {'a':'a', 'b':'b'}
demo(**myDict,)
#在调用处 将字典转换为关键字
