class Message:
    def __init__(self, client_name, message, time):
        #self.client_id = client_id
        self.client_name = client_name
        self.message = message
        self.time = time

    def get_client_name(self):
        return self.client_name

    def get_message(self):
        return self.message

    def get_time(self):
        return self.time