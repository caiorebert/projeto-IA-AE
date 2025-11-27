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
        medias_competencias = df[["nota_c1", "nota_c2", "nota_c3", "nota_c4", "nota_c5"]].mean().round(2)
        st.write(medias_competencias)
        st.markdown("""
        **Como interpretar:**  
        Esta tabela mostra a média das notas para cada competência avaliadas na turma.  
        Valores mais altos indicam melhor desempenho coletivo naquela competência.  
        O professor pode focar nas competências com médias mais baixas para direcionar reforços.
        """)

        st.subheader("Distribuição das Notas Finais (Histograma)")
        fig_hist = px.histogram(
            df,
            x="nota_final",
            nbins=10,
            title="Distribuição das Notas Finais na Turma",
            labels={"nota_final": "Nota Final"}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
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
        medias_erros = df[["metrica_um", "metrica_dois", "metrica_tres"]].mean().round(2)
        st.write(medias_erros)
        st.markdown("""
        **Como interpretar:**  
        Esta tabela mostra o número médio de erros detectados em pontuação, acentuação e grafia por aluno.  
        Áreas com médias elevadas indicam pontos fracos gerais da turma que podem ser trabalhados em aula.
        """)

    with tab_resumo:
       st.subheader("Resumo Automático para o Professor")

    cols_comp = [f"nota_c{i}" for i in range(1, 6)]
    soma_competencias = df[cols_comp].sum()
    # pega as 2 piores, não apenas 1
    pior_competencias = soma_competencias.nsmallest(2)
    melhor_competencia = soma_competencias.idxmax()
    melhor_media = soma_competencias.max()

    # monta o texto das piores competências
    if len(pior_competencias) >= 2:
        texto_piores = (
            f"- **{pior_competencias.index[0]}**, com média de {pior_competencias.values[0]}\n"
            f"- **{pior_competencias.index[1]}**, com média de {pior_competencias.values[1]}"
        )
    else:
        # fallback caso só haja um elemento por algum motivo
        texto_piores = f"- **{pior_competencias.index[0]}**, com média de {pior_competencias.values[0]}"

    st.markdown(f"""
    ✅ **Competência de Destaque:**  
    Parabéns, sua turma está apresentando melhor desempenho na **{melhor_competencia}**, com soma de {melhor_media}.

    ⚠️ **Competências que Precisam de Atenção:**  
    Sua turma demonstra mais dificuldade em:  
    {texto_piores}

    Recomendamos focar reforços e atividades nessas competências para melhorar o desempenho coletivo.
    """)

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
