"""----------------
Miru Shape Angle
----------------""" 

import copy
import scriptcontext as sc
import clr

clr.AddReference("Grasshopper")
from Grasshopper.Kernel.Data import GH_Path
from Grasshopper import DataTree

if run:

    rule = DataTree[object]()
    rule_ = [\
    ['shape2height', True],\
    ['grammar_key','shape2height'],\
    ['end_rule']]
    
    for i, r in enumerate(rule_):
        rule.Add(r)
else:
    rule = []
    