from matplotlib import rc
import daft

from enum import Enum


import __main__
import os
__all__ = ["NodeType", "NodeProperties", "DBN"]
__version__ = "0.0.1"


class NodeType(Enum):
    """
    Specifies the type of the node.
    Hidden:         unobserved random variable
    Observed:       observed random variable
    Variable:       not a RV that is modelled explicitly, but a node that is tied
                    to a set of times across slices.
    """
    Hidden = 0
    Observed = 1
    Variable = 2



class NodeProperties:
    """
    Simple class that holds the properties of a node. see :__init__:.
    """

    def __init__(self, name, x, y, nodeType=NodeType.Hidden, continuous=False, parentsPrevious=[], parentsNow=[],
                 plotParams={}, labelParams=None):
        """

        :param name:            the name that is going to be displayed inside the node.
                                Internally, this name is also used inside a lookup table, hence this name is required
                                to be unique.

        :param x:               the position (in node count, horizontally in the time slice), positive real number
        :param y:               the position (in node count + vertically in the time slice), positive real number

        :param nodeType:
        :param continuous:      whether the random variable is discrete or continuous. Depending on this property,
                                the way the node is displayed changes.

        :param parentsPrevious: List of parent identifiers to be linked from the previous slice
        :param parentsNow:      List of parent identifiers from the current slice.

        :param plotParams:      Additional plot parameters can be specified in this dict.
        :param labelParams:     Labels for the legend.
        """
        self.name = name
        self.x = x
        self.y = y

        self.nodeType = nodeType
        self.continuous = continuous

        self.parentsPrevious = parentsPrevious
        self.parentsNow = parentsNow

        self.plotParams = plotParams
        self.labelParams = labelParams


class DBN:
    """
    This is the base class that can be used to simplify the generation of DBN
    plots for a variable number of time slices.
    Benefits:
        1. One place to specify formatting conventions, that are maintained in a
           consistent way.
        2. With one line of code per hidden variable, DBN can be visualized quickly
           and generally.

    :author: Julius Hülsmann
    :email:  huelsmann@campus.tu-berlin.de
    """

    def __init__(self, exportDir="", verbose=True):
        """
        Sets up the default configuration (font faamily, border, etc.)
        """
        if (len(exportDir)):

            # Make sure that the export directory ends with "/" if it exists.
            if not exportDir[-1] == '/':
                exportDir =  exportDir + '/'

            # make absolute path
            if not exportDir[1] == "/":
                cwd = os.getcwd()
                exportDir =  cwd + "/" + exportDir

            # create directory
            if not os.path.isdir(exportDir):
                if verbose: print("[INFO]    Directory '" + exportDir + "' did not exist. creating :)")
                os.makedirs(exportDir)
            else:
                if verbose: print("[INFO]    Directory '" + exportDir + "' already exists!")



        self.exportDir = exportDir

        rc("font", family="serif", size=12)
        rc("text", usetex=True)

        # Borders with nothing but nothingness inside
        border = .0
        self.borderTop = border
        self.borderBottom = border
        self.borderLeft = border
        self.borderRight = border



        # mutable variables  initialized with 0
        self.maxx, self.maxy = 0, 0

        # Will contain all the configurations that occur in a slice.
        self.slice = {}


    def export(self, sliceBefore=1, sliceAfter=1, nodeSpace=1, centerSuffix="\\tau", exportFile=""):
        """
        To be called after all nodes have been added to the DBN.

        :param exportFile:          file name (+path) of the output pdf.
        :param sliceBefore:         the amount of slices to be displayed before the 'current' time slice
        :param sliceAfter:          " after the current time slice
        :param nodeSpace:           factor that determines the space between different nodes.
        :param centerSuffix:        the name that is written into the footer of each variable (with offset for
                                    different time slices).

        Example usage:
        dbn.export(0,, 5, 1, "") will create the time slices 0, \dots, 5)
        dbn.export(1, 1, 1, "t") will create time slices t-1, t, t+1

        """
        assert(sliceBefore >= 0 and sliceAfter >= 0)
        assert(nodeSpace > 0)


        # determine the name of the export file if non is specified.
        if not len(exportFile):
            name = __main__.__file__
            if (name and len(name) > 3):
                exportFile = __main__.__file__[:-3] + ".pdf"
            else:
                exportFile="out.pdf"
        else:
            assert(exportFile.endswith(".pdf") or exportFile.endswith(".jpg") or exportFile.endswith(".svg"))

        # compute the adequate size for the figure and initialize it.
        amountSlices = sliceBefore + sliceAfter + 1
        width  = self.borderLeft + self.borderRight + ((1+self.maxx)*amountSlices) * nodeSpace
        height = self.borderBottom + self.borderTop + (1+self.maxy) * nodeSpace
        self.pgm = daft.PGM(
            shape= [
                width,
                height
            ],
            origin = [
                -self.borderLeft,
                self.borderTop,
            ],
        )

        # attach all nodes that have been created.
        for sid, snum in enumerate(range(-sliceBefore, sliceAfter+1)):
            for name in self.slice:
                node = self.slice[name]
                cname = node.name + str(sid)

                if len(centerSuffix):
                    strnum = str(snum) if snum < 0 else "+" + str(snum) if snum > 0 else ""
                else:
                    strnum = str(snum)

                plotParams = node.plotParams

                if node.nodeType == NodeType.Variable:
                    plotParams["linestyle"] = ":"
                else:
                    plotParams["linestyle"] = "-"


                if node.continuous:
                    assert(node.nodeType != NodeType.Variable)
                    #plotParams["edgecolor"] = (1,1,1,0)
                    plotParams["linewidth"] = 1.5
                else:
                    #plotParams["hatch"] = ""
                    plotParams["linewidth"] = .5

                # In case the node is a variable node, only print the variable once:
                #   In case the variable contains information shared across slices, only print it in snum == 0
                #   In case the variable contains only information on the first slice, print if sid == 0
                paintNode = node.nodeType != NodeType.Variable
                if not paintNode:
                    isOnlyFirst  = len(node.parentsPrevious)
                    isEverySlice = len(node.parentsNow)
                    assert(isOnlyFirst == 0  or isEverySlice == 0)
                    paintNode = sid == 0 and not len(centerSuffix) if isOnlyFirst else snum == 0

                if paintNode:
                    x = sid * (self.maxx+1) * nodeSpace + (node.x+.5) * nodeSpace
                    y = height - (node.y + .5) * nodeSpace
                    self.pgm.add_node(
                        daft.Node(
                            name=cname,
                            content="$" + node.name + "_{" + centerSuffix + strnum + "}$",
                            x=x,
                            y=y,
                            observed=node.nodeType == NodeType.Observed,
                            plot_params = node.plotParams,
                            label_params = node.labelParams
                        )
                    )
                # add parents of the current time slice
                for p in node.parentsNow:

                    # variables can be connected across slices
                    if node.nodeType == NodeType.Variable:
                        if snum == sliceAfter:
                            for sid, sn2 in enumerate(range(-sliceBefore, sliceAfter+1)):
                                #self.pgm.add_edge(p + str(sid), node.name + str(sliceBefore), linestyle='-')
                                self.pgm.add_edge(node.name + str(sliceBefore), p + str(sid), linestyle='-')
                    else:
                        self.pgm.add_edge(p + str(sid), cname)

                    # in case this is not the first time slice, add links between
                    # nodes that exert influence across time slices.

                if node.nodeType == NodeType.Variable:
                    # if the node is a variable, the parentsPrevious are the parents
                    # of the 0th slice if displayed.
                    if centerSuffix=="" and sid==0:
                        for p in node.parentsPrevious:
                            self.pgm.add_edge(p + '0', cname, linestyle="-")
                            self.pgm.add_edge(cname, p + '0', linestyle="-")
                            #self.pgm.add_edge(p + '0', cname, head_width=0, linestyle=":", color="white")
                elif sid:
                    for p in node.parentsPrevious:
                        self.pgm.add_edge(p + str(sid-1), cname)



    # render and export.
        self.pgm.render()
        self.pgm.figure.savefig(self.exportDir + exportFile)

    def attach(self, nodeProperties):
        """
        Attach node to each slice and register its properties.
        :param:         node properties
        """
        assert(not nodeProperties.name in self.slice)

        self.slice[nodeProperties.name] = nodeProperties
        self.maxx = max(nodeProperties.x, self.maxx)
        self.maxy = max(nodeProperties.y, self.maxy)


