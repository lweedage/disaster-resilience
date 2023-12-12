# disaster-resilience

This repository shows the code for investigating the resilience of the Dutch cellular network.

## Data collecting + processing

We use the database of the Antenneregister, which gives all BSs of the Netherlands. The script `collect_antennas.py` collects these antenna's (subdivided per generation (GSM/UMTS/LTE/NR)), and join_antennas.py then combines these different json files into one (`antennas.json`).
However, this antenneregister does not show the MNO of each BS. We match this based to the BS based on the frequency they operate on, based on the [frequency overview on antennekaart](https://antennekaart.nl/page/frequencies).

Moreover, we use the zip code/square statistics data from Statistics Netherlands to find the user density and urbanity per zip code/500m x 500m square. We collect and refine this data in `get_population_data.py` or `get_population_data_zip_codes.py`, to add the scenario (UMa/RMA, based on urbanity).

## Objects

We define three classes of objects: `BaseStation`, `UE` and `Params`. The first two collect all data about a BS and a user and the last one combines all data together with all necessary information for the simulations.  

## Simulating

The simulations are done via running `main.py`. First, we initialize all parameters in a class, and then fill this object with a list of all BSs and users + properties. This initialization has a lot of input parameters to specify different scenario's with/without failure, and the `buffer_size`, which is the buffer around a region we also take into account to mitigate border effects. `capacity_distribution` is not important for this simulation, but can be used in `main_SNR.py` to investigate the capacity at every point in a region instead of the S(I)NR. The real simulation is done in `models.find_links(params)` (line 65), which outputs the important metrics such as FDP/FSP/SNR/SINR/capacity.


## Functions/models
`util.py`, `models.py` and `model_3GPP.py` are used in the simulations. `util.py` consists of useful functions and some fixed parameters, and the other two scripts contain all functions that are necessary to calculate all metrics and decide which user to connect to which BS.

## Other scripts
There are some other scripts in the repository that are used to calculate the S(I)NR at every location in a certain region (`main_SNR.py`), calculate the impact of a single BS failure (`main_BSfailure.py`) or plot some other stuff.

## Interface
On www.lotteweedage.nl/interface, you can find the visualization of our simulator.
