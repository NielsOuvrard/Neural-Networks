# Neural Network

## Introduction

First, a neural network implementation in Python.
Secondly, a converter from chessboards txt files to JSON files according to the neural network input format.

## Requirements

- Python 3.8
- [NumPy](https://numpy.org/)

## Usage

```bash
./my_torch [--new IN_LAYER [HIDDEN_LAYERS...] OUT_LAYER | --load LOADFILE] [--train | --predict] [--save SAVEFILE] FILE
```

### Use only the Neural Network Class

```python
NeuralNetwork(layers_sizes=..., evaluation_function=..., evaluation_function_derivative=...)
```

#### Parameters

- `layers_sizes` (list of int) – The number of neurons in each layer of the network. The length of the list represents the number of layers in the network, and the value of each element represents the number of neurons in that layer.
- `evaluation_function` (function) – The function used to evaluate the output of the network. The function must take a single parameter, a numpy.ndarray, and return a numpy.ndarray.
- `evaluation_function_derivative` (function) – The derivative of the evaluation function. The function must take a single parameter, a numpy.ndarray, and return a numpy.ndarray.

## Description

- `--new` Creates a new neural network with random weights. Each subsequent number represents the number of neurons on each layer, from left to right. For example, `./my_torch –new 3 4 5` will create a neural network with an input layer of 3 neurons, a hidden layer of 4 neurons, and an output layer of 5 neurons.
- `--load` Loads an existing neural network from `LOADFILE`, which must be a JSON file.
- `--train` Launches the neural network in training mode. Each board in `FILE` must contain inputs to send to the neural network, as well as the expected output.
- `--predict` Launches the neural network in prediction mode. Each board in `FILE` must contain inputs to send to the neural network, and optionally an expected output.
- `--save` Save neural network internal state into `SAVEFILE`.
- `FILE` FILE containing chessboards, which must be a JSON file.

## Example

### Example of usage

```bash
$ ./my_torch --new 64 20 20 1 --train --save save.json trainset.json
```

```bash
$ ./my_torch --load save.json --predict testset.json
...
Expected: 1, Predicted: 0.88 = 1 -> True
Accuracy:  0.88
```

### Example of input file

#### logical AND

```json
{
  "inputs": [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
  ],
  "output": [0, 0, 0, 1]
}
```

### Example of save file

```json
{
  "weights": [
    [
      //
    ]
  ],
  "biases": [
    [
      ///
    ]
  ],
  "layer_sizes": [
    // inputs
    // hidden layers (nb neutrons for each layer)
    // outputs
  ]
}
```

### Example of Neural Network

```python
nn = NeuralNetwork(
    layers_sizes=[2, 2, 1],
    evaluation_function=lambda x: 1 / (1 + np.exp(-x)),
    evaluation_function_derivative=lambda x: x * (1 - x)
)
```

## Authors

- [**Niels Ouvrard**](mailto:niels.ouvrard@epitech.eu)
- [**Leo Martin**](mailto:leo2.martin@epitech.eu)
