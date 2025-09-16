from .config import WARD_VISION_RADIUS

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dota 2 Ward Map - Match {match_id}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #0e1117; color: #fafafa;
            display: flex; flex-direction: column; align-items: center; padding: 2rem;
        }}
        h1, h2 {{ color: #fafafa; text-align: center; }}
        h2 {{ font-size: 1.2rem; font-weight: normal; margin-top: -1rem; margin-bottom: 2rem;}}
        #map-container {{
            position: relative;
            width: 512px; height: 512px;
            border: 1px solid #444;
        }}
        #map-image {{
            width: 100%; height: 100%; display: block;
        }}
        .ward {{
            position: absolute;
            width: {vision_diameter_px}px;
            height: {vision_diameter_px}px;
            background-color: rgba(255, 215, 0, 0.15);
            border: 1px solid #FFD700;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            box-sizing: border-box;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: opacity 0.3s ease;
            opacity: 0; /* Hidden by default */
            pointer-events: none; /* Not interactive by default */
        }}
        .ward::before {{
            content: '';
            width: 8px;
            height: 8px;
            background-color: #FFD700;
            border: 1px solid black;
            border-radius: 50%;
            position: absolute;
        }}
        .ward .tooltip {{
            visibility: hidden;
            min-width: 80px;
            background-color: rgba(0, 0, 0, 0.8);
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 8px;
            position: absolute;
            z-index: 1;
            bottom: 110%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 12px;
            white-space: nowrap;
        }}
        .ward:hover .tooltip {{
            visibility: visible;
            opacity: 1;
        }}
        #controls {{
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #262730;
            border-radius: 8px;
            width: 512px;
            box-sizing: border-box;
        }}
        #time-slider {{
            width: 100%;
            cursor: pointer;
        }}
        label {{
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <h1>Ward Visualization for Match {match_id}</h1>
    <h2>{team_name} (Radiant Only)</h2>
    <div id="map-container">
        <img id="map-image" src="../dota2_map2" alt="Dota 2 Map">
    </div>
    <div id="controls">
        <label for="time-slider">Show wards up to minute: <span id="slider-value">10</span></label>
        <input type="range" id="time-slider" min="0" max="{max_minutes}" value="10" step="1">
    </div>

    <script>
        const wardData = {ward_data_json};

        function format_mmss(t_sec) {{
            if (t_sec < 0) t_sec = 0;
            const m = Math.floor(t_sec / 60);
            const s = Math.round(t_sec % 60);
            return `${{m.toString().padStart(2, '0')}}:${{s.toString().padStart(2, '0')}}`;
        }}

        function placeWards() {{
            const container = document.getElementById('map-container');
            container.querySelectorAll('.ward').forEach(el => el.remove());

            wardData.forEach(ward => {{
                const wardDiv = document.createElement('div');
                wardDiv.className = 'ward';
                wardDiv.style.left = (ward.x / 128) * 100 + '%';
                wardDiv.style.top = (ward.y / 128) * 100 + '%';
                wardDiv.dataset.placementTime = ward.time_seconds;
                wardDiv.dataset.expirationTime = ward.expiration_time;

                const tooltip = document.createElement('span');
                tooltip.className = 'tooltip';
                tooltip.textContent = format_mmss(ward.time_seconds);
                wardDiv.appendChild(tooltip);
                
                container.appendChild(wardDiv);
            }});
        }}

        function updateWardVisibility(minuteLimit) {{
            const wards = document.querySelectorAll('.ward');
            const timeLimit = minuteLimit * 60;
            wards.forEach(ward => {{
                const placementTime = parseInt(ward.dataset.placementTime, 10);
                const expirationTime = parseInt(ward.dataset.expirationTime, 10);
                
                // Animate ward visibility based on its lifetime
                if (placementTime <= timeLimit && timeLimit < expirationTime) {{
                    ward.style.opacity = '1';
                    ward.style.pointerEvents = 'auto';
                }} else {{
                    ward.style.opacity = '0';
                    ward.style.pointerEvents = 'none';
                }}
            }});
        }}

        window.onload = () => {{
            placeWards();
            
            const slider = document.getElementById('time-slider');
            const sliderValueSpan = document.getElementById('slider-value');

            slider.value = Math.min(10, slider.max);
            sliderValueSpan.textContent = slider.value;
            updateWardVisibility(slider.value);

            slider.addEventListener('input', (event) => {{
                const minute = event.target.value;
                sliderValueSpan.textContent = minute;
                updateWardVisibility(minute);
            }});
        }};
    </script>
</body>
</html>
"""

def generate_html(match_id, team_name, wards_df):
    """
    Generates the HTML report from the template and data.
    """
    wards_json = wards_df.to_json(orient="records")
    
    # Calculate max time for the slider based on ward expiration
    max_time_seconds = wards_df["expiration_time"].max() if not wards_df.empty else 600
    max_minutes = int(max_time_seconds // 60) + 1
    
    # Calculate vision circle diameter in pixels for a 512px map
    vision_diameter_px = (WARD_VISION_RADIUS / 128) * 512 * 2

    # Populate the HTML template
    output_html = HTML_TEMPLATE.format(
        match_id=match_id,
        team_name=team_name,
        ward_data_json=wards_json,
        max_minutes=max_minutes,
        vision_diameter_px=vision_diameter_px
    )
    return output_html
