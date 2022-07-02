import argparse
import os
import pathlib
import random
import typing

import pycspr
from pycspr import NodeClient
from pycspr import NodeConnection
from pycspr.crypto import KeyAlgorithm
from pycspr.types import PrivateKey
from pycspr.types import Deploy
from pycspr.types import PublicKey
from pycspr import crypto

#def build_arguments():
_ARGS = argparse.ArgumentParser("Illustration of how to execute native transfers.")

_ARGS.add_argument(
    "--node-host",
    default="localhost",
    dest="node_host",
    help="Host address of target node.",
    type=str,
    )

_ARGS.add_argument(
    "--node-port-rpc",
    default=11101,
    dest="node_port_rpc",
    help="Node API JSON-RPC port.  Typically 7777 on most nodes.",
    type=int,
    )
    #print("ARGSSSSSSSSSSSSS", _ARGS)
    #return _ARGS

args = _ARGS.parse_args()

def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.
    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))

def starter(args):
    #set node client
    client = _get_client(args)

    #cp1 = Treasuery Account
    cp1_pv_key = "MC4CAQAwBQYDK2VwBCIEICDgdkR5F7tESDeffkvez3XTXa8QVyUpDggPciM9iCLh"
    cp1_pb_key =  bytes.fromhex("b100f3c3762b9382dff700abd19c719ce8b4efdd83e2c038017db5697ffe62fb")

    cp1 = PrivateKey(cp1_pv_key, cp1_pb_key)
    
    #cp2 = Destination address
    cp2_pb_key = bytes.fromhex(input("Enter the public address: "))
    
    cp2_pb_key = cp2_pb_key[1:]
    print("len: ", len(cp2_pb_key))
    print("new key: ", cp2_pb_key)
    cp2 = PublicKey(crypto.KeyAlgorithm.ED25519, cp2_pb_key)
    deploy = custom_transfer_function(cp1, cp2)
    deploy.approve(cp1)

    #send the transaction to the chain
    client.send_deploy(deploy)

    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")


def custom_transfer_function(cp1, cp2):
    deploy_params = pycspr.create_deploy_parameters(
        account=cp1,
        chain_name="Testnet"
        )

    deploy = pycspr.create_transfer(
            params=deploy_params,
            amount=int(100),
            target=cp2.account_key,
            correlation_id=random.randint(1, 1e6)
    )


    return deploy

#custom_args = build_arguments()
#custom_args = custom_args.parse_args()
starter(args)


"""
Note: We should remove the first byte of the key
because it is not part of the key
it is only a meta data that indicates that this is an address
Ref: https://bitcoin.stackexchange.com/questions/88885/convert-33-byte-public-key-with-no-parity-prefix-to-address
and we should also convert the hexa to raw bytes using python method bytes.fromhex()


cp1
pb key
01b100f3c3762b9382dff700abd19c719ce8b4efdd83e2c038017db5697ffe62fb

cp2
pb key
01d8956d47246fbe96f15114289d013a13452343d0a5316036f7bfe07ba49051a0
"""
