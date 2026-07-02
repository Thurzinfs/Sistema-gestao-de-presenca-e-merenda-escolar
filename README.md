# Sistema de Gestão de Presença e Merenda Escolar

## Visão Geral

O sistema monitora, por meio da carteirinha estudantil, a presença dos alunos na escola, permitindo:
 
- Registro de frequência escolar - presença de alunos na instituição.
- Contagem automática de refeições para a cantina - alimentação com base na mesma leitura de presença.
- Gestão da cantina: cardápio diário, controle de sobras e relatórios de movimentação.
- Envio automático de relatórios de contagem para a equipe da cantina via WhatsApp.

---

## Objetivo e critério de sucesso
 
- Gestão eficiente da merenda escolar, com quantidade de refeições calculada a partir de dados reais de presença.
- Frequência dos alunos registrada de forma organizada e auditável.
- Redução de desperdício de comida, a partir do cruzamento entre cardápio, quantidade de alunos e sobras.

---

## Escopo do projeto
 
### MVP (fase 1)
 
- Cadastro de escola, gestores, turmas, alunos e dispositivos.
- Importação em massa de alunos via planilha, com geração automática de QR code e exportação de carteirinhas em PDF.
- Leitura de presença e refeição via scanner(maquina) fixo(a) na entrada da escola.
- Contagem automática de presença e das três refeições do dia.
- Relatórios de presença e de contagem de refeições.
- Envio automático dos relatórios de contagem para a cantina via WhatsApp.
### Fase 2 — Gestão de cantina
 
- Cadastro de cardápio diário.
- Registro de sobra (peso total preparado vs. peso total que sobrou).
- Relatório mensal cruzando cardápio, quantidade de alunos por tipo de refeição e sobras, para análise de movimentação e desperdício.
### Fora de escopo (avaliado e descartado por ora)
 
- **Reconhecimento facial via IA**: avaliado como alternativa à carteirinha QR. Descartado no momento por exigir tratamento de dado biométrico sensível de menores (LGPD + ECA), custo de hardware mais alto e maior complexidade de manutenção, sem resolver um problema que o projeto tem hoje.
- **App mobile como leitor principal / site web como interface de leitura**: descartados como interface primária de leitura em favor da maquina fixa. Um app mobile pode ser reavaliado no futuro como ferramenta administrativa complementar (consulta de relatórios, cadastro emergencial).

---

## 👥 Perfis e Permissões
 
O sistema opera com um sistema de permissões hierárquico. Cada perfil possui responsabilidades bem definidas dentro da plataforma.
 
**Direção**
- Acesso total à plataforma
- Configura horários de corte de presença e horários de envio de relatórios
- Cadastra gestores
- Acumula todas as permissões de Coordenador e Monitor

**Coordenador**
- Cadastra e edita alunos e turmas
- Importa alunos em massa via planilha
- Acessa relatórios completos de presença e refeições
- Acumula todas as permissões de Monitor

**Monitor**
- Acompanha a máquina de leitura no dia a dia
- Resolve problemas pontuais (ex: aluno sem carteirinha)
- Consulta a presença do dia

**Cantina**
- Cadastra o cardápio diário
- Registra as sobras (Fase 2)
- Visualiza relatórios de contagem de refeição
- Não tem acesso a dados de frequência escolar dos alunos

---

## Arquitetura da solução
 
### Hardware
 
- **Computador Fixa** na entrada da escola, com **câmera acoplada** lendo o QR code da carteirinha.
- Único computador atende aos três momentos do dia: lanche da manhã, almoço e lanche da tarde.
- A pagina exibe os botões de escolha "Normal" / "Pouco" apenas para o momento do almoço.
### Fluxo de leitura no Sistema
 
1. Aluno aproxima a carteirinha da câmera.
2. Sistema confirma a leitura (nome e turma exibidos brevemente).
3. Para o momento do almoço, aluno escolhe o tipo de porção (Normal ou Pouco) na pagina.
4. Confirmação visual de sucesso, aluno segue para a fila.
A tela de confirmação se limpa automaticamente em poucos segundos, sem exigir interação, para não gerar gargalo na fila.
 
### Stack 
 
| Camada | Tecnologia sugerida | Motivo |
|---|---|---|
| Aplicação da maquina | Pagina Web, leitura via câmera | Roda direto na máquina fixa da entrada |
| Backend | Python (Django Ninja) | Baixo consumo de recursos, adequado a servidor modesto |
| Banco de dados | PostgreSQL | Volume de dados baixo, não exige infraestrutura pesada |
| Envio de relatório | WAHA (WhatsApp HTTP API, não oficial) | Menor custo/complexidade que a API oficial da Meta — ver ADR-002 |
| Infra | Docker/Docker Compose | Conteinerização utilizada para rodar e gerenciar a aplicação como um todo.

## Tecnologias
 
### Front-end
 
- HTML: estrutura da página exibida na máquina de leitura.
- CSS: estilização visual da página.
- JavaScript: comportamento interativo da página — acesso à câmera para leitura do QR code, exibição da confirmação de leitura e dos botões de escolha de refeição, comunicação com o backend.
### Backend
 
- Python 3.12+: linguagem principal utilizada no backend.
- Django / Django Ninja: framework de desenvolvimento web backend.
- PostgreSQL: banco de dados utilizado para persistência de dados.
### Infra
 
- Docker: conteinerização da aplicação, gerenciada como um todo.
- Docker Compose: gerenciador de containers a partir do Docker.
## Fluxogramas do projeto
 
Os diagramas abaixo foram construídos ao longo do desenho da solução e representam três níveis diferentes de detalhe do mesmo sistema: da visão macro (todos os módulos) até o ciclo de vida de uma única leitura.
 
### 1. Visão geral do fluxo
 
![Visão geral do fluxo do sistema](fluxograma/midia/arquitetura.png)
 
Mapa completo dos módulos do sistema e como eles se relacionam. A partir da **Escola**, derivam três ramos principais:
 
- **Gestores** e **Dispositivos**: cadastro de quem acessa o sistema e quais máquinas fazem leitura.
- **Turmas → Alunos**: cadastro acadêmico, do qual derivam **Presença** (frequência) e **Confirmação de Refeição** (com o **Tipo de Refeição** — Normal/Pouco — associado no momento do almoço).
- **Cantina → Cardápio → Relatório (Sobras)**: módulo da Fase 2, cadastro do cardápio diário e controle de desperdício.
O bloco **WAHA**, conectado à Escola via **Docker**, representa o serviço responsável por enviar o **Relatório (Cantina)** automaticamente pelo WhatsApp — ver [Integração com WhatsApp](#integração-com-whatsapp) e [ADR-002](#adr-002-envio-de-relatórios-via-whatsapp-usando-waha) para o detalhamento dessa decisão.
 
### 2. Base de fluxo (núcleo de presença e refeição)
 
![Base de fluxo do sistema](fluxograma/midia/base_fluxo.jpeg)
 
Recorte do fluxo geral, isolando apenas o núcleo de **Escola → Turmas → Alunos**, sem os módulos de cantina e envio de relatório. Usado como referência rápida para o funcionamento central do MVP: cadastro acadêmico gerando **Presença** e **Confirmação de Refeição** (com o respectivo **Tipo de Refeição**).
 
### 3. Fluxo de vida de uma leitura
 
![Fluxo de vida de uma leitura](fluxograma/midia/fluxo_vida.png)
 
Detalha o ciclo de uma leitura individual, do momento da captura até a geração de relatório:
 
1. **QRCode (captura)**: a câmera lê o QR code da carteirinha.
2. **App (identificação)**: o sistema identifica a qual aluno pertence aquele código.
3. **Validação**: checagem de duplicidade e das regras de negócio (horário de corte, momento do dia).
4. **Registro por turma (relatório)**: a leitura validada é agregada por turma, junto ao **Tipo da Refeição** quando aplicável (almoço).
5. **Relatórios**: consolidação final, consumida pelos gestores e pela cantina.
*Observação: ajuste os caminhos das imagens (`docs/diagramas/...`) acima conforme a pasta real onde os prints estão salvos no seu repositório.*

---

## Roadmap
 
1. **MVP**: cadastro (escola, gestores, turmas, alunos, dispositivos), importação em massa e geração de carteirinhas, aplicação de leitura no computador da entrada, regras de presença e refeição, relatórios básicos, envio via WhatsApp.
2. **Fase 2**: gestão de cantina (cardápio diário, registro de sobras, relatório mensal de movimentação).
3. **Reavaliações futuras**: mecanismo de detecção de momento, possível migração do WhatsApp para API oficial, possível expansão para reconhecimento facial ou múltiplas escolas (caso o contexto do projeto mude).

---

## Casos de Usos - UC

#### UC01: Cadastrar Escola
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Direção
- **Interessados e Interesses:**
  - **Direção:** quer que os dados da escola (horários, contatos) estejam corretos, pois eles alimentam todas as demais configurações do sistema.
  - **Coordenador, Monitor, Cantina:** dependem da escola já estar cadastrada para conseguir operar suas respectivas funcionalidades.
  - **Sistema:** precisa de um registro de escola válido para associar gestores, turmas, alunos e configurações de envio.
- **Pré-condições:** Sistema instalado e em execução; usuário autenticado com perfil Direção.
- **Cenário de Sucesso Principal:**
  1. Direção acessa a área de configurações administrativas do sistema.
  2. Sistema exibe o formulário de cadastro de escola.
  3. Direção informa nome da escola, horário de corte de presença, horários de envio de relatório (lanche manhã, almoço, lanche tarde) e número de WhatsApp de destino da cantina.
  4. Direção confirma o cadastro.
  5. Sistema valida os dados informados.
  6. Sistema cria o registro da escola e exibe confirmação de sucesso.
- **Extensões:**
  - **3a.** Direção deixa um campo obrigatório em branco: sistema exibe mensagem de erro no campo correspondente e mantém os dados já preenchidos nos demais campos.
  - **5a.** Horário informado em formato inválido: sistema recusa o cadastro e sinaliza o campo com erro, sem perder os demais dados preenchidos.
  - **5b.** Número de WhatsApp em formato inválido: sistema recusa o cadastro e orienta o formato esperado.
  - **6a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica e orienta o usuário a tentar novamente.
- **Requisitos Especiais:** Horários devem ser validados no formato HH:MM; número de WhatsApp deve seguir o padrão internacional E.164 (ex: +5511999999999); interface não precisa ser responsiva para mobile, já que o cadastro é feito uma vez, em ambiente administrativo.
- **Frequência:** Baixa — realizado uma única vez na implantação do sistema, com edições pontuais e raras depois (ex: mudança de horário de corte ou de número da cantina).
