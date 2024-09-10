# Python Web - Gerenciamento de Tarefas

## Instalação
1. Clone o [repositório](https://github.com/OJooohn/2024-trabalho-a2-topicos-especiais-software).
2. Abra o PyCharm e adicione o ambiente virtual (venv).
3. Abra o arquivo "_main.py_".
4. Clique em "Install requirements" no canto superior direito.
![Install requirements.png](img%2FInstall%20requirements.png)
5. Execute o arquivo "_main.py_".
6. Abra o link que aparece no console "_http://127.0.0.1:5000_".
7. Caso apareça a opção para criar o ambiente virtual usando o "_requirements.txt_", clique em "Create a virtual environment using requirements.txt" no canto superior direito.
![Create a virtual environment.png](img%2FCreate%20a%20virtual%20environment.png)

## Uso do Sistema
No canto superior direito, há um botão para alterar o tema da página (claro/escuro).

- Usuário Padrão
  - Login e Senha: admin

### Tela Inicial
A primeira tela que aparece no navegador, onde é feito o login dos usuários. 
Para ir à tela de registro, clique no link "_Faça o cadastro_".

### Registro
O usuário vai colocar suas informações, tais como nome, e-mail e senha, para se cadastrar no website. 
É necessário colocar um e-mail válido e confirmar a senha digitada. Após o registro, 
o usuário é redirecionado à Tela Inicial. Se quiser cancelar o registro, basta clicar no link "_Faça Login_".

### Dashboard
A tela terá algumas informações, como:
- Usuário logado (canto superior direito do card).
- Botão para sair da conta e voltar à Tela Inicial.
- Uma série de informações sobre as tarefas do usuário, mostrando nome, data, descrição e status.
- Um filtro de status para as tarefas, facilitando o gerenciamento das mesmas.
  - Para filtrar as tarefas pelo status, selecione o status desejado e clique no botão "_Filtrar_".
- Ao lado de cada tarefa, haverá duas ferramentas, exclusivamente para editar e excluir a tarefa.
- Botão para criar uma nova tarefa.

#### Tabela Padrão
Nome |    Data     |    Descrição     |    Status     | Ações
:---------:|:-----------:|:----------------:|:-------------:|:-------:
nome_tarefa | data_tarefa | descrição_tarefa | status_tarefa | ferramentas

#### Admin
Ao entrar como admin, você verá todas as tarefas de todos os usuários, com uma informação adicional 
de qual usuário a tarefa pertence. Não é possível editar ou excluir tarefas de outros usuários como admin, 
ficando a critério de cada usuário decidir o que fazer com suas próprias tarefas.

Usuário |    Nome     |    Data     | Descrição | Status
:---------: |:-----------:|:-----------:| :-------:|:---------:
nome_usuário | nome_tarefa | data_tarefa | descrição_tarefa | status_tarefa

### Criar Nova Tarefa
Após clicar no botão "_CRIAR NOVA TAREFA_" no Dashboard, você será redirecionado para outra página, 
onde deverá inserir o nome, data, descrição e usuários para a tarefa. 
Por padrão, a tarefa vem com a opção de status selecionada em "_Pendente_". 
Após preencher todos os campos, a tarefa será criada para todos os usuários selecionados. 
Se não houver usuários selecionados, a tarefa será criada somente para o usuário logado, exceto admin, 
que não poderá ter tarefas, apenas gerenciá-las.

### Editar Tarefa
Após clicar no botão "_EDITAR_" no Dashboard, você será redirecionado para outra página, 
onde todas as informações correspondentes à tarefa selecionada serão exibidas. 
Você poderá modificar qualquer campo, como nome, data, descrição e status. Após clicar no botão "_EDITAR TAREFA_", você será redirecionado para o Dashboard, onde poderá verificar se as alterações foram feitas corretamente.

### Excluir Tarefa
Após clicar no botão "_EDITAR_" no Dashboard, você será redirecionado para outra página. 
O website pedirá uma verificação do usuário para confirmar a exclusão da tarefa. 
Ao confirmar a exclusão, a página do Dashboard será atualizada para refletir a exclusão da tarefa.
