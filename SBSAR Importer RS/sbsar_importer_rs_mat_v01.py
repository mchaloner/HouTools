import hou
import random
import os

# code by Marcus Chaloner - http://www.marcuschaloner.com - 2020-2026

#name
newObjectName = ""

#geo paths
geo_path = "$HIP/geo/"
geoFilePath = ""

#Shader paths
tex_path = "$HIP/tex/"
baseColourPath = "2"
roughnessPath = ""
metalPath = ""
heightPath = ""
normalPath = ""

resX = 2048
resY = 2048 # make this customizable

geoNodeNetwork = hou.node("/obj/")
copsNodeNetwork = hou.node("/img/")
matNodeNetwork = hou.node("/mat/")
    
def bakeCOPmaps(filePath):
    
    # create cop network
    # needs SBSAR reader, Color Node, BaseColour, Roughness, Metal, Normal, Height (change if needed after sbsar read?)
    # read sbsar file

    sbsarName = os.path.basename(filePath)

    newSBSARcopNetwork = copsNodeNetwork.createNode("img",sbsarName);

    SBSARNode = newSBSARcopNetwork.createNode("labs::sbs_archive","SBSAR_Loader")
    SBSARNode.parm("size1").set(resX)
    SBSARNode.parm("size2").set(resY)
    SBSARNode.parm("file").set(filePath)

    

    colourPlaneNode = newSBSARcopNetwork.createNode("color","color_plane")

    colourPlaneNode.parm("overridesize").set(1)
    colourPlaneNode.parm("size1").set(resX)
    colourPlaneNode.parm("size2").set(resY)

    baseColourNode = newSBSARcopNetwork.createNode("delete","baseColour")
    roughnessNode = newSBSARcopNetwork.createNode("delete","roughness")
    normalNode = newSBSARcopNetwork.createNode("delete","normal")
    heightNode = newSBSARcopNetwork.createNode("delete","height")
    metalNode = newSBSARcopNetwork.createNode("delete","metal")

    baseColourNode.parm("delete").set(1)
    baseColourNode.parm("scope").set("Diffuse")

    roughnessNode.parm("delete").set(1)
    roughnessNode.parm("scope").set("Roughness")

    normalNode.parm("delete").set(1)
    normalNode.parm("scope").set("Normal")

    heightNode.parm("delete").set(1)
    heightNode.parm("scope").set("Height")
    
    metalNode.parm("delete").set(1)
    metalNode.parm("scope").set("Metallic")

    # rename Diffuse to C

    baseColourNodeRename = newSBSARcopNetwork.createNode("rename","baseColourRename")
    roughnessNodeRename = newSBSARcopNetwork.createNode("rename","roughnessRename")
    normalNodeRename = newSBSARcopNetwork.createNode("rename","normalRename")
    heightNodeRename = newSBSARcopNetwork.createNode("rename","heightRename")
    metalNodeRename = newSBSARcopNetwork.createNode("rename","metalRename")

    baseColourNodeRename.parm("from").set("Diffuse")
    baseColourNodeRename.parm("to").set("C")

    roughnessNodeRename.parm("from").set("Roughness")
    roughnessNodeRename.parm("to").set("C")

    normalNodeRename.parm("from").set("Normal")
    normalNodeRename.parm("to").set("C")

    heightNodeRename.parm("from").set("Height")
    heightNodeRename.parm("to").set("C")

    metalNodeRename.parm("from").set("Metallic")
    metalNodeRename.parm("to").set("C")

    baseColourROPNode = newSBSARcopNetwork.createNode("rop_comp","baseColourOut")
    roughnessROPNode = newSBSARcopNetwork.createNode("rop_comp","roughnessOut")
    normalROPNode = newSBSARcopNetwork.createNode("rop_comp","normalOut")
    heightROPNode = newSBSARcopNetwork.createNode("rop_comp","heightOut")
    metalROPNode = newSBSARcopNetwork.createNode("rop_comp","metalOut")

    # connect nodes

    baseColourNode.setInput(0,SBSARNode,0)
    roughnessNode.setInput(0,SBSARNode,0)
    normalNode.setInput(0,SBSARNode,0)
    heightNode.setInput(0,SBSARNode,0)
    metalNode.setInput(0,SBSARNode,0)

    baseColourNodeRename.setInput(0,baseColourNode,0)
    roughnessNodeRename.setInput(0,roughnessNode,0)
    normalNodeRename.setInput(0,normalNode,0)
    heightNodeRename.setInput(0,heightNode,0)
    metalNodeRename.setInput(0,metalNode,0)

    baseColourROPNode.setInput(0,baseColourNodeRename,0)
    roughnessROPNode.setInput(0,roughnessNodeRename,0)
    normalROPNode.setInput(0,normalNodeRename,0)
    heightROPNode.setInput(0,heightNodeRename,0)
    metalROPNode.setInput(0,metalNodeRename,0)

    imgfolder = sbsarName + "/"

    hipname = hou.expandString('$HIPNAME') + "/"

    global baseColourPath 
    global roughnessPath
    global metalPath
    global heightPath
    global normalPath

    #ready to bake

    baseColourPath = tex_path + hipname + imgfolder + sbsarName + "_basecolour.png"
    roughnessPath = tex_path + hipname + imgfolder + sbsarName + "_roughness.png"
    metalPath = tex_path + hipname + imgfolder + sbsarName + "_metal.png" # just black
    normalPath = tex_path + hipname + imgfolder + sbsarName + "_normal.exr"
    heightPath = tex_path + hipname + imgfolder + sbsarName + "_height.exr"

    ## randomise wood

    ##SBSARNode = selectedNode.node("SBSAR_Loader")
    randomSeed = random.randint(0, 1080)

    SBSARNode.parm("reload").pressButton()
    # random seed
    #SBSARNode.parm("sbs__randomseed").set(randomSeed)

    #SBSARNode.parm("sbs_normal_format").set("OpenGL")
    
    # set output paths
    baseColourROPNode.parm("copoutput").set(baseColourPath)
    roughnessROPNode.parm("copoutput").set(roughnessPath)
    normalROPNode.parm("copoutput").set(normalPath)
    heightROPNode.parm("copoutput").set(heightPath)
    metalROPNode.parm("copoutput").set(metalPath)

    baseColourROPNode.parm("trange").set(0)
    roughnessROPNode.parm("trange").set(0)
    normalROPNode.parm("trange").set(0)
    heightROPNode.parm("trange").set(0)
    metalROPNode.parm("trange").set(0)
    
    # render
    baseColourROPNode.parm("execute").pressButton()
    roughnessROPNode.parm("execute").pressButton()
    normalROPNode.parm("execute").pressButton()
    heightROPNode.parm("execute").pressButton()
    metalROPNode.parm("execute").pressButton()
    
def createRSMaterials(newObjectName):

    # create new redshift material
    rsMatName = newObjectName + "_RS_Mat"
    redshiftVOPNode = matNodeNetwork.createNode("redshift_vopnet",rsMatName)
    
    #mat and final node
    RSmatNode = redshiftVOPNode.createNode("redshift::Material",rsMatName)
    RSmatFinalNode = redshiftVOPNode.node("redshift_material1")
    
    # set to Metalness
    RSmatNode.parm("refl_fresnel_mode").set("2") #error

    # set GGX
    RSmatNode.parm("refl_brdf").set("1")

    # base colour
    baseColourTexNode = redshiftVOPNode.createNode("redshift::TextureSampler","Base_Colour")
    baseColourTexNode.parm("tex0").set(baseColourPath)
    baseColourTexNode.parm("tex0_colorSpace").set("sRGB")


    # ACES

    #acesOSLNode = redshiftVOPNode.createNode("redshift::rsOSL","rRGBtoACES")
    #acesOSLNode.parm("RS_osl_file").set("R:/RS_OSL_Nodes/ACESGamutConvert.osl")
    #acesOSLNode.parm("RS_osl_compile").pressButton()
    
    # roughness
    roughTexNode = redshiftVOPNode.createNode("redshift::TextureSampler","Roughness")
    roughTexNode.parm("tex0").set(roughnessPath)
    roughTexNode.parm("tex0_colorSpace").set("Raw")

    
    # metal
    metalTexNode = redshiftVOPNode.createNode("redshift::TextureSampler","Metal")
    metalTexNode.parm("tex0").set(metalPath)
    
    # normal
    normalTexNode = redshiftVOPNode.createNode("redshift::TextureSampler","Normal")
    normalTexNode.parm("tex0").set(normalPath)
    normalTexNode.parm("tex0_colorSpace").set("Raw")

    
    
    # extra bump node
    bumpNode = redshiftVOPNode.createNode("redshift::BumpMap","BumpReader")
    bumpNode.parm("inputType").set("1")

    bumpNode.parm("scale").set(0.1)
    
    # height
    heightTexNode = redshiftVOPNode.createNode("redshift::TextureSampler","Height")
    heightTexNode.parm("tex0").set(heightPath)
    heightTexNode.parm("tex0_colorSpace").set("Raw")

    
    
    # extra displace node
    displaceNode = redshiftVOPNode.createNode("redshift::Displacement","HeightReader")

    displaceNode.parm("scale").set(0.1)

    displaceNode.parm("newrange_min").set(-1)
    displaceNode.parm("newrange_max").set(1)
    
    # convert to ACES
    #acesOSLNode.setInput(0,baseColourTexNode,0)
    #RSmatNode.setInput(0, acesOSLNode, 0)

    RSmatNode.setInput(0,baseColourTexNode,0)
    
    RSmatNode.setInput(7, roughTexNode, 0)
    RSmatNode.setInput(14, metalTexNode, 0)
    
    bumpNode.setInput(0, normalTexNode, 0)
    displaceNode.setInput(0, heightTexNode, 0)
    
    RSmatFinalNode.setInput(2, bumpNode, 0)
    RSmatFinalNode.setInput(1, displaceNode, 0)

    RSmatFinalNode.setInput(0, RSmatNode, 0)

    
    matPath = "/mat/" + redshiftVOPNode.name()

    return matPath

def setGeoNodeParams(newGeoNode, materialPath, node):

    newGeoNode.parm("shop_materialpath").set(materialPath)

    newGeoNode.parm("RS_objprop_rstess_enable").set(1)
    newGeoNode.parm("RS_objprop_rstess_melenght").set(0)
    newGeoNode.parm("RS_objprop_rstess_maxsubd").set(2)
    newGeoNode.parm("RS_objprop_rstess_smoothBound").set(0)

    newGeoNode.parm("RS_objprop_displace_enable").set(1)
    newGeoNode.parm("RS_objprop_displace_scale").set(0.001)

    # join up nodes

    newGeoNode.setInput(0, node, 0)

def init():

    #path = hou.ui.selectFile(None, "select sbsar file", False,hou.fileType.Any, file_types: Collection[hou.fileType], None, None, False, None, hou.fileChooserMode.Read, 800, 800)
    path = hou.ui.selectFile(
    start_directory=None, 
    title="select sbsar file", 
    collapse_sequences=False, 
    file_type=hou.fileType.Any, 
    pattern=None, 
    default_value=None, 
    multiple_select=False, 
    image_chooser=None, 
    chooser_mode=hou.fileChooserMode.Read, 
    width=800, 
    height=800
    )
    #filePath = hou.ui.selectFile(None, "select sbsar file", False,hou.fileType.Any, None, None, False, None, hou.fileChooserMode.Read, 800, 800)

    # user selects cop 
        
    bakeCOPmaps(path)

    sbsarName = os.path.basename(path)

    materialPath = createRSMaterials(sbsarName)

init()