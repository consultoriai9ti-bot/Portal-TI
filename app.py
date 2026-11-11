"""Portal TI Ellenco — execute: python app.py (Python 3.9+)."""
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import argparse
import threading
import webbrowser

# Edite os nomes, categorias e links abaixo quando necessário.
PORTAIS = [
    ('Chamados TOTVS', 'Suporte', 'Abertura e acompanhamento de chamados.', 'https://suporte.totvs.com/portal/p/10098/customer-portal-dashboard', 'TO'),
    ('Chamados SISMA', 'Suporte', 'Central de atendimento SISMA.', 'https://assisteweb.trace.com.br/TraceGP/indexPopup.jsp', 'SI'),
    ('Meu RH', 'Pessoas', 'Acesso ao portal do colaborador.', 'https://meurh.ellenco.com.br/web/app/RH/PortalMeuRH/#/login', 'RH'),
    ('TAE', 'Documentos', 'Portal de assinatura eletrônica TOTVS.', 'https://totvssign.totvs.app/webapptotvssign/auth/welcome', 'TA'),
    ('Neogrid', 'Documentos', 'Portal de monitoramento fiscal.', 'https://portalmonitoramentototvs.fiscalneogrid.com/', 'NE'),
    ('Trello', 'Organização', 'Quadros, tarefas e projetos.', 'https://trello.com/', 'TR'),
    ('Carol Conect', 'Clockin', 'Conexão Clockin • requer acesso à rede interna.', 'http://100.64.251.231:8880/ui/login', 'CC'),
    ('Carol Backoffice', 'Clockin', 'Acesso ao painel Clockin.', 'https://ellenco.carol.ai/ellenco/apps/clockinapp/12.1.26100000/index.html#/dashboard', 'CB'),
    ('Carol ADM', 'Clockin', 'Administração do ambiente Carol.', 'https://ellenco.carol.ai/auth/login?env=ellenco&redirect=%2Fellenco%2Fcarol-ui%2Fcarol-app%2F8898a01454d745539c7f7ea9450fb6b9%2Fsettings', 'CA'),
]

PAGE = '''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Ellenco | Portal de TI</title>
<style>
:root{color-scheme:dark;--bg:#091526;--panel:#12243b;--text:#f1f6ff;--muted:#aec0d8;--line:#2b405b;--accent:#63d6c4}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 90% 0,#18395c,transparent 55%),var(--bg);font-family:Segoe UI,Arial,sans-serif;color:var(--text);min-height:100vh}header{border-bottom:1px solid var(--line);background:#0a182bd9}.bar{max-width:1200px;margin:auto;padding:24px 32px;display:flex;align-items:center;justify-content:space-between;gap:20px}.brand{font-size:23px;letter-spacing:3px;font-weight:800}.brand small{display:block;font-size:10px;letter-spacing:2px;color:var(--muted);margin-top:5px}.label{color:var(--muted);font-size:13px}main{max-width:1200px;margin:auto;padding:48px 32px}.eyebrow{color:var(--accent);font-size:12px;letter-spacing:2px;font-weight:700}h1{font-size:clamp(30px,5vw,46px);letter-spacing:-1px;margin:14px 0}p{color:var(--muted);line-height:1.6}.intro{margin:0 0 30px;max-width:640px}.tools{display:flex;gap:16px;align-items:end;margin:28px 0;flex-wrap:wrap}.search{flex:1;min-width:200px}.search label{display:block;font-size:13px;color:var(--muted);margin-bottom:8px}input{width:100%;background:#0c1c30;border:1px solid var(--line);border-radius:12px;padding:14px 16px;font:inherit;color:var(--text)}.filters{display:flex;flex-wrap:wrap;gap:7px}button{font:inherit;cursor:pointer;border:1px solid var(--line);background:transparent;color:var(--muted);border-radius:9px;padding:11px 13px;font-size:13px}button[aria-pressed=true]{background:var(--accent);color:#092025;border-color:var(--accent);font-weight:600}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #7ecbff;outline-offset:4px}.count{font-size:13px;color:var(--muted);margin:0 0 16px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.card{display:flex;flex-direction:column;min-height:238px;background:linear-gradient(135deg,#152940,#102036);border:1px solid var(--line);border-radius:18px;padding:24px;transition:transform .18s,border-color .18s}.card:hover{transform:translateY(-3px);border-color:#5b7f9e}.card[hidden]{display:none}.top{display:flex;justify-content:space-between;align-items:center;gap:12px}.icon{width:44px;height:44px;display:grid;place-items:center;border-radius:12px;background:#234560;color:#aee6ff;font-weight:700}.category{font-size:11px;color:var(--accent);border:1px solid #315b60;border-radius:20px;padding:5px 10px}h2{font-size:19px;margin:19px 0 5px}.card p{font-size:13px;margin:0 0 22px}.card a{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:auto;text-decoration:none;font-weight:600;font-size:14px;color:#e0f4ff;background:#244664;border:1px solid #396483;border-radius:9px;padding:12px 14px}.card a:hover{background:#315d80}footer{max-width:1200px;margin:0 auto;padding:4px 32px 30px;color:var(--muted);font-size:12px;display:flex;justify-content:space-between;gap:15px;flex-wrap:wrap}#empty{padding:30px;text-align:center;border:1px dashed var(--line);border-radius:14px}@media(max-width:900px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}.tools{align-items:stretch}.search{flex-basis:100%}}@media(max-width:560px){.grid{grid-template-columns:1fr}main{padding:30px 20px}.bar{padding:20px}.label{max-width:100px;text-align:right}.card{min-height:220px}footer{padding:5px 20px 25px}}@media(prefers-reduced-motion:reduce){.card{transition:none}.card:hover{transform:none}}
</style></head><body>
<header><div class="bar"><div class="brand">ELLENCO<small>CONSTRUÇÕES</small></div><span class="label">Tecnologia da Informação</span></div></header>
<main><div class="eyebrow">SEU PONTO DE ACESSO</div><h1>Portal de TI</h1><p class="intro">Todos os seus sistemas, em um só lugar.<br>Escolha um portal para começar.</p>
<div class="tools"><div class="search"><label for="search">Buscar portal</label><input id="search" type="search" placeholder="Digite o nome do sistema…"></div><div class="filters" aria-label="Filtrar por categoria">__FILTERS__</div></div>
<p class="count" id="count" role="status" aria-live="polite"></p><div class="grid">__CARDS__</div><p id="empty" hidden>Nenhum portal encontrado. Tente outro nome ou categoria.</p>
</main><footer><span>Ellenco Construções · Portal de TI</span><span>Os acessos abrem em uma nova aba.</span></footer>
<script>
const search=document.querySelector('#search'),cards=[...document.querySelectorAll('.card')],buttons=[...document.querySelectorAll('.filters button')];let category='Todos';
const normalize=s=>s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
function filter(){const q=normalize(search.value.trim());let total=0;cards.forEach(card=>{const show=(category==='Todos'||card.dataset.category===category)&&normalize(card.dataset.name+' '+card.dataset.category).includes(q);card.hidden=!show;if(show)total++});document.querySelector('#count').textContent=total+' de '+cards.length+' portais';document.querySelector('#empty').hidden=total>0;}
search.addEventListener('input',filter);buttons.forEach(button=>button.addEventListener('click',()=>{category=button.textContent;buttons.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));filter()}));filter();
</script></body></html>'''


def render_page():
    categories = ['Todos'] + list(dict.fromkeys(p[1] for p in PORTAIS))
    filters = ''.join(f'<button type="button" aria-pressed="{str(c == "Todos").lower()}">{escape(c)}</button>' for c in categories)
    cards = ''.join(
        f'<article class="card" data-name="{escape(name, quote=True)}" data-category="{escape(category, quote=True)}">'
        f'<div class="top"><span class="icon" aria-hidden="true">{escape(icon)}</span><span class="category">{escape(category)}</span></div>'
        f'<h2>{escape(name)}</h2><p>{escape(description)}</p>'
        f'<a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Acessar {escape(name, quote=True)} (nova aba)">Acessar portal <span aria-hidden="true">↗</span></a></article>'
        for name, category, description, url, icon in PORTAIS
    )
    return PAGE.replace('__FILTERS__', filters).replace('__CARDS__', cards).encode('utf-8')


class PortalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/', '/index.html'):
            self.send_error(404)
            return
        content = render_page()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(content)


def main():
    parser = argparse.ArgumentParser(description='Portal de TI Ellenco')
    parser.add_argument('--port', type=int, default=8501)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), PortalHandler)
    except OSError as exc:
        print(f'Não foi possível iniciar o portal: {exc}\nTente outra porta: python app.py --port 8502')
        raise SystemExit(1)
    url = f'http://127.0.0.1:{server.server_port}'
    print(f'Portal de TI Ellenco: {url}\nMantenha esta janela aberta. Para encerrar, pressione Ctrl+C.')
    if not args.no_browser:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nPortal encerrado.')
    finally:
        server.server_close()


if __name__ == '__main__':
    main()

