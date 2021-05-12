# <div align="center">Network Simulator - TCP/IP 📡</div>

##### <div align="center">Simulador de aplicação cliente/servidor </div>

<img src="https://media.giphy.com/media/3KVhhzvYKS9Cc55eNR/giphy.gif" width="100%" height="100%" />

## Notas do Projeto 📜

1. Este trabalho objetiva promover um entendimento aprofundado do funcionamento e importância das pilhas de protocolos no estudo de redes de computadores.
2. Este sistema simula uma aplicação, serviços oferecidos por cada camada e as interfaces entre elas.
3. A aplicação funciona em dois modos:
- Modo resposta (/ping)
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

## Equipe desenvolvedora 💻

- [Gabriel Tourinho](https://github.com/GTourinho/)
- [Paulo Bomfim](https://github.com/phbomfim/)
- []()
- []()

*Universidade Federal da Bahia - 2021.1 - MATA59 - Redes de Computadores*
