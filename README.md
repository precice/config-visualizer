# preCICE Config-Visualizer

The `config-visualizer` is a tool meant to help visualize and debug precice configuration xml files. This tool produces a dot file as output, which visualizes the various communicators and meshes defined in the configuration file and the movement of data between them.

This readme describes the installation and various functionalities of this tool

## Installation options

1.  Clone the repository and install locally as an editable package.
    This allows you to simply pull in order to update.

    ```
    git clone https://github.com/precice/config-visualizer.git
    pip3 install --user -e config-visualizer
    ```

2.  Install directly from the GitHub repository.
    This version does not require `git`.

    ```
    pip3 install --user https://github.com/precice/config-visualizer/archive/master.zip
    ```

Note: You maybe need to add your user pip installations to your path to make the config visualizer findable, i.e. `export PATH=$PATH:$HOME/.local/bin`.

## Usage

Run the tool directly from the command line.

Execute the following command to print some help on it:
```
precice-config-visualizer --help
```

Alternatively open the GUI:
```
precice-config-visualizer-gui
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

Note: The `dot` tool is part of the [graphviz package](https://www.ubuntuupdates.org/package/core/groovy/universe/base/graphviz).

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

## GUI

The tool ships with a GUI wrapper of the above.

You can launch the gui as such and then open a configuration file
```
precice-config-visualizer-gui
```

Or pass the file directly as an argument
```
precice-config-visualizer-gui <precice config filename>
```
