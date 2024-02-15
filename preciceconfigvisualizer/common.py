import sys
import types
from collections import defaultdict
from itertools import cycle

import pydot
from lxml import etree

if sys.version_info < (3, 6):
    raise RuntimeError(
        "This program requires python 3.6 or later but you attempted to run it"
        " with python {}.{}".format(sys.version_info.major.sys.version_info.minor)
    )


def isTrue(text):
    return text.lower() in ["yes", "1", "true", "on"]


def quote(text):
    return f'"{text}"'


def parseXML(content):
    p = etree.XMLParser(recover=True, remove_comments=True)
    return etree.fromstring(content, p)


def parseXMLFile(file):
    return parseXML(open(file, "rb").read())


def addNode(g, name, **attrs):
    n = pydot.Node(quote(name), **attrs)
    g.add_node(n)
    return n


def addEdge(g, src, dst, **attrs):
    e = pydot.Edge(quote(src), quote(dst), **attrs)
    g.add_edge(e)
    return e


def addUniqueEdge(g, src, dst, **attrs):
    for e in g.get_edge_list():
        es, ed = e.get_source().strip('"'), e.get_destination().strip('"')
        if es == src and ed == dst:
            return e
    e = pydot.Edge(quote(src), quote(dst), **attrs)
    g.add_edge(e)
    return e


def getEdge(g, src, dst):
    for e in g.get_edge_list():
        es, ed = e.get_source().strip('"'), e.get_destination().strip('"')
        if es == src and ed == dst:
            return e
    return None


def getParticipantNames(solverinterface):
    return [p.attrib["name"] for p in solverinterface.findall("participant")]


def getParticipantColor(solverinterface, blackOnly=False):
    names = getParticipantNames(solverinterface)
    colors = None
    if blackOnly:
        colors = cycle(["black"])
    else:
        colorblind = [
            "#0173B2",
            "#DE8F05",
            "#029E73",
            "#D55E00",
            "#CC78BC",
            "#CA9161",
            "#FBAFE4",
            "#949494",
            "#ECE133",
            "#56B4E9",
        ]
        colors = cycle(colorblind)
    return dict(zip(names, colors))


def configToGraph(ast, args):
    assert ast.tag == "precice-configuration"

    solverinterfaces = ast.findall("solver-interface")
    precice_version = -1
    si_dims = None  # precice v2

    assert len(solverinterfaces) in [0, 1]
    if len(solverinterfaces) == 1:
        precice_version = 2
        si_dims = solverinterfaces[0].attrib["dimensions"]
    elif len(solverinterfaces) == 0:
        precice_version = 3

    if precice_version == 2:
        root = solverinterfaces[0]
    elif precice_version == 3:
        root = ast

    g = pydot.Graph(
        layout="dot",
        splines="true",
        overlap="scale",
        compound=True,
        rankdir="LR",
        margin=args.margin,
    )
    dataType = {}
    meshes = {}
    meshDims = {}
    participantClusterName = {}
    m2nCluster = pydot.Cluster("m2n", label=quote("Communicators"))
    g.add_subgraph(m2nCluster)
    cplCluster = pydot.Cluster("cpl", label=quote("Coupling Schemes"))
    g.add_subgraph(cplCluster)

    participantColor = getParticipantColor(root, args.no_colors)

    for elem in root.iterchildren():
        if elem.tag.startswith("data"):
            kind = elem.tag[elem.tag.find(":") + 1 :]
            name = elem.attrib["name"]
            dataType[name] = kind
        elif "mesh" == elem.tag:
            name = elem.attrib["name"]
            meshDims[name] = elem.attrib["dimensions"] if si_dims is None else si_dims
            meshes[name] = [use.attrib["name"] for use in elem.findall("use-data")]
        elif "participant" == elem.tag:
            name = elem.attrib["name"]
            participant = pydot.Cluster(name, label=quote(name), style="bold")
            participantClusterName[name] = participant.get_name()
            color = participantColor[name]
            addNode(participant, name, color=color, shape="doubleoctagon")
            # use-mesh
            for use in elem.findall("use-mesh"):
                mesh = use.attrib["name"]
                meshname = f"{name}-{mesh}"
                provided = "provide" in use.attrib
                if provided:
                    label = mesh + (
                        ""
                        if mesh not in meshDims
                        else f"<SUP><I>{meshDims[mesh]}D</I></SUP>"
                    )
                    addNode(
                        participant,
                        meshname,
                        shape="cylinder",
                        label=f"<{label}>",
                        color=color,
                    )
                else:
                    pfrom = use.attrib["from"]
                    label = f"<{mesh} from {pfrom}>"
                    addNode(
                        participant,
                        meshname,
                        shape="cylinder",
                        label=label,
                        color=participantColor[pfrom],
                        style="dashed",
                    )
            # provide-mesh
            for use in elem.findall("provide-mesh"):
                mesh = use.attrib["name"]
                meshname = f"{name}-{mesh}"
                label = mesh + (
                    ""
                    if mesh not in meshDims
                    else f"<SUP><I>{meshDims[mesh]}D</I></SUP>"
                )
                if isTrue(use.attrib.get("dynamic", "no")):
                    mesh += "\ndynamic"
                addNode(
                    participant,
                    meshname,
                    shape="cylinder",
                    label=f"<{label}>",
                    color=color,
                )
            # receive-mesh
            for use in elem.findall("receive-mesh"):
                mesh = use.attrib["name"]
                meshname = f"{name}-{mesh}"
                pfrom = use.attrib["from"]
                addNode(
                    participant,
                    meshname,
                    shape="cylinder",
                    label=quote(f"{mesh}\nfrom {pfrom}"),
                    color=participantColor[pfrom],
                    style="dashed",
                )
            # read-data
            for read in elem.findall("read-data"):
                mesh = read.attrib["mesh"]
                meshNode = f"{name}-{mesh}"
                data = read.attrib["name"]
                if args.data_access == "full":
                    addEdge(
                        participant,
                        meshNode,
                        name,
                        label=quote(data),
                        tooltip=dataType[data],
                        color=color,
                    )
                elif args.data_access == "merged":
                    reversed = getEdge(participant, name, meshNode)
                    if reversed is None:
                        addUniqueEdge(participant, meshNode, name)
                    else:
                        reversed.set_dir("both")
            # write-data
            for write in elem.findall("write-data"):
                mesh = write.attrib["mesh"]
                meshNode = f"{name}-{mesh}"
                data = write.attrib["name"]
                if args.data_access == "full":
                    addEdge(
                        participant,
                        name,
                        meshNode,
                        label=quote(data),
                        tooltip=dataType[data],
                        color=color,
                    )
                elif args.data_access == "merged":
                    reversed = getEdge(participant, meshNode, name)
                    if reversed is None:
                        addUniqueEdge(participant, name, meshNode, color=color)
                    else:
                        reversed.set_dir("both")

            # watchpoint
            for watchpoint in elem.findall("watch-point"):
                wpmesh = watchpoint.attrib["mesh"]
                wpname = watchpoint.attrib["name"]
                wpcoord = watchpoint.attrib["coordinate"]
                if not args.no_watchpoints:
                    wpnode = f"{name}-WP-{wpname}"
                    addNode(
                        participant,
                        wpnode,
                        shape="note",
                        label=quote(f"{wpname}\nat ({wpcoord})"),
                        color=color,
                    )
                    addEdge(participant, wpnode, name, color=color)

            # other children
            mappings = []
            for child in elem.iterchildren():
                # register mappings
                if child.tag.startswith("mapping:"):
                    mkind = child.tag[child.tag.find(":") + 1 :]
                    mfrom = name + "-" + child.attrib["from"]
                    mto = name + "-" + child.attrib["to"]
                    # mappings.append((mfrom, mto, mkind))
                    if args.mappings == "full":
                        addEdge(
                            participant, mfrom, mto, label=quote(mkind), color=color
                        )
                    elif args.mappings == "merged":
                        e = getEdge(participant, mto, mfrom)
                        if e is None:
                            addEdge(participant, mfrom, mto, color=color)
                        else:
                            e.set_dir("both")

                # master
                if child.tag.startswith("master:"):
                    kind = child.tag[child.tag.find(":") + 1 :]
                    addNode(
                        participant, name + kind, shape="component", label=quote(kind)
                    )

            g.add_subgraph(participant)
        # m2n
        elif elem.tag.startswith("m2n"):
            kind = elem.tag[elem.tag.find(":") + 1 :]
            pfrom = elem.attrib["from" if "from" in elem.attrib else "connector"]
            pto = elem.attrib["to" if "to" in elem.attrib else "acceptor"]
            name = f"m2n-{pto}-{pfrom}"
            if args.communicators == "full":
                addNode(m2nCluster, name, shape="component", label=quote(kind))
                addEdge(
                    g,
                    name,
                    pto,
                    lhead=participantClusterName[pto],
                    dir="both",
                    color=participantColor[pto],
                )
                addEdge(
                    g,
                    name,
                    pfrom,
                    lhead=participantClusterName[pfrom],
                    dir="both",
                    color=participantColor[pfrom],
                )
            if args.communicators == "merged":
                addEdge(
                    g,
                    pfrom,
                    pto,
                    lhead=participantClusterName[pto],
                    ltail=participantClusterName[pfrom],
                    label=quote(kind),
                    dir="both",
                )

        # cpl schemes
        elif elem.tag.startswith("coupling-scheme"):
            kind = elem.tag[elem.tag.find(":") + 1 :]
            # Every cplscheme apart from multi
            name = "-".join(
                ["cpl", "multi"]
                + [e.attrib["name"] for e in elem.findall("participant")]
            )

            if kind == "multi":
                if args.cplschemes == "full":
                    addNode(cplCluster, name, shape="component", label=quote(kind))
                    for other in elem.findall("participant"):
                        thisName = other.attrib["name"]
                        e = addEdge(
                            g,
                            name,
                            thisName,
                            lhead=participantClusterName[thisName],
                            color=participantColor[thisName],
                        )
                        if other.get("control"):
                            e.set_taillabel("Controller")
                elif args.cplschemes == "merged":
                    addNode(
                        g, name, shape="circle", tooltip=quote(kind), label=quote("")
                    )
                    for other in elem.findall("participant"):
                        thisName = other.attrib["name"]
                        e = addEdge(g, name, thisName)
                        if other.get("control"):
                            e.set_style("bold")
                            e.set_tooltip("Controller")

            else:
                # Every cplscheme apart from multi
                first = elem.find("participants").attrib["first"]
                second = elem.find("participants").attrib["second"]
                name = f"cpl-{first}-{second}"

                if args.cplschemes == "full":
                    addNode(cplCluster, name, shape="component", label=quote(kind))
                    addEdge(
                        g,
                        name,
                        first,
                        lhead=participantClusterName[first],
                        taillabel=quote("first"),
                        color=participantColor[first],
                    )
                    addEdge(
                        g,
                        name,
                        second,
                        lhead=participantClusterName[second],
                        taillabel=quote("second"),
                        color=participantColor[second],
                    )
                elif args.cplschemes == "merged":
                    addUniqueEdge(
                        g,
                        first,
                        second,
                        dir="both",
                        taillabel=quote("first"),
                        headlabel=quote("second"),
                        label=quote(kind),
                    )

            # exchange tags
            # This is indepedant of the above
            for exchange in elem.findall("exchange"):
                mesh = exchange.attrib["mesh"]
                data = exchange.attrib["data"]
                pfrom = exchange.attrib["from"]
                pto = exchange.attrib["to"]
                init = isTrue(exchange.get("initialize", "no"))
                withSubsteps = isTrue(exchange.get("substeps", "no"))
                if args.data_exchange == "full":
                    pcolor = participantColor[pfrom]
                    style = "bold" if init else ""
                    tooltip = dataType[data] + (" initialized" if init else "")
                    color = f"{pcolor}:invis:{pcolor}" if withSubsteps else pcolor
                    addEdge(
                        g,
                        f"{pfrom}-{mesh}",
                        f"{pto}-{mesh}",
                        label=quote(data),
                        tooltip=tooltip,
                        color=color,
                        style=style,
                    )
                elif args.data_exchange == "merged":
                    addUniqueEdge(
                        g,
                        f"{pfrom}-{mesh}",
                        f"{pto}-{mesh}",
                        color=participantColor[pfrom],
                    )

    return g


def readBinary(streamlike):
    """
    Reading binary from sys.stdin requires to use the underlying buffer instead
    """
    try:
        return streamlike.buffer.read()
    except:
        return streamlike.read()


def configFileToDotCode(filename, args):
    xml = parseXML(readBinary(open(filename, "rb")))
    g = configToGraph(xml, args)
    return g.to_string()
