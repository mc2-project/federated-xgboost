'''
gRPC Server
'''
from concurrent import futures

#  import _credentials

from .rpc import fxgb_pb2
from .rpc import fxgb_pb2_grpc
import grpc

import ctypes
import sys

import pandas as pd
import json
import subprocess


def get_dmlc_vars(env):
    '''
    Returns list of strings representing DMLC variables needed for rabit.
    Parsed in allreduce_base.cc from '<name>=<value>' format.
    
    Param:
        env - Env protobuf
    
    Return:
        list containing DMLC variables
    '''
    temp = [
        'DMLC_TRACKER_URI=' + env.DMLC_TRACKER_URI,
        'DMLC_TRACKER_PORT=' + str(env.DMLC_TRACKER_PORT),
        'DMLC_ROLE=' + env.DMLC_ROLE,
        'DMLC_NODE_HOST=' + env.DMLC_NODE_HOST,
        'DMLC_NUM_WORKER=' + str(env.DMLC_NUM_WORKER),
        'DMLC_NUM_SERVER=' + str(env.DMLC_NUM_SERVER),
    ]
    # Python strings are unicode, but C strings are bytes, so we must convert to bytes.
    #  return [bytes(s, 'utf-8') for s in temp]
    return temp


class FederatedXGBoostServicer():
    ''' gRPC servicer class which implements worker machine RPCs API. '''

    def __init__(self):
        # A list of variables to configure rabit
        self.rabit_config = None

    def Init(self, request, context):
        '''
        Initializes rabit and environment variables.
        When worker receives this RPC, it can accept or reject the federated training session.

        Params:
            init_request - InitRequest proto containing DMLC variables to set up node communication with tracker
            context - RPC context. Contains metadata about the connection

        Return:
            WorkerResponse proto (confirmation of initializatison success or failure).
        '''
        print('Request from aggregator [%s] to start federated training session:' % context.peer())
        accept_job = None
        while accept_job not in {'Y', 'N'}:
            print("Please enter 'Y' to confirm or 'N' to reject.")
            accept_job = input("Join session? [Y/N]: ")
        if accept_job == 'Y':
            self.rabit_config = get_dmlc_vars(request.dmlc_vars)
            return fxgb_pb2.WorkerResponse(success=True)
        else:
            return fxgb_pb2.WorkerResponse(success=False)

    def Train(self, request, context):
        '''
        Starts distributed training.

        Params:
            train_request - TrainRequest proto containing XGBoost parameters for training
            context - RPC context containing metadata about the connection

        Return:
            WorkerResponse proto (confirmation of training success or failure).
        '''
        try:
            print('Starting federated training session')
            path_to_script = request.path
            rabit_config_str = json.dumps(self.rabit_config)
            cmd = ["python3", str(path_to_script), str(rabit_config_str)]

            # Real time output of process
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            for line in iter(process.stdout.readline, b''):
                line = line.decode("utf-8")
                sys.stdout.write(line)

            rc = process.returncode

            if rc == 0:
                return fxgb_pb2.WorkerResponse(success=True)
            else:
                return fxgb_pb2.WorkerResponse(success=False)
        except:
            return fxgb_pb2.WorkerResponse(success=False)


# Start gRPC server listening on port 'port'
def listen(port):
    """
    Params
    ------
    port : int
        Port to listen for aggregator
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    fxgb_pb2_grpc.add_FXGBWorkerServicer_to_server(FederatedXGBoostServicer(), server)
    #  server_credentials = grpc.ssl_server_credentials(
        #  ((_credentials.SERVER_CERTIFICATE_KEY, _credentials.SERVER_CERTIFICATE),))
    #  server.add_secure_port('[::]:' + port, server_credentials)
    server.add_insecure_port('[::]:' + str(port))
    print("Starting RPC server on port ", str(port))
    server.start()
    server.wait_for_termination()
