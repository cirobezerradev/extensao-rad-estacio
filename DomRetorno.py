from DomNFe import DomNFe

class DomRetorno(DomNFe):

    def __init__(self, url_xml: str):
        super().__init__(url_xml)
        self.cliente = self.dom_nfe.getElementsByTagName('xNome')[1].firstChild.data
    
    def status_cfop(self) -> bool:
        for c in self.cfop:
            if not c == 6902:
                return False
        return True

    