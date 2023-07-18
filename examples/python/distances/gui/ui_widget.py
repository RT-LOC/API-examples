# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'widget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(1215, 709)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Widget.sizePolicy().hasHeightForWidth())
        Widget.setSizePolicy(sizePolicy)
        Widget.setStyleSheet(u"")
        self.verticalLayout = QVBoxLayout(Widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.start_button = QPushButton(Widget)
        self.start_button.setObjectName(u"start_button")
        icon = QIcon()
        icon.addFile(u"startButton.png", QSize(), QIcon.Selected, QIcon.Off)
        self.start_button.setIcon(icon)
        self.start_button.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.start_button)

        self.pause_button = QPushButton(Widget)
        self.pause_button.setObjectName(u"pause_button")
        icon1 = QIcon()
        icon1.addFile(u"pauseButton.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pause_button.setIcon(icon1)
        self.pause_button.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.pause_button)

        self.stop_button = QPushButton(Widget)
        self.stop_button.setObjectName(u"stop_button")
        icon2 = QIcon()
        icon2.addFile(u"stopButton.png", QSize(), QIcon.Normal, QIcon.Off)
        self.stop_button.setIcon(icon2)
        self.stop_button.setIconSize(QSize(20, 20))

        self.horizontalLayout.addWidget(self.stop_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.ip_line_edit = QLineEdit(Widget)
        self.ip_line_edit.setObjectName(u"ip_line_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ip_line_edit.sizePolicy().hasHeightForWidth())
        self.ip_line_edit.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.ip_line_edit)

        self.port_line_edit = QLineEdit(Widget)
        self.port_line_edit.setObjectName(u"port_line_edit")
        sizePolicy1.setHeightForWidth(self.port_line_edit.sizePolicy().hasHeightForWidth())
        self.port_line_edit.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.port_line_edit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tabWidget = QTabWidget(Widget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.South)
        self.table_page = QWidget()
        self.table_page.setObjectName(u"table_page")
        self.verticalLayout_2 = QVBoxLayout(self.table_page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.tableWidget = QTableWidget(self.table_page)
        self.tableWidget.setObjectName(u"tableWidget")
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.tableWidget)

        self.tabWidget.addTab(self.table_page, "")
        self.text_page = QWidget()
        self.text_page.setObjectName(u"text_page")
        sizePolicy.setHeightForWidth(self.text_page.sizePolicy().hasHeightForWidth())
        self.text_page.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.text_page)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.textEdit = QTextEdit(self.text_page)
        self.textEdit.setObjectName(u"textEdit")

        self.horizontalLayout_2.addWidget(self.textEdit)

        self.tabWidget.addTab(self.text_page, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(Widget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.start_button.setText("")
        self.pause_button.setText("")
        self.stop_button.setText("")
        self.ip_line_edit.setText("")
        self.ip_line_edit.setPlaceholderText(QCoreApplication.translate("Widget", u"IP-adress", None))
        self.port_line_edit.setPlaceholderText(QCoreApplication.translate("Widget", u"Port", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.table_page), QCoreApplication.translate("Widget", u"cross.py", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.text_page), QCoreApplication.translate("Widget", u"main.py", None))
    # retranslateUi

