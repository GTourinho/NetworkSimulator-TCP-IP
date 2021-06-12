# <div align="center">Network Simulator - TCP/IP 📡</div>

##### <div align="center">Simulador de aplicação cliente/servidor </div>

https://user-images.githubusercontent.com/41840640/118033893-b7080600-b33f-11eb-8e28-e8693dc60705.mp4

## Notas do Projeto 📜

1. Este trabalho objetiva promover um entendimento aprofundado do funcionamento e importância das pilhas de protocolos no estudo de redes de computadores.
2. Este sistema simula uma aplicação, serviços oferecidos por cada camada e as interfaces entre elas.
3. A aplicação funciona em dois modos:
- Modo resposta
- Modo recuperação

## Prerequisitos ⚙️

1. Python 3 (min) - ```$ install python3``` ou [Python.org](https://www.python.org/downloads/)
2. Git - ```$ brew install git``` ou ```$ install git```


## Instalação 📌


##### 1. Clone o repositório

```$ git clone https://github.com/GTourinho/NetworkSimulator.git  ```

##### 2. Mude para o diretório de trabalho

```$ cd NetworkSimulator ```

##### 3. Execute a aplicação servidor

```$ py server/main.py  ```

##### 4. Execute a aplicação cliente

```$ py client/main.py  ```


## Instruções de uso 📋


##### 1. No modo resposta, o cliente envia 1 caractere que será respondido pela aplicação.
##### 2.  No modo recuperação, o cliente solicita que o servidor envie o último caracter já enviado.
##### 3. Para executar o modo resposta utilize o comando ```ping``` seguido do caractere desejado. Ex:

```$ ping c```

##### 4. Para executar o modo recuperação utilize o comando ```recover```:

```$ recover ```

## E como o programa funciona por trás? 🤔

- O nosso programa é iniciado na camada de aplicação e automaticamente, em todas as outras.
- A aplicação proporciona ao servidor/cliente endereços de IP's e MAC próprios, gerados aleatoriamente.
- O nosso servidor funciona com uma forma de "escuta" durante a execução do programa.

- A primeira etapa então é o estabelecimento de um ID para o cliente, onde consideramos que o mesmo não conhece o IP do servidor. 
- Portanto será enviado parar o IP de broadcast, que em teoria recebe de volta todos os IPS da rede, porém no nosso caso só existe o do servidor.

- O cliente quer enviar a mensagem 'GET_ID' mas como não conhece o IP do servidor, envia um 'get' de broadcast. 
- Recebe a mensagem de volta, para reconhecer o IP do servidor, e coloca na variável do IP destino.

- A camada de rede então é acionada. Nela receberá o IP destino e será criada um datagrama.
- Nesse datagrama colocamos o nosso IP e no final o IP de destino recebido pela aplicação, adicionando como cabeçalho do nosso pacote.

- Este pacote é enviado totalmente na camada de enlace. 
- Nesta camada analisamos o IP de destino enviado e verificamos se é o 255.255.255.255 de broadcast ou se não existe na nossa tabela ARP.
- Poderíamos até ter o caso em que o cliente conhece o IP do servidor mas não o seu MAC, porém nesses dois casos consideramos que o MAC de destino é o MAC de broadcast (FF:FF:FF:FF:FF).

- Cria-se um quadro Ethernet que vai conter os endereços MAC de origem e destino, e finalmente, será enviado para a camada física. 

- Neste momento o servidor recebe as informações e lê o quadro atual.
- Percebendo que o MAC de origem não está na tabela ARP, atualiza sua tabela, colocando como chave o IP e o MAC de origem.

- Neste momento o nosso servidor reconhece o IP e MAC do cliente.

- Verificando o MAC destino, que se trata do MAC de Broadcast, ele irá retornar o pacote para a camada de redes.
- O programa reconhece que será somente necessária o envio de uma mensagem padrão para que o cliente receba seu IP.

- O cliente recebe esta mensagem na sua camada de enlace. 
- Verificando que o MAC de origem não está contido na sua tabela ARP ele a alimenta, deste modo, passa a reconhecer o IP e o MAC do servidor. 
- Verificando que este endereço corresponde ao MAC de destino do quadro, retorna-o para a camada de redes.

- A camada de redes por sua vez reconhece que o seu IP corresponde ao IP de destino do datagrama e então retorna o restante do pacote para a camada de transporte. 

- Finalmente recebemos o IP de destino e no resto do envio da mensagem(do get_id) reconhecemos o IP do servidor como a variável de IP destino. 
- Neste momento temos o protocolo TCP para envio da mensagem(get_id).

- O protocolo utilizado é o de retransmissão seletiva, caracterizado pelo envio de byte por byte.

- Para cada byte é enviado também o ID do byte respectivo a janela. 

- Para simularmos o TCP foi adicionada uma chance de 80% para, cada item do pacote, ser enviado com sucesso(inclusive o próprio ack enviado pelo servidor pode vir corrompido).

- Este cabeçalho então será enviado para o servidor e será lido pela sua camada de transporte (que também irá realizar a soma do byte com ID e verificar se o checksum está correto).
- Em caso de sucesso,o ACK é enviado como ID do byte recebido.


- Desta maneira o cliente sempre checa se recebeu um ack. Tendo recebido, preenche a sua tabela da janela e quando todos forem positivos, a mensagem é enviada com sucesso. 
- Por fim definimos o envio de alguns astericos como forma de caracterizar o fim da mensagem.

- O servidor recebe esta mensagem e finaliza a conexão, enviando a mensagem para a camada de aplicação.

## Equipe desenvolvedora 💻

- [Gabriel Tourinho](https://github.com/GTourinho/)
- [Paulo Bomfim](https://github.com/phbomfim/)

*Universidade Federal da Bahia - 2021.1 - MATA59 - Redes de Computadores*
