from DomNFe import DomNFe
from datetime import datetime, timedelta

class DomRemessa(DomNFe):

    def __init__(self, url_xml: str) -> None:
        super().__init__(url_xml)
        self.cliente = self.dom_nfe.getElementsByTagName('xNome')[0].firstChild.data
        self.data_limite = self.calcular_dt_limite(self.data_emissao)

    def calcular_dt_limite(self, data) -> str:
        data = datetime.strptime(data, '%d/%m/%Y')
        data = data + timedelta(days=180)
        return data.strftime('%d/%m/%Y')

    def status_cfop(self) -> bool:
        for c in self.cfop:
            if not c == 6901:
                return False
        return True

