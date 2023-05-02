import os
import pandas as pd
import math
import Modules.logger as logger
from Paths.paths import PATH_SPLITTER_FOLDER
from os import path
import time
from Loader.osSelector import clearScreen

def CSVsplit():

    clearScreen()

    amount = int(input("How many accounts per CSV: "))

    def to_csv_batch(src_csv, dst_dir, size=amount, index=False):
        
        # Read source csv
        df = pd.read_csv(src_csv)
        
        # Initial values
        low = 0
        high = size

        # Loop through batches
        count = 1
        for i in range(math.ceil(len(df) / size)):

            fname = dst_dir+'/Batch_' + str(i+1) + '.csv'
            df[low:high].to_csv(fname, index=index)
            
            # Update selection
            low = high
            if (high + size < len(df)):
                high = high + size
            else:
                high = len(df)

            green_color = '\033[92m' #light green
            reset_color = '\033[0m' #reset color
            red_color = '\033[91m' #red
            print(f"{green_color}[{time.strftime('%H:%M:%S', time.localtime())}] [{count}] {'Generated pair: Successfully Split CSV'} {reset_color}")
            count+=1
            
            

    to_csv_batch(path.join(PATH_SPLITTER_FOLDER, "main.csv"), PATH_SPLITTER_FOLDER)
    