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

## Entidades e Módulos
 
### Módulo `school`
 
#### `School`
 
Representa a instituição de ensino e concentra as configurações gerais usadas pelos demais módulos.
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único da escola |
| `name` | Nome da instituição |
| `time_closing_presence` | Horário de corte para presença dentro do prazo (ex: 09:00) |
| `time_send_snack_morning` | Horário de envio automático do relatório do lanche da manhã via WhatsApp |
| `time_send_lunch` | Horário de envio automático do relatório do almoço via WhatsApp |
| `time_send_snack_afternoon` | Horário de envio automático do relatório do lanche da tarde via WhatsApp |
| `number_whats` | Número de WhatsApp da cantina, destino dos relatórios automáticos |
| `created_at` | Data e hora de criação do registro |
 
#### `Manager`
 
Representa os usuários do sistema (gestores) — Direção, Coordenador, Monitor e Cantina.
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único do gestor |
| `school_id` | Escola à qual o gestor pertence |
| `role` | Perfil de acesso (`direction`, `coordinator`, `monitor`, `canteen`), define as permissões dentro do sistema |
| `name` | Nome do gestor |
| `email` | E-mail usado para login, único no sistema |
| `password` | Senha de acesso, armazenada com hash |
| `active` | Indica se o gestor ainda está ativo (exclusão lógica) |
| `created_at` | Data e hora de criação do registro |
 
### Módulo `academic`
 
#### `Classroom`
 
Representa uma turma da escola, usada para agrupar os alunos.
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único da turma |
| `school_id` | Escola à qual a turma pertence |
| `name` | Nome/identificação da turma (ex: "9º Ano A") |
| `active` | Indica se a turma ainda está em funcionamento (exclusão lógica) |
| `created_at` | Data e hora de criação do registro |
 
#### `Student`
 
Representa o aluno, identificado unicamente pelo QR code de sua carteirinha estudantil.
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único do aluno |
| `classroom_id` | Turma à qual o aluno pertence |
| `name` | Nome do aluno |
| `RA` | Registro acadêmico/matrícula do aluno, único no sistema |
| `qr_code` | Código único gerado para a carteirinha estudantil, usado na leitura |
| `active` | Indica se o aluno ainda está matriculado (exclusão lógica) |
| `created_at` | Data e hora de criação do registro |
 
### Módulo `presence`
 
Núcleo do sistema — registra o evento bruto de leitura e as duas interpretações derivadas dele: presença e contagem de refeição.
 
#### `Readings`
 
Log bruto de cada leitura realizada na máquina da entrada. Nunca é apagado, funciona como auditoria de tudo que já aconteceu.
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único da leitura |
| `student_id` | Aluno identificado na leitura |
| `moment` | Momento do dia em que a leitura ocorreu (`snack_morning`, `lunch`, `snack_afternoon`) |
| `date_time` | Data e hora exatas da leitura |
 
#### `Frequency`
 
Registro de presença — um único registro por aluno, por dia, gerado a partir da primeira leitura.
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único do registro de presença |
| `student_id` | Aluno referente à presença |
| `date` | Data da presença |
| `on_time` | Indica se a leitura ocorreu dentro do horário de corte da escola (`time_closing_presence`) |
| `reading_id` | Leitura que originou este registro de presença |
 
#### `Register_Snack`
 
Registro de refeição — um registro por aluno, por dia, por momento (lanche manhã, almoço, lanche tarde são contados separadamente).
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único do registro de refeição |
| `student_id` | Aluno referente à refeição |
| `date` | Data da refeição |
| `moment` | Momento a que se refere este registro (`snack_morning`, `lunch`, `snack_afternoon`) |
| `type_snack` | Tipo de porção escolhida (`normal` ou `little`) — preenchido apenas quando `moment` é `lunch` |
| `reading_id` | Leitura que originou este registro de refeição |
 
### Módulo `canteen`
 
#### `Daily_Menu`
 
Cardápio cadastrado pela cantina para um dia específico.
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único do cardápio do dia |
| `school_id` | Escola à qual o cardápio pertence |
| `date` | Data a que se refere o cardápio |
| `main_course` | Descrição do prato principal servido |
| `manager_id` | Gestor da cantina que cadastrou o cardápio |
| `created_at` | Data e hora de criação do registro |
 
### Módulo `notifications`
 
#### `Logs_Whats`
 
Log de cada tentativa de envio automático de relatório via WhatsApp — permite auditar sucesso ou falha de envio.
 
| Campo | Descrição |
|---|---|
| `id` | Identificador único do log de envio |
| `school_id` | Escola referente ao envio |
| `date` | Data referente ao relatório enviado |
| `status` | Resultado do envio (`success` ou `failed`) |
| `message` | Texto exato da mensagem enviada (ou que tentou ser enviada) |
| `sent_on` | Data e hora em que o envio foi realizado |

---

## Roadmap
 
1. **MVP**: cadastro (escola, gestores, turmas, alunos, dispositivos), importação em massa e geração de carteirinhas, aplicação de leitura no computador da entrada, regras de presença e refeição, relatórios básicos, envio via WhatsApp.
2. **Fase 2**: gestão de cantina (cardápio diário, registro de sobras, relatório mensal de movimentação).
3. **Reavaliações futuras**: mecanismo de detecção de momento, possível migração do WhatsApp para API oficial, possível expansão para reconhecimento facial ou múltiplas escolas (caso o contexto do projeto mude).

---

## Casos de Usos - UC

### Escola
 
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
#### UC02: Retornar Escola
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Subfunção
- **Ator Primário:** Gestor autenticado (qualquer perfil)
- **Interessados e Interesses:**
  - **Gestor:** quer consultar os dados e configurações da escola (horários de corte, horários de envio, número de WhatsApp da cantina) para se orientar no uso do sistema.
  - **Sistema:** precisa desses dados tanto para telas administrativas quanto para aplicar regras de negócio (ex: usar `time_closing_presence` ao processar uma leitura).
- **Pré-condições:** Escola já cadastrada (UC01); usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Gestor acessa a área de configurações da escola.
  2. Sistema busca o registro da escola cadastrada.
  3. Sistema exibe os dados da escola (nome, horários de corte e de envio, número de WhatsApp).
- **Extensões:**
  - **2a.** Nenhuma escola cadastrada ainda: sistema informa que a configuração inicial não foi realizada e orienta a Direção a executar o UC01.
  - **2b.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica e orienta tentar novamente.
- **Requisitos Especiais:** Consulta somente leitura; não expõe nenhum dado de outro gestor ou aluno, apenas os dados da própria escola.
- **Frequência:** Alta — usada tanto internamente por outras telas e fluxos (ex: exibir horário de corte) quanto em consultas administrativas pontuais.
#### UC03: Atualizar Escola
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Direção
- **Interessados e Interesses:**
  - **Direção:** quer poder corrigir ou ajustar configurações da escola (ex: mudar o horário de corte, trocar o número de WhatsApp da cantina) sem precisar recriar o cadastro.
  - **Coordenador, Monitor, Cantina:** são afetados pelas mudanças (ex: novo horário de corte muda o comportamento da leitura no dia seguinte).
- **Pré-condições:** Escola já cadastrada; usuário autenticado com perfil Direção.
- **Cenário de Sucesso Principal:**
  1. Direção acessa a área de configurações administrativas.
  2. Sistema exibe o formulário preenchido com os dados atuais da escola.
  3. Direção altera um ou mais campos (nome, horários, número de WhatsApp).
  4. Direção confirma a atualização.
  5. Sistema valida os dados informados.
  6. Sistema atualiza o registro e exibe confirmação de sucesso.
- **Extensões:**
  - **5a.** Campo obrigatório deixado em branco: sistema exibe erro no campo, mantém os demais preenchidos.
  - **5b.** Horário em formato inválido: sistema recusa e sinaliza o campo.
  - **5c.** Número de WhatsApp em formato inválido: sistema recusa e orienta o formato esperado.
  - **6a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica e orienta tentar novamente.
- **Requisitos Especiais:** Mesmas validações de formato do UC01 (horário HH:MM, WhatsApp em E.164); alteração de horário de corte só afeta leituras futuras, nunca reprocessa registros de `Frequency` já existentes.
- **Frequência:** Baixa — ajustes pontuais e raros ao longo do ano letivo.
#### UC04: Deletar Escola
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Direção
- **Interessados e Interesses:**
  - **Direção:** quer poder remover o cadastro da escola em caso de descontinuação total do uso do sistema.
  - **Sistema:** precisa garantir que a exclusão não deixe dados órfãos (gestores, turmas, alunos, cardápios e logs vinculados a uma escola inexistente).
- **Pré-condições:** Escola cadastrada; usuário autenticado com perfil Direção.
- **Cenário de Sucesso Principal:**
  1. Direção acessa a área de configurações administrativas.
  2. Direção seleciona a opção de excluir a escola.
  3. Sistema solicita confirmação explícita, alertando que a ação é irreversível.
  4. Direção confirma.
  5. Sistema verifica se existem registros dependentes (gestores, turmas, cardápios, logs de envio).
  6. Sistema exclui o registro da escola.
  7. Sistema exibe confirmação da exclusão.
- **Extensões:**
  - **5a.** Existem registros dependentes: sistema recusa a exclusão e informa que é necessário remover ou desativar os registros dependentes antes de excluir a escola.
  - **6a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica e orienta tentar novamente.
- **Requisitos Especiais:** Como as chaves estrangeiras que apontam para `School` usam `on_delete=PROTECT`, a exclusão só é tecnicamente possível se não houver nenhum gestor, turma, cardápio ou log vinculado — na prática, um caso raríssimo para uma escola em uso real. **Recomenda-se avaliar a adição de um campo `active` em `School`**, seguindo o mesmo padrão de exclusão lógica já usado em `Manager`, `Classroom` e `Student`, em vez de depender de exclusão física.
- **Frequência:** Muito rara — só se aplicaria em cenário de descontinuação total do sistema.
### Turma
 
#### UC05: Cadastrar Turma
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Coordenador
- **Interessados e Interesses:**
  - **Coordenador:** quer organizar os alunos em turmas para facilitar o cadastro e a consulta de presença.
  - **Monitor:** depende das turmas existirem para localizar alunos durante o uso diário do sistema.
  - **Sistema:** precisa de uma turma válida para poder vincular alunos a ela.
- **Pré-condições:** Escola já cadastrada; usuário autenticado com perfil Coordenador ou Direção.
- **Cenário de Sucesso Principal:**
  1. Coordenador acessa a área de turmas.
  2. Sistema exibe a lista de turmas já cadastradas e a opção "Adicionar turma".
  3. Coordenador seleciona "Adicionar turma".
  4. Sistema exibe formulário (nome, turno).
  5. Coordenador preenche os dados e confirma.
  6. Sistema valida os dados informados.
  7. Sistema cria o registro da turma, vinculado à escola.
  8. Sistema exibe confirmação de sucesso.
- **Extensões:**
  - **6a.** Nome em branco: sistema exibe erro no campo, mantém os demais preenchidos.
  - **6b.** Já existe turma com esse nome na mesma escola: sistema recusa e informa duplicidade.
  - **7a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Nome da turma deve ser único dentro da mesma escola (`UniqueConstraint(escola, nome)`).
- **Frequência:** Média — concentrada no início do ano letivo, com cadastros esporádicos ao longo do ano.
#### UC06: Listar Turmas
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Subfunção
- **Ator Primário:** Coordenador, Monitor ou Direção
- **Interessados e Interesses:**
  - **Coordenador, Monitor, Direção:** precisam ver todas as turmas existentes para navegar até os alunos, gerar relatórios, ou escolher uma turma antes de cadastrar um novo aluno.
  - **Sistema:** usa essa listagem como base para diversas outras telas.
- **Pré-condições:** Usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Gestor acessa a área de turmas.
  2. Sistema busca todas as turmas cadastradas na escola, podendo filtrar por turno ou nome.
  3. Sistema exibe a lista de turmas (nome, turno, quantidade de alunos vinculados, status ativo).
- **Extensões:**
  - **2a.** Nenhuma turma cadastrada: sistema exibe lista vazia com opção de cadastrar a primeira (UC05).
  - **2b.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Por padrão, retorna apenas turmas ativas (`active=true`), a menos que explicitamente solicitado incluir as inativas; suporta paginação caso o número de turmas cresça.
- **Frequência:** Alta — consulta recorrente ao longo do uso diário do sistema.
#### UC07: Retornar Turma
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Subfunção
- **Ator Primário:** Coordenador, Monitor ou Direção
- **Interessados e Interesses:**
  - **Coordenador, Monitor, Direção:** querem ver os detalhes de uma turma específica, geralmente antes de editá-la ou para consultar os alunos vinculados a ela.
- **Pré-condições:** Turma já cadastrada; usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Gestor seleciona uma turma específica a partir da listagem (UC06).
  2. Sistema busca o registro daquela turma pelo identificador.
  3. Sistema exibe os dados detalhados da turma (nome, turno, status, quantidade de alunos ativos vinculados).
- **Extensões:**
  - **2a.** Turma não encontrada (identificador inválido ou removida): sistema exibe erro "turma não encontrada".
  - **2b.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Retorna também a contagem de alunos ativos vinculados, para dar contexto rápido ao gestor sem precisar de uma segunda consulta.
- **Frequência:** Alta — consultada sempre que o gestor acessa uma turma específica.
#### UC08: Atualizar Turma
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Coordenador
- **Interessados e Interesses:**
  - **Coordenador:** quer corrigir dados de uma turma (nome, turno) ou encerrar seu funcionamento (desativação) ao final do ano letivo.
- **Pré-condições:** Turma já cadastrada; usuário autenticado com perfil Coordenador ou Direção.
- **Cenário de Sucesso Principal:**
  1. Coordenador acessa a turma desejada (UC07).
  2. Sistema exibe o formulário preenchido com os dados atuais.
  3. Coordenador altera nome, turno ou status (ativo/inativo).
  4. Coordenador confirma.
  5. Sistema valida os dados.
  6. Sistema atualiza o registro e exibe confirmação.
- **Extensões:**
  - **5a.** Nome duplicado dentro da mesma escola: sistema recusa.
  - **6a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Desativar uma turma (`active=false`) não apaga os alunos vinculados a ela — apenas remove a turma das listagens padrão (ver UC06).
- **Frequência:** Baixa a média — ajustes pontuais (mudança de turno, encerramento de turma ao fim do ano).
### Gestor
 
#### UC09: Cadastrar Gestor
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Direção
- **Interessados e Interesses:**
  - **Direção:** quer conceder acesso ao sistema para a equipe (coordenadores, monitores, cantina).
  - **Sistema:** precisa de credenciais válidas e de um perfil definido para aplicar as regras de permissão.
- **Pré-condições:** Escola já cadastrada; usuário autenticado com perfil Direção.
- **Cenário de Sucesso Principal:**
  1. Direção acessa a área de gestores.
  2. Sistema exibe a lista de gestores cadastrados e a opção "Adicionar gestor".
  3. Direção seleciona "Adicionar gestor".
  4. Sistema exibe formulário (nome, e-mail, senha, perfil).
  5. Direção preenche os dados e confirma.
  6. Sistema valida os dados informados.
  7. Sistema cria o registro do gestor, armazenando a senha com hash.
  8. Sistema exibe confirmação de sucesso.
- **Extensões:**
  - **6a.** E-mail já cadastrado: sistema recusa por duplicidade.
  - **6b.** Campo obrigatório em branco: sistema exibe erro no campo.
  - **6c.** Senha não atende aos requisitos mínimos de segurança: sistema recusa e orienta os requisitos.
  - **7a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Senha nunca é armazenada nem retornada em texto puro; e-mail deve ser único no sistema; apenas o perfil Direção pode cadastrar novos gestores.
- **Frequência:** Baixa a média — concentrada no início de uso do sistema, com cadastros esporádicos por troca de equipe.
#### UC10: Retornar Gestor(es)
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Subfunção
- **Ator Primário:** Direção
- **Interessados e Interesses:**
  - **Direção:** quer consultar quem tem acesso ao sistema e com qual perfil.
- **Pré-condições:** Usuário autenticado com perfil Direção.
- **Cenário de Sucesso Principal:**
  1. Direção acessa a área de gestores.
  2. Sistema busca os gestores cadastrados na escola.
  3. Sistema exibe a lista (nome, e-mail, perfil, status ativo), sem expor a senha.
- **Extensões:**
  - **2a.** Nenhum gestor além de quem está logado: sistema exibe a lista contendo apenas o próprio usuário.
  - **2b.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** O campo `password` nunca é incluído na resposta; apenas o perfil Direção acessa a listagem completa de gestores.
- **Frequência:** Baixa — consulta administrativa, fora do fluxo operacional diário.
#### UC11: Atualizar Gestor
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Direção
- **Interessados e Interesses:**
  - **Direção:** quer corrigir dados de um gestor, mudar seu perfil de acesso, ou revogar seu acesso (desativação) quando ele deixa a equipe.
- **Pré-condições:** Gestor já cadastrado; usuário autenticado com perfil Direção.
- **Cenário de Sucesso Principal:**
  1. Direção acessa o gestor desejado.
  2. Sistema exibe o formulário preenchido com os dados atuais (exceto senha).
  3. Direção altera nome, perfil ou status (ativo/inativo).
  4. Direção confirma.
  5. Sistema valida os dados.
  6. Sistema atualiza o registro e exibe confirmação.
- **Extensões:**
  - **5a.** E-mail alterado para um já existente: sistema recusa por duplicidade.
  - **6a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Desativar um gestor (`active=false`) revoga o acesso ao sistema sem apagar seu histórico de ações (cardápios cadastrados, logs, etc.); alteração de senha segue fluxo próprio, fora do escopo deste UC.
- **Frequência:** Baixa — ajustes pontuais (mudança de perfil, desligamento de um gestor).
### Cardápio
 
#### UC12: Cadastrar Cardápio
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Cantina
- **Interessados e Interesses:**
  - **Cantina:** quer registrar o que será servido no dia.
  - **Direção, Coordenador:** acompanham o planejamento da alimentação.
  - **Sistema:** usa o cardápio cadastrado para compor o relatório mensal de movimentação (Fase 2).
- **Pré-condições:** Escola já cadastrada; usuário autenticado com perfil Cantina (ou superior).
- **Cenário de Sucesso Principal:**
  1. Cantina acessa a área de cardápio.
  2. Sistema exibe a opção "Cadastrar cardápio do dia".
  3. Cantina informa a data e o prato principal.
  4. Cantina confirma.
  5. Sistema valida os dados.
  6. Sistema cria o registro do cardápio, vinculado à escola e ao gestor que o cadastrou.
  7. Sistema exibe confirmação de sucesso.
- **Extensões:**
  - **5a.** Já existe cardápio cadastrado para essa data: sistema recusa e sugere editar o cardápio existente (ver UC14).
  - **5b.** Campo obrigatório em branco: sistema exibe erro no campo.
  - **6a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Apenas um cardápio por escola por dia (`UniqueConstraint(escola, data)`).
- **Frequência:** Alta — cadastro diário, feito rotineiramente pela cantina.
#### UC13: Retornar Cardápio
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Subfunção
- **Ator Primário:** Gestor autenticado (qualquer perfil)
- **Interessados e Interesses:**
  - **Cantina:** consulta o cardápio já cadastrado antes de atualizar.
  - **Direção, Coordenador:** acompanham o que está sendo servido.
- **Pré-condições:** Usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Gestor acessa a área de cardápio.
  2. Sistema busca o cardápio da data informada (ou de um intervalo de datas).
  3. Sistema exibe os dados (data, prato principal, quem cadastrou).
- **Extensões:**
  - **2a.** Nenhum cardápio cadastrado para a data consultada: sistema informa que ainda não foi cadastrado.
  - **2b.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Suporta consulta por data única ou por intervalo de datas, para uso futuro no relatório mensal da Fase 2.
- **Frequência:** Alta — consultada diariamente pela cantina e ocasionalmente pela gestão.
#### UC14: Atualizar Cardápio
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Cantina
- **Interessados e Interesses:**
  - **Cantina:** quer corrigir um erro de digitação ou uma mudança de última hora no prato do dia.
- **Pré-condições:** Cardápio do dia já cadastrado; usuário autenticado com perfil Cantina (ou superior).
- **Cenário de Sucesso Principal:**
  1. Cantina acessa o cardápio do dia desejado.
  2. Sistema exibe o formulário preenchido com os dados atuais.
  3. Cantina altera o prato principal.
  4. Cantina confirma.
  5. Sistema valida os dados.
  6. Sistema atualiza o registro e exibe confirmação.
- **Extensões:**
  - **5a.** Campo em branco: sistema exibe erro no campo.
  - **6a.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** A data do cardápio não pode ser alterada nesta operação — para mudar a data, cadastra-se um novo cardápio (UC12); alterações devem ser feitas preferencialmente antes do horário de envio automático do relatório via WhatsApp, para refletir corretamente na mensagem enviada.
- **Frequência:** Baixa — usada apenas para corrigir erro de digitação ou mudança de última hora.
### Presença
 
>  OBS: `Reading`, `Frequency` e `Register_Snack` não tem um "cadastrar" independente para cada uma — elas nascem de uma única ação física - o aluno passar a carteirinha - O UC15 descreve esse fluxo completo; os UCs seguintes cobrem a listagem de cada uma das três tabelas gravadas por ele.
 
#### UC15: Registrar Leitura (Presença e Refeição)
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Objetivo do usuário
- **Ator Primário:** Aluno (via máquina de leitura fixa na entrada da escola)
- **Interessados e Interesses:**
  - **Aluno:** quer que sua presença e, quando aplicável, sua refeição sejam registradas rapidamente, sem atrapalhar a fila.
  - **Monitor:** acompanha a máquina no dia a dia e intervém em caso de falha de leitura.
  - **Cantina:** depende desse registro para saber quantos alunos vão comer em cada momento e de qual tipo de porção.
  - **Sistema:** precisa aplicar corretamente as regras de dedução (presença só na primeira leitura do dia, contagem separada por momento, tipo de refeição só no almoço).
- **Pré-condições:** Aluno já cadastrado e vinculado a uma turma; carteirinha física em mãos; máquina de leitura operante.
- **Cenário de Sucesso Principal:**
  1. Aluno aproxima a carteirinha da câmera da máquina.
  2. Sistema lê o QR code e identifica o aluno correspondente.
  3. Sistema registra a leitura bruta (`Reading`), com o momento do dia identificado.
  4. Sistema verifica se é a primeira leitura do aluno no dia: em caso positivo, cria o registro de `Frequency`, calculando se está dentro do horário de corte (`on_time`).
  5. Sistema verifica se já existe registro de refeição para aquele aluno, data e momento: em caso negativo, cria o registro de `Register_Snack`.
  6. Se o momento identificado for o almoço, sistema exibe as opções "Normal" / "Pouco" na página, para o aluno escolher o tipo de porção.
  7. Sistema exibe confirmação visual de sucesso; a tela se limpa automaticamente para a leitura do próximo aluno.
- **Extensões:**
  - **2a.** QR code não reconhecido (carteirinha danificada ou mal posicionada): sistema exibe erro de leitura e orienta nova tentativa ou emissão de carteirinha provisória.
  - **2b.** QR code não corresponde a nenhum aluno cadastrado e ativo: sistema recusa e sinaliza carteirinha inválida.
  - **4a.** Não é a primeira leitura do dia: sistema não cria novo registro de `Frequency`, mas a leitura bruta é registrada normalmente (auditoria).
  - **5a.** Já existe registro de refeição para aquele momento: sistema não cria novo registro (evita duplicidade), mas a leitura bruta é registrada normalmente.
  - **6a.** Aluno segue para a fila sem selecionar o tipo de porção: `type_snack` permanece em branco; nos relatórios, é assumido como "normal" por padrão.
  - **7a.** Falha de conexão com o banco de dados: sistema orienta tentar novamente.
- **Requisitos Especiais:** A leitura deve ocorrer em poucos segundos por aluno, para não gerar fila; a tela deve resetar automaticamente, sem exigir interação extra do aluno ou de um monitor.
- **Frequência:** Altíssima — é a operação mais executada do sistema, repetida centenas de vezes por dia (3 momentos × todos os alunos presentes).
#### UC16: Listar Leituras
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Subfunção
- **Ator Primário:** Monitor, Coordenador ou Direção
- **Interessados e Interesses:**
  - **Monitor, Coordenador, Direção:** querem auditar o histórico bruto de leituras (ex: investigar uma reclamação, conferir se uma leitura realmente aconteceu).
- **Pré-condições:** Usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Gestor acessa a área de auditoria de leituras.
  2. Sistema busca as leituras registradas, filtrando obrigatoriamente por aluno e/ou por data.
  3. Sistema exibe a lista de leituras (aluno, momento, data e hora).
- **Extensões:**
  - **2a.** Nenhuma leitura encontrada para o filtro aplicado: sistema exibe lista vazia.
  - **2b.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** É o único registro que nunca é "filtrado por sucesso" — toda leitura aparece aqui, inclusive as que não geraram presença ou refeição por já existir um registro no mesmo dia/momento; por gerar grande volume de dados, a consulta exige paginação e pelo menos um filtro obrigatório (aluno ou intervalo de data), para evitar consultas muito amplas.
- **Frequência:** Baixa — usada apenas para auditoria pontual, fora do fluxo operacional diário.
#### UC17: Listar Frequência
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Subfunção
- **Ator Primário:** Coordenador, Monitor ou Direção
- **Interessados e Interesses:**
  - **Coordenador, Direção:** acompanham a frequência escolar dos alunos ao longo do tempo.
  - **Monitor:** consulta a presença do dia corrente, no uso operacional diário.
- **Pré-condições:** Usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Gestor acessa a área de presença.
  2. Sistema busca os registros de `Frequency`, podendo filtrar por turma, aluno, data ou status (dentro/fora do prazo).
  3. Sistema exibe a lista (aluno, data, se está dentro do prazo).
- **Extensões:**
  - **2a.** Nenhum registro para o filtro aplicado: sistema exibe lista vazia.
  - **2b.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Filtro por turma cruza com o cadastro acadêmico (`Student` → `Classroom`); a consulta do dia atual deve ser rápida o suficiente para uso operacional (ex: Monitor conferindo quem já chegou em tempo real).
- **Frequência:** Alta — consultada diariamente pela gestão e pela monitoria.
#### UC18: Listar Registro de Refeição
 
- **Escopo:** Sistema de Gestão de Presença e Merenda Escolar
- **Nível:** Subfunção
- **Ator Primário:** Cantina, Coordenador ou Direção
- **Interessados e Interesses:**
  - **Cantina:** precisa da contagem por momento e por tipo de porção para planejar a quantidade de comida a ser preparada.
  - **Direção, Coordenador:** acompanham o consumo de refeições ao longo do tempo.
- **Pré-condições:** Usuário autenticado.
- **Cenário de Sucesso Principal:**
  1. Gestor acessa a área de refeições.
  2. Sistema busca os registros de `Register_Snack`, podendo filtrar por data, momento (lanche manhã, almoço, lanche tarde) e tipo de porção.
  3. Sistema exibe a lista, com contagem agrupada por tipo quando o momento filtrado for o almoço.
- **Extensões:**
  - **2a.** Nenhum registro para o filtro aplicado: sistema exibe lista vazia.
  - **2b.** Falha de conexão com o banco de dados: sistema exibe mensagem de erro genérica.
- **Requisitos Especiais:** Essa é a consulta que alimenta a mensagem automática enviada via WhatsApp (ver Integração com WhatsApp); deve suportar agregação (contagem total e por tipo), não apenas listagem linha a linha.
- **Frequência:** Alta — consultada diariamente pela cantina, inclusive de forma automática pelo próprio sistema no envio via WhatsApp.

---

## Padrão de Commits

Este projeto segue o padrão **[Conventional Commits](https://www.conventionalcommits.org/)**, que ajuda a manter um histórico de commits organizado, legível e que facilita a geração automática de changelogs.

### Estrutura básica

```
<tipo>(<escopo opcional>): <descrição curta>
```

Exemplo:
```
feat(auth): adiciona login via Google
```

### Tipos de commit

| Tipo | Quando usar |
|------|-------------|
| **feat** | Adição de uma nova funcionalidade para o usuário |
| **fix** | Correção de um bug |
| **docs** | Alterações apenas na documentação (README, comentários, wiki) |
| **style** | Mudanças que não afetam a lógica do código (formatação, espaços, ponto e vírgula) |
| **refactor** | Alteração no código que não corrige bug nem adiciona funcionalidade, apenas melhora a estrutura |
| **perf** | Mudança de código focada em melhorar performance |
| **test** | Adição ou correção de testes automatizados |
| **build** | Alterações que afetam o sistema de build ou dependências externas (npm, webpack, etc.) |
| **ci** | Mudanças em arquivos e scripts de integração contínua (GitHub Actions, CI/CD) |
| **chore** | Tarefas de manutenção que não alteram código de produção (configs, scripts internos) |
| **revert** | Reverte um commit anterior |

### Boas práticas ao commitar

- **Use o imperativo**: escreva "adiciona", "corrige", "remove" em vez de "adicionado", "corrigido".
- **Um commit, uma responsabilidade**: evite misturar várias alterações não relacionadas no mesmo commit.
- **Commits pequenos e frequentes**: facilita revisão e reduz conflitos de merge.
- **Nunca commit direto na `main`/`master`**: sempre trabalhe em branches específicas.

### Padrão de branches

| Prefixo | Uso |
|---------|-----|
| `feature/` | Novas funcionalidades (ex: `feature/login-google`) |
| `fix/` | Correções de bugs (ex: `fix/erro-cadastro`) |
| `hotfix/` | Correções urgentes em produção |
| `chore/` | Tarefas de manutenção/configuração |
| `docs/` | Alterações apenas de documentação |

---

## Como contribuir

Siga os passos abaixo para configurar o projeto localmente e começar a contribuir.

### Pré-requisitos
 
- [Python 3.12+](https://www.python.org/) instalado
- [uv](https://docs.astral.sh/uv/getting-started/installation/) instalado
```bash
# instalar o uv (caso ainda não tenha)
curl -LsSf https://astral.sh/uv/install.sh | sh
```
 
### 1. Clone o repositório
 
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```
 
### 2. Acesse a pasta do projeto
 
```bash
cd nome-do-repositorio
```
 
### 3. Instale as dependências com o uv
 
O `uv` cria e gerencia automaticamente o ambiente virtual (`.venv`) com base no `pyproject.toml` / `uv.lock`.
 
```bash
uv sync
```
 
### 4. Ative o ambiente virtual (opcional)
 
O `uv run` já executa os comandos dentro do ambiente automaticamente, mas se preferir ativar manualmente:
 
```bash
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
```
 
### 5. Configure as variáveis de ambiente
 
```bash
cp .env.example .env
```
 
Edite o arquivo `.env` com as configurações necessárias (banco de dados, chaves, etc.).
 
### 6. Aplique as migrações do Django
 
```bash
uv run manage.py migrate
```
 
### 7. Suba o servidor de desenvolvimento
 
```bash
uv run manage.py runserver
```
 
A API estará disponível em `http://localhost:8000`, com a documentação automática do Django Ninja em `http://localhost:8000/api/docs`.
 
### 8. Crie uma branch a partir da `main`
 
```bash
git checkout main
git pull origin main
git checkout -b feature/nome-da-sua-feature
```
 
### 9. Faça suas alterações e commit seguindo o padrão
 
```bash
git add .
git commit -m "feat: adiciona funcionalidade X"
```
 
### 10. Envie sua branch para o repositório remoto
 
```bash
git push origin feature/nome-da-sua-feature
```
 
### 11. Abra um Pull Request
 
- Acesse o repositório no GitHub/GitLab.
- Abra um Pull Request da sua branch para a `main`.
- Descreva claramente o que foi feito e, se possível, referencie a issue relacionada.
- Aguarde a revisão de outro(a) desenvolvedor(a) antes do merge.
### Dicas úteis com o uv
 
| Comando | Descrição |
|---------|-----------|
| `uv add <pacote>` | Adiciona uma nova dependência ao projeto |
| `uv add --dev <pacote>` | Adiciona uma dependência apenas de desenvolvimento |
| `uv remove <pacote>` | Remove uma dependência |
| `uv sync` | Sincroniza o ambiente com o `uv.lock` |
| `uv lock` | Atualiza o arquivo de lock de dependências |
| `uv run <comando>` | Executa um comando dentro do ambiente virtual do projeto |
 
### Checklist antes de abrir o PR

- [ ] O código segue os padrões de estilo do projeto
- [ ] Os testes passam localmente
- [ ] A documentação foi atualizada (se necessário)
- [ ] Os commits seguem o padrão Conventional Commits
