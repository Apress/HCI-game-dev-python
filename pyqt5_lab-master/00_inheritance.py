class A:                           # Base class
    def __init__(self):            # With constructor
        print('initializing A.')

    def m1(self):
        print('A.m1()')

class B(A):               # Inherit from A.
    def m1(self):         # Overide m1.
        print(' B.m1()')

class C(A):                     # Inherit from A
    def __init__(self):         # Override constructor.
        print('initializing C.')

class D(A):                     # Make sure to call super constructor.
    def __init__(self):
        A.__init__(self)
        print('initializing D.')

#
# Laboratory exercises:
#
# 1. Run this script in an IPython shell. Instantiate one of each
# defined class and observe the messages printed.
#
#
