import streamlit as st
import pandas as pd
import plotly.express as px

def render_dashboard(chat_history: list[dict]) -> None:
    st.header("Dashboard de Métricas da Turma")

    if not chat_history:
        st.info("Nenhuma métrica para exibir.")
        return

    df = pd.DataFrame(chat_history)

    tab_graficos, tab_resumo, tab_legenda = st.tabs([
        "Gráficos e Estatísticas", 
        "Resumo para o Professor", 
        "Legenda das Métricas"
    ])

    with tab_graficos:
        st.subheader("Médias das Notas por Competência")

        cols_competencias = ["nota_c1", "nota_c2", "nota_c3", "nota_c4", "nota_c5"]
        medias = df[cols_competencias].mean().round(2)

        df_exibicao = pd.DataFrame({
            "Competência": [
                "Domínio da modalidade escrita formal da língua portuguesa",
                "Compreensão do tema e aplicação de conhecimentos",
                "Seleção e organização de argumentos",
                "Coesão textual",
                "Proposta de intervenção"],
            "Média da Turma": medias.values
        })

        st.dataframe(
            df_exibicao,
            hide_index=True,
            use_container_width=True
        )

        st.markdown("""
        **Como interpretar:**  
        Esta tabela mostra a média das notas para cada competência avaliadas na turma.  
        Valores mais altos indicam melhor desempenho coletivo naquela competência.  
        O professor pode focar nas competências com médias mais baixas para direcionar reforços.
        """)

        st.subheader("Distribuição das Notas Finais (Histograma)")
        df["Redacao_ID"] = df["Interação"].astype(str)

        fig_barras = px.bar(
            df,
            x="Redacao_ID",
            y="nota_final",
            text="nota_final",
            range_y=[0, 1000],
            title="Desempenho da Redação",
            labels={"nota_final": "Nota Final", "Redacao_ID": "Redação nº"}
        )

        fig_barras.update_traces(
            marker_color='#64FFDA',
            textposition='outside',
            width=0.4
        )

        fig_barras.update_layout(
            yaxis=dict(showgrid=True, gridcolor='#444'),
            xaxis=dict(showgrid=False)
        )

        st.plotly_chart(fig_barras, use_container_width=True)
        st.markdown("""
        **Como interpretar:**  
        O histograma mostra quantos alunos ficaram em cada faixa de nota.  
        Se a maioria estiver concentrada nas faixas baixas, a turma pode precisar de mais suporte.  
        Uma distribuição mais espalhada pode indicar diversidade no desempenho.
        """)

        if "Interação" in df.columns:
            st.subheader("Evolução da Nota Final ao Longo das Interações")
            media_por_interacao = df.groupby("Interação")["nota_final"].mean().reset_index()
            fig_media = px.line(
                media_por_interacao,
                x="Interação",
                y="nota_final",
                markers=True,
                labels={"nota_final": "Média da Nota Final", "Interação": "Interação"},
                title="Evolução da Nota Final na Turma"
            )
            st.plotly_chart(fig_media, use_container_width=True)
            st.markdown("""
            **Como interpretar:**  
            Este gráfico mostra se a média geral das notas está melhorando, piorando ou está estável conforme os alunos avançam nas interações.  
            Um crescimento indica progresso coletivo; quedas podem indicar dificuldades com novos temas ou conceitos.
            """)

        st.subheader("Média de Erros Linguísticos por Tipo")

        # 1. Seleciona as colunas e calcula a média
        cols_erros = ["metrica_um", "metrica_dois", "metrica_tres"]
        medias_erros = df[cols_erros].mean().round(2)

        # 2. Cria um DataFrame organizado com nomes amigáveis
        df_erros_exibicao = pd.DataFrame({
            "Tipo de Erro": ["Pontuação", "Acentuação", "Grafia"],  # Nomes reais
            "Média de Erros": medias_erros.values
        })

        # 3. Exibe a tabela limpa
        st.dataframe(
            df_erros_exibicao,
            hide_index=True,  # Remove a coluna de índice numérico
            use_container_width=True  # Ajusta à largura da tela
        )

        st.markdown("""
                **Como interpretar:** Esta tabela mostra o número médio de erros detectados em pontuação, acentuação e grafia por aluno.  
                Áreas com médias elevadas indicam pontos fracos gerais da turma que podem ser trabalhados em aula.
                """)

    with tab_resumo:
        st.subheader("Resumo Automático para o Professor")

        nomes_competencias = {
            "nota_c1": "C1: Escrita Formal",
            "nota_c2": "C2: Compreensão do Tema",
            "nota_c3": "C3: Argumentação",
            "nota_c4": "C4: Coesão Textual",
            "nota_c5": "C5: Proposta de Intervenção"
        }

        cols_comp = [f"nota_c{i}" for i in range(1, 6)]
        medias_competencias = df[cols_comp].mean().round(1)

        melhor_comp_cod = medias_competencias.idxmax()
        melhor_valor = medias_competencias.max()

        piores_comps = medias_competencias.nsmallest(2)

        with st.container():
            st.markdown("### Ponto Forte da Turma")
            st.success(
                f"**{nomes_competencias.get(melhor_comp_cod, melhor_comp_cod)}**\n\n"
                f"Esta é a competência com a maior média da turma: **{melhor_valor} pontos**."
            )

        st.divider()

        st.markdown("### Pontos de Atenção (Reforço Recomendado)")
        st.warning("Estas são as competências com as médias mais baixas. Considere revisar estes tópicos:")

        col1, col2 = st.columns(2)

        cod_pior_1 = piores_comps.index[0]
        val_pior_1 = piores_comps.values[0]
        with col1:
            st.metric(
                label=nomes_competencias.get(cod_pior_1, cod_pior_1),
                value=f"{val_pior_1} pontos",
                delta="- Média Baixa",
                delta_color="normal"
            )

        if len(piores_comps) > 1:
            cod_pior_2 = piores_comps.index[1]
            val_pior_2 = piores_comps.values[1]
            with col2:
                st.metric(
                    label=nomes_competencias.get(cod_pior_2, cod_pior_2),
                    value=f"{val_pior_2} pontos",
                    delta="- Média Baixa",
                    delta_color="normal"
                )

    with tab_legenda:
        st.subheader("Legenda das Métricas")
        st.markdown("""
        - **nota_final**: Nota global atribuída à redação.
        - **nota_c1** até **nota_c5**: Notas específicas por competência avaliativa.
        - **metrica_um**: Quantidade de erros de pontuação.
        - **metrica_dois**: Quantidade de erros de acentuação.
        - **metrica_tres**: Quantidade de erros de grafia.
        - **metrica_quatro**: Quantidade de erros de concordância verbal.
        - **metrica_cinco**: Quantidade de erros de concordância nominal.
        - **metrica_seis**: Nota atribuída para coerência textual.
        - **metrica_sete**: Quantidade de conectivos usados no texto.
        - **metrica_oito**: Variedade vocabular observada.
        - **metrica_nove**: Quantidade geral de erros gramaticais.
        - **metrica_dez**: Comprimento do texto em número de palavras.
        - **metrica_onze**: Sentimento predominante identificado no texto (ex: positivo, neutro, negativo).
        """)
