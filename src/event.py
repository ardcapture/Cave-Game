
class Event:

    subscribers = dict()

    def subscribe(self, event_type: str, fn):
        if not event_type in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(fn)

    def post_event(self, event_type: str, *args):
        if not event_type in self.subscribers:
            print(f"not event!")
            return
        for fn in self.subscribers[event_type]:
            print(f"event")
            return fn(*args)


eventObj = Event()
