import streamlit as st
from PIL import Image
import time

st.set_page_config(page_title="Ancient Tale", layout="wide")

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "character" not in st.session_state:
    st.session_state.character = None
if "hearts" not in st.session_state:
    st.session_state.hearts = 4
if "pearls_answered" not in st.session_state:
    st.session_state.pearls_answered = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# --- Navigation helper ---
def next_page(page):
    st.session_state.page = page

# --- Helper to show full image as background ---
def show_scene_background(image_path):
    try:
        img = Image.open(image_path)
        st.image(img, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"⚠️ Missing image: {image_path}")

# --- MENU PAGE ---
if st.session_state.page == "menu":
    show_scene_background("menu.png")
    st.markdown("<h1 style='text-align:center; font-size:60px; color:white;'>Ancient Tales</h1>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sign In", use_container_width=True):
            next_page("signin")
    with col2:
        if st.button("Enter as Guest", use_container_width=True):
            next_page("choose_character")

# --- SIGN IN PAGE ---
elif st.session_state.page == "signin":
    show_scene_background("menu.png")
    st.markdown("<h2 style='text-align:center; color:white;'>Sign In</h2>", unsafe_allow_html=True)
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        if email and password:
            next_page("choose_character")
        else:
            st.warning("Please enter your email and password")

# --- CHARACTER SELECTION PAGE ---
elif st.session_state.page == "choose_character":
    show_scene_background("menu.png")
    st.markdown("<h2 style='text-align:center; color:white; font-size:40px;'>Choose Your Character</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.image("dhabia.png", width=300)
        if st.button("Play as Dhabia"):
            st.session_state.character = "girl"
            next_page("scene_dubai1")
    with col2:
        st.image("nahyan.png", width=300)
        if st.button("Play as Nahyan"):
            st.session_state.character = "boy"
            next_page("scene_dubai1")

# --- Function to show scenes ---
c = st.session_state.character

def show_scene(scene_name, next_scene):
    if c:
        show_scene_background(f"{scene_name}{c}.png")
        if st.button("Next ➜", use_container_width=True):
            next_page(next_scene)

# --- DUBAI scenes ---
if st.session_state.page == "scene_dubai1":
    show_scene("dubainew1", "scene_dubai2")

elif st.session_state.page == "scene_dubai2":
    show_scene("dubainew2", "scene_welcome1")

# --- WELCOME scenes ---
elif st.session_state.page == "scene_welcome1":
    show_scene("welcome1", "scene_welcome2")

elif st.session_state.page == "scene_welcome2":
    show_scene("welcome2", "scene_kids1")

# --- KIDS scenes ---
elif st.session_state.page == "scene_kids1":
    show_scene("kids1", "scene_kids2")

elif st.session_state.page == "scene_kids2":
    show_scene("kids2", "scene_kids3")

elif st.session_state.page == "scene_kids3":
    show_scene("kids3", "scene_kids4")

elif st.session_state.page == "scene_kids4":
    show_scene("kids4", "scene_crew1")

# --- CREW scenes 1–9 ---
for i in range(1, 10):
    if st.session_state.page == f"scene_crew{i}":
        next_scene = "pearl_game" if i == 9 else f"scene_crew{i+1}"
        show_scene(f"crew{i}", next_scene)

# --- PEARL GAME ---
if st.session_state.page == "pearl_game":
    show_scene_background(f"pearlgame1{c}.png")

    if st.session_state.start_time is None:
        st.session_state.start_time = time.time()

    elapsed = time.time() - st.session_state.start_time
    hearts_left = 4 - int(elapsed // 30)
    st.session_state.hearts = max(hearts_left, 0)

    # Show hearts
    hearts_display = "❤️ " * st.session_state.hearts
    st.markdown(f"<h3 style='color:red; text-align:center;'>{hearts_display}</h3>", unsafe_allow_html=True)

    # Pearls and questions
    pearls = [
        ("pearl1.png", "What do pearl divers search for?", "Pearls"),
        ("pearl2.png", "Where did divers usually go?", "The sea"),
        ("pearl3.png", "What tool did they use to dive?", "Nose clip"),
        ("pearl4.png", "Who leads the divers?", "Naukhada")
    ]

    cols = st.columns(4)
    for i, (img, q, a) in enumerate(pearls):
        with cols[i]:
            st.image(img, width=100)
            if st.button(f"Pearl {i+1}", key=f"pearl{i}"):
                ans = st.text_input(q, key=f"q{i}")
                if ans:
                    st.success(f"Correct answer: {a}")
                    st.session_state.pearls_answered += 1

    if st.session_state.pearls_answered >= 4 or st.session_state.hearts == 0:
        next_page("ship")

# --- SHIP scene ---
if st.session_state.page == "ship":
    show_scene_background(f"ship1{c}.png")
    st.markdown("<h3 style='color:white;'>Naukhada asks: What is the role of teamwork in pearl diving?</h3>", unsafe_allow_html=True)
    st.text_input("Answer here")
    if st.button("Finish Round"):
        next_page("congrats1")

# --- CONGRATULATIONS scenes ---
if st.session_state.page == "congrats1":
    show_scene_background(f"congrats1{c}.png")
    st.markdown("<h1 style='color:gold; text-align:center;'>Congratulations!</h1>", unsafe_allow_html=True)
    time.sleep(5)
    next_page("congrats2")

elif st.session_state.page == "congrats2":
    show_scene_background(f"congrats2{c}.png")
    st.markdown("<h2 style='color:white; text-align:center;'>You completed the Ancient Tale!</h2>", unsafe_allow_html=True)
