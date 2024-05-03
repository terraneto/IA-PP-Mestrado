# UTILIZAÇÃO DE INTELIGÊNCIA ARTIFICIAL PARA COMBATER O SOBREPREÇO: aplicação de Machine Learning na pesquisa de preços de contratações de TI no Senado Federal

### Autor: Rubens Vasconcellos Terra Neto

## Introdução

O presente repositório se destina ao armazenamento dos dados e dos programas fonte desenvolvidos durante a elaboração da pesquisa elaborada no período de Março de 2022 a dezembro de 2023 como trabalho de conclusão de curso do Mestrado Profissional em Poder Legislativo da Câmara dos Deputados sob a supervisão do Prof. Dr. Fabiano Peruzzo Schwartz. O estudo propõe a construção de um algoritmo baseado em Inteligência Artificial e Deep learning capaz de indicar possíveis indícios de sobrepreços durante a fase de pesquisa de preços em Contratações de Tecnologia da Informação do Senado Federal, de forma a disponibilizar ao gestor público um ferramental que o ajude a elaborar projetos com maior acurácia, tendendo a minorar a preocupação e a inação de inúmeros gestores, decorrente do temor de ser auditado por um órgão de controle, que está muito mais preparado.


## Problema de Pesquisa

Toda contratação pública é feita através de processo licitatório e uma das etapas do planejamento desta contratação é a pesquisa de preços. Cabe ao gestor público buscar realizar esta fase com a maior acurácia possível, já que uma pesquisa de preços mal formulada é uma das causas de improbidades e irregularidades causadoras de dano ao erário na administração pública conforme Borges Júnior (2020).

Cabe destacar que a utilização de tecnologias nos órgãos de controle está muito mais aprimorada do que as tecnologias disponíveis para o gestor, como podemos notar no artigo de Peci e Braga (2021):

> Enquanto os órgãos de controle contam com recursos humanos especializados, com bases de dados sofisticados e com acesso privilegiado a dados sigilosos de transações financeiras e outras informações cruciais para compreender complexos cenários marcados pela corrupção, esta mesma capacidade não está disponível para o gestor público, o responsável direto pela tomada de decisões de políticas públicas. (PECI; BRAGA, 2021)

Neste sentido, pretende-se neste estudo utilizar a tecnologia de Machine Learning para treinar uma Inteligência Artificial para avaliar as contratações de tecnologia da informação, de forma a indicar a probabilidade de ocorrer sobrepreço. Por meio da utilização dos dados abertos das contratações, em especial os Dados Abertos do Sistema Integrado de Administração e Serviços Gerais – SIASG do Governo Federal.

Pretende-se elaborar um banco de dados a ser utilizado no treinamento de uma Inteligência Artificial, de forma a poder estimar a probabilidade de sobrepreço e o grau de acurácia da pesquisa. Como há uma gama muito grande de tipos de objetos possíveis, durante a pesquisa será selecionada uma categoria de objeto para servir de embrião para a modelagem da Inteligência Artificial (IA), já que não se possui tempo e recursos suficientes para poder no prazo da pesquisa desenvolver uma ferramenta que possa avaliar todo e qualquer tipo de objeto.

Esta impossibilidade está ligada ao fato de que quanto melhor forem os dados utilizados no treinamento da IA melhor será o seu desempenho. O processo de preparação dos dados coletados é fundamental não apenas para preparar a máquina para a realização das previsões, mas também para possibilitar o aprimoramento constante das habilidades de previsão.

Pretende-se ao final do estudo responder a seguinte questão “Qual o grau de confiabilidade pode-se conseguir com a utilização de machine learning na detecção de sobrepreço nas pesquisas de preço das contratações de tecnologia da informação?”.


## Objetivo

### Objetivo Geral

Desenvolver um algoritmo baseado em Inteligência Artificial e Deep learning capaz de
indicar possíveis indícios de sobrepreços durante a fase de pesquisa de preços em Contratações
de Tecnologia da Informação do Senado Federal.

### Objetivos específicos

• Levantar Bases de Dados existentes sobre às contratações de tecnologia da informação;

• Desenvolver uma ferramenta para obtenção e pré-processamento dos dados necessários
ao Treinamento da Inteligência Artificial;

• Disponibilizar repositório público dos dados de contratações de TI utilizado pela ferra-
menta;

• Levantar as técnicas, métodos e boas práticas mais recentes utilizados na detecções de
fraudes em compras;

• Treinar e utilizar um modelo de Inteligência Artificial na detecção
de sobrepreço nas contratações do banco de dados preparado;

• Prover uma ferramenta de avaliação de indícios de sobrepreços para uso efetivo no Senado
Federal;

• Avaliar o grau de confiabilidade da ferramenta na predição de sobrepreço;

## Estrutura do Repositório

### Dados consolidados das diversas tabelas da API de Compras Governamentais 

[Dados-APIComprasGovernamentais](Dados-APIComprasGovernamentais)

### JupyterNotebooks utilizados para a geração das tabelas do relatório

[Jupyter](Jupyter)

### Fontes do aplicativo desenvolvido

[PesqPrecos](PesqPrecos)

### Relatório de pesquisa do Mestrado Profissional em Poder Legislativo da Câmara dos Deputados

[Relatório Técnico](Relatório Técnico)

