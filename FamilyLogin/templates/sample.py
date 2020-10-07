
# x = [1,2,3,4,5]
# # for i in x:
# #     print(i)
# #iterator and iterable
# n = iter(x)
# print(n.__next__())
# print(n.__next__())
# print(n.__next__())
# print(n.__next__())
# print(n.__next__())
# print(n.__next__())

class MyNumbers:
    def __iter__(self):
        self.a = 1

    def __next__(self):
      print(self.a)
      self.a = self.a + 1

myclass = MyNumbers()
myclass.__iter__()
myclass.__next__()
myclass.__next__()
myclass.__next__()
myclass.__next__()
print(dir(MyNumbers))