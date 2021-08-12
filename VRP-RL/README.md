
# Reinforcement Learning for Solving the Vehicle Routing Problem

We use Reinforcement for solving Travelling Salesman Problem (TSP) and Vehicle Routing Problem (VRP).


## Paper
Implementation of our paper: [Reinforcement Learning for Solving the Vehicle Routing Problem](https://arxiv.org/abs/1802.04240v2). 

## Dependencies


* Numpy
* [tensorflow](https://www.tensorflow.org/)>=1.2
* tqdm

## How to Run
### Train
By default, the code is running in the training mode on a single gpu. For running the code, one can use the following command:
```bash
python main.py --task=vrp10
```

It is possible to add other config parameters like:
```bash
python main.py --task=vrp10 --gpu=0 --n_glimpses=1 --use_tanh=False 
```
There is a full list of all configs in the ``config.py`` file. Also, task specific parameters are available in ``task_specific_params.py``
### Inference
For running the trained model for inference, it is possible to turn off the training mode. For this, you need to specify the directory of the trained model, otherwise random model will be used for decoding:
```bash
python main.py --task=vrp10 --is_train=False --model_dir=./path_to_your_saved_checkpoint
```
The default inference is run in batch mode, meaning that all testing instances are fed simultanously. It is also possible to do inference in single mode, which means that we decode instances one-by-one. The latter case is used for reporting the runtimes and it will display detailed reports. For running the inference with single mode, you can try:
```bash
python main.py --task=vrp10 --is_train=False --infer_type=single --model_dir=./path_to_your_saved_checkpoint
```
### Logs
All logs are stored in ``result.txt`` file stored in ``./logs/task_date_time`` directory.
## Sample CVRP solution

![enter image description here](https://lh3.googleusercontent.com/eUh69ZQsIV4SIE6RjwasAEkdw2VZaTmaeR8Fqk33di70-BGU62fvmcp6HLeGLE61lJDS7jLMpFf2 "Sample VRP")

## Acknowledgements
Thanks to [pemami4911/neural-combinatorial-rl-pytorch](https://github.com/pemami4911/neural-combinatorial-rl-pytorch) for getting the idea of restructuring the code.


###

python main.py --task=vrp50 --batch_size 256 --random_seed 1 --disable_tqdm False --gpu 1,2,3
python main.py --task=vrp75 --batch_size 256 --random_seed 1 --disable_tqdm False --gpu 1,2,3
python main.py --task=vrp100 --batch_size 256 --random_seed 1 --disable_tqdm False --gpu 1,2,3
python main.py --task=vrp120 --batch_size 256 --random_seed 1 --disable_tqdm False --gpu 1,2,3

LEO_UPDATE=1 python main.py --task=vrp50 --is_train "False" --test_size 1 --infer_type single --load_path "/home/ubuntu/dev/VRP-RL/logs/vrp50-2021-08-09_10-38-25/model/" --log_dir logs/eval/
python main.py --task=vrp75 --is_train "False" --test_size 1 --infer_type single --load_path "/home/ubuntu/dev/VRP-RL/logs/vrp75-2021-08-04_10-49-26/model/" --log_dir logs/eval/
python main.py --task=vrp100 --is_train "False" --test_size 1 --infer_type single --load_path "/home/ubuntu/dev/VRP-RL/logs/vrp100-2021-08-04_10-49-31/model/" --log_dir logs/eval/
python main.py --task=vrp120 --is_train "False" --test_size 1 --infer_type single --load_path "/home/ubuntu/dev/VRP-RL/logs/vrp120-2021-08-04_10-49-36/model/" --log_dir logs/eval/


50  -> 30000
75  -> 50000
100 -> 30000
120 -> 20000