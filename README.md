# Federated XGBoost

## Introduction

**Federated XGBoost** is a gradient boosting library for the federated setting, based off the popular [XGBoost](https://github.com/dmlc/xgboost) project. In addition to offering the same efficiency, flexibility, and portability that vanilla XGBoost provides, Federated XGBoost enables multiple parties to jointly compute a model while keeping their data on site, avoiding the need for a central data storage. 

This project is no longer actively maintained.

## Installation

1. Clone this repository and its submodules.

```
git clone --recursive https://github.com/mc2-project/federated-xgboost.git
```

2. Install Federated XGBoost dependencies.

```
sudo apt-get install cmake libmbedtls-dev
pip3 install numpy grpcio grpcio-tools
```

3. Build Federated XGBoost.

```
cd federated-xgboost
mkdir build
cd build
cmake ..
make
```

4. Install the Python package.

```
cd python-package
sudo python3 setup.py install
```

## Quickstart
This quickstart uses the tutorial located in `demo/basic`. In this tutorial, each of the two parties in the federation starts an RPC server on port 50051 to listen for the aggregator. The aggregator sends invitations to all parties to join the computation. Once all parties have accepted the invitation, training commences -- the training script `demo.py` is run.

The implementation currently requires that each party's training data be at the same location, i.e., have the same path, and that the aggregator also have training data.

1. Modify `hosts.config` to contain the IP addresses of all parties in the federation. Each line in `hosts.config` follows the following format:

```
<ip_addr>:<port>
```

For the purposes of this demo, `<port>` should be `50051`.

2. This demo uses data from the [Higgs boson](https://archive.ics.uci.edu/ml/datasets/HIGGS) dataset. The `demo/data/` directory contains 4 files of training data: `hb_train_1.csv`, `hb_train_2.csv`, `hb_train_3.csv`, and `hb_train_4.csv`. At each party, change the name of a different training data file to `hb_train.csv`.

3. Start the RPC server at each party. 

```
python3 serve.py
```

4. At the aggregator, send invitations to all parties.

```
dmlc-core/tracker/dmlc-submit --cluster rpc --num-workers 2 --host-file hosts.config  --worker-memory 4g /path/to/federated-xgboost/demo/basic/demo.py
```

Each party should receive an invitation through their console:

```
Request from aggregator [ipv4:172.31.27.60:50432] to start federated training session:
Please enter 'Y' to confirm or 'N' to reject.
Join session? [Y/N]:
```

5. Once all parties submit `Y`, training begins.


