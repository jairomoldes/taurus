import sys
from taurus.qt.qtgui.panel import TaurusForm
from taurus.qt.qtgui.display import TaurusLabel
from taurus.qt.qtgui.application import TaurusApplication

app = TaurusApplication(sys.argv, cmd_line_parser=None)

panel = TaurusForm()
props = ['state', 'status', 'position', 'velocity', 'acceleration']
model = ['sys/taurustest/1/%s' % p for p in props]
panel.setModel(model)
panel[0].readWidgetClass = TaurusLabel
panel[2].writeWidgetClass = 'TaurusWheelEdit'

panel.show()
sys.exit(app.exec_())
