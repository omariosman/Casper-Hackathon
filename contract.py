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


#import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519
#cp1_pv_key = ed25519.Ed25519PrivateKey.from_private_bytes(open('wallet_key/OmarOsman23_secret_key.pem', 'rb').read()[:32])
#cp1_pv_key = str(cp1_pv_key)
#def build_arguments():
_ARGS = argparse.ArgumentParser("Illustration of how to execute native transfers.")

_ARGS.add_argument(
    "--cp1-secret-key-path",
    default="",
    dest="path_to_cp1_secret_key",
    help="Path to counter-party one's secret_key.pem file.",
    type=str,
    )

_ARGS.add_argument(
    "--cp1-secret-key-type",
    default=KeyAlgorithm.ED25519.name,
    dest="type_of_cp1_secret_key",
    help="Type of counter party one's secret key.",
    type=str,
    )

_ARGS.add_argument(
    "--cp2-account-key-path",
    default="",
    dest="path_to_cp2_account_key",
    help="Path to counter-party two's public_key_hex file.",
    type=str,
    )


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

_ARGS.add_argument(
    "--chain",
    default="casper-net-1",
    dest="chain_name",
    help="Name of target chain.",
    type=str,
    )

args = _ARGS.parse_args()

def _get_client(args: argparse.Namespace) -> NodeClient:
    """Returns a pycspr client instance.
    """
    return NodeClient(NodeConnection(
        host=args.node_host,
        port_rpc=args.node_port_rpc,
    ))


def _get_counter_parties(args: argparse.Namespace) -> typing.Tuple[PrivateKey, PublicKey]:
    """Returns the 2 counter-parties participating in the transfer.
    """
    cp1 = pycspr.parse_private_key(
        args.path_to_cp1_secret_key,
        args.type_of_cp1_secret_key,
        )
    cp2 = pycspr.parse_public_key(
        args.path_to_cp2_account_key
        )

    return cp1, cp2



def starter(args):
    #set node client
    client = _get_client(args)

    #cp1 = Treasuery Account
    cp1, cp2 = _get_counter_parties(args)


    # Set deploy.
    deploy: Deploy = _get_deploy(args, cp1, cp2)

    # Approve deploy.
    deploy.approve(cp1)

    # Dispatch deploy to a node.
    client.send_deploy(deploy)

    print(f"Deploy dispatched to node [{args.node_host}]: {deploy.hash.hex()}")
   
def _get_deploy(args: argparse.Namespace, cp1: PrivateKey, cp2: PublicKey) -> Deploy:
    """Returns transfer deploy to be dispatched to a node.
    """
    # Set standard deploy parameters.
    deploy_params = pycspr.create_deploy_parameters(
        account=cp1,
        chain_name=args.chain_name
        )

    # Set deploy.
    deploy = pycspr.create_transfer(
        params=deploy_params,
        amount=int(2.5e9),
        target=cp2.account_key,
        correlation_id=random.randint(1, 1e6)
        )

    return deploy

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
