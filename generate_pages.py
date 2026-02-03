import pandas as pd
import urllib.parse
import os
import re
import shutil

# 1. SETUP: Define the HTML Template
html_template = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Dora Tarjuma Quran 2026 - {{VENUE_NAME}}</title>
    
    <link href="https://fonts.googleapis.com/css2?family=Gulzar:wght@400;700&family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />

    <style>
        :root {
            --primary: #0F5132;
            --primary-dark: #072e1d;
            --accent: #108c00;
            --bg-light: #F3F4F6;
            --white: #ffffff;
            --text-dark: #1F2937;
            --text-gray: #6B7280;
            --whatsapp: #25D366;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; -webkit-tap-highlight-color: transparent; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: var(--bg-light); color: var(--text-dark); line-height: 1.6; padding-bottom: 5rem; overflow-x: hidden; }
        .urdu { font-family: 'Gulzar', serif; direction: rtl; line-height: 2.2; }

        .nav-bar { background: var(--white); padding: 0.8rem 1.2rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 100; }
        .nav-logo { height: 45px; width: auto; object-fit: contain; }
        .nav-whatsapp { background-color: var(--whatsapp); color: white; text-decoration: none; padding: 8px 16px; border-radius: 50px; font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 6px; transition: transform 0.2s; }
        .nav-whatsapp:active { transform: scale(0.95); }

        .hero-wrapper { background: linear-gradient(135deg, var(--primary), var(--primary-dark)); color: var(--white); position: relative; padding: 2rem 1.5rem 8rem 1.5rem; text-align: center; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px; }
        .sub-title { font-size: 1rem; opacity: 0.95; margin-bottom: 1rem; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; }
        .badge-container { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; margin-top: 1rem; }
        .badge { background: rgba(255,255,255,0.15); backdrop-filter: blur(5px); padding: 6px 14px; border-radius: 50px; font-size: 0.85rem; border: 1px solid rgba(255,255,255,0.2); display: flex; align-items: center; gap: 6px; }

        .video-wrapper { position: relative; z-index: 10; max-width: 350px; margin: -6rem auto 2rem auto; padding: 0 1rem; }
        .video-card { background: #000; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 40px rgba(0,0,0,0.4); border: 4px solid var(--white); aspect-ratio: 9/16; position: relative; }

        .form-wrapper { padding: 0 1rem; position: relative; z-index: 10; }
        .form-card { background: var(--white); border-radius: 24px; box-shadow: 0 10px 40px -10px rgba(0,0,0,0.1); padding: 2rem; max-width: 500px; margin: 0 auto; border-top: 6px solid var(--accent); }
        .progress-indicator { display: flex; justify-content: center; margin-bottom: 1.5rem; gap: 6px; }
        .dot { height: 6px; width: 6px; background: #e5e7eb; border-radius: 50%; transition: all 0.3s ease; }
        .dot.active { background: var(--primary); width: 24px; border-radius: 10px; }
        .step-content { display: none; animation: fadeIn 0.4s ease; }
        .step-content.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .question { font-size: 1.2rem; font-weight: 800; color: var(--primary); margin-bottom: 0.5rem; text-align: center; line-height: 1.3; }
        .question-sub { color: var(--text-gray); font-size: 1rem; margin-bottom: 1.5rem; text-align: center; }

        .btn-option { width: 100%; padding: 1rem; margin-bottom: 0.8rem; border: 2px solid #e5e7eb; background: var(--white); border-radius: 14px; font-size: 1rem; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: all 0.2s; color: var(--text-dark); }
        .btn-option:hover, .btn-option.selected { border-color: var(--primary); background: #ecfdf5; color: var(--primary-dark); transform: translateY(-2px); }
        .btn-primary { width: 100%; padding: 1.2rem; background: var(--primary); color: white; border: none; border-radius: 14px; font-size: 1.1rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(6, 78, 59, 0.3); margin-top: 1rem; transition: transform 0.1s; }
        .btn-primary:active { transform: scale(0.98); }
        .btn-back { background: transparent; color: var(--text-gray); border: none; font-weight: 600; margin-top: 12px; cursor: pointer; width: 100%; font-size: 0.9rem; }
        .input-group { margin-bottom: 1rem; text-align: left; }
        .input-group label { display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 6px; color: var(--text-dark); text-transform: uppercase; letter-spacing: 0.5px; }
        .input-group input { width: 100%; padding: 14px; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 1rem; transition: 0.2s; }
        .input-group input:focus { outline: none; border-color: var(--primary); background: #fff; }

        .info-section { max-width: 600px; margin: 3rem auto 0 auto; padding: 0 1rem; }
        .venue-box { background: var(--white); border-radius: 20px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); text-align: center; margin-bottom: 1.5rem; border: 1px solid #e5e7eb; }
        .venue-header { background: var(--primary); color: white; padding: 0.8rem; font-weight: 700; font-size: 0.9rem; letter-spacing: 1px; }
        .venue-body { padding: 1.5rem; }
        .venue-name { font-size: 1.5rem; font-weight: 800; color: var(--text-dark); margin-bottom: 5px; }
        .map-container { border-radius: 12px; overflow: hidden; height: 200px; position: relative; border: 1px solid #e5e7eb; margin-bottom: 15px; }
        .btn-map { display: flex; justify-content: center; align-items: center; gap: 10px; width: 100%; background: var(--primary); color: white; text-decoration: none; font-weight: 700; padding: 14px; border-radius: 12px; box-shadow: 0 4px 12px rgba(15, 81, 50, 0.2); transition: transform 0.2s; }
        .btn-map:hover { transform: translateY(-2px); background: var(--primary-dark); }
        .btn-map:active { transform: scale(0.98); }

        .features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.8rem; margin-bottom: 2rem; }
        .feature-box { background: var(--white); padding: 1rem 0.5rem; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.03); border: 1px solid #f0f0f0; }
        .feature-icon { font-size: 1.2rem; color: var(--accent); margin-bottom: 0.5rem; }
        .feature-text { font-size: 0.75rem; font-weight: 700; color: var(--primary); line-height: 1.2; }

        .success-box { text-align: center; padding: 2rem 0; }
        .success-icon { font-size: 3.5rem; color: var(--primary); margin-bottom: 1rem; }
        footer { text-align: center; margin-top: 3rem; color: var(--text-gray); font-size: 0.8rem; opacity: 0.7; }
    </style>
</head>
<body>

    <nav class="nav-bar">
        <img src="logo.svg" alt="Tanzeem" class="nav-logo" />
        <a href="https://wa.me/{{WA_PHONE}}?text=Assalamualaikum,%20I%20need%20more%20information%20about%20Dora%20Tarjuma%20Quran%20at%20{{VENUE_NAME}}" class="nav-whatsapp" target="_blank">
            <i class="fab fa-whatsapp" style="font-size: 1.1rem;"></i> <span>Contact</span>
        </a>
    </nav>

    <div class="hero-wrapper">
        <p class="sub-title">Tarawih with Brief Quranic Explanation</p>
        <div class="badge-container">
            <div class="badge"><i class="fas fa-moon"></i> From 1st Ramadan</div>
            <div class="badge"><i class="fas fa-clock"></i> 08:00 PM Every Night</div>
            <div class="badge"><i class="fas fa-users"></i> For Families</div>
        </div>
    </div>

    <div class="video-wrapper">
        <div class="video-card" style="position: relative; overflow: hidden;">
            <video id="promoVideo" autoplay muted playsinline style="width: 100%; height: 100%; object-fit: cover;">
                <source src="promo.mp4" type="video/mp4">
            </video>
            <div id="soundBtn" onclick="enableSound()" style="position: absolute; bottom: 20px; right: 20px; background: rgba(0,0,0,0.6); color: white; padding: 8px 16px; border-radius: 50px; font-size: 0.9rem; font-weight: 700; cursor: pointer; display: flex; align-items: center; gap: 8px; backdrop-filter: blur(4px); border: 1px solid rgba(255,255,255,0.3); z-index: 20;">
                <i class="fas fa-volume-mute" id="soundIcon"></i> <span id="soundText">Tap for Sound</span>
            </div>
        </div>
    </div>

    <script>
        function enableSound() {
            var video = document.getElementById("promoVideo");
            var btn = document.getElementById("soundBtn");
            var icon = document.getElementById("soundIcon");
            var text = document.getElementById("soundText");
            if (video.muted) {
                video.muted = false; video.currentTime = 0; video.play();
                icon.classList.remove("fa-volume-mute"); icon.classList.add("fa-volume-up");
                text.innerText = "Sound On"; btn.style.background = "rgba(15, 81, 50, 0.8)";
                setTimeout(() => { btn.style.opacity = '0'; transition = 'opacity 1s'; }, 3000);
            } else {
                video.muted = true; icon.classList.remove("fa-volume-up"); icon.classList.add("fa-volume-mute");
                text.innerText = "Tap for Sound"; btn.style.background = "rgba(0,0,0,0.6)";
            }
        }
        document.getElementById('promoVideo').addEventListener('ended', function() {
            var formSection = document.getElementById('registration-form');
            if (formSection) formSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
    </script>

    <div class="form-wrapper" id="registration-form">
        <div class="form-card">
            <form id="main-form">
                
                <input type="hidden" id="input_location" value="{{VENUE_NAME}}" />

                <div class="progress-indicator">
                    <div class="dot active" id="dot-1"></div><div class="dot" id="dot-2"></div><div class="dot" id="dot-3"></div>
                </div>

                <div class="step-content active" data-step="1">
                    <div class="question">Have you read the entire Quran with translation?</div>
                    <p class="question-sub urdu">کیا آپ نے کبھی پورا قرآن ترجمہ کے ساتھ پڑھا ہے؟</p>
                    <button type="button" class="btn-option" onclick="selectOption(1, 'Yes', this)"><i class="fas fa-check-circle" style="color:var(--primary)"></i> Yes (جی ہاں)</button>
                    <button type="button" class="btn-option" onclick="selectOption(1, 'No', this)"><i class="fas fa-times-circle" style="color:var(--text-gray)"></i> No (نہیں)</button>
                    <input type="hidden" id="input_read" />
                </div>
                <div class="step-content" data-step="2">
                    <div class="question">Do you want to understand the Quran this Ramadan?</div>
                    <p class="question-sub urdu">کیا آپ اس رمضان قرآن کو سمجھنا چاہتے ہیں؟</p>
                    <button type="button" class="btn-option" onclick="selectOption(2, 'Yes', this)">Yes, I want to Join</button>
                    <button type="button" class="btn-option" onclick="selectOption(2, 'Maybe', this)">Maybe later</button>
                    <input type="hidden" id="input_want" />
                    <button type="button" class="btn-back" onclick="prevStep(2)">Go Back</button>
                </div>
                <div class="step-content" data-step="3">
                    <div class="question">Final Step</div>
                    <p class="question-sub">Registration is Free</p>
                    <div class="input-group"><label>Full Name (نام)</label><input type="text" id="name" placeholder="Enter your name" required /></div>
                    <div class="input-group"><label>WhatsApp Number (موبائل)</label><input type="tel" id="mobile" placeholder="0300-XXXXXXX" required /></div>
                    <div class="input-group" style="display:flex; gap:10px;">
                        <div style="flex:1"><label>Age</label><input type="number" id="age" placeholder="25" /></div>
                        <div style="flex:2"><label>Profession</label><input type="text" id="profession" placeholder="Student, Job..." /></div>
                    </div>
                    <button type="button" class="btn-primary" onclick="submitForm()">COMPLETE REGISTRATION</button>
                    <button type="button" class="btn-back" onclick="prevStep(3)">Go Back</button>
                </div>
                <div class="step-content" id="success-step">
                    <div class="success-box">
                        <i class="fas fa-check-circle success-icon"></i>
                        <h2 style="color:var(--primary); margin-bottom:10px; font-weight:800;">JazakAllah Khair!</h2>
                        <p style="color:var(--text-gray); margin-bottom: 20px;">Your registration is confirmed.</p>
                        <div style="background:#f0fdf4; padding:15px; border-radius:12px; font-size:0.9rem; color:var(--primary-dark);">
                            For updates, save our number: <br><strong>{{PHONE}}</strong>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <div class="info-section">
        <div class="venue-box">
            <div class="venue-header">EVENT VENUE</div>
            <div class="venue-body">
                <div class="venue-name urdu" style="font-family: 'Noto Nastaliq Urdu', serif;">{{VENUE_NAME}}</div>
                <p class="urdu" style="color:var(--text-gray); margin-bottom:1.5rem; text-align: center;">{{ADDRESS}}</p>
                
                <div class="map-container">
                    <iframe src="{{EMBED_URL}}" width="100%" height="100%" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
                </div>

                <a href="{{MAP_LINK}}" target="_blank" class="btn-map">
                    <i class="fas fa-location-arrow"></i> GET DIRECTIONS
                </a>

            </div>
            
        </div>

        <a href="https://nearby.doraquran.pk" target="_blank" class="btn-map" style="margin-block: 20px">
            <i class="fas fa-location-arrow"></i> NEARBY DORA LOCATIONS APP
        </a>

        <div class="features-grid">
            <div class="feature-box"><div class="feature-icon"><i class="fas fa-female"></i></div><div class="feature-text">Ladies Arrangement</div></div>
            <div class="feature-box"><div class="feature-icon"><i class="fas fa-child"></i></div><div class="feature-text">Kids Activities</div></div>
            <div class="feature-box"><div class="feature-icon"><i class="fas fa-coffee"></i></div><div class="feature-text">Refreshments Served</div></div>
        </div>
    </div>

    <footer><p>© 2026 Tanzeem-e-Islami. All rights reserved.</p></footer>

    <script>
        // ──────────────────────────────────────────────
        // UI & Helper Functions (Standard Script)
        // ──────────────────────────────────────────────

        // Normalizes Pakistani numbers to 92XXXXXXXXXX
        window.formatPhone = function(raw) {
            let num = raw.replace(/[\s\-\(\)]/g, ""); 
            if (num.startsWith("+92")) num = num.slice(3);
            else if (num.startsWith("92") && num.length === 12) num = num.slice(2);
            else if (num.startsWith("0")) num = num.slice(1);
            return "92" + num; 
        };

        window.updateDots = function(step) { 
            document.querySelectorAll('.dot').forEach((d, i) => { 
                d.classList.remove('active'); 
                if (i + 1 === step) d.classList.add('active'); 
            }); 
        };

        window.selectOption = function(step, value, btn) {
            if (step === 1) document.getElementById('input_read').value = value;
            if (step === 2) document.getElementById('input_want').value = value;
            const buttons = btn.parentElement.querySelectorAll('.btn-option');
            buttons.forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            setTimeout(() => window.nextStep(step), 250);
        };

        window.nextStep = function(current) {
            document.querySelector(`.step-content[data-step="${current}"]`).classList.remove('active');
            const next = current + 1;
            const nextDiv = document.querySelector(`.step-content[data-step="${next}"]`);
            if (nextDiv) { nextDiv.classList.add('active'); window.updateDots(next); }
        };

        window.prevStep = function(current) {
            document.querySelector(`.step-content[data-step="${current}"]`).classList.remove('active');
            const prev = current - 1;
            document.querySelector(`.step-content[data-step="${prev}"]`).classList.add('active');
            window.updateDots(prev);
        };
    </script>

    <script type="module">
        import { neon } from "https://esm.sh/@neondatabase/serverless";

        const neon_db_url = "postgresql://neondb_owner:npg_j7SFZqzR5the@ep-empty-rice-a18ykd4a-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require";
        const sql = neon(neon_db_url);

        const ADMIN_PHONE = "{{WA_PHONE}}";
        const WA_PHONE = "{{WA_PHONE}}";

        const N8N_WEBHOOK_URL = "https://n8n.premierchoiceint.online/webhook/registration-trigger"
        const GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzXNQV7EreIbUiIMxuJQrDri_2BTehFLlauhpFGcVefP0I2Vnf8PyJYr5VdsXaztXlx/exec";

        window.submitForm = async function() {
            const name = document.getElementById('name').value.trim();
            const mobile = document.getElementById('mobile').value.trim();
            if (!name || !mobile) { alert("Please fill in your Name and WhatsApp Number."); return; }
            
            const btn = document.querySelector('.btn-primary');
            const originalText = btn.innerText;
            btn.innerText = "Processing...";
            btn.disabled = true;

            const timestamp = new Date().toISOString();
            const location = document.getElementById('input_location').value;
            const read = document.getElementById('input_read').value;
            const want = document.getElementById('input_want').value;
            const age = document.getElementById('age').value || '';
            const profession = document.getElementById('profession').value || '';

            // formatPhone is now in the global scope from the script above
            const formattedMobile = window.formatPhone(mobile);

            try {
                // Ensure the table exists (idempotent)
                await sql`CREATE TABLE IF NOT EXISTS "{{TABLE_NAME}}" (
                    id SERIAL PRIMARY KEY,
                    timestamp TEXT,
                    location TEXT,
                    read TEXT,
                    want TEXT,
                    name TEXT,
                    mobile TEXT,
                    age TEXT,
                    profession TEXT
                )`;



                

                // Insert the new registration
                await sql`INSERT INTO "{{TABLE_NAME}}" (timestamp, location, read, want, name, mobile, age, profession)
                    VALUES (${timestamp}, ${location}, ${read}, ${want}, ${name}, ${formattedMobile}, ${age}, ${profession})`;

                // ── 3. Fire n8n webhook (non-blocking) ──
                fetch(N8N_WEBHOOK_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        user_name:   name,
                        user_phone:  formattedMobile,       // 92XXXXXXXXXX
                        admin_phone: ADMIN_PHONE,           // dynamic 
                        age:         age,
                        profession:  profession,
                        venue:       location,
                        registered_at: timestamp
                    })
                }).catch(err => console.warn("n8n webhook call failed (non-critical):", err));

                // ── 4. Save to Google Sheet (Parallel) ──
                // Using text/plain to avoid CORS preflight (403) issues
                fetch(GOOGLE_SCRIPT_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                    body: JSON.stringify({
                        timestamp: timestamp,
                        location: location,
                        sheetName: location,
                        read: read,
                        want: want,
                        name: name, 
                        mobile: formattedMobile,
                        age: age,
                        profession: profession
                    })
                }).then(res => res.json())
                  .then(data => console.log("Google Sheet response:", data))
                  .catch(err => console.warn("Google Sheet call failed:", err));

                // Show success message
                document.querySelector(`.step-content[data-step="3"]`).classList.remove('active');
                document.getElementById('success-step').classList.add('active');
                document.querySelector('.progress-indicator').style.display = 'none';

            } catch (e) {
                console.error("Submission error:", e);
                alert("Submission failed. Please check your internet connection and try again.");
                btn.innerText = originalText;
                btn.disabled = false;
            }
        };
    </script>
</body>
</html>
"""

# 2. CONFIGURATION: CSV File Name
csv_file = 'DTQ 26 - Locations - Punjab Shumali.csv'

# 3. GENERATION LOOP
try:
    # Use pandas to read the CSV. 
    # Standard CSVs (like the one you uploaded) usually have the header on the first row (index 0).
    df = pd.read_csv(csv_file) 
    
    # Create an output directory
    output_dir = os.path.join("new_pages", "")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Found {len(df)} locations. Generating files...")

    for index, row in df.iterrows():
        # A. EXTRACT DATA based on your new CSV columns:
        # 'Location Name', 'Venue', 'Location Link', 'Contact Number'
        
        # 1. Filename (from 'Location Name', e.g., 'Abpara')
        loc_id = str(row['Location Name']).strip()
        
        # 2. Address (from 'Venue', e.g., 'Regalia Hotel, Street 48...')
        address = str(row['Venue']).strip()
        
        # 3. Venue Name (The building name, extracted from the first part of the address)
        #    Example: "Regalia Hotel, Street 48..." -> "Regalia Hotel"
        venue_name = address.split(',')[0].strip()
        
        # 4. Map Link (from 'Location Link')
        map_link = str(row['Location Link']).strip()
        
        # 5. Phone (from 'Contact Number')
        raw_phone = str(row['Contact Number'])
        if raw_phone.endswith('.0'):
            raw_phone = raw_phone[:-2]
        phone = raw_phone
        
        # B. PREPARE VARIABLES
        # Create a Google Maps Embed URL by searching the full address
        encoded_address = urllib.parse.quote(f"{address} Islamabad")
        embed_url = f"https://maps.google.com/maps?q={encoded_address}&t=&z=14&ie=UTF8&iwloc=&output=embed"
        
        # Format WhatsApp Phone (assuming Pakistan 92 code)
        clean_phone_for_wa = phone.replace('-', '').replace(' ', '').replace('+', '')
        if len(clean_phone_for_wa) >= 10 and not clean_phone_for_wa.startswith('92'):
             wa_phone = "92" + clean_phone_for_wa[-10:]
        else:
             wa_phone = clean_phone_for_wa

        # C. FILL TEMPLATE
        # Generate Table Name (e.g., registration-kashmir-plaza)
        sanitized_venue = re.sub(r'[^a-zA-Z0-9]+', '-', venue_name.lower()).strip('-')
        table_name = f"registration-{sanitized_venue}"

        filled_html = html_template.replace("{{VENUE_NAME}}", venue_name)
        filled_html = filled_html.replace("{{TABLE_NAME}}", table_name)
        filled_html = filled_html.replace("{{ADDRESS}}", address)
        filled_html = filled_html.replace("{{MAP_LINK}}", map_link)
        filled_html = filled_html.replace("{{EMBED_URL}}", embed_url)
        filled_html = filled_html.replace("{{PHONE}}", phone)
        filled_html = filled_html.replace("{{WA_PHONE}}", wa_phone)
        
        # D. SAVE FILE
        # D. SAVE FILE & ASSETS
        # Create a specific folder for this location (e.g. new_pages/Abpara)
        # Using loc_id as the folder name
        safe_folder_name = re.sub(r'[<>:"/\\|?*]', '', loc_id).strip()
        location_folder = os.path.join(output_dir, safe_folder_name)
        
        if not os.path.exists(location_folder):
            os.makedirs(location_folder)

        # 1. Save HTML
        filename = f"index.html"
        filepath = os.path.join(location_folder, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(filled_html)

        # 2. Copy Assets (logo.svg, promo.mp4)
        # They are located beside this script.
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        src_logo = os.path.join(current_dir, "logo.svg")
        if os.path.exists(src_logo):
            shutil.copy(src_logo, location_folder)
            
        src_promo = os.path.join(current_dir, "promo.mp4")
        if os.path.exists(src_promo):
            shutil.copy(src_promo, location_folder)

        print(f"✅ Generated: {location_folder} (with html, logo, video)")

    print(f"\n🎉 Success! All files are in the '{output_dir}' folder.")

except FileNotFoundError:
    print(f"❌ Error: Could not find '{csv_file}'. Make sure it is in the same folder.")
except KeyError as e:
    print(f"❌ Error: Column not found in CSV: {e}. Check your CSV headers.")
except Exception as e:
    print(f"❌ An error occurred: {e}")