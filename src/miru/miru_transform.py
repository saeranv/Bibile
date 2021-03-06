"""----------------
Miru Stepback
----------------""" 
import copy
import scriptcontext as sc
import rhinoscriptsyntax as rs
import clr
Grammar = sc.sticky["Grammar"]

clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree

if run:

    rule = DataTree[object]()
    rule_ = [\
    ['transform', True],\
    ['grammar_key','transform'],\
    ['transform_move', move_vector],\
    ['end_rule']]
    
    for i, r in enumerate(rule_):
        rule.Add(r)
else:
    rule = []
