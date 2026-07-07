import gradio as gr
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from fpdf import FPDF
import tempfile

theme_state = gr.State("dark")

COUNTRIES = {
    "India": [69.7, 6.7, 12.2, 8900],
    "USA": [78.9, 13.4, 16.3, 70249],
    "Norway": [82.3, 12.9, 18.1, 66494],
    "Nigeria": [54.7, 6.7, 10.0, 5196],
    "Japan": [84.5, 12.8, 15.2, 42420],
    "Brazil": [75.9, 8.0, 15.2, 15385],
    "Custom": [72.5, 8.5, 12.0, 15000]
}

def calculate_hdi(life_exp, mean_school, exp_school, gni, theme):
    health_index = max(0, min(1, (life_exp - 20) / 65))
    mean_edu_index = max(0, min(1, mean_school / 15))
    exp_edu_index = max(0, min(1, exp_school / 18))
    education_index = (mean_edu_index + exp_edu_index) / 2
    income_index = max(0, min(1, (np.log(gni) - np.log(100)) / (np.log(75000) - np.log(100))))

    hdi = (health_index * education_index * income_index) ** (1/3)
    hdi_score = round(hdi * 100, 2)

    if hdi_score >= 80: level, color1, color2, emoji, desc = "Very High HDI", "#00F5A0", "#00D9F5", "🏆", "World Class Development"
    elif hdi_score >= 70: level, color1, color2, emoji, desc = "High HDI", "#3B82F6", "#8B5CF6", "🚀", "Strong Development"
    elif hdi_score >= 55: level, color1, color2, emoji, desc = "Medium HDI", "#F59E0B", "#EF4444", "⚡", "Moderate Development"
    else: level, color1, color2, emoji, desc = "Low HDI", "#EF4444", "#991B1B", "📉", "Needs Improvement"

    bg = "#050714" if theme == "dark" else "#F0F9FF"
    card_bg = "rgba(15, 23, 42, 0.6)" if theme == "dark" else "rgba(255, 255, 255, 0.7)"
    text = "#FFFFFF" if theme == "dark" else "#0F172A"
    subtext = "#E2E8F0" if theme == "dark" else "#475569"

    # 1. 3D GLOBE
    fig_globe = go.Figure(data=[go.Surface(z=np.outer(np.cos(np.deg2rad(np.linspace(-90, 90, 50))), np.ones(50)),
        colorscale=[[0, color1], [1, color2]], showscale=False)])
    fig_globe.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False, bgcolor=bg), 
        paper_bgcolor=bg, height=400, title=dict(text="🌍 Global HDI Sphere", font=dict(color=text)))

    # 2. WORLD MAP
    df_map = px.data.gapminder().query("year==2007")
    df_map['hdi_sim'] = np.random.uniform(0.4, 0.95, len(df_map)) * 100
    fig_map = px.choropleth(df_map, locations="iso_alpha", color="hdi_sim", hover_name="country",
        color_continuous_scale=[[0, "#EF4444"], [0.5, "#F59E0B"], [1, "#00F5A0"]])
    fig_map.update_layout(paper_bgcolor=bg, geo=dict(bgcolor=bg), height=400, 
        title=dict(text="🗺️ World HDI Heatmap", font=dict(color=text)))

    # 3. AI SUGGESTIONS - FIXED VISIBILITY
    suggestions = []
    if health_index < 0.7: suggestions.append("🏥 Increase healthcare spending by 2% of GDP")
    if education_index < 0.7: suggestions.append("🎓 Invest in free primary + secondary education")
    if income_index < 0.7: suggestions.append("💰 Promote SMEs and digital economy for income growth")
    if hdi_score > 80: suggestions.append("🏆 Maintain policies. Focus on sustainability")
    if not suggestions: suggestions.append("✅ All indices are balanced")
    
    suggestions_html = f"""
    <div style='background:{card_bg}; backdrop-filter:blur(20px); padding:25px; border-radius:20px; border:1px solid {color1}40;'>
        <h3 style='color:{text}; margin-top:0;'>🤖 AI Policy Suggestions</h3>
        <div style='color:{subtext}; font-size:16px; line-height:1.8;'>{"<br>".join([f"• {s}" for s in suggestions])}</div>
    </div>
    """

    header_html = f"""
    <div style='background:linear-gradient(120deg, {color1}20, {color2}20); backdrop-filter:blur(30px); padding:40px; border-radius:28px; border:1px solid rgba(59,130,246,0.3); text-align:center;'>
        <h1 style='background:linear-gradient(90deg, #3B82F6, #00F5A0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size:48px; font-weight:900; margin:0;'>🌍 HDI Neural Intelligence</h1>
    </div>
    """

    # MAIN SCORE CARD
    result_html = f"""
    <div style='padding:50px; border-radius:32px; background:linear-gradient(135deg, {color1} 0%, {color2} 100%); color:white; text-align:center; box-shadow:0 0 80px {color1}50;'>
        <h1 style='font-size:80px; margin:0; font-weight:900;'>{emoji} {hdi_score}</h1>
        <h2 style='font-size:32px; margin:10px 0;'>{level}</h2>
        <p style='font-size:18px; opacity:0.9;'>{desc}</p>
    </div>
    """

    # FIXED STATS CARDS - TEXT NOW VISIBLE
    stats_html = f"""
    <div style='display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-top:25px;'>
        <div style='background:{card_bg}; backdrop-filter:blur(20px); padding:30px; border-radius:24px; border:1px solid {color1}50; box-shadow:0 0 20px {color1}20;'>
            <p style='color:{subtext}; font-size:14px; font-weight:600; margin:0; letter-spacing:1px;'>❤️ HEALTH INDEX</p>
            <h2 style='color:{text}; font-size:36px; font-weight:800; margin:10px 0 0 0;'>{health_index:.3f}</h2>
        </div>
        <div style='background:{card_bg}; backdrop-filter:blur(20px); padding:30px; border-radius:24px; border:1px solid {color2}50; box-shadow:0 0 20px {color2}20;'>
            <p style='color:{subtext}; font-size:14px; font-weight:600; margin:0; letter-spacing:1px;'>🎓 EDUCATION INDEX</p>
            <h2 style='color:{text}; font-size:36px; font-weight:800; margin:10px 0 0 0;'>{education_index:.3f}</h2>
        </div>
        <div style='background:{card_bg}; backdrop-filter:blur(20px); padding:30px; border-radius:24px; border:1px solid #8B5CF650; box-shadow:0 0 20px #8B5CF620;'>
            <p style='color:{subtext}; font-size:14px; font-weight:600; margin:0; letter-spacing:1px;'>💰 INCOME INDEX</p>
            <h2 style='color:{text}; font-size:36px; font-weight:800; margin:10px 0 0 0;'>{income_index:.3f}</h2>
        </div>
    </div>
    """

    fig = go.Figure(go.Indicator(mode="gauge+number", value=hdi_score, 
        title={'text': "HDI Score", 'font':{'color':text, 'size':20}}, 
        gauge={'bar': {'color': color1, 'thickness':0.4}, 'bgcolor': card_bg}))
    fig.update_layout(paper_bgcolor=bg, height=350)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatterpolar(r=[health_index*100, education_index*100, income_index*100], 
        theta=['Health', 'Education', 'Income'], fill='toself', line_color=color1))
    fig2.update_layout(polar=dict(bgcolor=card_bg, radialaxis=dict(color=text)), 
        paper_bgcolor=bg, font_color=text, height=350, showlegend=False)

    pdf_data = [hdi_score, level, health_index, education_index, income_index]
    return header_html, result_html, stats_html, fig_globe, fig_map, fig, fig2, suggestions_html, pdf_data

def load_country(name):
    return COUNTRIES.get(name, [72.5, 8.5, 12.0, 15000])

def generate_pdf(data):
    if data is None: return None
    hdi_score, level, h, e, i = data
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(200, 10, "HDI Neural Report", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 14)
    pdf.cell(200, 10, f"HDI Score: {hdi_score}", ln=True)
    pdf.cell(200, 10, f"Level: {level}", ln=True)
    pdf.cell(200, 10, f"Health: {h:.3f}", ln=True)
    pdf.cell(200, 10, f"Education: {e:.3f}", ln=True)
    pdf.cell(200, 10, f"Income: {i:.3f}", ln=True)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp.name)
    return tmp.name

with gr.Blocks(title="HDI Neural", css="""
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800;900&display=swap');
body {background: radial-gradient(ellipse at top, #1E293B 0%, #050714 100%);}
.gradio-container {font-family: 'Outfit';}
.gr-button {background: linear-gradient(90deg, #3B82F6, #8B5CF6)!important; border-radius: 18px!important; font-weight: 800!important; font-size:16px!important; border:none!important;}
.gr-button:hover {transform: translateY(-3px); box-shadow: 0 15px 40px rgba(59,130,246,0.4);}
""") as demo:
    theme_state = gr.State("dark")

    header = gr.HTML()

    with gr.Tabs():
        with gr.TabItem("🌐 Neural Prediction"):
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### 🎛️ Input Parameters")
                    country_dd = gr.Dropdown(list(COUNTRIES.keys()), value="India", label="🌎 Load Preset Country")
                    life_exp = gr.Slider(20, 85, value=69.7, step=0.1, label="Life Expectancy")
                    mean_school = gr.Slider(0, 15, value=6.7, step=0.1, label="Mean Schooling")
                    exp_school = gr.Slider(0, 18, value=12.2, step=0.1, label="Expected Schooling")
                    gni = gr.Slider(100, 75000, value=8900, step=100, label="GNI per Capita")
                    btn = gr.Button("⚡ ACTIVATE NEURAL MODEL", size="lg")
                    pdf_btn = gr.Button("📄 Generate PDF Report", variant="secondary")
                with gr.Column(scale=2):
                    result = gr.HTML()
                    stats = gr.HTML()
                    with gr.Row():
                        globe = gr.Plot()
                        world_map = gr.Plot()
                    with gr.Row():
                        gauge = gr.Plot()
                        radar = gr.Plot()
                    suggestions = gr.HTML()
            hidden_data = gr.State()

            country_dd.change(fn=load_country, inputs=country_dd, outputs=[life_exp, mean_school, exp_school, gni])
            btn.click(fn=calculate_hdi, inputs=[life_exp, mean_school, exp_school, gni, theme_state],
                      outputs=[header, result, stats, globe, world_map, gauge, radar, suggestions, hidden_data])
            pdf_btn.click(fn=generate_pdf, inputs=hidden_data, outputs=gr.File())

    gr.HTML("<div style='text-align:center; color:#64748B; padding:40px;'>Powered by HDI Neural AI © 2026</div>")

demo.launch(server_name="0.0.0.0", server_port=7860)