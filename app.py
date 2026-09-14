import base64

# =======================================================
# ABA 1: INÍCIO E GALERIA DE FOTOS (COM SLIDESHOW)
# =======================================================
with aba_home:
    st.subheader("Bem-vindos à Escola Dominical da Ala Periperi")
    st.write(
        "Este portal foi desenvolvido para apoiar nosso estudo semanal do evangelho, "
        "reforçar as escrituras e incentivar a preparação de cada membro para as aulas de domingo."
    )

    pasta_assets = "assets"
    fotos = []
    if os.path.exists(pasta_assets):
        fotos = [os.path.join(pasta_assets, f) for f in os.listdir(pasta_assets) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    st.divider()
    st.markdown("### 📸 Momentos e Atividades da Ala")

    if fotos:
        # Codifica as imagens para exibição fluida no carrossel HTML
        slides_html = ""
        dots_html = ""
        for idx, fpath in enumerate(fotos):
            with open(fpath, "rb") as img_file:
                b64_str = base64.b64encode(img_file.read()).decode()
            ext = os.path.splitext(fpath)[1].replace(".", "").lower()
            nome_legenda = os.path.splitext(os.path.basename(fpath))[0].replace("_", " ").title()
            
            display_style = "block" if idx == 0 else "none"
            slides_html += f"""
            <div class="slide fade" style="display: {display_style};">
                <img src="data:image/{ext};base64,{b64_str}" style="width:100%; height:420px; object-fit: cover; border-radius: 12px;">
                <div class="caption-text">{nome_legenda}</div>
            </div>
            """
            active_class = "active" if idx == 0 else ""
            dots_html += f'<span class="dot {active_class}" onclick="currentSlide({idx+1})"></span>'

        carrossel_codigo = f"""
        <style>
        .slideshow-container {{
            max-width: 850px;
            position: relative;
            margin: auto;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 8px 24px rgba(11, 37, 69, 0.15);
            background-color: #0b2545;
        }}
        .caption-text {{
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
            padding: 12px 20px;
            position: absolute;
            bottom: 0px;
            width: 100%;
            text-align: center;
            background: linear-gradient(to top, rgba(11, 37, 69, 0.85), transparent);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .prev, .next {{
            cursor: pointer;
            position: absolute;
            top: 50%;
            width: auto;
            padding: 14px 18px;
            margin-top: -22px;
            color: white;
            font-weight: bold;
            font-size: 20px;
            transition: 0.3s;
            user-select: none;
            background-color: rgba(0,0,0,0.35);
            border-radius: 50%;
            text-decoration: none;
            margin-left: 10px;
            margin-right: 10px;
        }}
        .next {{ right: 0; }}
        .prev:hover, .next:hover {{ background-color: rgba(197, 160, 89, 0.85); color: #0b2545; }}
        .dots-container {{ text-align: center; margin-top: 12px; }}
        .dot {{
            cursor: pointer;
            height: 11px;
            width: 11px;
            margin: 0 4px;
            background-color: #cbd5e1;
            border-radius: 50%;
            display: inline-block;
            transition: background-color 0.3s ease;
        }}
        .active, .dot:hover {{ background-color: #c5a059; }}
        .fade {{
            animation-name: fade;
            animation-duration: 1.0s;
        }}
        @keyframes fade {{
            from {{opacity: .4}} 
            to {{opacity: 1}}
        }}
        </style>

        <div class="slideshow-container">
            {slides_html}
            <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
            <a class="next" onclick="plusSlides(1)">&#10095;</a>
        </div>
        <div class="dots-container">
            {dots_html}
        </div>

        <script>
        let slideIndex = 1;
        let timer = null;

        function showSlides(n) {{
            let i;
            let slides = document.getElementsByClassName("slide");
            let dots = document.getElementsByClassName("dot");
            if (n > slides.length) {{slideIndex = 1}}    
            if (n < 1) {{slideIndex = slides.length}}
            for (i = 0; i < slides.length; i++) {{
                slides[i].style.display = "none";  
            }}
            for (i = 0; i < dots.length; i++) {{
                dots[i].className = dots[i].className.replace(" active", "");
            }}
            slides[slideIndex-1].style.display = "block";  
            dots[slideIndex-1].className += " active";
        }}

        function plusSlides(n) {{
            clearInterval(timer);
            showSlides(slideIndex += n);
            iniciarAutoSlide();
        }}

        function currentSlide(n) {{
            clearInterval(timer);
            showSlides(slideIndex = n);
            iniciarAutoSlide();
        }}

        function iniciarAutoSlide() {{
            timer = setInterval(function() {{
                slideIndex++;
                showSlides(slideIndex);
            }}, 4000);
        }}

        iniciarAutoSlide();
        </script>
        """
        import streamlit.components.v1 as components
        components.html(carrossel_codigo, height=480)
    else:
        st.info("💡 Coloque imagens na pasta `assets/` do projeto no GitHub para exibi-las no show de fotos.")
