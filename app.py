import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import io

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Optimizador de Espacios",
    page_icon="📦",
    layout="wide"
)

# --- Funciones de Simulación (Aquí iría la lógica de IA) ---

def detect_objects_placeholder(image_bytes):
    """
    Placeholder para la detección de objetos.
    En una aplicación real, aquí usarías un modelo de IA (como YOLO o Detectron2)
    para identificar objetos en la imagen y devolver sus coordenadas.
    """
    st.info("Simulación: Detectando objetos como estanterías, mesas, etc.")
    # Simulación de objetos detectados con sus cajas delimitadoras [x1, y1, x2, y2]
    # y un tipo de mobiliario.
    detected_objects = [
        {"label": "Estantería A", "box": [50, 50, 150, 250], "type": "storage"},
        {"label": "Estantería B", "box": [50, 300, 150, 500], "type": "storage"},
        {"label": "Mesa de Trabajo", "box": [200, 150, 300, 350], "type": "workspace"},
        {"label": "Caja 1", "box": [350, 400, 400, 450], "type": "item"},
        {"label": "Caja 2", "box": [350, 460, 400, 510], "type": "item"},
        {"label": "Espacio Vacío", "box": [200, 400, 300, 500], "type": "space"},
    ]
    return detected_objects

def generate_layouts_placeholder(objects, image_size):
    """
    Placeholder para el algoritmo de optimización.
    Aquí iría la lógica compleja para reorganizar los objetos detectados
    y proponer nuevas distribuciones que optimicen el espacio.
    """
    st.info("Simulación: Generando nuevas opciones de distribución del espacio.")
    layouts = []
    width, height = image_size

    # Opción 1 (Recomendada): Más organizada
    layout_1 = [
        {"label": "Estantería A", "box": [30, 30, 80, 400], "type": "storage"},
        {"label": "Estantería B", "box": [100, 30, 150, 400], "type": "storage"},
        {"label": "Mesa de Trabajo", "box": [200, 100, 300, 300], "type": "workspace"},
        {"label": "Caja 1", "box": [350, 50, 400, 100], "type": "item"},
        {"label": "Caja 2", "box": [350, 110, 400, 160], "type": "item"},
    ]
    layouts.append({"title": "Opción 1 (Recomendada)", "layout": layout_1})

    # Opción 2: Distribución alternativa
    layout_2 = [
        {"label": "Estantería A", "box": [30, 30, 250, 80], "type": "storage"},
        {"label": "Estantería B", "box": [30, 100, 250, 150], "type": "storage"},
        {"label": "Mesa de Trabajo", "box": [300, 200, 450, 350], "type": "workspace"},
        {"label": "Caja 1", "box": [30, 200, 80, 250], "type": "item"},
        {"label": "Caja 2", "box": [30, 260, 80, 310], "type": "item"},
    ]
    layouts.append({"title": "Opción 2", "layout": layout_2})

    return layouts

def render_layout_image(layout, image_size):
    """
    Dibuja una imagen representando una de las distribuciones propuestas.
    """
    width, height = image_size
    image = Image.new('RGB', (width, height), color = '#f0f2f6')
    draw = ImageDraw.Draw(image)

    # Colores para diferentes tipos de objetos
    colors = {
        "storage": "#4a90e2", # Azul
        "workspace": "#e2a34a", # Naranja
        "item": "#a2a2a2", # Gris
        "space": "#50e3c2" # Turquesa
    }

    try:
        # Intenta cargar una fuente, si no, usa la default.
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        font = ImageFont.load_default()

    for obj in layout:
        box = obj["box"]
        obj_type = obj.get("type", "item")
        color = colors.get(obj_type, "#000000")
        
        # Dibuja el rectángulo y un borde
        draw.rectangle(box, fill=color, outline="black", width=2)
        
        # Dibuja la etiqueta
        text_position = (box[0] + 5, box[1] + 5)
        draw.text(text_position, obj["label"], fill="white", font=font)

    return image

# --- Interfaz de Usuario con Streamlit ---

st.title("📦 Optimizador de Espacios de Bodega")
st.markdown("""
    Sube una foto de tu bodega o usa la cámara para capturar una imagen.
    La aplicación analizará la disposición actual y te propondrá distribuciones
    optimizadas para mejorar el flujo y el uso del espacio.
""")

# Carga de imagen
source_img = None
st.subheader("1. Carga la imagen de tu espacio")
uploader_col, camera_col = st.columns(2)

with uploader_col:
    uploaded_file = st.file_uploader(
        "Arrastra una imagen o haz clic para subir",
        type=['png', 'jpg', 'jpeg']
    )
    if uploaded_file:
        source_img = uploaded_file.getvalue()

with camera_col:
    camera_photo = st.camera_input("O usa la cámara para tomar una foto")
    if camera_photo:
        source_img = camera_photo.getvalue()

if source_img:
    st.subheader("2. Imagen Original")
    image = Image.open(io.BytesIO(source_img))
    st.image(image, caption="Espacio a analizar", use_column_width=True)

    if st.button("🚀 Analizar y Optimizar Espacio", type="primary"):
        with st.spinner("Analizando imagen y generando opciones... Por favor, espera."):
            
            # --- Proceso de Análisis y Optimización (Simulado) ---
            # 1. Detectar objetos en la imagen.
            detected_objects = detect_objects_placeholder(source_img)
            
            # 2. Generar nuevas distribuciones.
            new_layouts = generate_layouts_placeholder(detected_objects, image.size)
            
            # 3. Renderizar las nuevas distribuciones como imágenes.
            rendered_images = []
            for layout_option in new_layouts:
                rendered_img = render_layout_image(layout_option["layout"], image.size)
                rendered_images.append({
                    "title": layout_option["title"],
                    "image": rendered_img
                })

        st.success("¡Análisis completado! Aquí tienes las opciones.")
        st.subheader("3. Opciones de Distribución Optimizada")

        # Mostrar las opciones en columnas
        cols = st.columns(len(rendered_images))
        for i, option in enumerate(rendered_images):
            with cols[i]:
                st.image(option["image"], caption=option["title"], use_column_width=True)
else:
    st.info("Esperando una imagen para analizar...")
