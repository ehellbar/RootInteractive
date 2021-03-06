from RootInteractive.InteractiveDrawing.bokeh.bokehDraw import *
from RootInteractive.Tools.aliTreePlayer import *
import sys
import pytest
from bokeh.io import curdoc

if "ROOT" not in sys.modules:
    pytest.skip("ROOT module is not imported", allow_module_level=True)

#gSystem.Load("$ALICE_ROOT/lib/libSTAT.so")
from ROOT import TFile, gSystem

curdoc().theme = 'caliber'

if "ROOT" in sys.modules:
    TFile.SetCacheFileDir("../../data/")
    treeQA, treeList, fileList = LoadTrees("echo https://aliqat.web.cern.ch/aliqat/qcml/data/2018/LHC18q/trending_merged_LHC18q_withStatusTree.root", ".*", ".*sta.*", ".*", 0)
    treeQA.RemoveFriend(treeQA.GetFriend("Tstatus"))
    AddMetadata(treeQA, "chunkBegin.isTime", "1")
    AddMetadata(treeQA, "chunkMedian.isTime", "1")
    treeQA.SetAlias("meanMIPErr", "resolutionMIP*0.3")
    treeQA.SetAlias("meanMIPeleErr", "resolutionMIPele*0.3")
    treeQA.SetAlias("resolutionMIPErr", "resolutionMIP*0.02")

    treeQA.RemoveFriend(treeQA.GetFriend("tpcQA"))

varDraw = "(meanMIP,meanMIPele):meanMIPele:resolutionMIP"
varX = "meanMIP:chunkMedian:chunkMedian"
tooltips = [("MIP", "(@meanMIP)"), ("Electron", "@meanMIPele"), ("Global status", "(@global_Outlier,@global_Warning)"),
            ("MIP status(Warning,Outlier,Acc.)", "@MIPquality_Warning,@MIPquality_Outlier,@MIPquality_PhysAcc"), ("Run","@run")]
widgets = "tab.sliders(slider.meanMIP(45,55,0.1,45,55),slider.meanMIPele(50,80,0.2,50,80), slider.resolutionMIP(0,0.15,0.01,0,0.15)),"
widgets += "tab.checkboxGlobal(slider.global_Warning(0,1,1,0,1),checkbox.global_Outlier(0)),"
widgets += "tab.checkboxMIP(slider.MIPquality_Warning(0,1,1,0,1),checkbox.MIPquality_Outlier(0), checkbox.MIPquality_PhysAcc(1))"


def test_bokehDrawQAStandard():
    """
    Standard bok
    :return: None
    """
    QAlayout: str = "((0),(1),(2,x_visible=1),commonX=2,x_visible=1,y_visible=0,plot_height=250,plot_width=1000)"
    bokehDraw(treeQA, "meanMIP>0", "chunkMedian", varDraw, "MIPquality_Warning", widgets, 0, commonX=1, size=6, tooltip=tooltips, x_axis_type='datetime', layout=QAlayout)


def test_bokehDrawQAWithXarray():
    """
    Standard drawing test
    :return: None
    """
    QAlayout: str = '((0,commonX=0),(1),(2,x_visible=1),commonX=2,x_visible=1,y_visible=0,plot_height=250,plot_width=1000)'
    # xxx=bokehDraw(treeQA,"meanMIP>0",varX,"meanMIPele:meanMIPele:resolutionMIP","MIPquality_Warning",widgets,0,size=6,tooltip=tooltips,x_axis_type='datetime',layout=layout)
    bokehDraw(treeQA, "meanMIP>0", varX, "meanMIPele:meanMIPele:resolutionMIP", "MIPquality_Warning", widgets, 0, size=6, tooltip=tooltips, layout=QAlayout)


def test_bokehDrawQAYerr():
    """
    Test with error bars
    :return: None
    """
    QAlayout: str = "((0),(1),(2,x_visible=1),commonX=2,x_visible=1,y_visible=0,plot_height=250,plot_width=1000)"
    xxxErr = bokehDraw(treeQA, "meanMIP>0", "chunkMedian", "meanMIP:meanMIPele:resolutionMIP", "MIPquality_Warning",
                       widgets, 0, errY="meanMIPErr:meanMIPeleErr:resolutionMIPErr", commonX=1, size=6, tooltip=tooltips, x_axis_type='datetime', layout=QAlayout)

#test_bokehDrawQAStandard()
#test_bokehDrawQAWithXarray()
#test_bokehDrawQAYerr()
