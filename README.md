# UTILIZAÇÃO DE INTELIGÊNCIA ARTIFICIAL PARA COMBATER O SOBREPREÇO: aplicação de Machine Learning na pesquisa de preços de contratações de TI no Senado Federal

### Autor: Rubens Vasconcellos Terra Neto

> Status do Projeto: :heavy_check_mark: :warning: (em desenvolvimento)

## Introdução

O presente repositório se destina ao armazenamento dos dados e dos programas fonte desenvolvidos durante a elaboração da pesquisa elaborada no período de Março de 2022 a julho de 2023 como trabalho de conclusão de curso do Mestrado Profissional em Poder Legislativo da Câmara dos Deputados sob a supervisão do Prof. Dr. Fabiano Peruzzo Schwartz. O estudo propõe a construção de um algoritmo baseado em Inteligência Artificial e Deep learning capaz de indicar possíveis indícios de sobrepreços durante a fase de pesquisa de preços em Contratações de Tecnologia da Informação do Senado Federal, de forma a disponibilizar ao gestor público um ferramental que o ajude a elaborar projetos com maior acurácia, tendendo a minorar a preocupação e a inação de inúmeros gestores, decorrente do temor de ser auditado por um órgão de controle, que está muito mais preparado.


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

• Treinar e utilizar um modelo de Inteligência Artificial na estimativa de preços e detecção
de sobrepreço nas contratações de TI do banco de dados preparado;

• Prover uma ferramenta de avaliação de indícios de sobrepreços para uso efetivo no Senado
Federal;

• Avaliar o grau de confiabilidade da ferramenta na predição de sobrepreço;

## Cronograma

## Relatório de pesquisa do Mestrado Profissional em Poder Legislativo da Câmara dos Deputados

## Referências Bibliográficas da Pesquisa

BORGES JÚNIOR, R. A. A pesquisa de preços e seu papel fundamental nas licitações públicas. 2020. Disponível em: https://jus.com.br/artigos/79447/a-pesquisa-de-precos-e-seu-papel-fundamental-nas-licitacoes-publicas. Acesso em: 01 ago. 2021.

BRASIL. Lei nº 8.666, de 21 de junho de 1993. Regulamenta o art. 37, inciso XXI, da Constituição Federal, institui normas para licitações e contratos da Administração Pública e dá outras providências. Diário Oficial da União, Brasília, DF, jun. 1993. Disponível em: http://www.planalto.gov.br/ccivil_03/leis/L8666compilado.htm. Acesso em: 07 maio 2019.

BRASIL. Lei nº 10.520, de 17 de julho de 2002. Institui, no âmbito da União, Estados, Distrito Federal e Municípios, nos termos do art. 37, inciso XXI, da Constituição Federal, modalidade de licitação denominada pregão, para aquisição de bens e serviços comuns, e dá outras providências. Diário Oficial da União, Brasília, DF, jul. 2002. Disponível em: http://www.planalto.gov.br/ccivil_03/leis/2002/l10520.htm. Acesso em: 01 ago. 2021.

BRASIL. Lei nº 14.133, de 1º de abril de 2021. Lei de Licitações e Contratos Administrativos. Diário Oficial da União, Brasília, DF, abr. 2021. Disponível em: http://www.planalto.gov.br/ccivil_03/_ato2019-2022/2021/lei/L14133.htm. Acesso em: 21 mar. 2022.

BRASIL. Ministério da Economia. API de compras governamentais. 2021. Disponível em: http://compras.dados.gov.br/docs/home.html. Acesso em: 21 mar. 2022. 

BRASIL. Ministério da Economia. Painel de Preços. 2022. Url=https://paineldeprecos.planejamento.gov.br/. Acesso em: 05.09.2022. 

FORTINI, C.; MOTTA, F. Corrupção nas licitações e contratações públicas: sinais de alerta segundo a transparência internacional. A&C - Revista de Direito Administrativo & Constitucional, Revista de Direito Administrativo and Constitucional, v. 16, n. 64, p. 93, 2016. P. 27-44. 

FORTINI, C.; SHERMAN, A. Governança pública e combate à corrupção: novas perspectivas para o controle da administração pública brasileira. Interesse Público - IP, v. 19, n. 102, p. 27–44, 2017. Disponível em: https://www.editoraforum.com.br/wp-content/uploads/2017/11/governanca-combate-corrupcao.pdf. Acesso em: 21 mar. 2022. 

GÉRON Aurélien. Mãos à Obra: Aprendizado de máquina com scikit-learn, keras e tensorflow. 2ª. ed. Rio de Janeiro/RJ: Alta Books Editora, 2021. 640 p. ISBN 978-85-5081-548-0.

JUNQUILHO, T. A.; MAIA FILHO, M. S. Inteligência Artificial no Poder Judiciário: lições do Projeto Victor. v. 8, n. 48, 2021. Disponível em: https://revista.unitins.br/index.php/humanidadeseinovacao/article/view/5615. Acesso em: 23 mar. 2022. 

LIMA, W. C. Dados abertos governamentais no contexto da ciência cidadã: o caso da operação serenata de amor. In: IX ENCONTRO IBÉRICO DA ASOCIACIÓN DE EDUCACIÓN E INVESTIGACIÓN EN CIENCIA DE LA INFORMACIÓN DE IBEROAMÉRICA Y EL CARIBE (EDICIC), 9., 2019. Anais... 2019. Disponível em: http://hdl.handle.net/10316/95874. Acesso em: 21 mar. 2022. 

MATOS, G. R. Machine learning aplicado à gestão de activos físicos industriais. Dissertação (Mestrado em Engenharia Mecânica) — Instituto Superior de Engenharia de Lisboa, Lisboa, 2021. Disponível em: http://hdl.handle.net/10400.21/13524. Acesso em: 21 mar. 2022.

NOHARA, I. P.; COLOMBO, B. A. Tecnologias cívicas na interface entre direito e inteligência artificial: Operação serenata de amor para gostosuras ou travessuras? Revista de Direito Administrativo & Constitucional, v. 19, n. 76, p. 83, 2019. Disponível em: http://www.revistaaec.com/index.php/revistaaec/article/download/1100/807. Acesso em: 21 mar. 2022.

OLIVEIRA, C. C. O uso de Inteligência Artificial para Controle Social da Administração Pública: Uma Análise da Operação Serenata de Amor. Trabalho de Conclusão de Curso (Especialização em Gestão Pública) — Universidade Federal de São João del-Rei, 2018. Disponível em: http://hdl.handle.net/123456789/267. Acesso em: 21 mar. 2022. 

PANIS, A. C. Inovação em compras públicas: estudo de caso do robô ALICE da Controladoria-Geral da União (CGU). Dissertação (Mestrado em Administração) — Universidade de Brasília, 2020. Disponível em: https://repositorio.unb.br/handle/10482/38639. Acesso em: 21 mar. 2022. 

PECI, A.; BRAGA, M. V. A. Corrupção e capacidades assimétricas da gestão e do controle. Estadão, abr. 2021. Disponível em: https://repositorio.ufsc.br/bitstream/handle/123456789/222445/[corrupç~ao]corrupç~aoecapacidadesassimétricasdagest~aoedocontrole-estadao.pdf?sequence=1&isAllowed=y. Acesso em: 21 mar. 2022. 

POSSAMAI, A. J. Dados abertos no governo federal brasileiro : desafios de
transparência e interoperabilidade. 313 p. Tese (Doutorado em Ciência Política) —
Universidade Federal do Rio Grande do Sul. Instituto de Filosofia e Ciências Humanas.
Programa de Pós-Graduação em Ciência Política., Porto Alegre/RS, 2016. Disponível em:
http://hdl.handle.net/10183/156363. Acesso em: 25 abr. 2022. 

SENADO FEDERAL. Dados Abertos. 2022. Disponível em: https://www12.senado.leg.br/
dados-abertos. Acesso em: 29 abr. 2022. 

SILVA, A. V. e. Dados governamentais abertos à luz da accountability : um
estudo da Operação Serenata de Amor. Trabalho de Conclusão de Curso (Bacharelado
em Ciência Política) — Universidade de Brasília, Brasília, 2018. Disponível em:
https://bdm.unb.br/handle/10483/22555. Acesso em: 21 mar. 2022. 

SILVEIRA, S. M. A inteligência de fontes abertas na prevenção e combate a
corrupção em processo licitatório para aquisição de equipamentos de engenharia.
Trabalho de Conclusão de Curso (Especialização) – Curso Gestão, Assessoramento e
Estado-Maior — Escola de Formação Complementar do Exército, 2021. Disponível em:
https://bdex.eb.mil.br/jspui/handle/123456789/9529. Acesso em: 23 abr. 2022. C

SPEDICATO, G. A.; DUTANG, C.; PETRINI, L. Machine Learning Methods to Perform Pricing
Optimization. A Comparison with Standard GLMs. Variance, Casualty Actuarial Society,
v. 12, n. 1, p. 69–89, 2018. Disponível em: https://hal.archives-ouvertes.fr/hal-01942038.
Acesso em: 21 mar. 2022.

TRIBUNAL DE CONTAS DA UNIÃO. 5 motivos para a abertura de dados
na Administração Pública. [S.l.], 2015. Disponível em: https://portal.tcu.gov.br/
5-motivos-para-a-abertura-de-dados-na-administracao-publica.htm. Acesso em: 25 abr. 2022.

WOLSTAD, H. W. Machine learning as a tool for improved housing price
prediction : the applicability of machine learning in housing price prediction
and the economic implications of improvement to prediction accuracy.
Dissertação (Mestrado) — Norwegian School of Economics, 2020. Disponível em:
https://openaccess.nhh.no/nhh-xmlui/handle/11250/2739783. Acesso em: 21 mar. 2022.
