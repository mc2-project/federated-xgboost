#####################
Federated XGBoost Documentation
#####################

**Federated XGBoost** is an extension of `XGBoost <https://github.com/dmlc/xgboost>`_, a state-of-the-art gradient boosting library, to the federated setting.

Federated learning allows multiple parties to collaboratively learn a shared model while keeping each party's data at its respective site. It allows for collaborative learning with lower latencies without a central data storage, thereby improving the privacy of individual parties' data.

In the federated setting, a central party has a basic model that is initially broadcast to all parties. Each party locally trains the model with its own data, then sends a summary of the updates to the model back to the central party. In the decision tree case, parties would be sending the best local feature splits back to the central party. The central party then aggregates all updates, updates its own model with the aggregated update, and broadcasts the newly updated model to all parties. This process is then repeated over and over.

This project is currently under development as part of the broader `Multiparty Collaboration and Coopetition effort <https://github.com/mc2-project/mc2>`_ by the UC Berkeley `RISE Lab <https://rise.cs.berkeley.edu/>`_. 

********
Contents
********

.. toctree::
  :maxdepth: 2
  :titlesonly:

  build
  get_started
  tutorials/index
  faq
  GPU support <gpu/index>
  parameter
  Python package <python/index>
  CLI interface <cli>
  contribute
