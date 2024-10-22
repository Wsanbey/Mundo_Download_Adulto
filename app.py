from BuscarLink import MP4LinkExtractor
from flask import Flask, request, jsonify, render_template, Response
import requests
 
app = Flask(__name__)
  
@app.route('/')
def index():
    
    allowed_urls = []
    return render_template('index.html', whitelist=allowed_urls)


# Definição de cabeçalhos necessários para acessar o arquivo
def definir_headers(link):
    # Cabeçalhos personalizados
    HEADERS = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": link,  # Referer é muitas vezes necessário
        "Connection": "keep-alive",
    }
    return HEADERS

@app.route('/baixar_video', methods=['POST'])
def baixar_video():
    data = request.json
    URL = data.get("url")

    if not URL:
        return jsonify({"error": "URL é obrigatória."}), 400

    try:
        extractor = MP4LinkExtractor(URL)
        extractor.fetch_page()
        links_mp4 = extractor.extract_mp4_links()

        # Usar um set para evitar links duplicados
        unique_links = set(links_mp4)

        # Criar links proxy
        proxied_links = [f'/proxy?url={link}' for link in unique_links]
        
        # Criar a whitelist com os links únicos
        whitelist = list(unique_links)

        # Retornar os links proxy e a whitelist
        return jsonify({
            "links": proxied_links,  # Links de proxy
            "whitelist": whitelist  # Lista de links únicos
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/downloads')
def downloads():
    # Recupera o link de download da query string
    link = request.args.get('link')
    return render_template('downloads.html', link=link)


@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL é obrigatória."}), 400

    try:
        # Faz a requisição para o URL com os cabeçalhos necessários
        HEADERS = definir_headers(url)
        resposta = requests.get(url, headers=HEADERS, stream=True)
        resposta.raise_for_status()

        # Envia a resposta para o cliente
        return Response(resposta.iter_content(chunk_size=8192),
                        content_type=resposta.headers.get('Content-Type'),
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                            'Accept-Language': 'en-US,en;q=0.5',
                            "Content-Disposition": f"attachment; filename={url.split('/')[-1]}",
                            'Upgrade-Insecure-Requests': '1'
                        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
     

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    
    
