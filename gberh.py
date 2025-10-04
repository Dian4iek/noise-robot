import streamlit as st

st.markdown("""
    <style>
        [data-testid="stAppViewContainer"] {
            background-color: #E7D3BB;
        }
        [data-testid="stHeader"] {
            background-color: #E7D3BB;
        }
        [data-testid="stSidebar"] {
            background-color: #E7D3BB;
        }
        html, body {
            background-color: #E7D3BB;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Noise Robot 🤖")
st.write("Визначаю рівень шуму, кількість людей та рекомендований час перебування")

# 👇 Твої дані (залишені без змін)
data = {
    ("16:00", "Парк"): (46, 53, 7),
    ("16:00", "Дорога"): (47, 70, 11),
    ("17:00", "Дорога"): (54, 77, 15),
    ("17:00", "Парк"): (45, 72, 12),
}

# Таблиця допустимого часу
safe_time_table = {
    50: None,   # без обмежень
    60: 480,    # до 60 дБ — 8 год
    65: 240,    # до 65 дБ — 4 год
    70: 120,    # до 70 дБ — 2 год
    75: 60,     # до 75 дБ — 1 год
    80: 30,     # до 80 дБ — 30 хв
    85: 15,     # до 85 дБ — 15 хв
    90: 5,      # до 90 дБ — 5 хв
}

# Вибір користувача
time = st.selectbox("🕒 Яка година вас цікавить?", [
    "08:00","09:00","10:00","11:00","12:00","13:00","14:00",
    "15:00","16:00","17:00","18:00","19:00"
])
location = st.selectbox("📍 Яке місце вас цікавить?", ["Парк", "Дорога", "ТРЦ"])

# Результат
if (time, location) in data:
    dB_min, dB_max, people = data[(time, location)]
    avg_db = round((dB_min + dB_max) / 2)  # округлення до цілого

    st.subheader(f"🔊 У {location.lower()} о {time}: {dB_min}-{dB_max} дБ")
    st.write(f"**Середній рівень шуму:** {avg_db} дБ")
    st.write(f"**Кількість людей поруч:** {people} осіб")

    # Шукаємо рекомендований час
    recommended_minutes = None
    for db_threshold in sorted(safe_time_table.keys()):
        if avg_db <= db_threshold:
            recommended_minutes = safe_time_table[db_threshold]
            break

    if recommended_minutes is None:
        st.success("✅ Безпечний рівень шуму — обмежень немає")
    else:
        hours = recommended_minutes // 60
        mins = recommended_minutes % 60
        pretty_time = f"{hours} год {mins} хв" if hours else f"{mins} хв"
        st.info(f"🕓 Рекомендований максимум: **{pretty_time}**")

        # Візуальні рекомендації
        if avg_db <= 60:
            st.success("✅ Безпечно, можна перебувати довго")
        elif avg_db <= 75:
            st.warning("⚠️ Середній рівень шуму — краще обмежити час")
        else:
            st.error("🚫 Високий рівень шуму — уникати тривалого перебування")
else:
    st.warning("Для цього часу або місця поки немає даних. Додай свої вимірювання у таблицю 🔧")
