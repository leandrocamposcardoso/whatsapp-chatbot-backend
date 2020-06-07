from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class IbProtocolEntity(ProtocolEntity):
    '''
    <ib></ib>
    '''
    def __init__(self):
        super(IbProtocolEntity, self).__init__("ib")
    
    def toProtocolTreeNode(self):
        return self._createProtocolTreeNode({}, None, None)

    def __str__(self):
        return "Ib:\n"

    @staticmethod
    def fromProtocolTreeNode(node):
        return IbProtocolEntity()
