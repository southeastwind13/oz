import pickle


class PickleHelper():
    '''
    1. We use pickle to save state of the object. 
    2. Pickle depends deeply on the structure of your code, modules and classes. 
       You can only safely unpickle objects that were stored with the same code 
       structure.
    3. Main purpose of pickle remains to be short term storage of objects so 
       they could be transferred between parts of the system that you maintain, 
       for example, for interprocess communication or sending tasks to worker 
       farm run by celery. And pickle was never intended for long term storage 
       of the system state like you are implying.

    Example:
    p_load:TestPickle = PickleHelper.load_pickle(path)
    p_load.greet()
    '''

    @staticmethod
    def save_pickle(object, file_path:str):
        with open(file_path, 'wb') as file:
            pickle.dump(object, file)

    @staticmethod
    def load_pickle(file_path:str):
        with open(file_path, 'rb') as file:
            object = pickle.load(file)
            return object


class TestPickle():
    def __init__(self, name) -> None:
        self.name = name

    def greet(self):
        print(f"hello {self.name}")