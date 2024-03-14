# preCICE Config-Visualizer

The `config-visualizer` is a tool meant to help visualize and debug precice configuration xml files. This tool produces a dot file as output, which visualizes the various participants, communicators and meshes defined in the configuration file and the movement of data between them.

## Installation options

Install directly from PyPi using [pipx](https://pipx.pypa.io/stable/) or via pip:

```
pipx install precice-config-visualizer
```

## Usage

The config visualizer can be use via the CLI or the interactive GUI.

### GUI

```
precice-config-visualizer-gui [CONFIG-FILE]
```

You can launch the GUI directly from the command line.
Passing the path to a configuration file is optional.
All further adjustments are made directly in the GUI.

### CLI

```
precice-config-visualizer --help
precice-config-visualizer [OPTIONS] [-o OUTFILE] [<CONFIG-FILE>]
```

The command line version of the tool transforms the XML configuration file into a dot graph file.
This is especially useful if the output needs to be altered for various reasons.
To edit the actual graph, displaying it using a dot viewer such as [xdot](https://pypi.org/project/xdot/) can be helpful.

The tool reads from stdin if no configuration file is given as an argument and the output is printed to stdout if no output filename if specified using the `-o` option.

To generate `graph.dot` from `precice-config.xml` use:

```
precice-config-visualizer -o graph.dot precice-config.xml
```

To `precice-config.xml` as PDF use:

```
precice-config-visualizer precice-config.xml | dot -Tpdf -o graph.pdf
```

Further options can be used to control the output appearance. Some information can be turned off or merged.
For a full list of options, run:

```
precice-config-visualizer --help
```
