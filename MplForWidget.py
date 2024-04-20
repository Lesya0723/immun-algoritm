from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanavas


class MyMplCanavas(FigureCanavas):
    def __init__(self,fig,parent=None):
        self.fig = fig
        FigureCanavas.__init__(self,self.fig)
        FigureCanavas.selfSizePolicy(self, QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanavas.updateGeometry(self)
