# Hosting_Capacity_and_Power_Losses
1.	The main script (DATA.py) orchestrates the overall execution of the optimization process and should be the only file you run directly. The other files contain functions for specific tasks that are invoked by the main script as needed. You can modify the parameters in this file (DATA.py) as you need.

2.	The "Outcomes" folder contains subfolders where the results will be stored.

3.	The "Modified_IEEE123nodetestSystem" folder contains a sample distribution system.

4.	Below is an example outlining the steps to set up the main script (DATA.py):
4.1.	In “line 51: Seed_Range = [0, 1]” specifies the range of seed numbers to run, from the lower to the upper limit. In this example, the algorithm will run with two seeds: seed=0 and seed=1. If we had set Seed_Range = [4, 6], the algorithm would run three times with seeds 4, 5, and 6.

4.2.	"From lines 63 to 67, you should select the strategy you want to simulate. To choose a strategy, uncomment the line corresponding to your desired strategy by removing the “#” symbol at the beginning of that line. Keep the “#” symbols on all other lines. In the given example, line 67 is the only one without a “#” symbol, so the simulation would include the Combination of all Strategies.
For reference: 
line 63 belongs to “Network reconfiguration Strategy”
line 64 belongs to “OLTC Switching Strategy”
line 65 belongs to “Capacitor Switching Strategy”
line 66 belongs to “Volt-VAR Control Settings Strategy”
line 67 belongs to “Combination of all Strategies”

4.3.	In “line 74: individuos = 6” you should specify the number of individuals in the population needed to run the Non-Dominated Sorting Genetic Algorithm (NSGA-II). Always select an even number. In this example, the population consists of 6 individuals.

4.4.	In “line 75: iteraciones = 2” you should specify the number of iterations for the NSGA-II. In this example, the algorithm will perform 2 iterations.

4.5.	In “line 82: objeto = DSS(r"C:\Users\...\IEEE123Master.dss")”, you should replace the path "C:\Users\...\IEEE123Master.dss" with the path to the OpenDSS file in your computer. In the given example, the file is a modified version of the IEEE 123 bus system, named “IEEE123Master.dss”.

4.6.	In “line 89: Results_Folder = r"C:\Users\...\Outcomes"”, you should replace the path " C:\Users\...\Outcomes" with the path to the folder on your computer where you want the results to be stored. Note that the results will be saved as Excel files."
