import json
import math
from qiskit import BasicAer
from qiskit.aqua.algorithms import QSVM
from qiskit.aqua import run_algorithm, QuantumInstance
from qiskit.aqua.components.feature_maps import SecondOrderExpansion
from qiskit import IBMQ

servers = {
  'ibmq_16_melbourne': 14,
  'ibmq_qasm_simulator': 5,
  'ibmq_5_yorktown': 5,
  'ibmq_ouerense': 5,
  'ibmqx2': 5,
  'ibmq_5_tenerife': 5,
  'ibmqx4': 5
}

config = {
    'hub': 'ibm-q',
    'group': 'open',
    'project': 'main',
    'entanglement': 'linear', #linear|full
    'token': '5bbc74ec8c1689f70a3f1335edae4be2d05c7b9a56fa58a41e08e99930b5158babc63f1df1c26c7b59a0481d31c2e3882a957c7da971a379f7d2dacde10075e6',
    'server': 'ibmq_16_melbourne',
    'shots': 1024,
    'depth': 2,
    'seed': 10598,
    'local': False,
    'qbits': 5,
    'records': 10
}


if config['local']:
  config['server'] = 'qasm_simulator'
else:
  config['qbits'] = servers[config['server']]

data = json.load(open('data' + str(config['qbits']) + '.json', 'r'))

IBMQ.save_account(config['token'])
if config['local']:
  IBMQ.load_accounts(hub=None)
  feature_map = SecondOrderExpansion(feature_dimension=config['qbits'], depth=config['depth'], entanglement=config['entanglement'])
  qsvm = QSVM(feature_map, data["train"], data["test"])
  backend = BasicAer.get_backend(config['server'])
  quantum_instance = QuantumInstance(backend, shots=config['shots'], seed_transpiler=config['seed'])
  result = qsvm.run(quantum_instance)
  print(result)
else:
  IBMQ.load_accounts(hub=None)
  feature_map = SecondOrderExpansion(feature_dimension=config['qbits'], depth=config['depth'], entanglement=config['entanglement'])
  qsvm = QSVM(feature_map, data["train"], data["test"])
  provider = IBMQ.get_provider()
  backend = provider.get_backend(config['server'])
  quantum_instance = QuantumInstance(backend, shots=config['shots'], seed_transpiler=config['seed'], skip_qobj_validation=False)
  result = qsvm.run(quantum_instance)
  print(result)