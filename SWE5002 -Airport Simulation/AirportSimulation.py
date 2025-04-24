import random
import time

"""defines a flight object with an id and request type"""
class Flight:
    def __init__(self, flight_id, request_type):
        self.flight_id = flight_id
        self.request_type = request_type

"""handles landings and takeoffs using seperate queues and processes them"""
class Airport:
    def __init__(self):
        self.landings = [] #stores flights for landings in lists
        self.emergency_landings = [] #stores flights for emergency landings in lists
        self.takeoffs = [] #stores flights for takeoffs in lists
        self.log = [] #collects strings of messages to later write to file
        
    '''call this function to avoid repeating print()'''
    def log_message(self, message: str) -> None:
        print(message) #prints message in terminal
        self.log.append(message) #stores the message in self.log (for saving to a file later)

    '''receives a flight request and places it in the appropriate queue'''
    def flight_requests(self, flight_id, request_type):
        if request_type == "takeoff":
            self.takeoffs.append(Flight(flight_id, request_type)) #adds to takeoff queue
            self.log_message(f"Flight {flight_id} requests takeoff")
        elif request_type == "landing":
            self.landings.append(Flight(flight_id, request_type)) #adds to landing queue
            self.log_message(f"Flight {flight_id} requests landing")
        elif request_type == "emergency landing":
            self.emergency_landings.append(Flight(flight_id, request_type)) #adds to emergency queue
            self.log_message(f"Flight {flight_id} requests emergency landing")

    def process_landings(self):
        while self.emergency_landings: #first handles emergency landings
            flight = self.emergency_landings.pop(0) #removes flights from each list in FIFO order
            self.log_message(f"CONTROL: {flight.flight_id} land") #logs message
            time.sleep(1) #1 second delay for control time simulation
        while self.landings: #then handles normal landings
            flight = self.landings.pop(0) 
            self.log_message(f"CONTROL: {flight.flight_id} land")
            time.sleep(1)

    def process_takeoffs(self):
        if not self.emergency_landings and not self.landings: #only allows takeoffs if no landings are pending
            while self.takeoffs:
                flight = self.takeoffs.pop(0) #processes each takeoff request
                self.log_message(f"CONTROL: {flight.flight_id} takeoff") #logs message
                time.sleep(1) #adds delay

    def generate_flight_id(self):
        id = random.randrange(1, 10 ** 3) #generates a 3-digit flight ID
        flight_id = '{:03}'.format(id) #uses formatting to pad with zeros (e.g. 002)
        flight_id = str(id).zfill(3) 
        return str(flight_id) #returns the flight ID as a string

    '''Main simulation driver'''
    def run(self, iterations=10):
        for _ in range(iterations): #loop to generate a set number of flight requests
            time.sleep(1) 
            flight_id = self.generate_flight_id() #generates unique 3-digit flight ID
            request_type = random.choices(
                ["takeoff", "landing", "emergency landing"], #possible flight request types
                weights=[0.4, 0.4, 0.2] #probabilities for each type
            )[0] #selects the actual request type
            self.flight_requests(flight_id, request_type) #adds flight to appropriate queue
            
            #shows queue summary during simulation
            self.log_message(
                f"[Queue Status] Emergency: {len(self.emergency_landings)} | Landings: {len(self.landings)} | Takeoffs: {len(self.takeoffs)}"
            )

        self.log_message("\nCONTROL: Processing flights\n")
        self.process_landings() #handles landings first
        self.process_takeoffs() #then takeoffs

        #writes simulation log to control_log.txt
        with open("control_log.txt", "w") as f: 
            for entry in self.log:
                f.write(entry + "\n")

#starts simulation
if __name__ == "__main__":
    sim = Airport() 
    sim.run()