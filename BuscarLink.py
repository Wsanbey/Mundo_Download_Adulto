import requests
from bs4 import BeautifulSoup
import re

class MP4LinkExtractor:
    def __init__(self, url):
        self.url = url
        self.page_content = ""

    def fetch_page(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            # Parseia o conteúdo HTML da página
            soup = BeautifulSoup(response.text, 'html.parser')
            # Converte o conteúdo da página para string
            self.page_content = str(soup)
        else:
            raise Exception(f"Erro ao acessar a página. Status code: {response.status_code}")

    def extract_mp4_links(self):
        if not self.page_content:
            raise Exception("Conteúdo da página não foi carregado. Chame fetch_page() primeiro.")

        # Usa uma expressão regular para encontrar todas as URLs que começam com 'file:' e terminam com '.mp4'
        mp4_links = re.findall(r'https[^\s\'"]+\.mp4', self.page_content)
        return mp4_links
