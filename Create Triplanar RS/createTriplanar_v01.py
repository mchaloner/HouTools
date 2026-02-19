import hou
import random


def createParams(selectedNodes):

        node = selectedNodes[0]

        redshiftVOPNode = node.parent()

        # create scale offset and rot params

        scaleP = redshiftVOPNode.createNode("parameter","scale_p")
        offsetP = redshiftVOPNode.createNode("parameter","offset_p")
        rotP = redshiftVOPNode.createNode("parameter","rot_p")

        scaleP.parm("parmname").set("scaleP")
        offsetP.parm("parmname").set("offsetP")
        rotP.parm("parmname").set("rotP")

        # create vector makers

        scaleVNode = redshiftVOPNode.createNode("redshift::RSVectorMaker","scale")
        offsetVnode = redshiftVOPNode.createNode("redshift::RSVectorMaker","offset")
        rotVnode = redshiftVOPNode.createNode("redshift::RSVectorMaker","rotation")

        # connect everything

        scaleVNode.setInput(0, scaleP, 0)
        scaleVNode.setInput(1, scaleP, 0)
        scaleVNode.setInput(2, scaleP, 0)

        offsetVnode.setInput(0, offsetP, 0)
        offsetVnode.setInput(1, offsetP, 0)
        offsetVnode.setInput(2, offsetP, 0)

        rotVnode.setInput(0, rotP, 0)
        rotVnode.setInput(1, rotP, 0)
        rotVnode.setInput(2, rotP, 0)


        return [scaleVNode,offsetVnode,rotVnode]

def addTriPlanarNodes(node, paramNodes):

        redshiftVOPNode = node.parent()

        RSmatNode = redshiftVOPNode.node("Material1")

        newTriNodeName = node.name() + "_triplanar"

        triNode = redshiftVOPNode.createNode("redshift::TriPlanar",newTriNodeName)

        nodeConnects = node.outputConnections()

        inputNode = nodeConnects[0].outputNode()

        triNode.setInput(0, node, 0)

        inputNode.setInput(nodeConnects[0].inputIndex(), triNode, 0)

        # connect param nodes
        # scale
        triNode.setInput(4, paramNodes[0], 0)
        triNode.setInput(5, paramNodes[1], 0)
        triNode.setInput(6, paramNodes[2], 0)
        
        redshiftVOPNode.layoutChildren()


def init():

        paramNodes = createParams(hou.selectedNodes())

        for node in hou.selectedNodes():

                addTriPlanarNodes(node,paramNodes)


init()

# convert to triplaner