from src.pipe_and_sink.interface_pipe_and_sink import IPipeAndSink
class PreprocessingSink(IPipeAndSink):
    def __init__(self):
        self.unit_of_work = None

    def set_next(self, pipe_and_sink):
        pass

    def put(self, unit_of_work):
        self.unit_of_work = unit_of_work

    def get_unit_of_work(self):
        return self.unit_of_work