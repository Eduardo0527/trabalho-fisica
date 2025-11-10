# Simulador 3D: Partícula em Campo Magnético

Este projeto é um simulador 3D interativo, construído com **VPython**, que modela o movimento de uma partícula carregada em um campo magnético uniforme. A simulação calcula a trajetória da partícula em tempo real com base na **Força de Lorentz** e permite que o usuário ajuste todos os parâmetros iniciais.

$$\vec{F} = q(\vec{v} \times \vec{B})$$

A simulação utiliza o **método do Ponto Médio** para a integração numérica, o que garante uma trajetória estável que conserva a energia, evitando o problema de "espiral da morte" (aumento do raio) comum em simulações que usam o método de Euler simples.



## 🚀 Funcionalidades

* **Visualização 3D:** Renderiza a trajetória da partícula em um espaço 3D com eixos X (vermelho), Y (verde) e Z (azul).
* **Controles Interativos:** Permite ao usuário definir em tempo real:
    * Carga da partícula ($q$)
    * Massa da partícula ($m$)
    * Componentes da velocidade inicial ($\vec{v} = (v_x, v_y, v_z)$)
    * Componentes do campo magnético uniforme ($\vec{B} = (B_x, B_y, B_z)$)
* **Cálculo de Raio:** Calcula e exibe automaticamente o raio da componente circular do movimento, usando a fórmula $R = \frac{m \cdot v_{\perp}}{|q| \cdot B}$.
* **Reset da Simulação:** Um botão "Resetar" aplica instantaneamente todos os novos parâmetros e reinicia o movimento da partícula.

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **VPython (Visual Python):** Biblioteca para criação rápida de simulações e visualizações 3D em um navegador web.

## ⚙️ Como Executar (Usando o VS Code)

Para executar esta simulação no seu computador usando o Visual Studio Code, siga estes passos.

### 1. Pré-requisitos

* **Python 3:** Certifique-se de que o Python está instalado. Você pode baixá-lo em [python.org](https://www.python.org/).
* **VS Code:** Tenha o [Visual Studio Code](https://code.visualstudio.com/) instalado.
* **Extensão Python para VS Code:** Instale a extensão oficial do Python da Microsoft. Você pode encontrá-la na aba "Extensions" (Ctrl+Shift+X) procurando por `ms-python.python`.

### 2. Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```
    (Se você não usa o Git, apenas baixe os arquivos e abra a pasta no VS Code).

2.  **Crie um Ambiente Virtual (Recomendado):**
    Abra um terminal no VS Code (`Terminal` > `New Terminal`) e execute:
    ```bash
    # Cria um ambiente virtual chamado 'venv'
    python -m venv venv
    
    # Ativa o ambiente
    # No Windows (PowerShell/CMD):
    .\venv\Scripts\Activate
    # No macOS/Linux:
    source venv/bin/activate
    ```

3.  **Instale o VPython:**
    Com o ambiente ativado, instale a biblioteca VPython:
    ```bash
    pip install vpython
    ```

### 3. Execução

1.  **Abra o arquivo:** Abra o arquivo de script Python (ex: `simulacao.py`) no editor do VS Code.
2.  **Execute o Script:**
    Clique no **ícone de "Play"** no canto superior direito do editor do VS Code, ou clique com o botão direito no editor e selecione "Run Python File in Terminal".

    

3.  **Visualize no Navegador:**
    O VPython iniciará automatically um pequeno servidor web local. O seu navegador padrão **abrirá uma nova aba** (geralmente em `http://localhost:XXXX`) exibindo a simulação 3D interativa. Os controles definidos no código aparecerão à direita da cena.

## 🔬 Detalhes do Código

* `reset_simulation()`: Esta é a função principal que é chamada no início e sempre que o botão "Resetar" é pressionado. Ela lê todos os valores dos campos de `winput`, atualiza as propriedades da partícula e a variável global `B_field`, e recalcula o raio da trajetória.
* `while True:`: Este é o loop principal da simulação.
    * `rate(100)`: Limita o loop a 100 iterações por segundo, para que a simulação rode em uma velocidade visível.
    * **Lógica RK2 (Ponto Médio):** Em vez de calcular a força e atualizar a posição em um único passo (método de Euler), o código:
        1.  Calcula a aceleração no tempo $t$.
        2.  Usa essa aceleração para "prever" a velocidade no "ponto médio" do passo ($t + dt/2$).
        3.  Calcula a aceleração *neste ponto médio* (usando a velocidade prevista).

        4.  Usa esta aceleração do ponto médio para fazer a atualização final da velocidade e da posição. Este "passo extra" é o que torna o método muito mais estável para movimentos oscilatórios, como este.
