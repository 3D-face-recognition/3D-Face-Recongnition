from src.pipe_and_sink.interface_pipe_and_sink import IPipeAndSink

class PreprocessingPipe(IPipeAndSink):
    def __init__(self, filter):
        self.next_pipe = None
        self.filter = filter

    def set_next(self, pipe_and_sink):
        self.next_pipe = pipe_and_sink

    def put(self, unit_of_work):
        self.filter.filtering(unit_of_work)
        self.next_pipe.put(self.filter.get_unit_of_work())