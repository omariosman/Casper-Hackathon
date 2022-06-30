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



def starter():
    dest_public_Address = input("Enter the public address: ")
    custom_transfer_function("MC4CAQAwBQYDK2VwBCIEICDgdkR5F7tESDeffkvez3XTXa8QVyUpDggPciM9iCLh", dest_public_Address)


def custom_transfer_function(private_key, public_key):
    deploy_params = pycspr.create_deploy_parameters(
        account=private_key,
        chain_name="Testnet"
        )

    pycspr.create_transfer(
            params=deploy_params,
            amount=int(2.5e9),
            target=public_key,
            correlation_id=random.randint(1, 1e6)

    )


starter()
