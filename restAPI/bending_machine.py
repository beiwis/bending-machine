from time import sleep, time
import logging as log
import threading

class machine():
    def __init__(self, sps: float = 1, csv: bool = False, print: bool = True) -> None: 
        self.mode = 0 #0 for None, 1 for Automatic, 2 for Manual
        self.state = 0 #0 for Init, 1 for Waiting, 2 for Running, 3 for Error
        self.csv = csv
        self.print = print
        self.measures = {'Encoder':0, 'STG':0, 'Force':0}
        self.connect_ok = False
        self.measure_ok = False
        self.done = False
        if sps != 0:
            self.sampling = True
            self.period = 1/sps
            if (self.print or self.csv):
                threading.Thread(target = sample(self)) # We start the sampling thread
        else: self.sampling = False #FIXME: i think this is not needed
        # maybe start the control thread here,,,,

def control_thread(self):
     pass

def sample(self):
    t_ini = time()
    if self.state == 2: #So that we only take measurements when the machine is running a test    
        measures = self.get_measurements()
        if self.print: log.info(measures) #TODO: it might be necessary to parse the dictionary into string or something
        if self.csv: self.measures.update(measures)  
    sleep(self.period - time() + t_ini)