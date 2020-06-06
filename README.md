# Federated XGBoost

## Introduction

**Federated XGBoost** is a gradient boosted library for the federated setting, based off the popular [XGBoost](https://github.com/dmlc/xgboost) project. In addition to offering the same efficiency, flexibility, and portability that vanilla XGBoost provides, Federated XGBoost enables multiple parties to jointly compute a model while keeping their data on site, avoiding the need for a central data storage. 

This project is currently under development as part of the broader **mc<sup>2</sup>** effort (i.e., **M**ultiparty **C**ollaboration and **C**oopetition) by the UC Berkeley [RISE Lab](https://rise.cs.berkeley.edu/).

Please feel free to reach out to us if you would like to use Federated XGBoost for your applications. We also welcome contributions to our work!

## Installation

1. Clone this repository and its submodules.

```
git clone --recursive https://github.com/mc2-project/federated-xgboost.git
```

2. Build Federated XGBoost.

```
cd federated-xgboost
mkdir build
cd build
cmake ..
make
```

3. Install the Python package.

```
cd python-package
sudo python3 setup.py install
```

## Quickstart
This quickstart uses the tutorial located in `demo/basic`. In this tutorial, each party in the federation starts an RPC server on port 50051 to listen for the aggregator. The aggregator sends invitations to all parties to join the computation. Once all parties have accepted the invitation, training commences -- the training script `demo.py` is run.

In Federated XGBoost, the training script must be at the same location at each party.

1. Modify `hosts.config` to contain the IP addresses of all parties in the federation. Each line in `hosts.config` is in the following format

```
<ip_addr>:<port>
```

For the purposes of this demo, `<port>` should be `50051`.

2. Start the RPC server at each party. 

```
python3 serve.py
```

3. At the aggregator, send invitations to all parties.

```
../../dmlc-core/tracker/dmlc-submit --log-level DEBUG --cluster rpc --num-workers 2 --host-file hosts.config  --worker-memory 4g /path/to/federated-xgboost/demo/basic/demo.py
```

Each party should receive an invitation through their console:

```
Request from aggregator [ipv4:172.31.27.60:50432] to start federated training session:
Please enter 'Y' to confirm or 'N' to reject.
Join session? [Y/N]:
```

4. Once all parties submit `Y`, training begins.


