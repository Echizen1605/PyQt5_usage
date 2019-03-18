# coding:utf-8
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QStatusBar, \
							QLineEdit, \
							QSlider,\
							QHBoxLayout,\
							QVBoxLayout,\
							QGroupBox,\
							QWidget,\
							QApplication,\
							QComboBox,\
							QPushButton,\
							QFormLayout,\
							QMainWindow,\
							QDesktopWidget,\
							QColorDialog,\
							QFileDialog,\
							QAction,\
							QStyle

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont


# pyqt结合matplotlib的中介
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# matplotlib中文问题
matplotlib.use('qt4agg')
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
matplotlib.rcParams['axes.unicode_minus'] = False

class Config(QWidget):
	def __init__(self):
		super(Config, self).__init__()
		config_group = QtWidgets.QGroupBox(u"参数配置")
		lineconfig_group = QtWidgets.QGroupBox(u"线条风格配置")
		axisconfig_group = QtWidgets.QGroupBox(u"坐标轴风格配置")
		lineshow_group = QtWidgets.QGroupBox(u"线条风格预览")
		result_group = QtWidgets.QGroupBox(u"结果展示")

		# 当前绘图结果
		self.fig = None

		# 当前绘图总数据保存
		# 坐标轴信息
		self.min_x = 0.
		self.max_x = 1.
		self.min_y = 0.
		self.max_y = 1.
		self.x_text = u'The number of retrived samples'
		self.y_text = u'precision @ 256 bins'
		self.x_tick_list = [0., 0.5, 1.]
		self.x_label_list = ['0', '0.5', '1.0']
		self.y_tick_list = [0., 0.5, 1.]
		self.y_label_list = ['0', '0.5', '1.0']
		# 已有曲线信息
		self.formula_list = []
		self.ls_list = []
		self.lc_list = []
		self.lt_list = []
		self.mark_list = []
		self.mark_density_list = []

		# 当前绘图曲线元数据保存
		self.ls = '-'
		self.mark = 'o'
		self.formula = 'y=x**2'
		self.lc = '#00ff00'
		self.lt = 'Our Method'
		self.md = 5

		# 状态栏
		self.statusBar = QStatusBar()
		self.statusBar.setFont(QFont(u'华文楷体', 10))
		self.statusBar.showMessage(u"准备就绪")

		# 编辑公式
		self.math = QLineEdit()
		self.math.setPlaceholderText(u'输入线条公式')
		self.math.setClearButtonEnabled(True)

		# 线条风格
		self.linestyle = QComboBox()
		line_list = ["-", "--", "-.", ":"]
		for each in line_list:
			self.linestyle.addItem(each)

		# 标记风格
		self.markerstyle = QComboBox()
		marker_list = [".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4"
		"s", "p", "*", "h", "H", "+", "x", "D", "d", "|", "_"]
		for each in marker_list:
			self.markerstyle.addItem(each)

		# 设置线条标签名称
		self.label = QLineEdit()
		self.label.setPlaceholderText(u'Our Method')
		self.label.setClearButtonEnabled(True)

		# 设置线条颜色
		self.lineColor = QPushButton('更改线条颜色')
		self.lineColor.setToolTip("点击此按钮将更改线条颜色！")
		self.lineColor.setStatusTip("点击此按钮将更改线条颜色！")
		self.lineColor.clicked.connect(self.changeColor)
		self.lineColor.resize(self.lineColor.sizeHint())
		self.lineColor.installEventFilter(self)

		# 设置标记密集程度
		self.markDensity = QSlider(Qt.Horizontal)
		self.markDensity.setMinimum(1)
		self.markDensity.setMaximum(50)
		self.markDensity.setValue(5)
		self.markDensity.installEventFilter(self)

		# 横坐标轴范围
		self.x_scale = QLineEdit()
		self.x_scale.setPlaceholderText(u'输入横坐标轴最小和最大范围，以逗号分隔，如：0,1')
		self.x_scale.setClearButtonEnabled(True)

		# 纵坐标轴范围
		self.y_scale = QLineEdit()
		self.y_scale.setPlaceholderText(u'输入纵坐标轴最小和最大范围，以逗号分隔，如：0,1')
		self.y_scale.setClearButtonEnabled(True)

		# 横坐标轴标签名称
		self.x_label = QLineEdit()
		self.x_label.setPlaceholderText(u'The number of retrived samples')
		self.x_label.setClearButtonEnabled(True)

		# 纵坐标轴标签名称
		self.y_label = QLineEdit()
		self.y_label.setPlaceholderText(u'precision @ 256 bins')
		self.y_label.setClearButtonEnabled(True)

		# 横坐标刻度
		self.x_ticks = QLineEdit()
		self.x_ticks.setPlaceholderText(u'输入刻度名称，以逗号分隔，如0,0.5,1.0')
		self.x_ticks.setClearButtonEnabled(True)

		# 纵坐标刻度
		self.y_ticks = QLineEdit()
		self.y_ticks.setPlaceholderText(u'输入刻度名称，以逗号分隔，如0,0.5,1.0')
		self.y_ticks.setClearButtonEnabled(True)

		# 线条风格预览按钮
		self.lineview = QPushButton(u'预览')
		self.lineview.setToolTip("线条预览！")
		self.lineview.setStatusTip("线条预览！")
		self.lineview.clicked.connect(self.showLine)
		self.lineview.installEventFilter(self)


		# 布局设置
		main_layout = QVBoxLayout()

		# 参数外层布局
		config_outer_layout = QVBoxLayout()

		# 参数内层布局配置
		config_inner_layout = QHBoxLayout()
		config_inner_layout.addWidget(lineconfig_group)
		config_inner_layout.setStretchFactor(lineconfig_group, 1)
		config_inner_layout.addWidget(axisconfig_group)
		config_inner_layout.setStretchFactor(axisconfig_group, 1)
		config_inner_layout.addWidget(lineshow_group)
		config_inner_layout.setStretchFactor(lineshow_group, 1)

		# 线条布局
		line_layout = QFormLayout()
		line_layout.addRow(u'编辑公式', self.math)
		line_layout.addRow(u'线条风格', self.linestyle)
		line_layout.addRow(u'标记风格', self.markerstyle)
		line_layout.addRow(u'标签名称', self.label)
		line_layout.addRow(u'颜色配置', self.lineColor)
		line_layout.addRow(u'标记密度', self.markDensity)
		lineconfig_group.setLayout(line_layout)

		# 坐标轴布局
		tick_layout = QFormLayout()
		tick_layout.addRow(u'横坐标轴范围', self.x_scale)
		tick_layout.addRow(u'纵坐标轴范围', self.y_scale)
		tick_layout.addRow(u'横坐标轴标签名称', self.x_label)
		tick_layout.addRow(u'纵坐标轴标签名称', self.y_label)
		tick_layout.addRow(u'横坐标刻度', self.x_ticks)
		tick_layout.addRow(u'纵坐标刻度', self.y_ticks)
		axisconfig_group.setLayout(tick_layout)

		# 预览布局
		view = QVBoxLayout()

		# 预览显示
		self.view_face = QMainWindow()
		view.addWidget(self.view_face)
		# 预览按钮
		view.addWidget(self.lineview)
		lineshow_group.setLayout(view)

		# 中层按钮定义
		# 按钮一：显示最终结果
		# 按钮二：添加新的线条
		# 按钮三：删除最近一条线条
		self.showresult = QPushButton(u'刷新视图')
		self.showresult.setToolTip(u'刷新视图！')
		self.showresult.clicked.connect(self.resultShow)
		self.showresult.installEventFilter(self)

		self.addline = QPushButton(u'新增线条')
		self.addline.setToolTip(u'新增一条曲线！')
		self.addline.clicked.connect(self.addLine)
		self.addline.installEventFilter(self)

		self.removeline = QPushButton(u'删除线条')
		self.removeline.setToolTip(u'删除最近一条曲线！')
		self.removeline.clicked.connect(self.removeLine)
		self.removeline.installEventFilter(self)

		self.savefig = QPushButton(u'保存结果')
		self.savefig.setToolTip(u'将当前结果保存为高清图片！')
		self.savefig.clicked.connect(self.saveFig)
		self.savefig.installEventFilter(self)


		# 中层按钮布局
		center_layout = QHBoxLayout()
		center_layout.addWidget(self.showresult)
		center_layout.addWidget(self.addline)
		center_layout.addWidget(self.removeline)
		center_layout.addWidget(self.savefig)

		# 下层状态栏
		bottom_layout = QVBoxLayout()
		bottom_layout.addWidget(self.statusBar)

		config_outer_layout.addItem(config_inner_layout)
		config_outer_layout.addItem(center_layout)
		config_outer_layout.addItem(bottom_layout)

		config_group.setLayout(config_outer_layout)

		# 结果展示栏，设置为mainWindow
		result = QVBoxLayout()
		self.result = QMainWindow()
		result.addWidget(self.result)
		result_group.setLayout(result)

		main_layout.addWidget(config_group)
		main_layout.setStretchFactor(config_group, 1)
		main_layout.addWidget(result_group)
		main_layout.setStretchFactor(result_group, 2)
		self.setLayout(main_layout)

		cp = QDesktopWidget().availableGeometry().center()
		window_width = int(cp.x()*2*0.7)
		window_height = int(cp.y()*2*0.7)
		self.setGeometry(cp.x()-window_width//2, cp.y()-window_height//2, window_width, window_height)

	def changeColor(self):
		col = QColorDialog.getColor()
		if col.isValid():
			self.lc = col.name()


	def showLine(self):
		# self.view_face.setFixedWidth(230)
		# self.view_face.setSizePolicy(self.view_face.sizeHint())
		# 获取参数
		self.formula = self.math.text()
		if self.formula == "":
			self.formula = self.math.placeholderText()
		self.ls = self.linestyle.currentText()
		self.mark = self.markerstyle.currentText()
		self.lt = self.label.text()
		if self.lt == "":
			self.lt = self.label.placeholderText()
		self.md = self.markDensity.value()

		x0 = np.linspace(0, 1, 100)
		try:
			formula_str = self.formula.split('=')[1]
			y0 = [eval(formula_str) for x in x0]
		except Exception as ex:
			return
		plt.cla()
		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		ax.plot(x0, y0, color=self.lc, ls=self.ls, marker=self.mark, label=self.lt, markevery=self.md)
		ax.legend(loc='best')
		self.fig = fig
		canvas = FigureCanvas(fig)
		self.view_face.setCentralWidget(canvas)


	def resultShow(self):
		try:
			x_scale_text = self.x_scale.text()
			if x_scale_text == "":
				x_scale_text = self.x_scale.placeholderText()
			self.min_x, self.max_x = [float(k.strip()) for k in x_scale_text.strip().split(',')]
		except Exception as ex:
			pass

		try:
			y_scale_text = self.y_scale.text()
			if y_scale_text == "":
				y_scale_text = self.y_scale.placeholderText()
			self.min_y, self.max_y = [float(k.strip()) for k in y_scale_text.strip().split(',')]
		except Exception as ex:
			pass

		self.x_text = self.x_label.text()
		if self.x_text == "":
			self.x_text = self.x_label.placeholderText()
		self.y_text = self.y_label.text()
		if self.y_text == "":
			self.y_text = self.y_label.placeholderText()

		try:
			x_tick_str = self.x_ticks.text()
			if x_tick_str == "":
				x_tick_str = self.x_ticks.placeholderText()
			self.x_label_list = [k.strip() for k in x_tick_str.strip().split(',')]
			self.x_tick_list = np.linspace(self.min_x, self.max_x, len(self.x_label_list))
		except Exception as ex:
			pass

		try:
			y_tick_str = self.y_ticks.text()
			if y_tick_str == "":
				y_tick_str = self.y_ticks.placeholderText()
			self.y_label_list = [k.strip() for k in y_tick_str.strip().split(',')]
			self.y_tick_list = np.linspace(self.min_y, self.max_y, len(self.y_label_list))
		except Exception as ex:
			pass

		fig = plt.figure()
		ax = fig.add_subplot(1,1,1)
		for index in range(len(self.formula_list)):
			x0 = np.linspace(self.min_x, self.max_x, 100)
			y0 = [eval(self.formula_list[index].split('=')[1]) for x in x0]
			ax.plot(x0, y0, color=self.lc_list[index], ls=self.ls_list[index], marker=self.mark_list[index], markevery=self.mark_density_list[index], label=self.lt_list[index])
		ax.legend(loc='best')
		ax.set_xticks(self.x_tick_list)
		ax.set_xticklabels(self.x_label_list)
		ax.set_yticks(self.y_tick_list)
		ax.set_yticklabels(self.y_label_list)
		ax.set_xlabel(self.x_text)
		ax.set_ylabel(self.y_text)
		ax.set_xlim(self.min_x, self.max_y)
		ax.set_ylim(self.min_y, self.max_y)
		canvas = FigureCanvas(fig)
		self.result.setCentralWidget(canvas)


	def addLine(self):
		try:
			x = 1
			temp = eval(self.math.text().split('=')[1])
			math_txt = self.math.text()
			if math_txt == "":
				math_txt = self.math.placeholderText()
			self.formula_list.append(math_txt)
			self.ls_list.append(self.linestyle.currentText())
			self.mark_list.append(self.markerstyle.currentText())
			label_txt = self.label.text()
			if label_txt == "":
				label_txt = self.label.placeholderText()
			self.lt_list.append(label_txt)
			self.lc_list.append(self.lc)
			self.mark_density_list.append(self.md)
			self.resultShow()
		except Exception as ex:
			pass


	def removeLine(self):
		try:
			assert(len(self.formula_list) != 0)
			self.formula_list.pop()
			self.ls_list.pop()
			self.mark_list.pop()
			self.lt_list.pop()
			self.lc_list.pop()
			self.mark_density_list.pop()
			self.resultShow()
		except Exception as ex:
			pass


	def saveFig(self):
		dialog = QFileDialog()
		filename, filetype = dialog.getSaveFileName(self, "图像保存", "./result.png"\
                  ,"All Files (*);;JPEG Files (*.jpg);;PNG Files (*.png);;SVG Files (*.svg)")
		if filename!="" and self.fig:
			plt.savefig(filename)


	def eventFilter(self, obj, event):
		if event.type() == QEvent.HoverEnter:
			if obj == self.lineColor:
				self.statusBar.showMessage(u"点击此按钮将更改线条颜色！")
				return False
			elif obj == self.markDensity:
				value = self.markDensity.value()
				self.statusBar.showMessage(str(value))
				return False
			elif obj == self.lineview:
				self.statusBar.showMessage(u"线条预览！")
				return False
			elif obj == self.showresult:
				self.statusBar.showMessage(u"刷新当前视图，重新显示图片！")
				return False
			elif obj == self.addline:
				self.statusBar.showMessage(u'新增一条曲线！')
				return False
			elif obj == self.removeline:
				self.statusBar.showMessage(u'删去最近的一条曲线！')
				return False
			elif obj == self.savefig:
				self.statusBar.showMessage(u'将当前结果保存为高清图片！')
				return False
		elif event.type() == 2 or event.type() == 129:
			if obj == self.markDensity:
				value = self.markDensity.value()
				self.statusBar.showMessage(str(value))
				self.showLine()
				return False
			else:
				return False
		else:
			return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    crawl = Config()
    crawl.show()
    sys.exit(app.exec_())






