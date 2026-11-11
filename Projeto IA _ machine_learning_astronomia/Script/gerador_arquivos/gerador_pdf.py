import os
import sys
from typing import List
from fpdf import FPDF

# Garante que a raiz do projeto esteja no sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from dados.Bancodedados.EstrelarDao import StarDTO


class RelatorioAstronomicoPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        # Em vez de new_x/new_y, usamos ln=1 para pular a linha
        self.cell(0, 10, "Catálogo de Dados Astronômicos", border=0, ln=1, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def gerar_pdf_catalogo(estrelas: List[StarDTO], caminho_saida: str) -> str:
    """Gera um arquivo PDF formatado com a lista de estrelas recebida."""
    pdf = RelatorioAstronomicoPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=10)

    # Cabeçalho da Tabela
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(35, 8, "Nome", border=1)
    pdf.cell(25, 8, "Classe", border=1)
    pdf.cell(35, 8, "Temp (K)", border=1)
    pdf.cell(35, 8, "Dist (AL)", border=1)
    pdf.cell(50, 8, "Estágio", border=1, new_x="LMARGIN", new_y="NEXT")

    # Linhas de Dados
    pdf.set_font("Helvetica", size=9)
    for star in estrelas:
        pdf.cell(35, 7, str(star.nameStar), border=1)
        pdf.cell(25, 7, str(star.spectralClass), border=1)
        pdf.cell(35, 7, f"{star.temperatureStar_K:.1f}", border=1)
        pdf.cell(35, 7, f"{star.distanceStar_LY:.1f}", border=1)
        pdf.cell(50, 7, str(star.evolutionaryStage), border=1, new_x="LMARGIN", new_y="NEXT")

    # Garante que a pasta de destino existe
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
    pdf.output(caminho_saida)
    print(f"✅ [GERADOR] PDF gerado com sucesso em: {caminho_saida}")
    return caminho_saida

if __name__ == "__main__":
    # Teste de execução direta do gerador
    caminho_pdf_destino = os.path.join(BASE_DIR, "dados", "relatorio_estrelas.pdf")
    
    # Dados fictícios ajustados aos campos exigidos pela StarDTO
    estrelas_teste = [
        StarDTO(
            nameStar="Sol",
            spectralClass="G2V",
            mainSpectralClass="G",
            temperatureStar_K=5778.0,
            luminosityStar_logSun=0.0,
            radiusStar_logSun=0.0,
            massStar_logSun=1.0,
            distanceStar_LY=0.0,
            evolutionaryStage="Sequência Principal"
        ),
        StarDTO(
            nameStar="Sirius A",
            spectralClass="A1V",
            mainSpectralClass="A",
            temperatureStar_K=9940.0,
            luminosityStar_logSun=1.4,
            radiusStar_logSun=0.23,
            massStar_logSun=2.06,
            distanceStar_LY=8.6,
            evolutionaryStage="Sequência Principal"
        ),
        StarDTO(
            nameStar="Betelgeuse",
            spectralClass="M1-M2",
            mainSpectralClass="M",
            temperatureStar_K=3500.0,
            luminosityStar_logSun=5.1,
            radiusStar_logSun=2.88,
            massStar_logSun=16.5,
            distanceStar_LY=642.5,
            evolutionaryStage="Supergigante Vermelha"
        )
    ]
    
    gerar_pdf_catalogo(estrelas_teste, caminho_pdf_destino)