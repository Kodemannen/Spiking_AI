import matplotlib.pyplot as plt
import numpy as np
import nest.topology as topp
import nest
import seaborn as sns
import sys
# np.random.seed(eval(sys.argv[1]))
np.random.seed(10)
sns.set()


def Plot_connectome(population, positions, connections, ax):

    # Plotting connections:
    pop_size = len(population)
    pop_indices = np.arange(pop_size)
    pop_gids = np.arange(population[0], population[-1]+1)

    n_connections = len(connections)


    for i in range(n_connections):

        synapse = connections[i] # Synapse number i in the network. (source-gid, target-gid, target-thread, synapse-id, port)
        gid_sender = synapse[0]
        gid_receiver = synapse[1]

        index_sender = np.where()
        index_receiver

        sender_position = positions[synapse[0]-1]
        receiver_position = positions[synapse[1]-1]

        xs = [sender_position[0], receiver_position[0]]
        ys = [sender_position[1], receiver_position[1]]

        ax.plot(xs,ys, linewidth=0.1, alpha=0.2, color="grey")

    # Plotting neurons:
    ax.scatter(*zip(*positions), alpha=.7, color="grey")

    return None



def Create_population_positions(N, distribution):

    if distribution.lower()=="uniform":
        positions = np.random.uniform(low=0, high=1, size=(N, 2)) # the i'th list [j,k] means neuron i had position (j,k)
    elif distribution.lower()=="gaussian":
        positions = np.random.normal(loc=0, scale=1, size=(N, 2)) # the i'th list [j,k] means neuron i had position (j,k)
    elif distribution.lower()=="column":
        positions = np.zeros(shape=(N,2))
        positions[:,1] = np.linspace(-1,1,N)

    return positions



if __name__ == "__main__":

      ####################
     # Hyperparameters: #
    ####################
    simtime = 100.0 # ms
    N_main = 100 # number of neurons
    N_sensory = 20
    plot = True
    epsilon = 0.1
    indegree = 10
    sensory_rate = 10.0 # Hz?

    nest.SetKernelStatus({"overwrite_files": True})


      ############################################
     # Creating network and experimental tools: #
    ############################################
    # Neuron populations:
    population_main    = nest.Create("iaf_psc_delta", N_main)
    population_sensory = nest.Create("parrot_neuron", N_sensory)
    poisson_generator  = nest.Create("poisson_generator")

    spike_detector = nest.Create("spike_detector", params={"to_file":True,"label":"spike_times.txt"})
    # Spike_detector is a device needed for gathering the spikes of the particular neurons we are interested in



      ###########################
     # Setting up connections: #
    ###########################
    nest.Connect(population_sensory, spike_detector)
    nest.Connect(population_main, population_main, conn_spec={"rule": "fixed_indegree", "indegree": indegree})
    nest.Connect(poisson_generator, population_sensory)

    # Fetching connectons for plotting:
    connections_main    = nest.GetConnections(target=population_main)
    connections_sensory = nest.GetConnections(target=population_sensory)
    # connections_..[i] is connection number i in the list of connections in the network? Can be given with an argument source=arg or target=arg. (source-gid, target-gid, target-thread, synapse-id, port)



      #########################
     # Setting up positions: #
    #########################
    positions_main    = Create_population_positions(N_main, distribution="gaussian")
    positions_sensory = Create_population_positions(N_sensory, distribution="column")


    nest.SetStatus(poisson_generator, {"rate": sensory_rate})


    nest.Simulate(simtime)

    events = nest.GetStatus(spike_detector)[0]["events"]
    senders = events["senders"]
    times = events["times"]
    #plt.scatter(times,senders)
    #plt.show()

    if plot==True:
        fig, ax = plt.subplots()
        Plot_connectome(population_main, positions_main, connections_main, ax)
        print("hore")
        Plot_connectome(population_sensory, positions_sensory, connections_sensory, ax)
        fig.savefig("fig.pdf")

