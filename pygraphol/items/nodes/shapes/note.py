# -*- coding: utf-8 -*-

##########################################################################
#                                                                        #
#  pyGraphol: a python design tool for the Graphol language.             #
#  Copyright (C) 2015 Daniele Pantaleone <danielepantaleone@me.com>      #
#                                                                        #
#  This program is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by  #
#  the Free Software Foundation, either version 3 of the License, or     #
#  (at your option) any later version.                                   #
#                                                                        #
#  This program is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          #
#  GNU General Public License for more details.                          #
#                                                                        #
#  You should have received a copy of the GNU General Public License     #
#  along with this program. If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################
#                                                                        #
#  Graphol is developed by members of the DASI-lab group of the          #
#  Dipartimento di Informatica e Sistemistica "A.Ruberti" at Sapienza    #
#  University of Rome: http://www.dis.uniroma1.it/~graphol/:             #
#                                                                        #
#     - Domenico Lembo <lembo@dis.uniroma1.it>                           #
#     - Marco Console <console@dis.uniroma1.it>                          #
#     - Valerio Santarelli <santarelli@dis.uniroma1.it>                  #
#     - Domenico Fabio Savo <savo@dis.uniroma1.it>                       #
#                                                                        #
##########################################################################


from pygraphol.functions import snapPointToGrid
from pygraphol.items.nodes.shapes.common import Label
from pygraphol.items.nodes.shapes.mixins import ShapeResizableMixin
from PyQt5.QtCore import QPointF, Qt, QRectF
from PyQt5.QtGui import QColor, QPen,  QPainterPath, QPolygonF, QPainter, QPixmap, QFont
from PyQt5.QtWidgets import QGraphicsPolygonItem


class Note(QGraphicsPolygonItem, ShapeResizableMixin):
    """
    This class implements an note shape which is used to render the 'Value-Restriction' node.
    """
    FoldSize = 12.0
    MinWidth = 140.0
    MinHeight = 60.0

    indexTR = 0
    indexTL = 1
    indexBL = 2
    indexBR = 3
    indexRT = 4
    indexEE = 5

    shapePen = QPen(QColor(0, 0, 0), 1.1, Qt.SolidLine)

    def __init__(self, **kwargs):
        """
        Initialize the octagon shape.
        """
        shape_w = max(kwargs.pop('width', self.MinWidth), self.MinWidth)
        shape_h = max(kwargs.pop('height', self.MinHeight), self.MinHeight)

        super().__init__(**kwargs)

        # initialize the polygon
        self.setPolygon(Note.getPolygon(shape_w, shape_h, Note.FoldSize))

        # initialize shape label with default text
        self.label = Label(self.node.name, parent=self)

        # calculate positions
        self.updateHandlesPos()
        self.updateLabelPos()

    ################################################## EVENT HANDLERS ##################################################

    def contextMenuEvent(self, menuEvent):
        """
        Bring up the context menu for the given node.
        :param menuEvent: the context menu event instance.
        """
        scene = self.scene()
        scene.clearSelection()

        self.setSelected(True)

        contextMenu = self.contextMenu()

        collection = self.label.contextMenuAdd()
        if collection:
            contextMenu.addSeparator()
            for action in collection:
                contextMenu.addAction(action)

        contextMenu.exec_(menuEvent.screenPos())

    ##################################################### GEOMETRY #####################################################

    def boundingRect(self):
        """
        Returns the shape bounding rectangle.
        :rtype: QRectF
        """
        polygon = self.polygon()
        offset = self.handleSize + self.handleSpan
        x = polygon[self.indexTL].x()
        y = polygon[self.indexTL].y()
        w = polygon[self.indexBR].x() - x
        h = polygon[self.indexBL].y() - y
        return QRectF(x - offset, y - offset, w + offset * 2, h + offset * 2)

    def interactiveResize(self, handle, fromRect, mousePressedPos, mousePos):
        """
        Handle the interactive resize of the shape.
        :type handle: int
        :type fromRect: QRectF
        :type mousePressedPos: QPointF
        :type mousePos: QPointF
        :param handle: the currently selected resizing handle.
        :param fromRect: the bouding rect before the resizing operation started.
        :param mousePressedPos: the position where the mouse has been pressed.
        :param mousePos: the current mouse position.
        """
        scene = self.scene()
        toPoly = self.polygon()
        toRect = self.boundingRect()
        doSnap = scene.settings.value('scene/snap_to_grid', False, bool)
        offset = self.handleSize + self.handleSpan
        fold = self.FoldSize

        minBoundingRectWidth = self.MinWidth + (self.handleSize + self.handleSpan) * 2
        minBoundingRectHeight = self.MinHeight + (self.handleSize + self.handleSpan) * 2

        if handle == self.handleTL:

            newX = fromRect.left() + mousePos.x() - mousePressedPos.x()
            newY = fromRect.top() + mousePos.y() - mousePressedPos.y()
            newX = snapPointToGrid(newX, scene.GridSize, -offset, doSnap)
            newY = snapPointToGrid(newY, scene.GridSize, -offset, doSnap)
            toRect.setLeft(newX)
            toRect.setTop(newY)

            ## CLAMP SIZE
            if toRect.width() < minBoundingRectWidth:
                toRect.setLeft(toRect.left() - minBoundingRectWidth + toRect.width())
            if toRect.height() < minBoundingRectHeight:
                toRect.setTop(toRect.top() - minBoundingRectHeight + toRect.height())

            toPoly[self.indexTL] = QPointF(toRect.left() + offset, toRect.top() + offset)
            toPoly[self.indexBL] = QPointF(toRect.left() + offset, toPoly[self.indexBL].y())
            toPoly[self.indexTR] = QPointF(toPoly[self.indexTR].x(), toRect.top() + offset)
            toPoly[self.indexRT] = QPointF(toPoly[self.indexRT].x(), toRect.top() + offset + fold)
            toPoly[self.indexEE] = QPointF(toPoly[self.indexEE].x(), toRect.top() + offset)

        elif handle == self.handleTM:

            newY = fromRect.top() + mousePos.y() - mousePressedPos.y()
            newY = snapPointToGrid(newY, scene.GridSize, -offset, doSnap)
            toRect.setTop(newY)

            ## CLAMP SIZE
            if toRect.height() < minBoundingRectHeight:
                toRect.setTop(toRect.top() - minBoundingRectHeight + toRect.height())

            toPoly[self.indexTL] = QPointF(toPoly[self.indexTL].x(), toRect.top() + offset)
            toPoly[self.indexTR] = QPointF(toPoly[self.indexTR].x(), toRect.top() + offset)
            toPoly[self.indexRT] = QPointF(toPoly[self.indexRT].x(), toRect.top() + offset + fold)
            toPoly[self.indexEE] = QPointF(toPoly[self.indexEE].x(), toRect.top() + offset)

        elif handle == self.handleTR:

            newX = fromRect.right() + mousePos.x() - mousePressedPos.x()
            newY = fromRect.top() + mousePos.y() - mousePressedPos.y()
            newX = snapPointToGrid(newX, scene.GridSize, +offset, doSnap)
            newY = snapPointToGrid(newY, scene.GridSize, -offset, doSnap)
            toRect.setRight(newX)
            toRect.setTop(newY)

            ## CLAMP SIZE
            if toRect.width() < minBoundingRectWidth:
                toRect.setRight(toRect.right() + minBoundingRectWidth - toRect.width())
            if toRect.height() < minBoundingRectHeight:
                toRect.setTop(toRect.top() - minBoundingRectHeight + toRect.height())

            toPoly[self.indexTL] = QPointF(toPoly[self.indexTL].x(), toRect.top() + offset)
            toPoly[self.indexTR] = QPointF(toRect.right() + offset - fold, toRect.top() + offset)
            toPoly[self.indexRT] = QPointF(toRect.right() + offset, toRect.top() + offset + fold)
            toPoly[self.indexBR] = QPointF(toRect.right() + offset, toPoly[self.indexBR].y())
            toPoly[self.indexEE] = QPointF(toRect.right() + offset - fold, toRect.top() + offset)

        elif handle == self.handleML:

            newX = fromRect.left() + mousePos.x() - mousePressedPos.x()
            newX = snapPointToGrid(newX, scene.GridSize, -offset, doSnap)
            toRect.setLeft(newX)

            ## CLAMP SIZE
            if toRect.width() < minBoundingRectWidth:
                toRect.setLeft(toRect.left() - minBoundingRectWidth + toRect.width())

            toPoly[self.indexTL] = QPointF(toRect.left() + offset, toPoly[self.indexTL].y())
            toPoly[self.indexBL] = QPointF(toRect.left() + offset, toPoly[self.indexBL].y())

        elif handle == self.handleMR:

            newX = fromRect.right() + mousePos.x() - mousePressedPos.x()
            newX = snapPointToGrid(newX, scene.GridSize, +offset, doSnap)
            toRect.setRight(newX)

            ## CLAMP SIZE
            if toRect.width() < minBoundingRectWidth:
                toRect.setRight(toRect.right() + minBoundingRectWidth - toRect.width())

            toPoly[self.indexTR] = QPointF(toRect.right() + offset - fold, toPoly[self.indexTR].y())
            toPoly[self.indexRT] = QPointF(toRect.right() + offset, toPoly[self.indexRT].y())
            toPoly[self.indexBR] = QPointF(toRect.right() + offset, toPoly[self.indexBR].y())
            toPoly[self.indexEE] = QPointF(toRect.right() + offset - fold, toPoly[self.indexEE].y())

        elif handle == self.handleBL:

            newX = fromRect.left() + mousePos.x() - mousePressedPos.x()
            newY = fromRect.bottom() + mousePos.y() - mousePressedPos.y()
            newX = snapPointToGrid(newX, scene.GridSize, -offset, doSnap)
            newY = snapPointToGrid(newY, scene.GridSize, +offset, doSnap)
            toRect.setLeft(newX)
            toRect.setBottom(newY)

            ## CLAMP SIZE
            if toRect.width() < minBoundingRectWidth:
                toRect.setLeft(toRect.left() - minBoundingRectWidth + toRect.width())
            if toRect.height() < minBoundingRectHeight:
                toRect.setBottom(toRect.bottom() + minBoundingRectHeight - toRect.height())

            toPoly[self.indexTL] = QPointF(toRect.left() + offset, toPoly[self.indexTL].y())
            toPoly[self.indexBL] = QPointF(toRect.left() + offset, toRect.bottom() + offset)
            toPoly[self.indexBR] = QPointF(toPoly[self.indexBR].x(), toRect.bottom() + offset)

        elif handle == self.handleBM:

            newY = fromRect.bottom() + mousePos.y() - mousePressedPos.y()
            newY = snapPointToGrid(newY, scene.GridSize, +offset, doSnap)
            toRect.setBottom(newY)

            ## CLAMP SIZE
            if toRect.height() < minBoundingRectHeight:
                toRect.setBottom(toRect.bottom() + minBoundingRectHeight - toRect.height())

            toPoly[self.indexBL] = QPointF(toPoly[self.indexBL].x(), toRect.bottom() + offset)
            toPoly[self.indexBR] = QPointF(toPoly[self.indexBR].x(), toRect.bottom() + offset)

        elif handle == self.handleBR:

            newX = fromRect.right() + mousePos.x() - mousePressedPos.x()
            newY = fromRect.bottom() + mousePos.y() - mousePressedPos.y()
            newX = snapPointToGrid(newX, scene.GridSize, +offset, doSnap)
            newY = snapPointToGrid(newY, scene.GridSize, +offset, doSnap)
            toRect.setRight(newX)
            toRect.setBottom(newY)

            ## CLAMP SIZE
            if toRect.width() < minBoundingRectWidth:
                toRect.setRight(toRect.right() + minBoundingRectWidth - toRect.width())
            if toRect.height() < minBoundingRectHeight:
                toRect.setBottom(toRect.bottom() + minBoundingRectHeight - toRect.height())

            toPoly[self.indexBL] = QPointF(toPoly[self.indexBL].x(), toRect.bottom() + offset)
            toPoly[self.indexBR] = QPointF(toRect.right() + offset, toRect.bottom() + offset)
            toPoly[self.indexTR] = QPointF(toRect.right() + offset - fold, toPoly[self.indexTR].y())
            toPoly[self.indexRT] = QPointF(toRect.right() + offset, toPoly[self.indexRT].y())
            toPoly[self.indexEE] = QPointF(toRect.right() + offset - fold, toPoly[self.indexEE].y())

        self.prepareGeometryChange()
        self.setPolygon(toPoly)
        self.updateHandlesPos()
        self.updateLabelPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        :rtype: QPainterPath
        """
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    ################################################ AUXILIARY METHODS #################################################

    @staticmethod
    def getPolygon(shape_w, shape_h, fold_size):
        """
        Returns the initialized polygon according to the given width/height.
        :param shape_w: the shape width.
        :param shape_h: the shape height.
        :param fold_size: the width of the fold.
        :rtype: QPolygonF
        """
        return QPolygonF([
            QPointF(+(shape_w / 2) - fold_size, -(shape_h / 2)),  # 0
            QPointF(-(shape_w / 2), -(shape_h / 2)),              # 1
            QPointF(-(shape_w / 2), +(shape_h / 2)),              # 2
            QPointF(+(shape_w / 2), +(shape_h / 2)),              # 3
            QPointF(+(shape_w / 2), -(shape_h / 2) + fold_size),  # 4
            QPointF(+(shape_w / 2) - fold_size, -(shape_h / 2)),  # 5
        ])

    @staticmethod
    def getFold(polygon, fold_size):
        """
        Returns the initialized fold polygon.
        :param polygon: the initialize shape polygon.
        :param fold_size: the width of the fold.
        :rtype: QPolygonF
        """
        return QPolygonF([
            QPointF(polygon[Note.indexTR].x(), polygon[Note.indexTR].y()),
            QPointF(polygon[Note.indexTR].x(), polygon[Note.indexTR].y() + fold_size),
            QPointF(polygon[Note.indexRT].x(), polygon[Note.indexRT].y()),
            QPointF(polygon[Note.indexTR].x(), polygon[Note.indexTR].y()),
        ])

    def height(self):
        """
        Returns the height of the shape.
        :rtype: int
        """
        return self.boundingRect().height() - 2 * (self.handleSize + self.handleSpan)

    def width(self):
        """
        Returns the width of the shape.
        :rtype: int
        """
        return self.boundingRect().width() - 2 * (self.handleSize + self.handleSpan)

    ################################################### ITEM DRAWING ###################################################
    
    @classmethod
    def image(cls, **kwargs):
        """
        Returns an image suitable for the palette.
        :rtype: QPixmap
        """
        shape_w = 54
        shape_h = 34
        fold_size = 10

        # Initialize the pixmap
        pixmap = QPixmap(kwargs['w'], kwargs['h'])
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)

        # Initialize the shape
        polygon = Note.getPolygon(shape_w, shape_h, fold_size)

        # Initialize the fold
        fold = Note.getFold(polygon, fold_size)

        # Draw the polygon
        painter.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        painter.setBrush(QColor(252, 252, 252))
        painter.translate(kwargs['w'] / 2, kwargs['h'] / 2)
        painter.drawPolygon(polygon)
        painter.drawPolygon(fold)

        # Draw the text within the rectangle
        painter.setFont(QFont('Arial Narrow', 11, QFont.Light))
        painter.drawText(polygon.boundingRect(), Qt.AlignCenter, 'value\nrestriction')

        return pixmap
    
    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        :param painter: the active painter.
        :param option: the style option for this item.
        :param widget: the widget that is being painted on.
        """
        # Select the correct brush for the shape
        shapeBrush = self.shapeSelectedBrush if self.isSelected() else self.shapeBrush

        # Draw the polygon
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(shapeBrush)
        painter.setPen(self.shapePen)
        painter.drawPolygon(self.polygon())

        # Draw the fold
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(shapeBrush)
        painter.setPen(self.shapePen)
        painter.drawPolygon(Note.getFold(self.polygon(), Note.FoldSize))

        if self.isSelected():
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setBrush(self.handleBrush)
            painter.setPen(self.handlePen)
            for handle, rect in self.handles.items():
                if self.selectedHandle is None or handle == self.selectedHandle:
                    painter.drawEllipse(rect)