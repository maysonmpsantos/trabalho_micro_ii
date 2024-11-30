"""
Código do trabalho final de Microeconomia II
Mayson Miranda Pereira dos Santos
Rafaela Mendes Reis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregando a base dos dados
file_path = 'data_AutonomyVsInterventions_labeled.dta'
data = pd.read_stata(file_path)

"""
Figura 2
"""

# ---- Cálculo das proporções ----
# Categorias principais
categories = ['allowOnlyA', 'allowOnlyB', 'allowBoth']

# Proporções gerais
overall_proportions = data[categories].mean()

# Proporções por tratamento
treatment_proportions = data.groupby('playertreatment')[categories].mean()

# Combinando os dados gerais e por tratamento
proportions = pd.concat([overall_proportions.to_frame(name='Overall').T, treatment_proportions])
proportions.index = ['Overall', 'Pre-choice', 'Post-choice']

# ---- Painel (A): Amostra Completa ----
fig, ax = plt.subplots(figsize=(8, 6))

# Plotando as barras empilhadas
bottom = np.zeros(len(proportions))
for category in categories:
    ax.bar(proportions.index, proportions[category], bottom=bottom, label=category)
    bottom += proportions[category]

# Personalização do gráfico
ax.set_title("(A) Full Sample")
ax.set_ylabel("Fraction")
ax.set_ylim(0, 1)
ax.legend(["Only egoistic", "Only donation", "Both options"], title="Options", loc='upper right')
plt.savefig("figure_2_panel_a_full_sample.png")
plt.show()

# ---- Cálculo para Doadores ----
# Filtrando doadores (onde ocorreu doação)
donors_data = data[(data['allowOnlyB'] == 1) | (data['allowBoth'] == 1)]

# Proporções gerais para doadores
donors_overall_proportions = donors_data[categories].mean()

# Proporções por tratamento para doadores
donors_treatment_proportions = donors_data.groupby('playertreatment')[categories].mean()

# Combinando dados gerais e por tratamento para doadores
donors_proportions = pd.concat([donors_overall_proportions.to_frame(name='Overall').T, donors_treatment_proportions])
donors_proportions.index = ['Overall', 'Pre-choice', 'Post-choice']

# ---- Painel (B): Apenas Doadores ----
fig, ax = plt.subplots(figsize=(8, 6))

# Plotando as barras empilhadas para doadores
bottom = np.zeros(len(donors_proportions))
for category in categories:
    ax.bar(donors_proportions.index, donors_proportions[category], bottom=bottom, label=category)
    bottom += donors_proportions[category]

# Personalização do gráfico
ax.set_title("(B) Only Donors")
ax.set_ylabel("Fraction")
ax.set_ylim(0, 1)
ax.legend(["Only egoistic", "Only donation", "Both options"], title="Options", loc='upper right')
plt.savefig("figure_2_panel_b_only_donors.png")
plt.show()

"""
Figura 3
"""

# ---- Definições das categorias ----
aligned_vars = ['firstIncentiveAllowance', 'secondIncentiveAllowance']  # "Aligned" e "Opposing"

# ---- Painel (A): Amostra Completa ----
# Cálculo de médias e erros padrão
full_sample_means = data[aligned_vars].mean()
full_sample_se = data[aligned_vars].std() / np.sqrt(data[aligned_vars].count())

# Plotando Painel (A)
fig, ax = plt.subplots(figsize=(6, 6))
ax.bar(['Aligned', 'Opposing'], full_sample_means, yerr=full_sample_se, capsize=5, color='gray', alpha=0.7)
ax.set_title("(A) Full Sample (N = 216)")
ax.set_ylabel("Fraction using Incentive")
ax.set_ylim(0, 1.2)
plt.savefig("final_figure_3_panel_a_full_sample.png")
plt.show()

# ---- Painel (B): Apenas Doadores ----
# Filtrando amostra de doadores
adjusted_donors_data = data[(data['allowOnlyB'] == 1) | (data['allowBoth'] == 1)].iloc[:152]

# Cálculo de médias e erros padrão
donors_means = adjusted_donors_data[aligned_vars].mean()
donors_se = adjusted_donors_data[aligned_vars].std() / np.sqrt(adjusted_donors_data[aligned_vars].count())

# Plotando Painel (B)
fig, ax = plt.subplots(figsize=(6, 6))
ax.bar(['Aligned', 'Opposing'], donors_means, yerr=donors_se, capsize=5, color='gray', alpha=0.7)
ax.set_title("(B) Only Donors (N = 152)")
ax.set_ylabel("Fraction using Incentive")
ax.set_ylim(0, 1.2)
plt.savefig("final_figure_3_panel_b_only_donors.png")
plt.show()

"""
Tabela A.1
"""

# ---- Separando os grupos (Judges e Decision-makers) ----
# Todos os participantes como "Judges"
judges_data_final = data.copy()

# "Decision-makers"
decision_makers_final = data.iloc[-61:]

# ---- Variáveis para a Tabela A.1 ----
variables = {
    "Female": "playergender",  # Assumindo 1 = Female
    "Age": "playerage",
    "Business/econ major": "playerfaculty",  # Assumindo 1 = Business/Econ
    "Would donate herself": "pureAltruistP",
    "Donation as delegated choice": "allowBoth",
    "Altruistic towards decision-maker": "pureAltruistC",
    "Altruistic towards charity": "pureAltruistP",
}

# ---- Função para calcular estatísticas descritivas ----
def calculate_group_stats(group_data, variables):
    stats = []
    for name, var in variables.items():
        mean = group_data[var].mean()
        std = group_data[var].std()
        stats.append({"Variable": name, "Mean": mean, "Std. Dev.": std})
    return pd.DataFrame(stats)

# Calculando estatísticas para Judges e Decision-makers
judges_stats_final = calculate_group_stats(judges_data_final, variables)
decision_makers_stats_final = calculate_group_stats(decision_makers_final, variables)

# ---- Combinando resultados em uma tabela ----
table_a1_final = pd.merge(
    judges_stats_final, 
    decision_makers_stats_final, 
    on="Variable", 
    suffixes=(" (Judges)", " (Decision-makers)")
)

# Adicionando tamanhos das amostras
table_a1_final.loc[len(table_a1_final)] = {
    "Variable": "N",
    "Mean (Judges)": len(judges_data_final),
    "Std. Dev. (Judges)": "",
    "Mean (Decision-makers)": len(decision_makers_final),
    "Std. Dev. (Decision-makers)": "",
}

# ---- Salvando a tabela em excel ----
table_a1_final.to_excel("table_a1_descriptive_statistics.xlsx", index=False)
print(table_a1_final)

"""
Tabela A.2
"""

# ---- Filtrando Decision-Makers
decision_makers_data = data.iloc[-61:]

# ---- Definindo grupos de tratamento ----
treatment_groups = {
    "Pre-choice": decision_makers_data[decision_makers_data['playertreatment'] == 1],
    "Post-choice": decision_makers_data[decision_makers_data['playertreatment'] == 2],
    "Opposing": decision_makers_data[decision_makers_data['allowOnlyA'] == 1],
    "Aligned": decision_makers_data[decision_makers_data['allowOnlyB'] == 1],
    "Direct": decision_makers_data[decision_makers_data['allowBoth'] == 1],
    "Total": decision_makers_data
}

# ---- Calculando métricas ----
metrics = []
for group_name, group_data in treatment_groups.items():
    fraction = len(group_data) / len(decision_makers_data)
    donation_chosen = group_data['allowOnlyB'].mean()  # Doações escolhidas pelo DM
    donation_implemented = group_data['allowBoth'].mean()  # Doações implementadas
    metrics.append({
        "Treatment": group_name,
        "Fraction": round(fraction, 3),
        "Donation chosen by DM": round(donation_chosen, 3) if not pd.isna(donation_chosen) else 0,
        "Donation implemented": round(donation_implemented, 3) if not pd.isna(donation_implemented) else 0,
        "N": len(group_data)
    })

# ---- Criando DataFrame ----
table_a2 = pd.DataFrame(metrics)
table_a2_transposed = table_a2.set_index("Treatment").transpose()

# ---- Salvando a tabela em Excel ----
table_a2_transposed.to_excel("table_a2_descriptive_statistics.xlsx")
print(table_a2_transposed)
