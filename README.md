# preCICE Config-Visualizer

The `config-visualizer` is a tool meant to help visualize and debug precice configuration xml files. This tool produces a dot file as output, which visualizes the various communicators and meshes defined in the configuration file and the movement of data between them.

This readme describes the installation and various functionalities of this tool

## Installation

1. Clone the repository:

```
git clone git@github.com:precice/config-visualizer
```

2. Install the requirements

```
python3 -m pip install --user .
```

## Usage

Run the tool directly from the command line.

Execute the following command to print some help on it:
```
precice-config-visualizer --help
```

## Functionalities

The tool transforms the xml configuration file into a dot graph file.
```
precice-config-visualizer <precice config filename>
```

It is pipe-friendly, so it can be used in scripts etc:
```
cat config.xml | precice-config-visualizer | dot -Tpdf > config.pdf
```

This code accepts several inputs seen below. These inputs can be accepted at startup or as stdin at runtime. Most of the optional parameters are used to hide or simplify the various relationships between participants, communicators and meshes---use them to adjust the fidelity of output as required for easier viewing.

 Note three available options `{full, merged, hide}`: 
 - `full` is the default setting, and displays all information
 - `merged` combines all the various connections between two nodes into a single connection
 - `hide` removes the information completely

  ### Positional Parameters
  ```
  infile, 
  ```
          The XML configuration file. Omit to read from stdin.


  ### Optional Parameters
  ```
  -o [OUTFILE], --outfile [OUTFILE] 
  ```
          The resulting dot file. Omit to output to stdout.

  ```
  --data-access {full,merged,hide} 
  ```
          Verbosity of the displayed read/write access between mesh and participant.

  ```
  --data-exchange {full,merged,hide} 
  ```
          Verbosity of the displayed data exchange between meshes.
  ```
  --communicators {full,merged,hide} 
  ```
          Verbosity of the displayed of communicators.
  ```
  --cplschemes {full,merged,hide} 
  ```
          Verbosity of the displayed of coupling schemes.
  ```
  --no-colors           
  ```
          Disable colors in the output.
