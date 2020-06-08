from numpy import genfromtxt
from .core import DMatrix
from . import rabit
import json


class Federated:
    def __init__(self, rabit_config):
        """
        Parameters
        ----------
        rabit_config : string 
            string representation of Rabit configuration variables
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
            Absolute path to data. Must be the same at each party.
        
        Returns
        -------
        dmat : DMatrix
            DMatrix representation of the loaded
        """
        data = genfromtxt(data, delimiter=',')
        dmat = DMatrix(data[:, 1:], label=data[:, 0], missing=missing, weight=weight, silent=silent, feature_names=feature_names, feature_types=feature_types, nthread=nthread)
        return dmat
    
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
        """
        Shut down the tracker
        """
        rabit.finalize()
