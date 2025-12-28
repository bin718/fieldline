import streamlit as st 
import numpy as np 
import matplotlib.pyplot as plt 

st.title("전기장 & 전기장선 시뮬레이션") 

# 사이드바 
st.sidebar.header("전하 1 설정") 
q1 = st.sidebar.slider("전하량 1 (Q1)", -10.0, 10.0, 4.0, step=2.0) 
x1 = st.sidebar.slider("전하 1의 X위치", -4.0, 0.0, -2.0, step=1.0) 

st.sidebar.header("전하 2 설정") 
q2 = st.sidebar.slider("전하량 2 (Q2)", -10.0, 10.0, -4.0, step=2.0) 
x2 = st.sidebar.slider("전하 2의 X위치", 0.0, 4.0, 2.0, step=1.0) 

# 격자 설정 
x = np.linspace(-5, 5, 25) 
y = np.linspace(-5, 5, 25) 
X, Y = np.meshgrid(x, y) 

# 전기장 계산 함수 
k=9e9 
def electric_field(x, y): 
    Ex, Ey = 0.0, 0.0 

    for q, cx in [(q1, x1), (q2, x2)]: 
        dx = x - cx 
        dy = y 
        r2 = dx**2 + dy**2 

        if r2 < 1e-6: 
            continue 
        
        r = np.sqrt(r2) 
        Ex += k * q * dx / r**3 
        Ey += k* q * dy / r**3 
            
    return Ex, Ey 
        
        
# 전기장선 추적 함수 (dr 고정) 
dr = 0.05 
steps = 400 

def trace_field_line(x0, y0, direction=1): 
    x, y = x0, y0 
    xs, ys = [x], [y] 

    for _ in range(steps): 
        Ex, Ey = electric_field(x, y) 
        E = np.sqrt(Ex**2 + Ey**2) + 1e-9

        if E < 1e-6: 
            break 
        
        x += direction * Ex / E * dr 
        y += direction * Ey / E * dr 

        xs.append(x) 
        ys.append(y) 
        
    return xs, ys 
    
    
# 전기장 벡터 계산 
Ex = np.zeros_like(X) 
Ey = np.zeros_like(Y) 

for i in range(X.shape[0]): 
    for j in range(X.shape[1]): 
        Ex[i, j], Ey[i, j] = electric_field(X[i, j], Y[i, j]) 
        
E = np.sqrt(Ex**2 + Ey**2) 
        

# 시각화 
fig, ax = plt.subplots(figsize=(8, 7)) 

# 전기장 벡터 
ax.quiver(X, Y, Ex/E, Ey/E, color='black', alpha=0.3) 

# 전기장선 시작점 
angles = np.linspace(0, 2*np.pi, 16)

starts1 = [(x1 + 0.2*np.cos(a), 0.2*np.sin(a)) for a in angles] 
starts2 = [(x2 + 0.2*np.cos(a), 0.2*np.sin(a)) for a in angles] 

dir1 = 1 if q1 >0 else -1
dir2 = 1 if q2 >0 else -1

for x0, y0 in starts1: 
    xs, ys = trace_field_line(x0, y0,dir1) 
    ax.plot(xs, ys, 'b') 

for x0, y0 in starts2: 
    xs, ys = trace_field_line(x0, y0,dir2) 
    ax.plot(xs, ys, 'b') 
    
# 전하 표시 
ax.scatter([x1], [0], c='red' if q1 > 0 else 'blue', s=200, edgecolors='black') 
ax.scatter([x2], [0], c='red' if q2 > 0 else 'blue', s=200, edgecolors='black') 

ax.set_xlim(-5, 5) 
ax.set_ylim(-5, 5) 
ax.set_aspect('equal') 
ax.grid(True, linestyle=':', alpha=0.6) 

st.pyplot(fig)
