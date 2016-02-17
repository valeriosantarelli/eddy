# -*- coding: utf-8 -*-

##########################################################################
#                                                                        #
#  Eddy: a graphical editor for the construction of Graphol ontologies.  #
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
#  #####################                          #####################  #
#                                                                        #
#  Graphol is developed by members of the DASI-lab group of the          #
#  Dipartimento di Ingegneria Informatica, Automatica e Gestionale       #
#  A.Ruberti at Sapienza University of Rome: http://www.dis.uniroma1.it/ #
#                                                                        #
#     - Domenico Lembo <lembo@dis.uniroma1.it>                           #
#     - Valerio Santarelli <santarelli@dis.uniroma1.it>                  #
#     - Domenico Fabio Savo <savo@dis.uniroma1.it>                       #
#     - Marco Console <console@dis.uniroma1.it>                          #
#                                                                        #
##########################################################################


from PyQt5.QtCore import QFile, QIODevice, QPointF, QRectF
from PyQt5.QtWidgets import QApplication
from PyQt5.QtXml import QDomDocument

from eddy.core.datatypes import Item
from eddy.core.exceptions import ParseError
from eddy.core.functions import snapF
from eddy.core.loaders.common import AbstractLoader
from eddy.ui.scene import DiagramScene


class GraphmlLoader(AbstractLoader):
    """
    This class can be used to import Graphol ontologies created using the Graphol paletter for yEd.
    """
    def __init__(self, mainwindow, filepath, parent=None):
        """
        Initialize the Graphml importer.
        :type mainwindow: MainWindow
        :type filepath: str
        :type parent: QObject
        """
        super().__init__(mainwindow, filepath, parent)
        self.keys = dict()

    ####################################################################################################################
    #                                                                                                                  #
    #   NODES                                                                                                          #
    #                                                                                                                  #
    ####################################################################################################################

    def buildAttributeNode(self, node):
        """
        Build an Attribute node using the given QDomElement.
        :type node: QDomElement
        :rtype: AttributeNode
        """
        return self.buildNodeFromGenericNode(Item.AttributeNode, node)

    def buildComplementNode(self, node):
        """
        Build a Complement node using the given QDomElement.
        :type node: QDomElement
        :rtype: ComplementNode
        """
        return self.buildNodeFromShapeNode(Item.ComplementNode, node)

    def buildConceptNode(self, node):
        """
        Build a Concept node using the given QDomElement.
        :type node: QDomElement
        :rtype: ConceptNode
        """
        return self.buildNodeFromGenericNode(Item.ConceptNode, node)

    def buildDatatypeRestrictionNode(self, node):
        """
        Build a DatatypeRestriction node using the given QDomElement.
        :type node: QDomElement
        :rtype: DatatypeRestrictionNode
        """
        return self.buildNodeFromShapeNode(Item.DatatypeRestrictionNode, node)

    def buildDisjointUnionNode(self, node):
        """
        Build a DisjointUnion node using the given QDomElement.
        :type node: QDomElement
        :rtype: DisjointUnionNode
        """
        return self.buildNodeFromShapeNode(Item.DisjointUnionNode, node)

    def buildDomainRestrictionNode(self, node):
        """
        Build a DomainRestriction node using the given QDomElement.
        :type node: QDomElement
        :rtype: DomainRestrictionNode
        """
        item = self.buildNodeFromShapeNode(Item.DomainRestrictionNode, node)
        if item:
            data = node.firstChildElement('data')
            while not data.isNull():
                if data.attribute('key', '') == self.keys['node_key']:
                    shapeNode = data.firstChildElement('y:ShapeNode')
                    nodeLabel = shapeNode.firstChildElement('y:NodeLabel')
                    item.setText(nodeLabel.text())
                data = data.nextSiblingElement('data')
        return item

    def buildEnumerationNode(self, node):
        """
        Build an Enumeration node using the given QDomElement.
        :type node: QDomElement
        :rtype: EnumerationNode
        """
        return self.buildNodeFromShapeNode(Item.EnumerationNode, node)

    def buildIndividualNode(self, node):
        """
        Build an Individual node using the given QDomElement.
        :type node: QDomElement
        :rtype: IndividualNode
        """
        item = self.buildNodeFromShapeNode(Item.IndividualNode, node)
        if item:
            data = node.firstChildElement('data')
            while not data.isNull():
                if data.attribute('key', '') == self.keys['node_key']:
                    shapeNode = data.firstChildElement('y:ShapeNode')
                    nodeLabel = shapeNode.firstChildElement('y:NodeLabel')
                    item.setText(nodeLabel.text())
                data = data.nextSiblingElement('data')
        return item

    def buildIntersectionNode(self, node):
        """
        Build an Intersection node using the given QDomElement.
        :type node: QDomElement
        :rtype: IntersectionNode
        """
        return self.buildNodeFromShapeNode(Item.IntersectionNode, node)

    def buildRangeRestrictionNode(self, node):
        """
        Build a RangeRestriction node using the given QDomElement.
        :type node: QDomElement
        :rtype: RangeRestrictionNode
        """
        item = self.buildNodeFromShapeNode(Item.RangeRestrictionNode, node)
        if item:
            data = node.firstChildElement('data')
            while not data.isNull():
                if data.attribute('key', '') == self.keys['node_key']:
                    shapeNode = data.firstChildElement('y:ShapeNode')
                    nodeLabel = shapeNode.firstChildElement('y:NodeLabel')
                    item.setText(nodeLabel.text())
                data = data.nextSiblingElement('data')
        return item

    def buildRoleNode(self, node):
        """
        Build a Role node using the given QDomElement.
        :type node: QDomElement
        :rtype: RoleNode
        """
        return self.buildNodeFromGenericNode(Item.RoleNode, node)

    def buildRoleChainNode(self, node):
        """
        Build a RoleChain node using the given QDomElement.
        :type node: QDomElement
        :rtype: RoleChainNode
        """
        return self.buildNodeFromShapeNode(Item.RoleChainNode, node)

    def buildRoleInverseNode(self, node):
        """
        Build a RoleInverse node using the given QDomElement.
        :type node: QDomElement
        :rtype: RoleInverseNode
        """
        return self.buildNodeFromShapeNode(Item.RoleInverseNode, node)

    def buildValueDomainNode(self, node):
        """
        Build a Value-Domain node using the given QDomElement.
        :type node: QDomElement
        :rtype: ValueDomainNode
        """
        item = self.buildNodeFromShapeNode(Item.ValueDomainNode, node)
        if item:
            data = node.firstChildElement('data')
            while not data.isNull():
                if data.attribute('key', '') == self.keys['node_key']:
                    shapeNode = data.firstChildElement('y:ShapeNode')
                    nodeLabel = shapeNode.firstChildElement('y:NodeLabel')
                    item.setText(nodeLabel.text())
                data = data.nextSiblingElement('data')
        return item

    def buildUnionNode(self, node):
        """
        Build a Union node using the given QDomElement.
        :type node: QDomElement
        :rtype: UnionNode
        """
        return self.buildNodeFromShapeNode(Item.UnionNode, node)

    def buildValueRestrictionNode(self, node):
        """
        Build a ValueRestriction node using the given QDomElement.
        :type node: QDomElement
        :rtype: ValueRestrictionNode
        """
        return self.buildNodeFromUMLNoteNode(Item.ValueRestrictionNode, node)

    ####################################################################################################################
    #                                                                                                                  #
    #   EDGES                                                                                                          #
    #                                                                                                                  #
    ####################################################################################################################

    def buildInclusionEdge(self, edge):
        """
        Build an Inclusion edge using the given QDomElement.
        :type edge: QDomElement
        :rtype: InclusionEdge
        """
        item = self.buildEdgeFromGenericEdge(Item.InclusionEdge, edge)
        if item:
            data = edge.firstChildElement('data')
            while not data.isNull():
                if data.attribute('key', '') == self.keys['edge_key']:
                    polyLineEdge = data.firstChildElement('y:PolyLineEdge')
                    arrows = polyLineEdge.firstChildElement('y:Arrows')
                    if arrows.attribute('source', '') == 'standard' and arrows.attribute('target', '') == 'standard':
                        item.complete = True
                        item.updateEdge()
                data = data.nextSiblingElement('data')
        return item

    def buildInputEdge(self, edge):
        """
        Build an Input edge using the given QDomElement.
        :type edge: QDomElement
        :rtype: InputEdge
        """
        item = self.buildEdgeFromGenericEdge(Item.InputEdge, edge)
        if item:
            data = edge.firstChildElement('data')
            while not data.isNull():
                if data.attribute('key', '') == self.keys['edge_key']:
                    polyLineEdge = data.firstChildElement('y:PolyLineEdge')
                    arrows = polyLineEdge.firstChildElement('y:Arrows')
                    if arrows.attribute('source', '') == 't_shape':
                        # FIXME: item.functional = True
                        item.updateEdge()
                data = data.nextSiblingElement('data')
        return item

    ####################################################################################################################
    #                                                                                                                  #
    #   AUXILIARY METHODS                                                                                              #
    #                                                                                                                  #
    ####################################################################################################################

    def buildEdgeFromGenericEdge(self, item, edge):
        """
        Build an edge using the given item type and QDomElement.
        :type item: Item
        :type edge: QDomElement
        :rtype: AbstractEdge
        """
        data = edge.firstChildElement('data')
        while not data.isNull():

            if data.attribute('key', '') == self.keys['edge_key']:

                points = []
                polyLineEdge = data.firstChildElement('y:PolyLineEdge')
                path = polyLineEdge.firstChildElement('y:Path')
                collection = path.elementsByTagName('y:Point')
                for i in range(0, collection.count()):
                    point = collection.at(i).toElement()
                    pos = QPointF(float(point.attribute('x')), float(point.attribute('y')))
                    pos = QPointF(snapF(pos.x(), DiagramScene.GridSize), snapF(pos.y(), DiagramScene.GridSize))
                    points.append(pos)

                kwargs = {
                    'id': edge.attribute('id'),
                    'source': self.scene.node(edge.attribute('source')),
                    'target': self.scene.node(edge.attribute('target')),
                    'breakpoints': points,
                }

                item = self.factory.create(item=item, scene=self.scene, **kwargs)
                # yEd, differently from the node pos whose origin matches the TOP-LEFT corner,
                # consider the center of the shape as original anchor point (0,0). So if the
                # anchor point hs a negative X it's moved a bit on the left with respect to
                # the center of the shape (the same applies for the Y axis)
                sourceP = QPointF(float(path.attribute('sx')), float(path.attribute('sy')))
                sourceP = item.source.pos() + sourceP
                sourceP = QPointF(snapF(sourceP.x(), DiagramScene.GridSize), snapF(sourceP.y(), DiagramScene.GridSize))

                targetP = QPointF(float(path.attribute('tx')), float(path.attribute('ty')))
                targetP = item.target.pos() + targetP
                targetP = QPointF(snapF(targetP.x(), DiagramScene.GridSize), snapF(targetP.y(), DiagramScene.GridSize))

                painterPath = item.source.painterPath()
                if painterPath.contains(item.source.mapFromScene(sourceP)):
                    item.source.setAnchor(item, sourceP)

                painterPath = item.target.painterPath()
                if painterPath.contains(item.target.mapFromScene(targetP)):
                    item.target.setAnchor(item, targetP)

                item.source.addEdge(item)
                item.target.addEdge(item)
                return item

            data = data.nextSiblingElement('data')

        return None

    def buildNodeFromGenericNode(self, item, node):
        """
        Build a node using the given item type and QDomElement.
        :type item: Item
        :type node: QDomElement
        :rtype: AbstractNode
        """
        data = node.firstChildElement('data')
        while not data.isNull():

            if data.attribute('key', '') == self.keys['node_key']:

                genericNode = data.firstChildElement('y:GenericNode')
                geometry = genericNode.firstChildElement('y:Geometry')
                nodeLabel = genericNode.firstChildElement('y:NodeLabel')

                kwargs = {
                    'id': node.attribute('id'),
                    'height': float(geometry.attribute('height')),
                    'width': float(geometry.attribute('width')),
                }

                item = self.factory.create(item=item, scene=self.scene, **kwargs)
                # yEd uses the TOP-LEFT corner as (0,0) coordinate => we need to translate our
                # position (0,0), which is instead at the center of the shape, so that the TOP-LEFT
                # corner of the shape in yEd matches the TOP-LEFT corner of the shape in Eddy.
                # Additionally we force-snap the position to the grid so that items say aligned.
                pos = QPointF(float(geometry.attribute('x')), float(geometry.attribute('y')))
                pos = pos + QPointF(item.width() / 2, item.height() / 2)
                pos = QPointF(snapF(pos.x(), DiagramScene.GridSize), snapF(pos.y(), DiagramScene.GridSize))
                item.setPos(pos)
                item.setText(nodeLabel.text())
                return item

            data = data.nextSiblingElement('data')

        return None

    def buildNodeFromShapeNode(self, item, node):
        """
        Build a node using the given item type and QDomElement.
        :type item: Item
        :type node: QDomElement
        :rtype: AbstractNode
        """
        data = node.firstChildElement('data')
        while not data.isNull():

            if data.attribute('key', '') == self.keys['node_key']:

                shapeNode = data.firstChildElement('y:ShapeNode')
                geometry = shapeNode.firstChildElement('y:Geometry')

                kwargs = {
                    'id': node.attribute('id'),
                    'height': float(geometry.attribute('height')),
                    'width': float(geometry.attribute('width')),
                }

                item = self.factory.create(item=item, scene=self.scene, **kwargs)
                # yEd uses the TOP-LEFT corner as (0,0) coordinate => we need to translate our
                # position (0,0), which is instead at the center of the shape, so that the TOP-LEFT
                # corner of the shape in yEd matches the TOP-LEFT corner of the shape in Eddy.
                # Additionally we force-snap the position to the grid so that items say aligned.
                pos = QPointF(float(geometry.attribute('x')), float(geometry.attribute('y')))
                pos = pos + QPointF(item.width() / 2, item.height() / 2)
                pos = QPointF(snapF(pos.x(), DiagramScene.GridSize), snapF(pos.y(), DiagramScene.GridSize))
                item.setPos(pos)
                return item

            data = data.nextSiblingElement('data')

        return None

    def buildNodeFromUMLNoteNode(self, item, node):
        """
        Build a node using the given item type and QDomElement.
        :type item: Item
        :type node: QDomElement
        :rtype: AbstractNode
        """
        data = node.firstChildElement('data')
        while not data.isNull():

            if data.attribute('key', '') == self.keys['node_key']:

                umlNoteNode = data.firstChildElement('y:UMLNoteNode')
                geometry = umlNoteNode.firstChildElement('y:Geometry')
                nodeLabel = umlNoteNode.firstChildElement('y:NodeLabel')

                kwargs = {
                    'id': node.attribute('id'),
                    'height': float(geometry.attribute('height')),
                    'width': float(geometry.attribute('width')),
                }

                item = self.factory.create(item=item, scene=self.scene, **kwargs)
                # yEd uses the TOP-LEFT corner as (0,0) coordinate => we need to translate our
                # position (0,0), which is instead at the center of the shape, so that the TOP-LEFT
                # corner of the shape in yEd matches the TOP-LEFT corner of the shape in Eddy.
                # Additionally we force-snap the position to the grid so that items say aligned.
                pos = QPointF(float(geometry.attribute('x')), float(geometry.attribute('y')))
                pos = pos + QPointF(item.width() / 2, item.height() / 2)
                pos = QPointF(snapF(pos.x(), DiagramScene.GridSize), snapF(pos.y(), DiagramScene.GridSize))

                item.setPos(pos)
                item.setText(nodeLabel.text())

                return item

            data = data.nextSiblingElement('data')

        return None

    def itemFromGraphmlNode(self, element):
        """
        Returns the item matching the given Graphml node.
        :type element: QDomElement
        :rtype: Item
        """
        data = element.firstChildElement('data')
        while not data.isNull():

            # NODE
            if data.attribute('key', '') == self.keys['node_key']:

                # GENERIC NODE
                genericNode = data.firstChildElement('y:GenericNode')
                if not genericNode.isNull():

                    configuration = genericNode.attribute('configuration', '')
                    if configuration == 'com.yworks.entityRelationship.small_entity':
                        return Item.ConceptNode
                    if configuration == 'com.yworks.entityRelationship.attribute':
                        return Item.AttributeNode
                    if configuration == 'com.yworks.entityRelationship.relationship':
                        return Item.RoleNode

                # SHAPE NODE
                shapeNode = data.firstChildElement('y:ShapeNode')
                if not shapeNode.isNull():

                    shape = shapeNode.firstChildElement('y:Shape')
                    if not shape.isNull():

                        shapeType = shape.attribute('type', '')
                        if shapeType == 'octagon':
                            return Item.IndividualNode
                        if shapeType == 'roundrectangle':
                            return Item.ValueDomainNode

                        if shapeType == 'hexagon':

                            # We need to identify DisjointUnion from the color and not by checking the empty label
                            # because in some ontologies created under yEd another operator node has been copied
                            # over and the background color has been changed despite the label not being removed.
                            fill = shapeNode.firstChildElement('y:Fill')
                            if not fill.isNull():
                                color = fill.attribute('color', '')
                                if color == '#000000':
                                    return Item.DisjointUnionNode

                            nodeLabel = shapeNode.firstChildElement('y:NodeLabel')
                            if not nodeLabel.isNull():
                                nodeText = nodeLabel.text().strip()
                                if nodeText == 'and':
                                    return Item.IntersectionNode
                                if nodeText == 'or':
                                    return Item.UnionNode
                                if nodeText == 'not':
                                    return Item.ComplementNode
                                if nodeText == 'oneOf':
                                    return Item.EnumerationNode
                                if nodeText == 'chain':
                                    return Item.RoleChainNode
                                if nodeText == 'inv':
                                    return Item.RoleInverseNode
                                if nodeText == 'data':
                                    return Item.DatatypeRestrictionNode

                        if shapeType == 'rectangle':
                            fill = shapeNode.firstChildElement('y:Fill')
                            if not fill.isNull():
                                color = fill.attribute('color', '')
                                if color == '#000000':
                                    return Item.RangeRestrictionNode
                                return Item.DomainRestrictionNode

                # UML NOTE NODE
                umlNoteNode = data.firstChildElement('y:UMLNoteNode')
                if not umlNoteNode.isNull():
                    return Item.ValueRestrictionNode

            if data.attribute('key', '') == self.keys['edge_key']:

                polyLineEdge = data.firstChildElement('y:PolyLineEdge')
                if not polyLineEdge.isNull():
                    lineStyle = polyLineEdge.firstChildElement('y:LineStyle')
                    if not lineStyle.isNull():
                        lineType = lineStyle.attribute('type', '')
                        if lineType == 'line':
                            return Item.InclusionEdge
                        if lineType == 'dashed':
                            return Item.InputEdge

            data = data.nextSiblingElement('data')

        return None

    ####################################################################################################################
    #                                                                                                                  #
    #   DIAGRAM SCENE GENERATION                                                                                       #
    #                                                                                                                  #
    ####################################################################################################################

    def run(self):
        """
        Perform ontology import from .graphml file format.
        """
        file = QFile(self.filepath)

        try:

            if not file.open(QIODevice.ReadOnly):
                raise IOError('File not found: {}'.format(self.filepath))

            document = QDomDocument()
            if not document.setContent(file):
                raise ParseError('could not initialize DOM document')

            # 1) INITIALIZE XML ROOT ELEMENT
            root = document.documentElement()

            # 2) READ KEYS FROM THE DOCUMENT
            key = root.firstChildElement('key')
            while not key.isNull():
                if key.attribute('yfiles.type', '') == 'nodegraphics':
                    self.keys['node_key'] = key.attribute('id')
                if key.attribute('yfiles.type', '') == 'edgegraphics':
                    self.keys['edge_key'] = key.attribute('id')
                key = key.nextSiblingElement('key')

            # 3) GENERATE ARBITRARY DIAGRAM SCENE
            self.scene = self.mainwindow.createScene(DiagramScene.MaxSize, DiagramScene.MaxSize)

            # 4) INITIALIZE GRAPH ELEMENT
            graph = root.firstChildElement('graph')

            # 5) GENERATE NODES
            element = graph.firstChildElement('node')
            while not element.isNull():

                # noinspection PyArgumentList
                QApplication.processEvents()

                node = None
                item = self.itemFromGraphmlNode(element)

                try:

                    if item is Item.AttributeNode:
                        node = self.buildAttributeNode(element)
                    elif item is Item.ComplementNode:
                        node = self.buildComplementNode(element)
                    elif item is Item.ConceptNode:
                        node = self.buildConceptNode(element)
                    elif item is Item.DatatypeRestrictionNode:
                        node = self.buildDatatypeRestrictionNode(element)
                    elif item is Item.DisjointUnionNode:
                        node = self.buildDisjointUnionNode(element)
                    elif item is Item.DomainRestrictionNode:
                        node = self.buildDomainRestrictionNode(element)
                    elif item is Item.EnumerationNode:
                        node = self.buildEnumerationNode(element)
                    elif item is Item.IndividualNode:
                        node = self.buildIndividualNode(element)
                    elif item is Item.IntersectionNode:
                        node = self.buildIntersectionNode(element)
                    elif item is Item.RangeRestrictionNode:
                        node = self.buildRangeRestrictionNode(element)
                    elif item is Item.RoleNode:
                        node = self.buildRoleNode(element)
                    elif item is Item.RoleChainNode:
                        node = self.buildRoleChainNode(element)
                    elif item is Item.RoleInverseNode:
                        node = self.buildRoleInverseNode(element)
                    elif item is Item.UnionNode:
                        node = self.buildUnionNode(element)
                    elif item is Item.ValueDomainNode:
                        node = self.buildValueDomainNode(element)
                    elif item is Item.ValueRestrictionNode:
                        node = self.buildValueRestrictionNode(element)

                    if not node:
                        raise ValueError('unknown node with id {}'.format(element.attribute('id')))

                except Exception as e:
                    self.errors.append(e)
                else:
                    self.scene.addItem(node)
                    self.scene.guid.update(node.id)
                finally:
                    element = element.nextSiblingElement('node')

            # 6) GENERATE EDGES
            element = graph.firstChildElement('edge')
            while not element.isNull():

                # noinspection PyArgumentList
                QApplication.processEvents()

                node = None
                item = self.itemFromGraphmlNode(element)

                try:

                    if item is Item.InclusionEdge:
                        node = self.buildInclusionEdge(element)
                    elif item is Item.InputEdge:
                        node = self.buildInputEdge(element)

                    if not node:
                        raise ValueError('unknown edge with id {}'.format(element.attribute('id')))

                except Exception as e:
                    self.errors.append(e)
                else:
                    self.scene.addItem(node)
                    self.scene.guid.update(node.id)
                    node.updateEdge()
                finally:
                    element = element.nextSiblingElement('edge')

            # 7) CENTER DIAGRAM
            R1 = self.scene.sceneRect()
            R2 = self.scene.visibleRect(margin=0)
            moveX = snapF(((R1.right() - R2.right()) - (R2.left() - R1.left())) / 2, DiagramScene.GridSize)
            moveY = snapF(((R1.bottom() - R2.bottom()) - (R2.top() - R1.top())) / 2, DiagramScene.GridSize)
            if moveX or moveY:
                collection = [x for x in self.scene.items() if x.node or x.edge]
                for item in collection:
                    # noinspection PyArgumentList
                    QApplication.processEvents()
                    item.moveBy(moveX, moveY)
                for item in collection:
                    # noinspection PyArgumentList
                    QApplication.processEvents()
                    if item.edge:
                        item.updateEdge()

            # 8) RESIZE DIAGRAM SCENE
            R3 = self.scene.visibleRect(margin=20)
            size = max(R3.width(), R3.height(), DiagramScene.MinSize)
            self.scene.setSceneRect(QRectF(-size / 2, -size / 2, size, size))

        finally:

            file.close()