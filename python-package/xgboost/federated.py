from numpy import genfromtxt
from .training import train
from .core import DMatrix, Booster
from . import rabit
import logging
import json

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

class Federated:
    def __init__(self, rabit_config):
        """
        Parameters
        ----------
        rabit_config : list
            list of Rabit configuration variables
        """
        rabit_config_lst = json.loads(rabit_config)

        # Python strings are unicode, but C strings are bytes, so we must convert to bytes.
        rabit_config = [bytes(s, 'utf-8') for s in rabit_config_lst]

        rabit.init(rabit_config)

    def load_data(self, data, missing=None, weight=None, 
            silent=False, feature_names=None,
            feature_types=None, nthread=None):
        """
        Load data as DMatrix

        Parameters
        ----------
        data : string
            Path to data. Must be the same at each party.
        
        Returns
        -------
        dmat : DMatrix
        """
        logging.info("Loading test data")
        data = genfromtxt(data, delimiter=',')
        dmat = DMatrix(data[:, 1:], label=data[:, 0], missing=missing, weight=weight, silent=silent, feature_names=feature_names, feature_types=feature_types, nthread=nthread)
        return dmat
    
    #  def train(self, dtrain, params, num_rounds, evals):
    #      """Federation-wise training of a booster with given parameters
    #  
    #      Parameters
    #      ----------
    #      dtrain : DMatrix
    #          Training data
    #      params : dict
    #          Booster params
    #      num_rounds : int
    #          Number of boosting iterations
    #      evals : list of pairs (DMatrix, string)
    #          List of items to be evaluated during training. This allows users to watch performance on the validation set
    #      """
    #      bst = train(params, dtrain, num_boost_round=num_rounds, evals=evals)
    #      return bst

    def get_num_parties(self):
        """
        Get number of parties in the federation

        Returns
        -------
        n : int
            Total number of parties in the federation
        """
        return rabit.get_world_size()

    def shutdown(self):
        logging.info("Shutting down tracker")
        rabit.finalize()
