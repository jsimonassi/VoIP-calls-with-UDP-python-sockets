class Cronometer:
    """
    Classe que gerência o cronômetro durante uma chamada.
    """
    def __init__(self, label):
        self.current_time = 0
        self.is_counting = False
        self.label = label

    def start_counter(self):
        self.is_counting = True
        self.get_timer()

    def stop_counter(self):
        self.is_counting = False
        self.current_time = 0

    def get_timer(self):
        self.current_time += 1
        self.label['text'] = self.get_formatted_time()
        if self.is_counting:
            self.label.after(1000, self.get_timer)

    def get_formatted_time(self):
        hour = self.current_time // 3600
        over = self.current_time % 3600
        minutes = over // 60
        seconds = over % 60
        return str(hour) + ":" + str(minutes) + ":" + str(seconds)
