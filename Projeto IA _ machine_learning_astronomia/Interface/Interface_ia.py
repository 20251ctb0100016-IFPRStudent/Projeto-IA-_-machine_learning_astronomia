import os
import time
import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from datetime import datetime

ctk.set_appearance_mode("dark")

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))


def desenhar_card_arredondado(canvas, x1, y1, x2, y2, raio=15, cor_fundo="#0d1117", cor_borda="#30363d", largura_borda=1):
    pontos = [
        x1+raio, y1, x2-raio, y1, x2, y1, x2, y1+raio,
        x2, y2-raio, x2, y2, x2-raio, y2, x1+raio, y2,
        x1, y2, x1, y2-raio, x1, y1+raio, x1, y1
    ]
    return canvas.create_polygon(pontos, fill=cor_fundo, outline=cor_borda, width=largura_borda, smooth=True)

# Uma herança com o custom Tkinter
class canvaIA(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Aprendizado Supervisionado de Máquina de Classificação Objetos Celestes (ASMCOC)!")
        self.geometry("1597x987")
        
        self.lista_videos = [
            os.path.join(PASTA_ATUAL, "UniversoVideo1.mp4"),
            os.path.join(PASTA_ATUAL, "UniversoVideo4.mp4"),
        ]
        
        self.indice_video_atual = 0
        self.cap = None
        self.tempo_inicio_video = 0 
        
        self.id_fundo_form = None
        self.id_card_form = None
        self.formularioDados = None
        
        # Variáveis de Controle do CRUD e Tabela
        self.contador_id = 1
        self.tabela = None
        #uma dicionario de lista para o cada seleção de menu com classificações diferentes
        self.mapa_classificacoes = {
            "Estrelas_BuracosNegros_Quasares": {
                "Classificação Espectral (Spectral Class)": [
                    "Temperature (K)", "Color_Index_BV", "Log_Temperature"
                ],
                "Estágio Evolutivo (Evolutionary Stage)": [
                    "Luminosity (L/Lo)", "Radius (R/Ro)", "Mass (M/Mo)", "log_g", "Log_Luminosity"
                ],
                "Estimativa Astrofísica e Distância": [
                    "Distance (ly)", "Log_Radius", "Log_Mass"
                ]
            },
            "aglomerados_de_galaxias": {
                "Morfologia do Aglomerado": [
                    "Distance (Mpc)", "Redshift_z", "Member_Galaxies_Count", "Virial_Radius (Mpc)"
                ],
                "Massa e Emissão de Raios-X": [
                    "Intracluster_Gas_Temp (keV)", "XRay_Luminosity (erg/s)", "Log_Total_Mass", "Log_XRay_Luminosity"
                ]
            },
            "aglomerados_estelares": {
                "Tipo e Estrutura do Aglomerado": [
                    "Distance (kpc)", "Age (Gyr)", "Estimated_Stars_Count", "Core_Radius (pc)", "Tidal_Radius (pc)"
                ],
                "Massa, Metalicidade e Densidade": [
                    "Total_Mass (M/Mo)", "Metallicity_[Fe/H]", "Stellar_Density (stars/pc3)"
                ]
            },
            "galaxias_morphology": {
                "Tipo Hubble e Morfologia Geral": [
                    "Distance (Mly)", "Effective_Radius (kpc)", "Log_Radius_kpc"
                ],
                "Massa Estelar, Luminosidade e Formação Estelar": [
                    "Stellar_Mass (M/Mo)", "Luminosity (L/Lo)", "Star_Formation_Rate (M_sun/yr)", "Log_Stellar_Mass", "Log_Luminosity"
                ]
            },
            "superaglomerados_de_galaxias": {
                "Classificação da Estrutura Cósmica": [
                    "Distance (Mpc)", "Redshift_z", "Member_Clusters_Count", "Extent_Length (Mpc)"
                ],
                "Sobredensidade e Massa do Superaglomerado": [
                    "Total_Mass (M/Mo)", "Overdensity_Factor", "Log_Total_Mass", "Log_Extent_Mpc"
                ]
            },
            "superaglomerados_estelares": {
                "Análise Estrutural e Galáxia Hospedeira": [
                    "Effective_Radius (pc)", "Age (Myr)", "Star_Formation_Rate (M_sun/yr)"
                ],
                "Densidade Central, Massa e Luminosidade": [
                    "Total_Mass (M/Mo)", "Central_Density (M_sun/pc3)", "Luminosity (L/Lo)", "Log_Total_Mass", "Log_Luminosity"
                ]
            }
        }
        
        self.carregar_video_atual()
        
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0, bg="black")
        self.canvas.pack(fill="both", expand=True)
        
        self.id_fundo = self.canvas.create_image(0, 0, anchor="nw")
        
        titulo = (
            "Bem-vindos à Interface Gráfica de Aprendizado Supervisionado\n"
            "de Máquina de Classificação de Objetos Celestes!"
        )
        self.id_titulo = self.canvas.create_text(
            0, 0, text=titulo, font=("Times", 20, "bold"), fill="white", justify="center" 
        )

        subtitulo = (
            '"Olhe para as estrelas e não para os seus pés. Tente fazer sentido do que você vê e maravilhe-se com o que faz o universo existir."'
        )
        self.id_subtitulo = self.canvas.create_text(
            0, 0, text=subtitulo, font=("Times", 13, "italic"), fill="white", justify="center"
        )

        self.id_fundo_card_dataset = desenhar_card_arredondado(self.canvas, 0, 0, 1, 1, raio=15)
        self.card_info_dataset = ctk.CTkFrame(self.canvas, fg_color="#0d1117", corner_radius=0)
        # as estilizações
        ctk.CTkLabel(
            self.card_info_dataset, 
            text="📌 Datasets Astronômicos Integrados", 
            font=("Arial", 10, "bold"), 
            text_color="#58a6ff", 
            fg_color="transparent"
        ).pack(anchor="w", padx=15, pady=(15, 0))
        
        texto_dataset_real = (
            "• Categorias: Estrelas/Quasares, Galáxias, Aglomerados\n"
            "• Propriedades: Espectrais, Fotométricas, Densidade, Massa\n"
            "• Estruturas: Superaglomerados e Aglomerados Estelares\n"
            "• Arquivos: Datasets CSV Customizados e SDSS"
        )
        ctk.CTkLabel(
            self.card_info_dataset, 
            text=texto_dataset_real, 
            font=("Arial", 9), 
            text_color="#8b949e", 
            fg_color="transparent", 
            justify="left"
        ).pack(anchor="w", padx=15, pady=(5, 15))
        
        self.id_card_dataset = self.canvas.create_window(0, 0, window=self.card_info_dataset, anchor="nw")

        self.id_fundo_card_metricas = desenhar_card_arredondado(self.canvas, 0, 0, 1, 1, raio=15)
        self.card_metricas = ctk.CTkFrame(self.canvas, fg_color="#0d1117", corner_radius=0)
        
        ctk.CTkLabel(
            self.card_metricas, 
            text="🧪 Algoritmos Supervisionados", 
            font=("Arial", 10, "bold"), 
            text_color="#3fb950", 
            fg_color="transparent"
        ).pack(anchor="w", padx=15, pady=(15, 0))
        
        texto_algoritmos = (
            "• Modelos Tabulares: Random Forest / XGBoost\n"
            "• Modelos de Imagem: CNN (ResNet / EfficientNet)\n"
            "• Validação: Cross-Validation (k=5)\n"
            "• Entrada: Atributos astrofísicos ou imagens"
        )
        ctk.CTkLabel(
            self.card_metricas, 
            text=texto_algoritmos, 
            font=("Arial", 9), 
            text_color="#8b949e", 
            fg_color="transparent", 
            justify="left"
        ).pack(anchor="w", padx=15, pady=(5, 15))
        
        self.id_card_metricas = self.canvas.create_window(0, 0, window=self.card_metricas, anchor="ne")

        self.id_fundo_card_central = desenhar_card_arredondado(self.canvas, 0, 0, 1, 1, raio=15, largura_borda=2)
        self.card_central = ctk.CTkFrame(self.canvas, fg_color="#0d1117", corner_radius=0)
        
        lbl_card = ctk.CTkLabel(
            self.card_central, 
            text="Selecione o Modo de Análise", 
            font=("Arial", 13, "bold"), 
            text_color="#58a6ff", 
            fg_color="transparent"
        )
        lbl_card.pack(padx=25, pady=(20, 15))
        #botão que vai aparecer logo na tela de classificações de dados
        self.btn_dados = ctk.CTkButton(
            self.card_central, 
            text="📊 Classificação de Dados Tabulares", 
            font=("Arial", 10, "bold"),
            fg_color="#21262d", 
            text_color="white", 
            hover_color="#30363d",
            width=270,
            height=38,
            corner_radius=8,
            command=self.abrir_classificacao_dados
        )
        self.btn_dados.pack(padx=25, pady=8)
        #botão que vai aparecer logo na tela de classificações de imagens
        self.btn_imagens = ctk.CTkButton(
            self.card_central, 
            text="🌌 Classificação de Imagens de Galáxias", 
            font=("Arial", 10, "bold"),
            fg_color="#21262d", 
            text_color="white", 
            hover_color="#30363d",
            width=270,
            height=38,
            corner_radius=8,
            command=self.abrir_classificacao_imagens
        )
        self.btn_imagens.pack(padx=25, pady=(8, 20))

        self.id_card_central = self.canvas.create_window(0, 0, window=self.card_central, anchor="ne")

        self.id_fundo_btn_voltar = desenhar_card_arredondado(self.canvas, 0, 0, 1, 1, raio=12, cor_fundo="#0d1117", cor_borda="#30363d", largura_borda=1)

        self.btn_voltar = ctk.CTkButton(
            self.canvas,
            text="🏠 Voltar ao Início",
            font=("Arial", 11, "bold"),
            fg_color="#0d1117",
            text_color="#58a6ff",
            hover_color="#21262d",
            width=140,
            height=32,
            corner_radius=0,
            command=self.mostrar_tudo
        )
        self.id_btn_voltar = self.canvas.create_window(0, 0, window=self.btn_voltar, anchor="nw")

        self.canvas.itemconfig(self.id_fundo_btn_voltar, state="hidden")
        self.canvas.itemconfig(self.id_btn_voltar, state="hidden")
        #uma lista para facilitar na parte de esconder e mostrar os objetos que coloquei na lista
        self.elementos_interface = [
            self.id_titulo,
            self.id_subtitulo,
            self.id_card_dataset,
            self.id_fundo_card_dataset,
            self.id_card_metricas,
            self.id_fundo_card_metricas,
            self.id_card_central,
            self.id_fundo_card_central
        ]

        self.bind("<Configure>", self.redimensionar_e_reorganizar)
        self.bind("<h>", lambda event: self.alternar_visibilidade())
        self.bind("<H>", lambda event: self.alternar_visibilidade())

        self.atualizar_video_fundo()
    #metodo para esconder todos os elementos da interface, exceto o botão de voltar
    def esconder_tudo(self):
        for item in self.elementos_interface:
            self.canvas.itemconfig(item, state="hidden")
        self.canvas.itemconfig(self.id_fundo_btn_voltar, state="normal")
        self.canvas.itemconfig(self.id_btn_voltar, state="normal")

    def mostrar_tudo(self):
        for item in self.elementos_interface:
            self.canvas.itemconfig(item, state="normal")
        self.canvas.itemconfig(self.id_fundo_btn_voltar, state="hidden")
        self.canvas.itemconfig(self.id_btn_voltar, state="hidden")
        
        if self.id_card_form and self.id_fundo_form:
            self.canvas.itemconfig(self.id_card_form, state="hidden")
            self.canvas.itemconfig(self.id_fundo_form, state="hidden")

    def alternar_visibilidade(self):
        estado_atual = self.canvas.itemcget(self.id_titulo, "state")
        if estado_atual == "hidden":
            self.mostrar_tudo()
        else:
            self.esconder_tudo()

    def carregar_video_atual(self):
        if self.cap is not None:
            self.cap.release()
            
        caminho_video = self.lista_videos[self.indice_video_atual]
        self.cap = cv2.VideoCapture(caminho_video)
        self.tempo_inicio_video = time.time()

    def atualizar_video_fundo(self):
        ret, frame = self.cap.read()
        tempo_decorrido = time.time() - self.tempo_inicio_video
        
        if not ret or tempo_decorrido >= 20.0:
            self.indice_video_atual = (self.indice_video_atual + 1) % len(self.lista_videos)
            self.carregar_video_atual()
            ret, frame = self.cap.read()

        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imagem_pil = Image.fromarray(frame_rgb)

            largura = self.winfo_width()
            altura = self.winfo_height()

            if largura > 100 and altura > 100:
                imagem_redimensionada = imagem_pil.resize((largura, altura), Image.Resampling.BILINEAR)
                self.imagem_ctk = ImageTk.PhotoImage(imagem_redimensionada)
                self.canvas.itemconfig(self.id_fundo, image=self.imagem_ctk)

        self.after(33, self.atualizar_video_fundo)

    # Estilização ormulario com fundo transparente(não deu certo)
    def abrir_classificacao_dados(self):
        self.esconder_tudo()

        if self.formularioDados is None:
            self.formularioDados = ctk.CTkFrame(self.canvas, fg_color="transparent", corner_radius=0)
            self.id_fundo_form = desenhar_card_arredondado(self.canvas, 0, 0, 1, 1, raio=15, cor_fundo="#0d1117", cor_borda="#30363d")
            self.id_card_form = self.canvas.create_window(0, 0, window=self.formularioDados, anchor="center")

        self.canvas.itemconfig(self.id_card_form, state="normal")
        self.canvas.itemconfig(self.id_fundo_form, state="normal")

        self.carregar_etapa1_categoria()

    def carregar_etapa1_categoria(self):
        for child in self.formularioDados.winfo_children():
            child.destroy()

        ctk.CTkLabel(
            self.formularioDados,
            text="📊 Seleção de Categoria Astronômica",
            font=("Arial", 14, "bold"),
            text_color="#58a6ff",
            fg_color="transparent"
        ).pack(padx=30, pady=(20, 10))

        ctk.CTkLabel(
            self.formularioDados,
            text="Escolha a categoria do objeto para configurar o modelo:",
            font=("Arial", 10),
            text_color="#8b949e",
            fg_color="transparent"
        ).pack(padx=30, pady=(0, 15))

        self.combo_categoria = ctk.CTkOptionMenu(
            self.formularioDados,
            values=list(self.mapa_classificacoes.keys()),
            width=300,
            fg_color="#161b22",
            button_color="#21262d",
            dropdown_fg_color="#0d1117"
        )
        self.combo_categoria.pack(padx=30, pady=10)

        btn_avancar = ctk.CTkButton(
            self.formularioDados,
            text="Avançar ➔",
            font=("Arial", 11, "bold"),
            fg_color="#238636",
            hover_color="#2ea043",
            width=180,
            height=32,
            command=self.carregar_etapa2_classificacoes
        )
        btn_avancar.pack(padx=30, pady=(15, 20))

        self.redimensionar_e_reorganizar(None)

    def carregar_etapa2_classificacoes(self):
        categoria_selecionada = self.combo_categoria.get()

        for child in self.formularioDados.winfo_children():
            child.destroy()

        ctk.CTkLabel(
            self.formularioDados,
            text=f"🎯 Categoria: {categoria_selecionada}",
            font=("Arial", 13, "bold"),
            text_color="#58a6ff",
            fg_color="transparent"
        ).pack(padx=30, pady=(20, 5))

        ctk.CTkLabel(
            self.formularioDados,
            text="Selecione as classificações desejadas (seleção múltipla):",
            font=("Arial", 9),
            text_color="#8b949e",
            fg_color="transparent"
        ).pack(padx=30, pady=(0, 15))

        self.vars_check = {}
        opcoes_disponiveis = self.mapa_classificacoes[categoria_selecionada]

        for opcao in opcoes_disponiveis:
            var = ctk.BooleanVar(value=False)
            chk = ctk.CTkCheckBox(
                self.formularioDados,
                text=opcao,
                variable=var,
                font=("Arial", 10),
                text_color="#c9d1d9",
                fg_color="#1f6beb",
                hover_color="#388bfd"
            )
            chk.pack(anchor="w", padx=35, pady=5)
            self.vars_check[opcao] = var

        btn_avancar2 = ctk.CTkButton(
            self.formularioDados,
            text="Avançar para Entrada de Dados ➔",
            font=("Arial", 11, "bold"),
            fg_color="#238636",
            hover_color="#2ea043",
            width=230,
            height=32,
            command=lambda: self.carregar_etapa3_entradas(categoria_selecionada)
        )
        btn_avancar2.pack(padx=30, pady=(20, 20))

        self.redimensionar_e_reorganizar(None)

    def carregar_etapa3_entradas(self, categoria):
        self.categoria_atual_processada = categoria
        opcoes_escolhidas = [op for op, var in self.vars_check.items() if var.get()]

        if not opcoes_escolhidas:
            return 

        campos_necessarios = set()
        for op in opcoes_escolhidas:
            campos_da_opcao = self.mapa_classificacoes[categoria][op]
            campos_necessarios.update(campos_da_opcao)

        for child in self.formularioDados.winfo_children():
            child.destroy()

        ctk.CTkLabel(
            self.formularioDados,
            text="⚡ Preenchimento dos Atributos Exigidos",
            font=("Arial", 13, "bold"),
            text_color="#3fb950",
            fg_color="transparent"
        ).pack(padx=30, pady=(20, 5))

        resumo_opcoes = " + ".join(opcoes_escolhidas)
        ctk.CTkLabel(
            self.formularioDados,
            text=f"Análises: {resumo_opcoes}",
            font=("Arial", 8, "italic"),
            text_color="#8b949e",
            fg_color="transparent",
            wraplength=380
        ).pack(padx=30, pady=(0, 15))

        self.entradas_dados = {}

        frame_inputs = ctk.CTkFrame(self.formularioDados, fg_color="transparent")
        frame_inputs.pack(padx=20, pady=5)

        for campo in sorted(list(campos_necessarios)):
            row_frame = ctk.CTkFrame(frame_inputs, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)

            lbl = ctk.CTkLabel(
                row_frame,
                text=f"{campo}:",
                font=("Arial", 10, "bold"),
                text_color="#c9d1d9",
                fg_color="transparent",
                width=180,
                anchor="e"
            )
            lbl.pack(side="left", padx=(0, 10))

            entry = ctk.CTkEntry(
                row_frame,
                placeholder_text="Informe o valor",
                width=160,
                height=28,
                fg_color="#161b22",
                border_color="#30363d"
            )
            entry.pack(side="left")
            self.entradas_dados[campo] = entry

        btn_executar = ctk.CTkButton(
            self.formularioDados,
            text="🚀 Processar via IA",
            font=("Arial", 11, "bold"),
            fg_color="#1f6beb",
            hover_color="#388bfd",
            width=200,
            height=34,
            command=self.executar_predicao_ia
        )
        btn_executar.pack(padx=30, pady=(20, 20))

        self.redimensionar_e_reorganizar(None)

    # Uma simulação de predição feito pela ia generativa
    def executar_predicao_ia(self):
        dados_usuario = {campo: entry.get() or "0.0" for campo, entry in self.entradas_dados.items()}
        print("=== DADOS DE ENTRADA COLETADOS ===")
        print(dados_usuario)

        cat = getattr(self, "categoria_atual_processada", "Geral")

        # Regra de classificação de exemplo do modelo IA
        if "Estrelas" in cat:
            predicao = "STAR (Anã Amarela - Classe G)"
        elif "galaxias" in cat:
            predicao = "GALAXY (Espiral Sc)"
        else:
            predicao = "QSO (Quasar Alto Redshift)"

        data_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resumo_entradas = str(dados_usuario).replace("'", "").replace("{", "").replace("}", "")[:35] + "..."

        # Se a tabela ainda não existir no formulário, ela é construída
        if self.tabela is None:
            self._construir_tabela_e_botoes_crud()

        # Insere a predição atual no histórico visual da tabela
        self.tabela.insert("", "end", values=(self.contador_id, cat, predicao, resumo_entradas, data_registro))
        
        print(f"[MYSQL INSERT] INSERT INTO tb_classificacoes VALUES ({self.contador_id}, '{cat}', '{predicao}', '{data_registro}');")
        self.contador_id += 1

        # Redimensiona o container arredondado para cobrir a nova tabela
        self.redimensionar_e_reorganizar(None)
        messagebox.showinfo("Classificação Concluída", f"Predição Realizada com Sucesso!\nResultado: {predicao}")

    def _construir_tabela_e_botoes_crud(self):
        """Desenha a tabela Treeview e a barra de botões CRUD dentro do formulário"""
        frame_tabela_container = ctk.CTkFrame(self.formularioDados, fg_color="transparent")
        frame_tabela_container.pack(fill="x", padx=20, pady=(10, 15))

        ctk.CTkLabel(
            frame_tabela_container,
            text="📋 Histórico de Classificações & Banco de Dados (CRUD)",
            font=("Arial", 11, "bold"),
            text_color="#58a6ff"
        ).pack(anchor="w", pady=(5, 5))

        # Estilização da tabela com tema dark
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#161b22", foreground="#c9d1d9", fieldbackground="#161b22", rowheight=24, font=('Arial', 9))
        style.configure("Treeview.Heading", background="#21262d", foreground="white", font=('Arial', 9, 'bold'))
        style.map("Treeview", background=[('selected', '#1f6beb')], foreground=[('selected', 'white')])

        colunas = ("id", "categoria", "predicao", "entradas", "data")
        self.tabela = ttk.Treeview(frame_tabela_container, columns=colunas, show="headings", height=5)

        self.tabela.heading("id", text="ID")
        self.tabela.heading("categoria", text="Categoria")
        self.tabela.heading("predicao", text="Predição IA")
        self.tabela.heading("entradas", text="Valores Inseridos")
        self.tabela.heading("data", text="Data/Hora")

        self.tabela.column("id", width=40, anchor="center")
        self.tabela.column("categoria", width=140)
        self.tabela.column("predicao", width=140, anchor="center")
        self.tabela.column("entradas", width=160)
        self.tabela.column("data", width=120, anchor="center")

        self.tabela.pack(fill="x", expand=True, pady=5)

        # BARRA DE BOTÕES CRUD
        frame_botoes = ctk.CTkFrame(frame_tabela_container, fg_color="transparent")
        frame_botoes.pack(fill="x", pady=5)

        btn_read = ctk.CTkButton(
            frame_botoes, text="🔍 Ler (READ)", font=("Arial", 10, "bold"), fg_color="#21262d", hover_color="#30363d", width=110, height=28, command=self.crud_read
        )
        btn_read.pack(side="left", padx=4)

        btn_update = ctk.CTkButton(
            frame_botoes, text="✏️ Editar (UPDATE)", font=("Arial", 10, "bold"), fg_color="#d97706", hover_color="#b45309", width=110, height=28, command=self.crud_update
        )
        btn_update.pack(side="left", padx=4)

        btn_delete = ctk.CTkButton(
            frame_botoes, text="🗑️ Excluir (DELETE)", font=("Arial", 10, "bold"), fg_color="#da3633", hover_color="#f85149", width=110, height=28, command=self.crud_delete
        )
        btn_delete.pack(side="left", padx=4)

    # Uma simulação de banco de dados também feito pela ia
    def crud_read(self):
        sel = self.tabela.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um registro na tabela para visualizar.")
            return
        vals = self.tabela.item(sel[0])["values"]
        messagebox.showinfo("Detalhes do Registro", f"ID: {vals[0]}\nCategoria: {vals[1]}\nPredição: {vals[2]}\nAtributos: {vals[3]}\nData: {vals[4]}")

    def crud_update(self):
        sel = self.tabela.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um registro na tabela para alterar.")
            return
        item = sel[0]
        vals = list(self.tabela.item(item)["values"])
        vals[2] = "RE-CLASSIFICADO (Manual)"
        self.tabela.item(item, values=vals)
        print(f"[MYSQL UPDATE] UPDATE tb_classificacoes SET predicao='{vals[2]}' WHERE id={vals[0]};")
        messagebox.showinfo("Sucesso", f"Registro ID #{vals[0]} atualizado no Banco de Dados!")

    def crud_delete(self):
        sel = self.tabela.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um registro na tabela para apagar.")
            return
        item = sel[0]
        id_reg = self.tabela.item(item)["values"][0]
        self.tabela.delete(item)
        print(f"[MYSQL DELETE] DELETE FROM tb_classificacoes WHERE id={id_reg};")
        messagebox.showinfo("Sucesso", f"Registro ID #{id_reg} deletado do Banco de Dados!")
        self.redimensionar_e_reorganizar(None)

    def abrir_classificacao_imagens(self):
        print("Módulo de Classificação Morfológica por Visão Computacional")
        self.esconder_tudo()

    def atualizar_fundo_vetorial(self, id_fundo, id_window, anchor="nw", margem=4, raio=12, largura_borda=1):
        self.update_idletasks()
        bbox = self.canvas.bbox(id_window)
        if bbox:
            x1, y1, x2, y2 = bbox
            x1 -= margem
            y1 -= margem
            x2 += margem
            y2 += margem
            
            pontos = [
                x1+raio, y1, x2-raio, y1, x2, y1, x2, y1+raio,
                x2, y2-raio, x2, y2, x2-raio, y2, x1+raio, y2,
                x1, y2, x1, y2-raio, x1, y1+raio, x1, y1
            ]
            self.canvas.coords(id_fundo, *pontos)
            self.canvas.tag_lower(id_fundo, id_window)

    def redimensionar_e_reorganizar(self, event):
        largura = self.winfo_width()
        altura = self.winfo_height()
        
        posicao_x_centro = largura // 2
        
        self.canvas.coords(self.id_titulo, posicao_x_centro, 55)
        self.canvas.coords(self.id_subtitulo, posicao_x_centro, altura - 25)
        
        self.canvas.coords(self.id_card_dataset, 40, 110)
        self.atualizar_fundo_vetorial(self.id_fundo_card_dataset, self.id_card_dataset, anchor="nw")
        
        self.canvas.coords(self.id_card_metricas, largura - 40, 110)
        self.atualizar_fundo_vetorial(self.id_fundo_card_metricas, self.id_card_metricas, anchor="ne")
        
        posicao_x_direita = largura - 40
        posicao_y_menu = altura // 2 + 50
        self.canvas.coords(self.id_card_central, posicao_x_direita, posicao_y_menu)
        self.atualizar_fundo_vetorial(self.id_fundo_card_central, self.id_card_central, anchor="ne", largura_borda=2)

        self.canvas.coords(self.id_btn_voltar, 35, 35)
        self.atualizar_fundo_vetorial(self.id_fundo_btn_voltar, self.id_btn_voltar, anchor="nw", margem=2, raio=10)

        if self.id_card_form and self.id_fundo_form:
            posicao_y_centro = altura // 2
            self.canvas.coords(self.id_card_form, posicao_x_centro, posicao_y_centro)
            self.atualizar_fundo_vetorial(
                self.id_fundo_form,
                self.id_card_form,
                anchor="center",
                largura_borda=2
            )

    def destroy(self):
        if self.cap:
            self.cap.release()
        super().destroy()


if __name__ == "__main__":
    app = canvaIA()
    app.mainloop()