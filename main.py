"""
CDFJ-Opportunity - Centro de Direcionamento à Faculdade Juvenil
================================================================
Portal que liga jovens dos 18 aos 35 anos a oportunidades de estudo no exterior:
sites de bolsas de estudo, mentoria para candidaturas e encaminhamento para pessoas
capacitadas que ajudam a tratar da documentação necessária.

Problema que resolve: os jovens não sabem onde procurar bolsas nem quem os ajuda nas
candidaturas. Depois do cadastro (nome, e-mail, telefone, senha) a lista de sites de bolsas
aparece automaticamente e é actualizada por pesquisa na web.

Executar:  python main.py   (abre http://127.0.0.1:5000)
No telemóvel o mesmo ficheiro é o ponto de entrada do APK (Kivy + WebView, ver buildozer.spec).
"""
import os
import threading
import webbrowser

from database import Database
from web import criar_app

PORTA = int(os.environ.get("PORT", 5000))
INTERVALO_ACTUALIZACAO = 24 * 3600  # segundos


def e_android():
    return "ANDROID_ARGUMENT" in os.environ


def caminho_bd():
    if e_android():
        from android.storage import app_storage_path # type: ignore
        return os.path.join(app_storage_path(), "cdfj.db")
    return os.environ.get("CDFJ_DB", os.path.join(os.path.dirname(os.path.abspath(__file__)), "cdfj.db"))


def agendar_actualizacao(servico):
    """Pesquisa novas bolsas em segundo plano e repete a cada 24 horas."""
    def tarefa():
        try:
            servico.actualizar_automaticamente()
        except Exception as e:  # nunca deixar a manutenção derrubar a app
            print("Actualização ignorada:", e)
        temporizador = threading.Timer(INTERVALO_ACTUALIZACAO, tarefa)
        temporizador.daemon = True
        temporizador.start()
    threading.Thread(target=tarefa, daemon=True).start()


def correr_android(app):
    from kivy.app import App # type: ignore
    from kivy.clock import Clock # type: ignore
    from kivy.uix.widget import Widget # type: ignore

    class CDFJApp(App):
        def build(self):
            threading.Thread(target=lambda: app.run(host="127.0.0.1", port=PORTA, use_reloader=False),
                             daemon=True).start()
            Clock.schedule_once(self.abrir_webview, 3)
            return Widget()

        def abrir_webview(self, *_):
            from android.runnable import run_on_ui_thread # type: ignore
            from jnius import autoclass # type: ignore
            WebView = autoclass("android.webkit.WebView")
            WebViewClient = autoclass("android.webkit.WebViewClient")
            atividade = autoclass("org.kivy.android.PythonActivity").mActivity

            @run_on_ui_thread
            def criar():
                wv = WebView(atividade)
                wv.getSettings().setJavaScriptEnabled(True)
                wv.setWebViewClient(WebViewClient())
                atividade.setContentView(wv)
                wv.loadUrl(f"http://127.0.0.1:{PORTA}")
            criar()

    CDFJApp().run()


def main():
    app = criar_app(Database(caminho_bd()))
    agendar_actualizacao(app.servico_bolsas)
    if e_android():
        correr_android(app)
    else:
        threading.Timer(1.2, lambda: webbrowser.open(f"http://127.0.0.1:{PORTA}")).start()
        app.run(host="0.0.0.0", port=PORTA, use_reloader=False)


if __name__ == "__main__":
    main()
