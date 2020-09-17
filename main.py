import gi
import bd_class
import threading, time
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import GLib

def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

class Main:
    def __init__(self):
        gladefile = "interface1.glade"          #Arquivo de interface glade
        self.builder = gtk.Builder()            #Criando o builder do gtk
        self.builder.add_from_file(gladefile)   #Atribuindo o arquivo glade ao builder

        self.cor = "#008800"                    #Cores em hexadecimal

        btn_cadastrar = self.builder.get_object("btn_cadastro")
        self.ppup_caixa = self.builder.get_object("popover")
        self.ppup_texto = self.builder.get_object("popoverLabel")
        btn_cadastrar.connect("clicked", self.adicionar_linha)

        #Acesso ao banco de dados
        self.bd = bd_class.Banco_de_dados('bd.bd', 'pessoas')
        self.bd.conectar_banco_de_dados()
        #self.bd.criar_tabela() #Criaçao
        self.lista_bd = self.bd.ler_tabela()

        self.model = self.builder.get_object("lista1")
        self.lista = self.builder.get_object("lista")
        colid = gtk.TreeViewColumn('id', gtk.CellRendererText(), text=0)
        self.lista.append_column(colid)
        colnome = gtk.TreeViewColumn('nome', gtk.CellRendererText(), text=1)
        self.lista.append_column(colnome)
        colidade = gtk.TreeViewColumn('idade', gtk.CellRendererText(), text=2)
        self.lista.append_column(colidade)
        self.carregar_itens_da_lista()

        gtk_window = self.builder.get_object("Main")
        gtk_window.connect("delete-event", gtk.main_quit)
        gtk_window.show_all()

    def adicionar_linha(self, widget):
        self.nomeEntrada = self.builder.get_object("input_nome")
        self.nomeSaida = self.nomeEntrada.get_text().strip()
        self.idadeEntrada = self.builder.get_object("input_idade")
        self.idadeSaida = self.idadeEntrada.get_text().strip()
        self.id = int(len(self.model))
        self.bd.inserir_dados(self.id, self.nomeSaida, self.idadeSaida)
        self.model.append([self.id, self.nomeSaida, self.idadeSaida])
        self.mostrar_popup()


    def carregar_itens_da_lista(self):
        self.model.clear()
        for r in self.lista_bd:
            self.model.append([r[0],r[1],r[2]])

    def mostrar_popup(self):
        msg = "<span foreground='" + self.cor + "'>Adicionado com sucesso!</span>"
        self.ppup_texto.set_markup(msg)
        self.ppup_caixa.popup()
        self.esconder_popup()

    @threaded
    def esconder_popup(self):
        time.sleep(3)
        GLib.idle_add(self.ppup_caixa.popdown)


if __name__ == '__main__':
    main = Main()
    gtk.main()
