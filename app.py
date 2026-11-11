"""Portal TI Ellenco. Inicie com: streamlit run app.py"""
import streamlit as st
from html import escape
import unicodedata

st.set_page_config(page_title="Ellenco | Portal de TI", page_icon="🔗", layout="wide")

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

st.markdown("""<style>
.stApp {background:radial-gradient(ellipse at top right,#193958,transparent 60%),#091526;color:#f1f6ff}
[data-testid="stHeader"]{background:#091526}
.block-container{max-width:1240px;padding-top:2.5rem;padding-bottom:2rem}
[data-testid="stHeadingWithActionElements"] h1 {color:#f1f6ff}
[data-testid="stWidgetLabel"] p {color:#d0deee}
.brand{border-bottom:1px solid #2b405b;padding:5px 0 24px;margin-bottom:32px;font-size:24px;font-weight:800;letter-spacing:3px;color:#f1f6ff}
.brand small{font-size:12px;font-weight:400;letter-spacing:1px;display:block;color:#aec0d8;margin-top:6px}
.intro{color:#aec0d8;margin-bottom:24px;font-size:17px}
.portal-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:18px 0 30px}
.portal-card{padding:24px;border:1px solid #2b405b;border-radius:18px;background:linear-gradient(135deg,#152940,#102036);display:flex;flex-direction:column;min-height:250px}
.portal-top{display:flex;justify-content:space-between;align-items:center;gap:10px}
.portal-icon{padding:11px;border-radius:12px;background:#234560;color:#aee6ff;font-weight:700}
.portal-category{font-size:12px;color:#80e4d2}
.portal-card h2{font:600 20px 'Segoe UI',sans-serif;color:#f1f6ff;margin:20px 0 8px}
.portal-card p{color:#aec0d8;font-size:14px;line-height:1.5;margin:0 0 24px}
.portal-card a{display:block;margin-top:auto;padding:12px 16px;border-radius:9px;background:#244664;color:#e0f4ff!important;text-decoration:none;font-weight:600}
.portal-card a:hover{background:#315d80}.portal-card a:focus-visible{outline:3px solid #7ecbff;outline-offset:3px}
.portal-footer{color:#aec0d8;font-size:12px;border-top:1px solid #2b405b;padding-top:18px}
@media(max-width:950px){.portal-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:600px){.portal-grid{grid-template-columns:1fr}}
</style>""", unsafe_allow_html=True)
st.markdown('<div class="brand">ELLENCO<small>CONSTRUÇÕES · TECNOLOGIA DA INFORMAÇÃO</small></div>', unsafe_allow_html=True)
st.title("Portal de TI")
st.markdown('<p class="intro">Todos os seus sistemas, em um só lugar. Escolha um portal para começar.</p>', unsafe_allow_html=True)
left, right = st.columns([2, 1])
with left:
    search = st.text_input("Buscar portal", placeholder="Digite o nome do sistema…")
with right:
    category = st.selectbox("Categoria", ["Todos"] + list(dict.fromkeys(p[1] for p in PORTAIS)))

def normalize(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.lower()) if not unicodedata.combining(c))

filtered = [p for p in PORTAIS if (category == "Todos" or p[1] == category) and normalize(search.strip()) in normalize(p[0] + " " + p[1])]
st.caption(f"{len(filtered)} de {len(PORTAIS)} portais")
cards = []
for name, group, description, url, icon in filtered:
    cards.append(f'<article class="portal-card"><div class="portal-top"><span class="portal-icon" aria-hidden="true">{escape(icon)}</span><span class="portal-category">{escape(group)}</span></div><h2>{escape(name)}</h2><p>{escape(description)}</p><a href="{escape(url, quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Acessar {escape(name, quote=True)} em nova aba">Acessar portal ↗</a></article>')
if cards:
    st.markdown('<div class="portal-grid">' + ''.join(cards) + '</div>', unsafe_allow_html=True)
else:
    st.info("Nenhum portal encontrado. Tente outro nome ou categoria.")
st.markdown('<div class="portal-footer">Ellenco Construções · Os acessos abrem em uma nova aba. Carol Conect requer acesso à rede interna.</div>', unsafe_allow_html=True)
