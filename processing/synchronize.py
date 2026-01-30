class Synchronizer:
    def __init__(self, events, transcript_segments):
        self.events = sorted(events, key=lambda x: x['timestamp'])
        self.segments = sorted(transcript_segments, key=lambda x: x['start'])

    def sync(self):
        """
        Merges events and transcripts.
        Returns a list of steps. Each step has:
        - event: The browser event
        - transcript: Combined text of audio segments relevant to this step
        """
        if not self.events:
            return []

        # Initialize steps with events
        steps = []
        for i, event in enumerate(self.events):
            step = {
                "event": event,
                "transcript": ""
            }
            steps.append(step)

        # Assign segments to the appropriate step
        # Heuristic: Assign segment to the event that happened immediately before the segment start,
        # or if the segment started before the first event, assign to the first event.
        # Actually, a better heuristic might be:
        # The "Step 1" covers time from Event 1 timestamp until Event 2 timestamp.
        
        # Let's define the time window for Step[i] as [Event[i].timestamp, Event[i+1].timestamp)
        # For the last event, it's [Event[i].timestamp, end_of_time)
        
        # However, users often speak *while* or *before* clicking.
        # Let's try: Assign segment to the closest event in time?
        # Or: Use the "Time Window" approach. All audio *after* Event A and *before* Event B belongs to Event A.
        # But what about audio *before* Event A? Maybe belong to "Introduction"? 
        # For simplicity, let's merge "orphan" audio to the *next* event if it's start, or *previous* event otherwise.
        
        # Revised Heuristic:
        # Create a timeline.
        # Step i corresponds to Event i.
        # Audio segments are assigned to Step i if segment.start >= Event[i].timestamp and segment.start < Event[i+1].timestamp.
        # Audio before first event is assigned to first event.
        
        for segment in self.segments:
            seg_start = segment['start']
            
            # Find the event that started before this segment
            # We want the index i such that events[i].timestamp <= seg_start
            
            assigned_index = -1
            
            # Start from the end to find the last event that occurred before segment start
            for i in range(len(self.events) - 1, -1, -1):
                # Adjust event timestamp to be relative to start of recording if needed. 
                # Assuming both are unix timestamps or both are relative.
                # In main.py we will normalize timestamps.
                if self.events[i]['timestamp'] <= seg_start:
                    assigned_index = i
                    break
            
            if assigned_index == -1:
                # Segment started before any event. Assign to first event.
                assigned_index = 0
                
            steps[assigned_index]['transcript'] += segment['text'] + " "

        return steps
