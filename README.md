# Neural Network

## Introduction

First, a neural network implementation in Python.
Secondly, a converter from chessboards txt files to JSON files according to the neural network input format.

## Usage

```bash
./my_torch [--new IN_LAYER [HIDDEN_LAYERS...] OUT_LAYER | --load LOADFILE] [--train | --predict] [--save SAVEFILE] FILE
```

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

## Authors

- [**Niels Ouvrard**](mailto:niels.ouvrard@epitech.eu)
- [**Leo Martin**](mailto:leo2.martin@epitech.eu)
