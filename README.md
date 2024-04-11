# preCICE Config-Visualizer

The `config-visualizer` is a tool meant to help visualize and debug precice configuration xml files. This tool produces a dot file as output, which visualizes the various participants, communicators and meshes defined in the configuration file and the movement of data between them.

## Installation options

Install directly from PyPi using [pipx](https://pipx.pypa.io/stable/) or via pip:

```
pipx install precice-config-visualizer
```

To also install [the GUI](https://pypi.org/project/precice-config-visualizer-gui/), run:

```
pipx install 'precice-config-visualizer[gui]'
```

## Usage

```
precice-config-visualizer --help
precice-config-visualizer [OPTIONS] [-o OUTFILE] [<CONFIG-FILE>]
```

The command line version of the tool transforms the XML configuration file into a dot graph and either outputs it to the terminal or writes it to a file.
If the extension of the output file is `.png`, `.pdf`, `.svg`, or `.jpg`, then the tool will render the output using `graghviz`.
The dot output is especially useful if the output needs to be altered for various reasons.
To edit the dot version of the graph, displaying it using a dot viewer such as [xdot](https://pypi.org/project/xdot/) can be helpful.

The tool reads from stdin if no configuration file is given as an argument and the output is printed to stdout if no output filename if specified using the `-o` option.

To generate `graph.dot` from `precice-config.xml` use:

```
precice-config-visualizer precice-config.xml > graph.dot
precice-config-visualizer -o graph.dot precice-config.xml
```

To generate an image from `precice-config.xml` use:

```
precice-config-visualizer -o graph.png precice-config.xml
precice-config-visualizer -o graph.pdf precice-config.xml
precice-config-visualizer -o graph.svg precice-config.xml
```

To modify the dot graph from `precice-config.xml` yourself use:

```
precice-config-visualizer precice-config.xml > graph.dot
# Edit graph.dot here
dot -Tpdf -o graph.pdf graph.dot
```

Further options can be used to control the output appearance. Some information can be turned off or merged.
For a full list of options, run:

```
precice-config-visualizer --help
```
