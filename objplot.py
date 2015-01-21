#coding: gbk
import sys
import math
import os

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import main_ui

import numpy as np
import pyqtgraph as pg


class Main(QMainWindow, main_ui.Ui_MainWindow):
	def __init__(self, parent=None):
		super(Main, self).__init__(parent)
		self.setupUi(self)
		self._initUi()
		
		self.data = {}
		self.sorted_key = []
		self.plots = {}

		self.listModel = QStandardItemModel(self.listView)
		self.listView.setModel(self.listModel)

		self._initEvents()

	def _initUi(self):
		self.plotWidget = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
		self.plotLayout.addWidget(self.plotWidget)
		self.plotWidget.setMouseEnabled(x=False, y=False)
		self.plotWidget.enableAutoRange(pg.ViewBox.XYAxes, True, True, True)

	def _initEvents(self):
		self.action_load.triggered.connect(self._load)
		self.listModel.itemChanged.connect(self.on_item_changed)

	def on_item_changed(self, item):
		key = str(item.text())
	
		if not item.checkState():
			del self.plots[key]
		else:
			self.plots[key] = True
		
		cnt = 0
		self.plotWidget.plotItem.clear()
		for k in self.plots.keys():
			data = self.data[k]
			xd = range(len(data))
			self.plotWidget.plot(y=data, x=xd, pen=(cnt, 20))
			cnt += 1

	def _load(self):
		self.data = {}
		self.sorted_key = []
		fileName = QFileDialog.getOpenFileName(self, u"打开pyobjs.txt文件", u"", u"文件(*.txt)")
		if fileName:
			with open(fileName, 'r') as fp:
				for line in fp:
					line_data = line.strip().split('\t')
					key = line_data[0]
					self.sorted_key.append(key)
					self.data[key] = [int(cnt) for cnt in line_data[1:]]
		self._updateUI()

	def _updateUI(self):
		self.listModel.clear()
		for k in self.sorted_key:
			item = QStandardItem(k)
			item.setCheckable(True)
			self.listModel.appendRow(item)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = Main()
	main.show()
	app.exec_()
