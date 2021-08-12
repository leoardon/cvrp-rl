import argparse
import os
import numpy as np
from utils.data_utils import save_dataset

def parse_file(path):
    data = {}
    with open(path) as f:
        aggregate_section = ""
        values = []
        for l in f.readlines():
            if ":" in l:
                key, val = l.split(":", 1)
                data[key.strip().lower()] = val.strip()
            elif l.strip() == "NODE_COORD_SECTION":
                if values:
                    data[aggregate_section.lower()] = values
                aggregate_section = "NODE_COORD_SECTION"
                values = []
            elif l.strip() == "DEMAND_SECTION":
                if values:
                    data[aggregate_section.lower()] = values
                aggregate_section = "DEMAND_SECTION"
                values = []
            elif l.strip() == "DEPOT_SECTION":
                if values:
                    data[aggregate_section.lower()] = values
                aggregate_section = "DEPOT_SECTION"
                values = []
            elif l.strip() == "EOF":
                if values:
                    data[aggregate_section.lower()] = values
            elif aggregate_section == "NODE_COORD_SECTION":
                vs = []
                for i, v in enumerate(l.strip().split()):
                    if i == 0:
                        vs.append(int(v))
                    else:
                        vs.append(float(v))
                values.append(tuple(vs))
            elif aggregate_section in ("DEMAND_SECTION", "DEPOT_SECTION"):
                values.append(tuple(int(v) for v in l.strip().split()))

    data["node_coord_section"] = {v[0]: list(v[1:]) for v in data["node_coord_section"]}
    data["demand_section"] = {v[0]: v[1] for v in data["demand_section"]}
    data["capacity"] = int(data["capacity"])

    return data

def _process_data(parsed_data):
    depot_node = parsed_data["depot_section"][0][0]
    capacity = parsed_data["capacity"]

    coordinates = np.array(list(parsed_data["node_coord_section"].values()))
    v_min, v_max = coordinates.min(), coordinates.max()
    coordinates = (coordinates - v_min) / (v_max - v_min)
    coordinates = dict(zip(parsed_data["node_coord_section"].keys(), coordinates.tolist()))

    data = [
        coordinates[depot_node],
        [v for k, v in coordinates.items() if k != depot_node],
        [v for k, v in parsed_data["demand_section"].items() if k != depot_node],
        capacity
    ]

    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", help="Filename of the problem file to transform to a dataset.")
    parser.add_argument("--data_dir", default='data', help="Create datasets in data_dir/problem (default 'data')")
    parser.add_argument("--problem", default='cvrp', help="Problem type (default 'cvrp')")
    parser.add_argument("--name", type=str, default=None, help="Name to identify dataset")
    parser.add_argument("--instances", type=int, default=1, help="The number of instances in the dataset")
    parser.add_argument("-f", action='store_true', help="Set true to overwrite")

    opts = parser.parse_args()

    assert os.path.isfile(opts.filename), \
        f"File {opts.filename} doesn't exist."

    parsed_data = parse_file(opts.filename)
    data = _process_data(parsed_data)
    dataset = [data] * opts.instances

    datadir = os.path.join(opts.data_dir, opts.problem)
    os.makedirs(datadir, exist_ok=True)

    name = opts.name or opts.filename.rsplit("/", 1)[-1].replace(".vrp", "")
    output_filename = os.path.join(datadir, f"{name}.pkl")

    assert opts.f or not os.path.isfile(output_filename), \
        "File already exists! Try running with -f option to overwrite."

    save_dataset(dataset, output_filename)