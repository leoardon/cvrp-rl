import matplotlib.pyplot as plt
import argparse
import torch
import cv2
import io
import os
import numpy as np
from utils.data_utils import load_dataset, check_extension
from parse_data import parse_file
import imageio
from utils import load_problem


def _plot_tour(city_tour, coordinates, dpi = 600, show = True):
    
    if not show: 
        plt.ioff()
    
    fig = plt.figure(figsize=(8,6))
  
    index = tour.view(-1, 1).repeat(1,2).long()

    xy = torch.gather(coordinates, 0, index)
    plt.axis([-0.05, 1.05]*2)
    plt.plot(xy[:,0], xy[:,1], color = 'black', zorder = 1)

    g1 = plt.scatter(xy[:,0], xy[:,1], marker = 'H', s = 25, c = 'blue', zorder = 2)
    g2 = plt.scatter(xy[0,0], xy[0,1], marker = 'H', s = 25, c = 'red', zorder = 2)
    handle = [g1, g2]
    plt.legend(handle, ['node', 'depot'])
    
    if not show:
        buf = io.BytesIO()
        plt.savefig(buf, dpi=dpi)
        plt.close(fig)
        buf.seek(0)
        img_arr = np.frombuffer(buf.getvalue(), dtype=np.uint8)
        buf.close()
        img = cv2.imdecode(img_arr, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    else:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", help="The path to the results of the evaluation")
    parser.add_argument("--problem", help="The path to the problem config")
    parser.add_argument("--dataset", help="The path to the dataset")
    parser.add_argument("--name", help="The name of the problem")

    opts = parser.parse_args()

    # results_path = "/home/ubuntu/dev/attention-learn-to-route/results/cvrp/CMT13/CMT13-cvrp_120_20210602T110249_epoch-30-sample1000-t1-0-1.pkl"
    # results_path = "/home/ubuntu/dev/attention-learn-to-route/results/cvrp/X-n294-k50/X-n294-k50-cvrp_293_20210608T071841_epoch-29-bs5000-t1-0-1.pkl"
    results = load_dataset(check_extension(opts.results))
    # problem_config = parse_file("/home/ubuntu/dev/cvrplib/Christofides, Mingozzi and Toth (1979)/CMT13.vrp")
    # dataset = load_problem("cvrp").make_dataset(filename="/home/ubuntu/dev/attention-learn-to-route/data/cvrp/CMT13.pkl")
    problem_config = parse_file(opts.problem) # "/home/ubuntu/dev/cvrplib/Uchoa et al. (2014) [X]/X-n294-k50.vrp")
    dataset = load_problem("cvrp").make_dataset(filename=opts.dataset) # "/home/ubuntu/dev/attention-learn-to-route/data/cvrp/X-n294-k50.pkl")

    tour = torch.tensor([0] + results[0][0][1])
    coordinates = torch.cat([dataset[0]["depot"].view(1, 2), dataset[0]["loc"]])
    print(tour)

    with imageio.get_writer(f'./results/cvrp/{opts.name}/result.gif', mode='I') as writer:
        img = _plot_tour(tour, coordinates, show=False)
        writer.append_data(img)