import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px

st.set_page_config(
    page_title="Thông tin khí thải CO2",
    page_icon="🌿",
    layout="wide"
)

# Hàm tạo màu theo emission
def color_by_emission(emission):
    if emission < 10:
        return [0, 128, 0, 160]       # xanh lá (thấp)
    elif emission < 50:
        return [255, 165, 0, 160]     # cam (trung bình)
    else:
        return [255, 0, 0, 160]       # đỏ (cao)

# Hàm lời khuyên theo emission
def advice_by_co2(co2):
    if co2 < 10:
        return "Lượng khí thải thấp, bạn đang góp phần bảo vệ môi trường. Hãy duy trì!"
    elif co2 < 50:
        return "Lượng khí thải trung bình, hãy cân nhắc giảm sử dụng các thiết bị gây ô nhiễm."
    else:
        return "Lượng khí thải cao, bạn nên hạn chế hoạt động gây ô nhiễm và tìm giải pháp thân thiện môi trường."

# Đọc dữ liệu
df = pd.read_csv('latest_submission_with_coords.csv')

# Thêm cột màu và lời khuyên trước khi tạo layer
df['color'] = df['emission'].apply(color_by_emission)
df['advice'] = df['emission'].apply(advice_by_co2)

view_state = pdk.ViewState(
    latitude=df['latitude'].mean(),
    longitude=df['longitude'].mean(),
    zoom=6,
    pitch=0
)

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position='[longitude, latitude]',
    get_fill_color='color',
    get_radius=1000,
    pickable=True
)

tooltip = {
    "html": "<b>Kinh độ:</b> {longitude} <br/>"
            "<b>Vĩ độ:</b> {latitude} <br/>"
            "<b>Năm:</b> {year} <br/>"
            "<b>Tuần:</b> {week_no} <br/>"
            "<b>Khí thải CO2:</b> {emission} <br/>"
            "<b>Lời khuyên:</b> {advice}",
    "style": {
        "backgroundColor": "steelblue",
        "color": "white",
        "fontSize": "12px",
        "padding": "5px",
        "borderRadius": "5px"
    }
}

r = pdk.Deck(
    layers=[scatter_layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style='mapbox://styles/mapbox/satellite-streets-v11',
    api_keys={'mapbox': 'YOUR_MAPBOX_ACCESS_TOKEN'},
)

st.markdown(
    """
    <style>
    .deckgl-wrapper {
        width: 100% !important;
        height: 900px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Thông tin lượng khí thải CO2")  # Tiêu đề chung

# Tạo 2 tab
tab1, tab2 = st.tabs(["Bản đồ khí thải CO2", "Thông tin & Biểu đồ"])

with tab1:
    selected = st.pydeck_chart(r, use_container_width=True)

with tab2:
    st.subheader("Chọn thông tin để xem lượng khí thải CO2 và biểu đồ")

    # Lấy danh sách các cặp (lat, lon) duy nhất
    coords = df[['latitude', 'longitude']].drop_duplicates().reset_index(drop=True)
    coords_str = coords.apply(lambda row: f"{row['latitude']:.4f}, {row['longitude']:.4f}", axis=1)

    selected_coord = st.selectbox("Chọn tọa độ (latitude, longitude)", coords_str)

    # Lấy giá trị lat và lon từ chuỗi đã chọn
    lat_sel, lon_sel = map(float, selected_coord.split(','))

    # Lọc dataframe theo tọa độ đã chọn
    df_coord = df[(df['latitude'] == lat_sel) & (df['longitude'] == lon_sel)]

    # Chọn năm trong các năm có dữ liệu của tọa độ đó
    years = df_coord['year'].unique()
    selected_year = st.selectbox("Chọn năm", sorted(years))

    # Lọc theo năm đã chọn
    df_year = df_coord[df_coord['year'] == selected_year]

    # Chọn tuần trong các tuần có dữ liệu
    weeks = df_year['week_no'].unique()
    selected_week = st.selectbox("Chọn tuần", sorted(weeks))

    if st.button("Xác nhận"):
        # Lọc dữ liệu theo tọa độ, năm, tuần
        df_filtered = df_year[df_year['week_no'] == selected_week]

        if df_filtered.empty:
            st.warning("Không tìm thấy dữ liệu cho lựa chọn này!")
        else:
            row = df_filtered.iloc[0]
            st.write(f"**Lượng khí thải CO2: {row['emission']}**")

            # Biểu đồ đường lượng khí thải theo tuần (của năm và tọa độ đó)
            data_plot = df_year.sort_values('week_no')

            fig = px.line(
                data_plot,
                x='week_no',
                y='emission',
                title=f'Lượng khí thải CO2 năm {selected_year} tại ({lat_sel:.4f}, {lon_sel:.4f})',
                labels={'week_no': 'Tuần trong năm', 'emission': 'Lượng khí thải CO2'}
            )
            st.plotly_chart(fig, use_container_width=True)

