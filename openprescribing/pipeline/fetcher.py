# This is just a sketch!

class Fetcher(object):
    def __init__(self, task_definition):
        pass

    def run(self):
        datestamp = self.get_most_recent_datestamp()

        if self.already_uploaded(datestamp):
            return

        if not self.already_fetched():
            self.fetch(datestamp)

        self.upload_to_storage(datestamp)
