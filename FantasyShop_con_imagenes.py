
import streamlit as st
from dataclasses import dataclass

st.set_page_config(page_title="Fantasy Shop", page_icon="🧙", layout="wide")

st.markdown("""
<style>
.stApp {background-color:#111018;}
h1,h2,h3 {color:#c77dff;}
.stButton>button {background:#7b2cbf;color:white;}
</style>
""", unsafe_allow_html=True)

@dataclass
class Producto:
    id_producto:int
    nombre:str
    categoria:str
    precio:float
    imagen:str

productos = [
    Producto(2001,"DragonSkin Haptic Armor","Traje Háptico",1499.99,"image(60).png"),
    Producto(2002,"Arcane Vision X","Gafas VR",899.99,"image(63).png"),
    Producto(2003,"Phantom Touch Gloves","Guantes Hápticos",499.99,"image(64).png"),
    Producto(2004,"Rune Motion Tracker","Sensores",299.99,"image(62).png"),
    Producto(2005,"Mystic Glide Elite","Mouse Glides",39.99,"image(61).png"),
]

if "carrito" not in st.session_state:
    st.session_state.carrito = []

menu = st.sidebar.radio("Menú",["Inicio","Catálogo","Carrito","Estadísticas"])

if menu == "Inicio":
    st.title("🧙 Fantasy Shop")
    st.subheader("Gaming inmersivo y realidad virtual")
    st.write("Fantasy Shop combina fantasía y tecnología para ofrecer experiencias inmersivas de nueva generación.")
    st.markdown("### 🔥 Productos Destacados")
    st.success("DragonSkin Haptic Armor")
    st.success("Arcane Vision X")
    st.success("Phantom Touch Gloves")

elif menu == "Catálogo":
    st.title("📦 Catálogo")

    for p in productos:
        c1, c2 = st.columns([1,2])

        with c1:
            try:
                st.image(p.imagen, use_container_width=True)
            except:
                st.info("Imagen no encontrada")

        with c2:
            st.subheader(p.nombre)
            st.write(f"Categoría: {p.categoria}")
            st.write(f"Precio Base: USD {p.precio:.2f}")

            if st.button(f"Agregar al carrito {p.id_producto}"):
                st.session_state.carrito.append({
                    "nombre": p.nombre,
                    "categoria": p.categoria,
                    "imagen": p.imagen,
                    "precio_base": p.precio,
                    "precio_final": p.precio,
                    "detalle": "Sin personalizar"
                })
                st.success("Producto agregado")

        st.markdown("---")

elif menu == "Carrito":
    st.title("🛒 Carrito")

    if not st.session_state.carrito:
        st.info("El carrito está vacío.")
    else:
        for i,item in enumerate(st.session_state.carrito):

            try:
                st.image(item["imagen"], width=250)
            except:
                pass

            st.subheader(item["nombre"])
            st.write(f"Precio actual: USD {item['precio_final']:.2f}")

            if item["categoria"] == "Traje Háptico":
                color = st.selectbox("Color",["Negro","Violeta","Rojo","Blanco"],key=f"c{i}")
                intensidad = st.selectbox("Intensidad",["Baja","Media","Alta"],key=f"in{i}")
                sensores = st.checkbox("Sensores extra",key=f"s{i}")
                grabado = st.text_input("Grabado personalizado",key=f"g{i}")

                if st.button("Aplicar Personalización",key=f"p{i}"):
                    total = item["precio_base"]
                    if intensidad == "Media": total += 50
                    elif intensidad == "Alta": total += 100
                    if sensores: total += 150
                    if grabado: total += 25

                    item["precio_final"] = total
                    item["detalle"] = f"{color} | {intensidad} | Sensores:{sensores} | Grabado:{grabado}"

            elif item["categoria"] == "Gafas VR":
                audio = st.checkbox("Audio integrado",key=f"a{i}")
                premium = st.checkbox("Correa premium",key=f"pr{i}")
                vision = st.checkbox("Campo visual avanzado",key=f"v{i}")

                if st.button("Personalizar VR",key=f"vr{i}"):
                    total = item["precio_base"]
                    if audio: total += 80
                    if premium: total += 60
                    if vision: total += 120
                    item["precio_final"] = total

            elif item["categoria"] == "Guantes Hápticos":
                talle = st.selectbox("Talle",["S","M","L","XL"],key=f"t{i}")
                sensibilidad = st.selectbox("Sensibilidad",["Baja","Media","Alta"],key=f"se{i}")

                if st.button("Personalizar Guantes",key=f"gu{i}"):
                    total = item["precio_base"]
                    if sensibilidad == "Media": total += 30
                    elif sensibilidad == "Alta": total += 60
                    item["precio_final"] = total
                    item["detalle"] = f"Talle:{talle} | Sensibilidad:{sensibilidad}"

            st.write("Configuración:", item["detalle"])

            if st.button("Quitar del carrito", key=f"e{i}"):
                st.session_state.carrito.pop(i)
                st.rerun()

            st.markdown("---")

        total = sum(x["precio_final"] for x in st.session_state.carrito)
        st.success(f"💰 Total del carrito: USD {total:.2f}")

elif menu == "Estadísticas":
    st.title("📊 Estadísticas")
    st.metric("Productos disponibles", len(productos))
    st.metric("Categorías", len(set(p.categoria for p in productos)))
    st.metric("Productos en carrito", len(st.session_state.carrito))
    st.metric("Valor carrito USD", f"{sum(x['precio_final'] for x in st.session_state.carrito):.2f}")
