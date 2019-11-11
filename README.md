# preCICE Config-Visualizer

The `config-visualizer` is a tool meant to help visualize and debug precice configuration xml files. 
This readme describes the installation and various functionalities of this tool

## Installation

Clone the repository:
`git clone git@github.com:precice/config-visualizer`

Install the requirements
`python -m pip install requirements.txt`

Run the tool
`python3 visualize.py <precice config filename>`

## Functionalities

This code accepts several inputs seen below. These inputs can be accepted
at startup or as stdin at runtime.
  Positional Parameters
  infile, 
          The XML configuration file. Omit to read from stdin.

  Keyword Parameters
  -o [OUTFILE], --outfile [OUTFILE] 
          The resulting dot file. Omit to output to stdout.
  --data-access {full,merged,hide} 
          Verbosity of the displayed read/write access between mesh and participant.
  --data-exchange {full,merged,hide} 
          Verbosity of the displayed data exchange between meshes.
  --communicators {full,merged,hide} 
          Verbosity of the displayed of communicators.
  --cplschemes {full,merged,hide} 
          Verbosity of the displayed of coupling schemes.
  --no-colors           
          Disable colors in the output.