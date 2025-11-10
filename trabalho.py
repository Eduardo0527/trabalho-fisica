from vpython import *

# 1. Configurar a cena
scene = canvas(title='Movimento de uma partícula em um B uniforme',
               width=1500, height=800,  # <-- TELA GRANDE
               background=color.gray(0.1),
               align='right') # <-- Controles à direita

# Posição da câmera ajustada para a cena maior
scene.camera.pos = vector(0, 0, 20) 

# 2. Definir constantes e variáveis globais
# B_field agora é uma variável global, inicializada aqui
global B_field
B_field = vector(0, 0, 1)
dt = 0.01              # Passo de tempo
t = 0                  # Tempo inicial

# Eixos para referência visual (comprimento 10)
arrow(pos=vector(0,0,0), axis=vector(10,0,0), color=color.red, shaftwidth=0.05)
arrow(pos=vector(0,0,0), axis=vector(0,10,0), color=color.green, shaftwidth=0.05)
arrow(pos=vector(0,0,0), axis=vector(0,0,10), color=color.blue, shaftwidth=0.05)
label(pos=vector(10,0,0), text='X', color=color.red, opacity=0, box=False)
label(pos=vector(0,10,0), text='Y', color=color.green, opacity=0, box=False)
label(pos=vector(0,0,10), text='Z', color=color.blue, opacity=0, box=False)

# --- Funções de Controle ---

def placeholder():
    """
    Função vazia usada para satisfazer o requisito 'bind' dos widgets.
    """
    pass

def reset_simulation():
    """
    Chamada pelo botão 'Resetar' E uma vez no início.
    Reinicia a partícula e ATUALIZA O CAMPO B e o RAIO.
    """
    global particula, t, B_field # B_field agora é global
    
    # 1. Tenta ler os números dos widgets
    val_vx = w_vx.number
    val_vy = w_vy.number
    val_vz = w_vz.number
    val_charge = w_charge.number
    val_mass = w_mass.number
    
    # --- NOVOS VALORES PARA O CAMPO B ---
    val_bx = w_bx.number
    val_by = w_by.number
    val_bz = w_bz.number

    # 2. Verificação de 'None' (para a inicialização)
    if val_vx is None: val_vx = 0.0
    if val_vy is None: val_vy = 0.0
    if val_vz is None: val_vz = 0.0
    if val_charge is None: val_charge = 0.0
    if val_mass is None: val_mass = 0.0
    if val_bx is None: val_bx = 0.0
    if val_by is None: val_by = 0.0
    if val_bz is None: val_bz = 0.0
    
    # 3. Reseta a posição
    particula.pos = vector(0, 0, 0)
    
    # 4. Atualiza a variável global B_field
    B_field = vector(val_bx, val_by, val_bz)
    
    # 5. Usa os valores verificados para a partícula
    particula.velocity = vector(val_vx, val_vy, val_vz)
    particula.charge = val_charge
    particula.mass = val_mass
    
    # Garante que a massa não seja zero ou negativa
    if particula.mass <= 0:
        particula.mass = 1.0
        w_mass.text = "1.0"
        
    # --- 6. CALCULAR E EXIBIR O RAIO ---
    B_mag = B_field.mag
    q_abs = abs(particula.charge)
    
    v_perp_mag = 0
    if B_mag > 0: # Evita divisão por zero na projeção
        # v_paralelo = projeção de v em B
        v_parallel = proj(particula.velocity, B_field)
        # v_perpendicular = v - v_paralelo
        v_perpendicular = particula.velocity - v_parallel
        v_perp_mag = v_perpendicular.mag
    else:
        # Se B=0, não há rotação, v_perp é a velocidade total
        v_perp_mag = particula.velocity.mag 

    # Calcula o denominador R = (m * v_perp) / (q * B)
    denominator = q_abs * B_mag
    
    if denominator == 0:
        # Movimento linear (carga neutra ou campo B nulo)
        radius_text.text = "Infinito (mov. linear)"
    else:
        R_calc = (particula.mass * v_perp_mag) / denominator
        # Formata o número para 3 casas decimais
        radius_text.text = f"{R_calc:.3f}" 
        
    # --- 7. Limpa o rastro e reseta o tempo ---
    particula.make_trail = False
    particula.clear_trail() 
    particula.make_trail = True
    
    t = 0

# --- Controles de UI (Interface do Usuário) ---
button(text="Resetar Simulação", bind=reset_simulation)
scene.append_to_caption('\n\n--- Partícula ---')

scene.append_to_caption('\nCarga (q): ')
w_charge = winput(text='0.0', type='numeric', bind=placeholder)

scene.append_to_caption('\nMassa (m): ')
w_mass = winput(text='1.0', type='numeric', bind=placeholder)

scene.append_to_caption('\nVelocidade Inicial (Vx): ')
w_vx = winput(text='0.0', type='numeric', bind=placeholder)

scene.append_to_caption('\nVelocidade Inicial (Vy): ')
w_vy = winput(text='0.0', type='numeric', bind=placeholder)

Vz = 0.0
scene.append_to_caption('\nVelocidade Inicial (Vz): ')
w_vz = winput(text='0.0', type='numeric', bind=placeholder)

# --- NOVOS CONTROLES PARA CAMPO B ---
scene.append_to_caption('\n\n--- Campo Magnético ---')
scene.append_to_caption('\nCampo Bx: ')
w_bx = winput(text='0.0', type='numeric', bind=placeholder)
scene.append_to_caption('\nCampo By: ')
w_by = winput(text='0.0', type='numeric', bind=placeholder)
scene.append_to_caption('\nCampo Bz: ')
w_bz = winput(text='0.0', type='numeric', bind=placeholder)

# --- NOVO WIDGET PARA EXIBIR O RAIO ---
scene.append_to_caption('\n\n--- Dados Calculados ---')
scene.append_to_caption('\nRaio (R): ')
radius_text = wtext(text='-') # 'wtext' é um texto que pode ser atualizado

# --- Configuração Inicial da Partícula ---
particula = sphere(pos=vector(0, 0, 0),
                   radius=0.2,
                   color=color.yellow,
                   make_trail=True,
                   trail_type='curve',
                   trail_color=color.cyan,
                   retain=1000)

# Chama a função de reset uma vez para configurar o estado inicial
reset_simulation()

# --- Loop da Simulação (MÉTODO DO PONTO MÉDIO - RK2) ---
# Este método é de ordem superior (Runge-Kutta 2) e conserva a energia
# muito melhor que o método de Euler, impedindo o raio de aumentar.
while True:
    rate(100) 
    
    # 1. Salvar estado atual (t)
    v_old = particula.velocity
    pos_old = particula.pos
    
    # 2. Calcular aceleração em (t) com base em v(t)
    a_old = (particula.charge / particula.mass) * cross(v_old, B_field)
    
    # 3. Estimar velocidade no "ponto médio" (t + dt/2)
    # v(t + dt/2) = v(t) + a(t) * (dt/2)
    v_mid = v_old + a_old * (dt / 2.0)
    
    # 4. Calcular aceleração no "ponto médio" (usando v_mid)
    # a(t + dt/2) = (q/m) * v(t + dt/2) x B
    a_mid = (particula.charge / particula.mass) * cross(v_mid, B_field)
    
    # 5. Atualizar velocidade para (t + dt) usando a aceleração do ponto médio
    # v(t + dt) = v(t) + a(t + dt/2) * dt
    particula.velocity = v_old + a_mid * dt
    
    # 6. Atualizar Posição para (t + dt) usando a velocidade do ponto médio
    # x(t + dt) = x(t) + v(t + dt/2) * dt
    particula.pos = pos_old + v_mid * dt
    
    # 7. Atualizar o tempo
    t = t + dt