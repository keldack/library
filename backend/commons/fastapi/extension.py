
def test_decorateur(x):

    print(x)

    def inner_function(func):

        def wrapper(*args, **kwargs):

            print ("before call")
            
            print("args", args)
            print("kwargs", kwargs)
            result = func(*args, **kwargs)

            print ("after call")

            return result

        return wrapper
    
    return inner_function

