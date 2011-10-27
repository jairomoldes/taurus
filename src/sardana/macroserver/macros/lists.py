import re

from taurus.console import Alignment
from taurus.console.list import List
from sardana.macroserver.macro import *

Left, Right, HCenter = Alignment.Left, Alignment.Right, Alignment.HCenter

################################################################################
#
# List of elements related macros
#
################################################################################

class _ls(Macro):
    param_def = [
        ['filter',
         ParamRepeat(['filter', Type.String, '.*', 'a regular expression filter'], min=0, max=1),
         '.*', 'a regular expression filter'],
    ]

    def get_column_names(self):
        cols = []
        for col in self.cols:
            if isinstance(col, tuple):
                col = col[0]
            cols.append(col)
        return cols
    
    def get_column_members(self):
        cols = []
        for col in self.cols:
            if isinstance(col, tuple):
                col = col[1]
            cols.append(col.lower())
        return cols
    
    def run(self, *filter):
        self.warning('This macro is not intended to be executed directly by the user')
        return

class lsdef(_ls):
    """List all macro definitions"""

    cols  = 'Name', 'Module', 'Brief Description'
    width =     -1,       -1,                  -1
    align =  Right,    Right,                Left

    def run(self, filter):
        
        cols = self.get_column_names()
        out = List(cols, text_alignment=self.align,
                   max_col_width=self.width)
        
        for m in self.getMacros(filter):
            if m.getName().startswith("_"):
                continue
            out.appendRow([m.getName(), m.getModuleName(), m.getBriefDescription()])
        
        for line in out.genOutput():
            self.output(line)


class _lsobj(_ls):
    
    subtype = Macro.All

    cols  = 'Name', 'Type', 'Controller', 'Axis'#, 'State'
    width =     -1,     -1,           -1,     -1#,      -1
    align =  Right,  Right,        Right,  Right#,   Right

    def objs(self, filter):
        return self.findObjs(filter, type_class=self.type, subtype=self.subtype,
                             reserve=False)

    def obj2Row(self, o, cols=None):
        cols = cols or self.get_column_members()
        ret = []
        for col in cols:
            value = getattr(o, col)
            if value is None:
                value = '-----'
            ret.append(value)
        return ret
    
    def run(self, filter):
        objs = self.objs(filter)
        nb = len(objs)
        if nb is 0:
            if self.subtype is Macro.All:
                t = self.type.lower()
            else:
                t = self.subtype.lower()
            self.output('No %ss defined' % t)
            return
        
        cols = self.get_column_names()
        out = List(cols, text_alignment=self.align,
                   max_col_width=self.width)
        objs.sort()
        for obj in objs:
            out.appendRow( self.obj2Row(obj) )
        for line in out.genOutput():
            self.output(line)
    

class lsm(_lsobj):
    """Lists all motors"""
    type = Type.Motor

class lspm(lsm):
    """Lists all existing motors"""
    subtype = 'PseudoMotor'

class lscom(_lsobj):
    """Lists all communication channels"""
    type = Type.ComChannel
    
class lsior(_lsobj):
    """Lists all IORegisters"""
    type = Type.IORegister

class lsexp(_lsobj):
    """Lists all experiment channels"""
    type = Type.ExpChannel
    
class lsct(lsexp):
    """Lists all Counter/Timers"""
    subtype = 'CounterTimer'
    
class ls0d(lsexp):
    """Lists all 0D experiment channels"""
    subtype = 'ZeroDExpChannel'
    
class ls1d(lsexp):
    """Lists all 1D experiment channels"""
    subtype = 'OneDExpChannel'

class ls2d(lsexp):
    """Lists all 2D experiment channels"""
    subtype = 'TwoDExpChannel'

class lspc(lsexp):
    """Lists all pseudo counters"""
    subtype = 'PseudoCounter'

class lsctrllib(_lsobj):
    """Lists all existing controller classes"""
    type = Type.ControllerClass
    cols = 'Name', 'Type', 'Library', 'Family'

class lsctrl(_lsobj):
    """Lists all existing controllers"""
    type = Type.Controller
    cols = 'Name', 'Type', 'Class', 'Module'

class lsi(_lsobj):
    """Lists all existing instruments"""
    type = Type.Instrument
    cols = 'Name', 'Type', ('Parent', 'parent_instrument')

class lsa(_lsobj):
    """Lists all existing objects"""
    type = (Type.Motor, Type.ComChannel, Type.ExpChannel, Type.IORegister)
    
class lsmeas(_lsobj):
    """List existing measurement groups"""

    type = Type.MeasurementGroup

    cols  = 'Active', 'Name', 'Timer', 'Experim. channels'
    width =       -1,     -1,      -1,                  50
    align =  HCenter,  Right,   Right,                Left
    
    def prepare(self, filter, **opts):
        try:
            self.mnt_grp = self.getEnv('ActiveMntGrp').lower() or None
        except:
            self.mnt_grp = None

    def obj2Row(self, o):
        if self.mnt_grp and (o.getName().lower() == self.mnt_grp):
            active = '*'
        else:
            active = ' '
        return active, o.name, o.getTimerName(), ", ".join(o.getChannelNames())

