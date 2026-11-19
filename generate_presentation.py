import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_presentation(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # COLOR PALETTE (Dark Cinema Futuristic Aesthetic)
    BG_DARK = RGBColor(11, 15, 25)          # #0B0F19 - Deep Void
    CARD_BG = RGBColor(19, 27, 46)          # #131B2E - Dark Slate Blue
    CARD_BG_ALT = RGBColor(24, 34, 56)      # #182238 - Lighter Card Surface
    CARD_BORDER = RGBColor(38, 53, 84)      # #263554 - Subtle Boundary
    CARD_BORDER_ACCENT = RGBColor(99, 102, 241) # #6366F1 - Indigo Accent

    ACCENT_PURPLE = RGBColor(139, 92, 246)  # #8B5CF6 - Electric Purple
    ACCENT_VIOLET = RGBColor(168, 85, 247)  # #A855F7 - Neon Violet
    ACCENT_CYAN = RGBColor(6, 182, 212)     # #06B6D4 - Cyber Cyan
    ACCENT_BLUE = RGBColor(56, 189, 248)    # #38BDF8 - Bright Blue
    ACCENT_CORAL = RGBColor(244, 63, 94)    # #F43F5E - Crimson Rose
    ACCENT_AMBER = RGBColor(245, 158, 11)   # #F59E0B - Warm Amber
    ACCENT_GREEN = RGBColor(16, 185, 129)   # #10B981 - Emerald Green

    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_BODY = RGBColor(226, 232, 240)     # #E2E8F0 - Soft Off-White
    TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8 - Slate Muted
    TEXT_MUTED_LIGHT = RGBColor(180, 195, 215)

    FONT_HEADING = "Segoe UI"
    FONT_BODY = "Segoe UI"
    FONT_CODE = "Consolas"

    def apply_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, badge_text, title_text, subtitle_text):
        # Category Badge
        badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.40), Inches(3.2), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = RGBColor(26, 36, 60)
        badge.line.color.rgb = ACCENT_PURPLE
        badge.line.width = Pt(1)
        tf_b = badge.text_frame
        tf_b.word_wrap = False
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_b = tf_b.paragraphs[0]
        p_b.text = badge_text.upper()
        p_b.font.name = FONT_HEADING
        p_b.font.size = Pt(8.5)
        p_b.font.bold = True
        p_b.font.color.rgb = ACCENT_BLUE
        p_b.alignment = PP_ALIGN.CENTER

        # Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.76), Inches(11.733), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        # Subtitle
        tb_sub = slide.shapes.add_textbox(Inches(0.8), Inches(1.33), Inches(11.733), Inches(0.35))
        tf_sub = tb_sub.text_frame
        tf_sub.word_wrap = True
        tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = TEXT_MUTED

    def add_footer(slide, current_slide, total_slides=14):
        # Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Pt(1))
        line.fill.solid()
        line.fill.fore_color.rgb = RGBColor(26, 36, 58)
        line.line.fill.background()

        # Left label
        tb_l = slide.shapes.add_textbox(Inches(0.8), Inches(7.12), Inches(6.5), Inches(0.3))
        tf_l = tb_l.text_frame
        tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
        p_l = tf_l.paragraphs[0]
        p_l.text = "CINEVERSE · Engineering Project Review 1 (Project Title Identification)"
        p_l.font.name = FONT_BODY
        p_l.font.size = Pt(9)
        p_l.font.color.rgb = TEXT_MUTED

        # Right label
        tb_r = slide.shapes.add_textbox(Inches(10.533), Inches(7.12), Inches(2.0), Inches(0.3))
        tf_r = tb_r.text_frame
        tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
        p_r = tf_r.paragraphs[0]
        p_r.text = f"Slide {current_slide:02d} / {total_slides:02d}"
        p_r.alignment = PP_ALIGN.RIGHT
        p_r.font.name = FONT_BODY
        p_r.font.size = Pt(9)
        p_r.font.bold = True
        p_r.font.color.rgb = ACCENT_CYAN

    def create_card(slide, left, top, width, height, bg=CARD_BG, border=CARD_BORDER, border_width=Pt(1.2)):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = border
        card.line.width = border_width
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    apply_background(slide1)

    # Top Review Badge
    badge1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.1), Inches(0.65), Inches(5.133), Inches(0.38))
    badge1.fill.solid()
    badge1.fill.fore_color.rgb = RGBColor(28, 38, 64)
    badge1.line.color.rgb = ACCENT_PURPLE
    badge1.line.width = Pt(1.5)
    tf_b1 = badge1.text_frame
    tf_b1.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b1 = tf_b1.paragraphs[0]
    p_b1.text = "ACADEMIC ENGINEERING PROJECT · REVIEW 1"
    p_b1.font.name = FONT_HEADING
    p_b1.font.size = Pt(9.5)
    p_b1.font.bold = True
    p_b1.font.color.rgb = ACCENT_BLUE
    p_b1.alignment = PP_ALIGN.CENTER

    # Title: CINEVERSE
    tb_title = slide1.shapes.add_textbox(Inches(1.0), Inches(1.15), Inches(11.333), Inches(1.0))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "CINEVERSE"
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(48)
    p_t.font.bold = True
    p_t.font.color.rgb = TEXT_WHITE
    p_t.alignment = PP_ALIGN.CENTER

    # Subtitle
    tb_sub = slide1.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(11.333), Inches(0.55))
    tf_s = tb_sub.text_frame
    tf_s.word_wrap = True
    p_s = tf_s.paragraphs[0]
    p_s.text = "Virtual Cinema Experience & Smart Movie Ticket Booking Platform"
    p_s.font.name = FONT_HEADING
    p_s.font.size = Pt(18)
    p_s.font.bold = True
    p_s.font.color.rgb = ACCENT_CYAN
    p_s.alignment = PP_ALIGN.CENTER

    # Tagline Chip
    tag_card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.3), Inches(2.70), Inches(4.733), Inches(0.42))
    tag_card.fill.solid()
    tag_card.fill.fore_color.rgb = RGBColor(19, 27, 46)
    tag_card.line.color.rgb = ACCENT_AMBER
    tag_card.line.width = Pt(1.2)
    tf_tag = tag_card.text_frame
    tf_tag.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = 'Tagline: “Know Your View Before You Book.”'
    p_tag.font.name = FONT_BODY
    p_tag.font.size = Pt(11.5)
    p_tag.font.bold = True
    p_tag.font.color.rgb = ACCENT_AMBER
    p_tag.alignment = PP_ALIGN.CENTER

    # Card 1: Team Members
    card_team = create_card(slide1, 0.9, 3.4, 5.6, 3.3, bg=CARD_BG, border=CARD_BORDER_ACCENT)
    tb_team = slide1.shapes.add_textbox(Inches(1.15), Inches(3.55), Inches(5.1), Inches(3.0))
    tf_team = tb_team.text_frame
    tf_team.word_wrap = True
    
    p = tf_team.paragraphs[0]
    p.text = "PROJECT TEAM MEMBERS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(10)

    members = [
        ("1. Abhinay Sai", "2510030103", "System Architecture & 3D Simulation"),
        ("2. Ramesh", "2510030303", "Frontend React & UI/UX Design"),
        ("3. Poli Naidu", "2510030160", "Java 17 Spring Boot & PostgreSQL"),
        ("4. Chandu", "2510030083", "Concurrency, Redis & QA Testing")
    ]
    for name, roll, role in members:
        p_m = tf_team.add_paragraph()
        p_m.text = f"•  {name}  —  "
        p_m.font.name = FONT_BODY
        p_m.font.size = Pt(10.5)
        p_m.font.bold = True
        p_m.font.color.rgb = TEXT_WHITE
        
        run_roll = p_m.add_run()
        run_roll.text = f"Roll: {roll}\n"
        run_roll.font.bold = True
        run_roll.font.color.rgb = ACCENT_CYAN
        
        run_role = p_m.add_run()
        run_role.text = f"    Role Focus: {role}"
        run_role.font.size = Pt(9)
        run_role.font.color.rgb = TEXT_MUTED
        p_m.space_after = Pt(6)

    # Card 2: Institutional Metadata & Placeholders
    card_inst = create_card(slide1, 6.8, 3.4, 5.6, 3.3, bg=CARD_BG, border=CARD_BORDER)
    tb_inst = slide1.shapes.add_textbox(Inches(7.05), Inches(3.55), Inches(5.1), Inches(3.0))
    tf_inst = tb_inst.text_frame
    tf_inst.word_wrap = True

    p = tf_inst.paragraphs[0]
    p.text = "ACADEMIC & INSTITUTIONAL METADATA"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(12)

    inst_items = [
        ("Department:", "Department of Computer Science & Engineering [Placeholder]"),
        ("College / Univ:", "College of Engineering & Technology [Placeholder]"),
        ("Faculty Guide:", "Prof. / Dr. [Faculty Guide Name Placeholder]"),
        ("Evaluation Review:", "Review 1 – Project Title Identification"),
        ("Academic Year:", "2026 – 2027"),
        ("Project Status:", "Title Approved · Architecture & Stack Formulated")
    ]
    for lbl, val in inst_items:
        p_i = tf_inst.add_paragraph()
        run_l = p_i.add_run()
        run_l.text = f"{lbl} "
        run_l.font.name = FONT_BODY
        run_l.font.size = Pt(10)
        run_l.font.bold = True
        run_l.font.color.rgb = TEXT_MUTED

        run_v = p_i.add_run()
        run_v.text = val
        run_v.font.name = FONT_BODY
        run_v.font.size = Pt(10)
        run_v.font.bold = True
        run_v.font.color.rgb = TEXT_WHITE
        p_i.space_after = Pt(5)

    add_footer(slide1, 1)

    # =========================================================================
    # SLIDE 2: INTRODUCTION
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    apply_background(slide2)
    add_header(slide2, "Background & Motivation", "Introduction: The Evolution of Movie Ticket Booking", "Bridging the critical spatial gap between 2D digital convenience and real physical theatre optics")

    intro_cols = [
        ("Digital Booking Era", ACCENT_BLUE, [
            ("Massive Adoption", "Cinema ticketing has largely migrated from physical box-office counters to high-traffic web and mobile booking applications."),
            ("Transaction Convenience", "Platforms allow moviegoers to browse shows, pick cinemas, and complete payments within seconds."),
            ("Shift in Expectations", "Audiences invest in premium exhibition formats (IMAX, 4DX, Dolby Atmos) and expect corresponding booking transparency.")
        ]),
        ("Traditional Limitations", ACCENT_CORAL, [
            ("2D Flat Grids", "Conventional platforms still rely on flat matrices of uniform circles, ignoring auditorium geometry."),
            ("Zero Depth Perception", "Consumers cannot perceive screen distance, elevation rake, or vertical line of sight."),
            ("Viewing Angle Risks", "Extreme side-row seats cause image keystone distortion and severe neck fatigue that remain invisible during checkout.")
        ]),
        ("The CINEVERSE Vision", ACCENT_PURPLE, [
            ("Virtual Cinema Experience", "CINEVERSE re-engineers seat selection by embedding an interactive WebGL-powered 3D virtual cinema environment."),
            ("Pre-Booking Viewpoint", "Allows moviegoers to inspect the exact eye-level perspective, sightline, and screen coverage prior to purchase."),
            ("Informed Transparency", "Eliminates post-booking seat regret, delivering peace of mind and transforming conventional ticketing.")
        ], CARD_BORDER_ACCENT)
    ]

    col_w = 3.65
    gap = 0.38
    start_x = 0.8
    card_y = 1.85
    card_h = 3.8

    for i, col in enumerate(intro_cols):
        border_col = col[3] if len(col) > 3 else CARD_BORDER
        card = create_card(slide2, start_x + i * (col_w + gap), card_y, col_w, card_h, bg=CARD_BG, border=border_col)
        tb = slide2.shapes.add_textbox(Inches(start_x + i * (col_w + gap) + 0.2), Inches(card_y + 0.2), Inches(col_w - 0.4), Inches(card_h - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = col[0]
        p.font.name = FONT_HEADING
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col[1]
        p.space_after = Pt(10)

        for heading, body in col[2]:
            p_b = tf.add_paragraph()
            r_h = p_b.add_run()
            r_h.text = f"•  {heading}: "
            r_h.font.bold = True
            r_h.font.size = Pt(9.5)
            r_h.font.color.rgb = TEXT_WHITE
            
            r_txt = p_b.add_run()
            r_txt.text = body
            r_txt.font.size = Pt(9)
            r_txt.font.color.rgb = TEXT_MUTED
            p_b.space_after = Pt(8)

    # Bottom Highlight Banner
    banner = create_card(slide2, 0.8, 5.85, 11.733, 1.0, bg=CARD_BG_ALT, border=ACCENT_AMBER)
    tb_ban = slide2.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.333), Inches(0.8))
    tf_ban = tb_ban.text_frame
    tf_ban.word_wrap = True
    p_ban = tf_ban.paragraphs[0]
    p_ban.text = "CORE PARADIGM SHIFT:"
    p_ban.font.name = FONT_HEADING
    p_ban.font.size = Pt(10)
    p_ban.font.bold = True
    p_ban.font.color.rgb = ACCENT_AMBER

    p_ban2 = tf_ban.add_paragraph()
    p_ban2.text = "“Traditional ticketing tells users WHERE they sit; CINEVERSE reveals WHAT THEY WILL ACTUALLY SEE. By marrying WebGL spatial computing with enterprise ticketing, we eliminate blind seat selection entirely.”"
    p_ban2.font.name = FONT_BODY
    p_ban2.font.size = Pt(10.5)
    p_ban2.font.color.rgb = TEXT_BODY
    p_ban2.font.italic = True

    add_footer(slide2, 2)

    # =========================================================================
    # SLIDE 3: ABSTRACT
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    apply_background(slide3)
    add_header(slide3, "Executive Summary", "Project Abstract", "Concise academic summary of the project's purpose, proposed solution, major features, and expected outcomes")

    # Left Column: Concise Academic Abstract Paragraph
    card_abs = create_card(slide3, 0.8, 1.85, 7.6, 5.0, bg=CARD_BG, border=CARD_BORDER)
    tb_abs = slide3.shapes.add_textbox(Inches(1.1), Inches(2.05), Inches(7.0), Inches(4.6))
    tf_abs = tb_abs.text_frame
    tf_abs.word_wrap = True

    p = tf_abs.paragraphs[0]
    p.text = "ACADEMIC ABSTRACT"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.space_after = Pt(10)

    abstract_text = (
        "In the contemporary movie exhibition industry, online movie ticketing platforms have established themselves as vital commercial portals. "
        "However, established commercial systems such as BookMyShow and District remain constrained by static, two-dimensional seat layouts. "
        "These abstracted grids fail to convey crucial spatial attributes—including screen elevation, field-of-view angle, screen-to-seat distance, "
        "and architectural occlusions—frequently leading to suboptimal seat selection, ocular fatigue, and consumer dissatisfaction.\n\n"
        "To address this critical gap, this project develops CINEVERSE, an advanced web-based movie ticket booking platform centered on an "
        "interactive virtual 3D cinema simulation. Utilizing client-side WebGL and Three.js coupled with a high-performance Java 17 and Spring Boot "
        "backend, CINEVERSE computes real-time, seat-specific eye-level camera projections within a 3D digital twin of the auditorium.\n\n"
        "The architecture incorporates PostgreSQL for ACID-compliant transactional persistence and Redis for temporary seat reservation leases, "
        "guaranteeing strict single-sale invariants under concurrent peak booking conditions. Major capabilities include an interactive 3D seat previewer, "
        "split-screen Seat Battle™ angle comparison, smart seat filtering, and automated e-ticketing. The expected outcome is a fully functional prototype "
        "that eliminates blind seat selection, elevates consumer purchasing confidence, and establishes an academic baseline for future VR and AI integrations."
    )
    p_body = tf_abs.add_paragraph()
    p_body.text = abstract_text
    p_body.font.name = FONT_BODY
    p_body.font.size = Pt(10.2)
    p_body.font.color.rgb = TEXT_BODY
    p_body.space_before = Pt(4)

    # Right Column: 3 Key Outcome & Foundation Cards
    right_x = 8.65
    right_w = 3.88
    metrics = [
        ("PROJECT PURPOSE", "Eliminate Blind Seating", "Solve visual perspective uncertainties that cause neck strain and poor viewing angles in multiplex auditoriums.", ACCENT_PURPLE),
        ("PROPOSED SOLUTION", "Virtual 3D Simulator", "Client-side WebGL (Three.js) camera projection rendering real-time eye-level sightlines from any seat.", ACCENT_CYAN),
        ("EXPECTED OUTCOME", "Full-Stack Web Prototype", "End-to-end booking application with interactive 3D preview, concurrency locks, and QR e-ticketing.", ACCENT_GREEN)
    ]

    for j, (title, subtitle, desc, acc_col) in enumerate(metrics):
        m_top = 1.85 + j * 1.7
        m_h = 1.55
        card_m = create_card(slide3, right_x, m_top, right_w, m_h, bg=CARD_BG, border=CARD_BORDER)
        tb_m = slide3.shapes.add_textbox(Inches(right_x + 0.2), Inches(m_top + 0.15), Inches(right_w - 0.4), Inches(m_h - 0.3))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True

        p1 = tf_m.paragraphs[0]
        p1.text = title
        p1.font.name = FONT_HEADING
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = acc_col

        p2 = tf_m.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.space_after = Pt(4)

        p3 = tf_m.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_BODY
        p3.font.size = Pt(9)
        p3.font.color.rgb = TEXT_MUTED

    add_footer(slide3, 3)

    # =========================================================================
    # SLIDE 4: EXISTING SYSTEM
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    apply_background(slide4)
    add_header(slide4, "Market Landscape", "Existing System Analysis", "Review of established movie booking platforms and their standard operational capabilities")

    # Top Overview Context Card
    card_top = create_card(slide4, 0.8, 1.85, 11.733, 1.05, bg=CARD_BG, border=CARD_BORDER)
    tb_top = slide4.shapes.add_textbox(Inches(1.0), Inches(1.95), Inches(11.333), Inches(0.85))
    tf_top = tb_top.text_frame
    tf_top.word_wrap = True
    p = tf_top.paragraphs[0]
    p.text = "PROMINENT EXISTING PLATFORMS EVALUATED:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    p_p = tf_top.add_paragraph()
    p_p.text = "• BookMyShow: The dominant aggregator across India   • District: Emerging live entertainment ticketing   • Theatre Websites: PVR-INOX, Cinepolis native portals"
    p_p.font.name = FONT_BODY
    p_p.font.size = Pt(10.5)
    p_p.font.bold = True
    p_p.font.color.rgb = TEXT_WHITE

    # 4 Grid Cards of Common Capabilities
    cards_4 = [
        ("1. Movie Discovery & Information", ACCENT_BLUE, [
            ("Catalogue Exploration", "Centralized browsing of current theatrical releases and upcoming films across multiple languages."),
            ("Media & Metadata", "Trailers, synopses, censor ratings, casting details, and certified runtime specifications."),
            ("User Sentiment & Ratings", "Crowdsourced review aggregations, star ratings, and community critiques.")
        ]),
        ("2. Showtime & Theatre Schedules", ACCENT_PURPLE, [
            ("Consolidated Schedules", "Multi-theatre schedules showing timing availability across metropolitan cities."),
            ("Format Classification", "Tagging of screening projection formats (Standard 2D, 3D, IMAX, 4DX, Dolby Atmos)."),
            ("Flexible Filtering", "Search filters by date, location radius, preferred language, and pricing tier.")
        ]),
        ("3. 2D Seat Maps & Selection", ACCENT_AMBER, [
            ("Grid Matrix Representation", "2D row-and-column layout indicating seat states (Available, Reserved, Wheelchair)."),
            ("Category Segmentation", "Color-coded brackets dividing seating into Silver, Gold, Platinum, and Recliner rows."),
            ("Multi-Seat Selection", "Enforces maximum ticket limits and contiguous seat reservation policies.")
        ]),
        ("4. Online Payments & Confirmation", ACCENT_GREEN, [
            ("Payment Gateway Integration", "Support for UPI, Net Banking, Credit/Debit cards, and digital wallet providers."),
            ("Instant Booking Confirmation", "Automated delivery of booking references via SMS, WhatsApp, and email."),
            ("Digital E-Tickets", "Generation of verifiable QR-code passes for contactless admission at theatre turnstiles.")
        ])
    ]

    card_w = 5.7
    card_h = 1.95
    coords = [
        (0.8, 3.05), (6.833, 3.05),
        (0.8, 5.15), (6.833, 5.15)
    ]

    for idx, (title, color, bullets) in enumerate(cards_4):
        cx, cy = coords[idx]
        c = create_card(slide4, cx, cy, card_w, card_h, bg=CARD_BG, border=CARD_BORDER)
        tb = slide4.shapes.add_textbox(Inches(cx + 0.2), Inches(cy + 0.15), Inches(card_w - 0.4), Inches(card_h - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(11.5)
        pt.font.bold = True
        pt.font.color.rgb = color
        pt.space_after = Pt(4)

        for b_title, b_desc in bullets:
            pb = tf.add_paragraph()
            rh = pb.add_run()
            rh.text = f"•  {b_title}: "
            rh.font.bold = True
            rh.font.size = Pt(8.8)
            rh.font.color.rgb = TEXT_WHITE
            
            rt = pb.add_run()
            rt.text = b_desc
            rt.font.size = Pt(8.5)
            rt.font.color.rgb = TEXT_MUTED
            pb.space_after = Pt(2)

    add_footer(slide4, 4)

    # =========================================================================
    # SLIDE 5: PROBLEMS IN EXISTING SYSTEMS
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    apply_background(slide5)
    add_header(slide5, "Critical Gap Identification", "Problems & Gaps in Existing Systems", "Objective engineering analysis of usability bottlenecks and physical perspective ambiguities")

    problems = [
        ("1. Limited Visualization of Actual Seat Perspectives", ACCENT_CORAL, [
            ("Flat Matrix Limitation", "2D layouts represent seats as identical abstract dots, completely hiding sightline angles."),
            ("No Real-World Context", "Users cannot see how the curved projection screen or speaker arrays appear from their chosen coordinates.")
        ]),
        ("2. Difficulty Understanding Screen Distance & Angles", ACCENT_CORAL, [
            ("Missing Elevation Rake", "Cannot distinguish between flat incline seating versus steep stadium-raked auditoriums."),
            ("Severe Off-Axis Distortions", "Edge seats cause significant horizontal keystone stretching and ocular fatigue, unknown at booking time.")
        ]),
        ("3. Uncertainty While Choosing Seats (Blind Booking)", ACCENT_AMBER, [
            ("Front-Row Neck Fatigue Risk", "Patrons frequently choose front rows unaware of excessive upward vertical viewing angles (>35°)."),
            ("Occlusion & Pillar Risks", "Physical obstructions such as safety railings, support pillars, or sound booths are not indicated on 2D maps.")
        ]),
        ("4. Difficulty Coordinating Group Bookings", ACCENT_AMBER, [
            ("Manual Coordination Friction", "Organizing group bookings requires taking screenshots of seat maps and sharing across chat groups."),
            ("Hold Expiration Drop-offs", "By the time consensus is reached, seats frequently time out or get snapped up by concurrent bookers.")
        ]),
        ("5. Limited Opportunity to Explore Theatre Virtually", ACCENT_PURPLE, [
            ("Zero Pre-Visit Exploration", "First-time visitors cannot inspect cinema ambiance, aisle proximity, or accessibility accommodations."),
            ("No Tier Comparison Tool", "Lacks any side-by-side visual comparison to assess whether a higher-priced tier provides better value.")
        ])
    ]

    p_w = 11.733
    p_h = 0.88
    p_gap = 0.14
    p_top_start = 1.85

    for idx, (title, color, points) in enumerate(problems):
        y = p_top_start + idx * (p_h + p_gap)
        c = create_card(slide5, 0.8, y, p_w, p_h, bg=CARD_BG, border=CARD_BORDER)

        # Left Accent Strip
        strip = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(y), Inches(0.12), Inches(p_h))
        strip.fill.solid()
        strip.fill.fore_color.rgb = color
        strip.line.fill.background()

        tb = slide5.shapes.add_textbox(Inches(1.05), Inches(y + 0.08), Inches(11.3), Inches(p_h - 0.16))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = title
        r1.font.name = FONT_HEADING
        r1.font.size = Pt(11)
        r1.font.bold = True
        r1.font.color.rgb = color
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = f"• {points[0][0]}: {points[0][1]}    • {points[1][0]}: {points[1][1]}"
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.8)
        p2.font.color.rgb = TEXT_BODY

    add_footer(slide5, 5)

    # =========================================================================
    # SLIDE 6: PROPOSED SYSTEM
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    apply_background(slide6)
    add_header(slide6, "Proposed Architecture", "Proposed System: CINEVERSE Smart Platform", "A smarter, immersive cinema ticketing solution powered by WebGL 3D spatial simulation")

    pillars = [
        ("1. Interactive Virtual 3D Auditorium", ACCENT_BLUE, [
            ("WebGL-Rendered Digital Twin", "Built on Three.js and React Three Fiber to render responsive 3D auditorium environments directly inside web browsers."),
            ("Architecturally Calibrated Geometry", "Accurately represents screen curvature radius, speaker placements, and stadium seating step elevations."),
            ("Zero Hardware / Plugin Barriers", "Runs smoothly on modern desktop and mobile browsers supporting standard WebGL 2.0.")
        ]),
        ("2. Seat-Specific Viewing Perspective", ACCENT_PURPLE, [
            ("Eye-Level Camera Transform", "Dynamically repositions the virtual camera to the exact (x, y, z) coordinates and tilt angle of any selected seat."),
            ("True Field-of-View (FOV) Simulation", "Simulates actual human binocular viewing cones, revealing exact screen coverage percentage and keystone distortions."),
            ("Obstruction & Distance Verification", "Enables users to evaluate line-of-sight clearance over forward rows, railings, or acoustic fixtures.")
        ]),
        ("3. Smart Seat Selection Engine", ACCENT_CYAN, [
            ("Acoustic Sweet-Spot Identification", "Highlights rows aligned with optimal multi-channel audio convergence (Dolby Atmos / 7.1 surround)."),
            ("SMPTE / THX Standard Compliance", "Calculates optimum 36°–40° viewing angle immersion zones for maximum comfort without neck strain."),
            ("Preference-Based Filters", "Quick filters for center screen lovers, extra legroom seekers, and aisle access accessibility.")
        ]),
        ("4. Seamless Movie Discovery & Booking", ACCENT_GREEN, [
            ("Centralized Catalogue & Schedules", "Comprehensive movie listings with showtimes, format indicators, trailers, and verified ratings."),
            ("Distributed 10-Minute Seat Locks", "Redis in-memory temporary holds prevent race conditions during 3D preview and checkout."),
            ("End-to-End E-Ticketing Pipeline", "Integrated payment gateways, automated booking confirmations, and cryptographically signed QR passes.")
        ])
    ]

    card_w = 5.7
    card_h = 2.4
    coords = [
        (0.8, 1.85), (6.833, 1.85),
        (0.8, 4.45), (6.833, 4.45)
    ]

    for idx, (title, color, bullets) in enumerate(pillars):
        cx, cy = coords[idx]
        c = create_card(slide6, cx, cy, card_w, card_h, bg=CARD_BG, border=CARD_BORDER)
        tb = slide6.shapes.add_textbox(Inches(cx + 0.25), Inches(cy + 0.18), Inches(card_w - 0.5), Inches(card_h - 0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = color
        pt.space_after = Pt(6)

        for b_title, b_desc in bullets:
            pb = tf.add_paragraph()
            rh = pb.add_run()
            rh.text = f"•  {b_title}: "
            rh.font.bold = True
            rh.font.size = Pt(9.2)
            rh.font.color.rgb = TEXT_WHITE
            
            rt = pb.add_run()
            rt.text = b_desc
            rt.font.size = Pt(8.8)
            rt.font.color.rgb = TEXT_MUTED
            pb.space_after = Pt(3)

    add_footer(slide6, 6)

    # =========================================================================
    # SLIDE 7: UNIQUE FEATURES
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    apply_background(slide7)
    add_header(slide7, "Innovation & Differentiation", "CINEVERSE Unique Feature Suite", "Clear academic distinction between core prototype deliverables and future enhancements")

    # Left Column: Core Prototype Features (Review 1 -> Final Delivery)
    card_core = create_card(slide7, 0.8, 1.85, 5.7, 5.0, bg=CARD_BG, border=CARD_BORDER_ACCENT)
    tb_core = slide7.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.2), Inches(4.7))
    tf_core = tb_core.text_frame
    tf_core.word_wrap = True

    p = tf_core.paragraphs[0]
    p.text = "CORE PROTOTYPE FEATURES (DELIVERABLES)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(8)

    core_features = [
        ("1. Virtual 3D Cinema Simulator", "Interactive client-side WebGL simulation allowing users to step inside a 3D auditorium and inspect eye-level sightlines from any seat.", "STATUS: CORE DELIVERABLE"),
        ("2. Digital Twin Theatre Exploration", "Sample 3D digital model of an IMAX / Dolby Atmos cinema reflecting accurate screen curve, seating rake, and lighting ambiance.", "STATUS: CORE DELIVERABLE"),
        ("3. Seat Battle™ (Compare Seats)", "Side-by-side split viewport allowing users to compare view perspectives of two candidate seats (e.g., Row C Center vs. Row F Corner).", "STATUS: CORE DELIVERABLE"),
        ("5. Smart Seat Finder", "Algorithmic recommendation overlay highlighting acoustic sweet-spots, optimal THX viewing angles, and unobstructed clear sightlines.", "STATUS: CORE DELIVERABLE")
    ]

    for title, desc, status in core_features:
        p_f = tf_core.add_paragraph()
        r_t = p_f.add_run()
        r_t.text = title + "  "
        r_t.font.bold = True
        r_t.font.size = Pt(9.8)
        r_t.font.color.rgb = ACCENT_CYAN

        r_st = p_f.add_run()
        r_st.text = f"[{status}]\n"
        r_st.font.size = Pt(8)
        r_st.font.bold = True
        r_st.font.color.rgb = ACCENT_GREEN

        r_d = p_f.add_run()
        r_d.text = desc
        r_d.font.size = Pt(8.6)
        r_d.font.color.rgb = TEXT_BODY
        p_f.space_after = Pt(6)

    # Right Column: Future Enhancements (Concept Roadmap)
    card_fut = create_card(slide7, 6.833, 1.85, 5.7, 5.0, bg=CARD_BG, border=CARD_BORDER)
    tb_fut = slide7.shapes.add_textbox(Inches(7.08), Inches(2.0), Inches(5.2), Inches(4.7))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True

    p = tf_fut.paragraphs[0]
    p.text = "PLANNED FUTURE ENHANCEMENTS (ROADMAP)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(8)

    fut_features = [
        ("4. AI Movie Concierge", "Conversational AI assistant utilizing natural language processing to recommend movies, ideal showtimes, and customized seat tiers based on user mood.", "STATUS: FUTURE SCOPE"),
        ("6. Movie Decision Room™", "Real-time collaborative group booking room where friends join via link to vote on movies, suggest seat clusters, and split payments seamlessly.", "STATUS: FUTURE SCOPE"),
        ("7. Cinema Passport™ Rewards", "Gamified loyalty system awarding digital cinema stamps, viewing milestone badges, and exclusive premiere perks to frequent moviegoers.", "STATUS: FUTURE SCOPE")
    ]

    for title, desc, status in fut_features:
        p_f = tf_fut.add_paragraph()
        r_t = p_f.add_run()
        r_t.text = title + "  "
        r_t.font.bold = True
        r_t.font.size = Pt(10)
        r_t.font.color.rgb = ACCENT_AMBER

        r_st = p_f.add_run()
        r_st.text = f"[{status}]\n"
        r_st.font.size = Pt(8)
        r_st.font.bold = True
        r_st.font.color.rgb = ACCENT_PURPLE

        r_d = p_f.add_run()
        r_d.text = desc
        r_d.font.size = Pt(8.8)
        r_d.font.color.rgb = TEXT_BODY
        p_f.space_after = Pt(12)

    add_footer(slide7, 7)

    # =========================================================================
    # SLIDE 8: USE CASE DIAGRAM (VISUAL UML USE CASE SPECIFICATION)
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    apply_background(slide8)
    add_header(slide8, "System Modelling", "UML Use Case Specification", "Formal functional decomposition illustrating actors, system boundary, and core use cases")

    # Central System Boundary Box
    boundary = create_card(slide8, 3.6, 1.85, 6.133, 5.0, bg=RGBColor(16, 23, 40), border=RGBColor(59, 130, 246), border_width=Pt(1.5))
    tb_b = slide8.shapes.add_textbox(Inches(3.7), Inches(1.9), Inches(5.9), Inches(0.3))
    tf_b = tb_b.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "«system» CINEVERSE Core Booking Platform"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = ACCENT_CYAN
    p_b.alignment = PP_ALIGN.CENTER

    # Left Actor: CUSTOMER
    card_c = create_card(slide8, 0.8, 1.85, 2.5, 5.0, bg=CARD_BG, border=CARD_BORDER_ACCENT)
    tb_c = slide8.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(2.3), Inches(4.7))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "ACTOR:\nCUSTOMER"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(12)

    p_c_desc = tf_c.add_paragraph()
    p_c_desc.text = "Primary end-user seeking to browse, preview seats in 3D, and complete digital ticket bookings."
    p_c_desc.font.name = FONT_BODY
    p_c_desc.font.size = Pt(8.5)
    p_c_desc.font.color.rgb = TEXT_MUTED
    p_c_desc.alignment = PP_ALIGN.CENTER
    p_c_desc.space_after = Pt(14)

    p_c_scope = tf_c.add_paragraph()
    p_c_scope.text = "INTERACTS WITH:\n• 10 Customer Use Cases\n• 3D Simulation Viewport\n• Payment Gateway"
    p_c_scope.font.name = FONT_BODY
    p_c_scope.font.size = Pt(8.5)
    p_c_scope.font.bold = True
    p_c_scope.font.color.rgb = ACCENT_CYAN
    p_c_scope.alignment = PP_ALIGN.CENTER

    # Right Top Actor: THEATRE PARTNER
    card_tp = create_card(slide8, 10.033, 1.85, 2.5, 2.35, bg=CARD_BG, border=CARD_BORDER)
    tb_tp = slide8.shapes.add_textbox(Inches(10.15), Inches(1.95), Inches(2.25), Inches(2.15))
    tf_tp = tb_tp.text_frame
    tf_tp.word_wrap = True
    p_tp = tf_tp.paragraphs[0]
    p_tp.text = "ACTOR:\nTHEATRE PARTNER"
    p_tp.font.name = FONT_HEADING
    p_tp.font.size = Pt(11)
    p_tp.font.bold = True
    p_tp.font.color.rgb = ACCENT_PURPLE
    p_tp.alignment = PP_ALIGN.CENTER
    p_tp.space_after = Pt(6)

    p_tp2 = tf_tp.add_paragraph()
    p_tp2.text = "Cinema operator responsible for theatre layouts & show management.\n\n• Provide Theatre Layout\n• Update Show Information"
    p_tp2.font.name = FONT_BODY
    p_tp2.font.size = Pt(8)
    p_tp2.font.color.rgb = TEXT_BODY
    p_tp2.alignment = PP_ALIGN.CENTER

    # Right Bottom Actor: ADMINISTRATOR
    card_adm = create_card(slide8, 10.033, 4.45, 2.5, 2.4, bg=CARD_BG, border=CARD_BORDER)
    tb_adm = slide8.shapes.add_textbox(Inches(10.15), Inches(4.55), Inches(2.25), Inches(2.2))
    tf_adm = tb_adm.text_frame
    tf_adm.word_wrap = True
    p_adm = tf_adm.paragraphs[0]
    p_adm.text = "ACTOR:\nADMINISTRATOR"
    p_adm.font.name = FONT_HEADING
    p_adm.font.size = Pt(11)
    p_adm.font.bold = True
    p_adm.font.color.rgb = ACCENT_AMBER
    p_adm.alignment = PP_ALIGN.CENTER
    p_adm.space_after = Pt(6)

    p_adm2 = tf_adm.add_paragraph()
    p_adm2.text = "System authority overseeing platform governance & master data.\n\n• Manage Movies & Shows\n• Manage Theatres & Layouts\n• Manage Bookings & Audit"
    p_adm2.font.name = FONT_BODY
    p_adm2.font.size = Pt(8)
    p_adm2.font.color.rgb = TEXT_BODY
    p_adm2.alignment = PP_ALIGN.CENTER

    # Inside Boundary: Customer Use Case Bubbles (Left Column Inside Boundary)
    cust_ucs = [
        "Register", "Login", "Browse Movies", "Select Theatre",
        "Select Showtime", "View Seat Map", "Preview Seat in 3D",
        "Book Tickets", "Make Payment", "View E-Ticket"
    ]
    
    uc_col1_x = 3.85
    uc_col2_x = 6.75
    uc_w = 2.65
    uc_h = 0.38
    uc_gap = 0.08
    y_start = 2.25

    # Left Column (Customer Use Cases)
    for i, uc_text in enumerate(cust_ucs):
        y = y_start + i * (uc_h + uc_gap)
        bubble = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(uc_col1_x), Inches(y), Inches(uc_w), Inches(uc_h))
        bubble.fill.solid()
        bubble.fill.fore_color.rgb = RGBColor(22, 32, 54)
        bubble.line.color.rgb = ACCENT_BLUE if uc_text == "Preview Seat in 3D" else CARD_BORDER
        bubble.line.width = Pt(1.5 if uc_text == "Preview Seat in 3D" else 1.0)
        tf_b = bubble.text_frame
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf_b.paragraphs[0]
        p.text = f"«use case» {uc_text}"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.bold = (uc_text == "Preview Seat in 3D")
        p.font.color.rgb = ACCENT_CYAN if uc_text == "Preview Seat in 3D" else TEXT_WHITE
        p.alignment = PP_ALIGN.CENTER

    # Right Column Inside Boundary: Partner & Admin Use Cases
    partner_admin_ucs = [
        # Theatre Partner Use Cases (Top)
        ("Provide Theatre Layout", ACCENT_PURPLE),
        ("Update Show Information", ACCENT_PURPLE),
        # Administrator Use Cases (Bottom)
        ("Manage Movies", ACCENT_AMBER),
        ("Manage Theatres", ACCENT_AMBER),
        ("Manage Shows", ACCENT_AMBER),
        ("Manage Seat Layouts", ACCENT_AMBER),
        ("Manage Bookings", ACCENT_AMBER)
    ]

    for j, (uc_text, u_col) in enumerate(partner_admin_ucs):
        y = y_start + (j if j < 2 else j + 1) * (uc_h + uc_gap + 0.15)
        bubble = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(uc_col2_x), Inches(y), Inches(uc_w), Inches(uc_h))
        bubble.fill.solid()
        bubble.fill.fore_color.rgb = RGBColor(22, 32, 54)
        bubble.line.color.rgb = u_col
        bubble.line.width = Pt(1)
        tf_b = bubble.text_frame
        tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf_b.paragraphs[0]
        p.text = f"«use case» {uc_text}"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = u_col
        p.alignment = PP_ALIGN.CENTER

    add_footer(slide8, 8)

    # =========================================================================
    # SLIDE 9: SOFTWARE REQUIREMENTS
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    apply_background(slide9)
    add_header(slide9, "Technical Stack", "Software Requirements & Architecture Stack", "Enterprise-grade, open-source technology stack chosen for high performance, concurrency, and 3D fidelity")

    tech_stack = [
        ("Frontend Web Layer", ACCENT_BLUE, [
            ("React.js (v18+)", "Modern single-page application framework delivering reactive UI component rendering."),
            ("HTML5 & CSS3", "Semantic structure, responsive viewport layouts, and accessible UI controls."),
            ("JavaScript (ES6+)", "Client logic, asynchronous state management, and API REST communication.")
        ]),
        ("3D Graphics Rendering", ACCENT_PURPLE, [
            ("Three.js Library", "WebGL-based 3D scene creation, camera projection matrices, and mesh loaders."),
            ("React Three Fiber (R3F)", "Declarative React integration for component-based 3D virtual cinema scene graph."),
            ("Perspective Camera", "Dynamic camera transforms mapping selected seat (x, y, z) coordinates to eye-level.")
        ]),
        ("Backend Services", ACCENT_CYAN, [
            ("Java 17 (LTS)", "Modern enterprise runtime providing records, sealed classes, and strong memory management."),
            ("Spring Boot 3.x", "Microservices framework powering high-throughput REST APIs and domain services."),
            ("Spring Security", "Stateless authentication, password hashing, and Role-Based Access Control (RBAC).")
        ]),
        ("Database Layer", ACCENT_GREEN, [
            ("PostgreSQL 15+", "Robust relational database maintaining ACID guarantees for users, shows, and bookings."),
            ("Relational Integrity", "Enforces foreign-key constraints, normalized layouts, and transactional persistence."),
            ("Spring Data JPA", "Hibernate-based ORM for clean, maintainable repository queries and data mapping.")
        ]),
        ("Caching & Concurrency", ACCENT_AMBER, [
            ("Redis In-Memory Store", "High-speed key-value cache handling 10-minute temporary seat reservation holds."),
            ("Temporary Hold TTL", "Time-To-Live auto-release of unconfirmed seats prevents permanent blocking."),
            ("Distributed Concurrency", "Atomic lease operations guarantee a seat is sold at most once under rush load.")
        ]),
        ("Engineering Tools", ACCENT_CORAL, [
            ("IDEs (VS Code / IntelliJ)", "Optimized development environments for full-stack React and Java Spring Boot."),
            ("Git & GitHub", "Distributed version control, branch management, code reviews, and issue tracking."),
            ("Postman API Client", "Automated endpoint testing, payload validation, and REST API contract verification.")
        ])
    ]

    card_w = 3.65
    card_h = 2.4
    start_x = 0.8
    y_row1 = 1.85
    y_row2 = 4.45

    for idx, (title, color, items) in enumerate(tech_stack):
        col_i = idx % 3
        row_i = idx // 3
        cx = start_x + col_i * (card_w + 0.38)
        cy = y_row1 if row_i == 0 else y_row2

        c = create_card(slide9, cx, cy, card_w, card_h, bg=CARD_BG, border=CARD_BORDER)
        tb = slide9.shapes.add_textbox(Inches(cx + 0.2), Inches(cy + 0.15), Inches(card_w - 0.4), Inches(card_h - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(5)

        for item_name, item_desc in items:
            p_i = tf.add_paragraph()
            r_n = p_i.add_run()
            r_n.text = f"• {item_name}: "
            r_n.font.bold = True
            r_n.font.size = Pt(8.5)
            r_n.font.color.rgb = TEXT_WHITE

            r_d = p_i.add_run()
            r_d.text = item_desc
            r_d.font.size = Pt(8.2)
            r_d.font.color.rgb = TEXT_MUTED
            p_i.space_after = Pt(2)

    add_footer(slide9, 9)

    # =========================================================================
    # SLIDE 10: HARDWARE REQUIREMENTS
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    apply_background(slide10)
    add_header(slide10, "System Specifications", "Hardware Requirements: Minimum vs. Recommended", "Hardware baselines for client execution, developer workstations, and responsive multi-device verification")

    # Left Card: Minimum Hardware Requirements
    card_min = create_card(slide10, 0.8, 1.85, 5.7, 4.0, bg=CARD_BG, border=CARD_BORDER)
    tb_min = slide10.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.2), Inches(3.7))
    tf_min = tb_min.text_frame
    tf_min.word_wrap = True

    p = tf_min.paragraphs[0]
    p.text = "MINIMUM HARDWARE REQUIREMENTS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(12)

    min_specs = [
        ("Dual-Core Processor", "Intel Core i3 / AMD Athlon (2.0 GHz or higher)"),
        ("8 GB System RAM", "Sufficient for modern operating system and browser WebGL runtime"),
        ("10 – 20 GB Free Storage", "Local storage for operating system, browser caching, and build files"),
        ("WebGL-Compatible Graphics", "Integrated GPU supporting WebGL 2.0 (Intel HD / Iris Xe / AMD Vega)"),
        ("Stable Internet Connection", "Minimum 5 Mbps connection for seamless asset streaming and API calls")
    ]
    for lbl, val in min_specs:
        p_s = tf_min.add_paragraph()
        r_l = p_s.add_run()
        r_l.text = f"•  {lbl}\n    "
        r_l.font.bold = True
        r_l.font.size = Pt(9.5)
        r_l.font.color.rgb = TEXT_WHITE

        r_v = p_s.add_run()
        r_v.text = val
        r_v.font.size = Pt(9)
        r_v.font.color.rgb = TEXT_MUTED
        p_s.space_after = Pt(5)

    # Right Card: Recommended Hardware Requirements
    card_rec = create_card(slide10, 6.833, 1.85, 5.7, 4.0, bg=CARD_BG, border=CARD_BORDER_ACCENT)
    tb_rec = slide10.shapes.add_textbox(Inches(7.08), Inches(2.0), Inches(5.2), Inches(3.7))
    tf_rec = tb_rec.text_frame
    tf_rec.word_wrap = True

    p = tf_rec.paragraphs[0]
    p.text = "RECOMMENDED HARDWARE REQUIREMENTS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    p.space_after = Pt(12)

    rec_specs = [
        ("Intel Core i5 / AMD Ryzen 5 or better", "Hexa-Core high-clock processor for rapid compilation and 60 FPS rendering"),
        ("16 GB High-Speed RAM", "Smooth simultaneous execution of Spring Boot, PostgreSQL, Redis, and React dev server"),
        ("Solid State Drive (SSD) Storage", "256 GB+ NVMe SSD for instant project loading and disk I/O operations"),
        ("Modern Web Browser", "Google Chrome, Microsoft Edge, or Mozilla Firefox with full WebGL 2.0 support"),
        ("Smartphone for Responsive Testing", "iOS / Android device for testing mobile touch gestures, orbital controls, and checkout")
    ]
    for lbl, val in rec_specs:
        p_s = tf_rec.add_paragraph()
        r_l = p_s.add_run()
        r_l.text = f"•  {lbl}\n    "
        r_l.font.bold = True
        r_l.font.size = Pt(9.5)
        r_l.font.color.rgb = TEXT_WHITE

        r_v = p_s.add_run()
        r_v.text = val
        r_v.font.size = Pt(9)
        r_v.font.color.rgb = TEXT_MUTED
        p_s.space_after = Pt(5)

    # Bottom Spec Summary Note
    bot_card = create_card(slide10, 0.8, 6.0, 11.733, 0.85, bg=CARD_BG_ALT, border=CARD_BORDER)
    tb_bot = slide10.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.333), Inches(0.7))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    p_b = tf_bot.paragraphs[0]
    p_b.text = "CLIENT-SIDE SHADER COMPUTATION ARCHITECTURE:"
    p_b.font.name = FONT_HEADING
    p_b.font.size = Pt(9.5)
    p_b.font.bold = True
    p_b.font.color.rgb = ACCENT_CYAN

    p_b2 = tf_bot.add_paragraph()
    p_b2.text = "Because Three.js utilizes client-side WebGL GPU shaders, the 3D calculation executes locally on the user's device without imposing GPU server costs on the backend. This guarantees high scalability and responsive 60 FPS interaction."
    p_b2.font.name = FONT_BODY
    p_b2.font.size = Pt(9)
    p_b2.font.color.rgb = TEXT_BODY

    add_footer(slide10, 10)

    # =========================================================================
    # SLIDE 11: FEASIBILITY STUDY
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    apply_background(slide11)
    add_header(slide11, "Project Viability", "Feasibility Study Analysis", "Formal academic validation demonstrating technical, economic, and operational execution viability")

    feasibility_data = [
        ("Technical Feasibility", ACCENT_BLUE, [
            ("Proven WebGL Maturity", "Three.js and WebGL 2.0 are native web standards supported across 98%+ of modern browsers with zero external plugin requirements."),
            ("Standard 3D Camera Maths", "Eye-level seat viewpoint simulation utilizes established 3D linear algebra (translation, Euler rotations, and FOV perspective transforms)."),
            ("Enterprise Backend Patterns", "Java 17, Spring Boot, PostgreSQL, and Redis represent battle-tested architectures with comprehensive documentation and community support."),
            ("Lightweight Server Load", "Client-side rendering ensures the central backend only processes standard JSON REST payloads and seat state concurrency.")
        ]),
        ("Economic Feasibility", ACCENT_GREEN, [
            ("100% Open-Source Technologies", "React, Three.js, Spring Boot, PostgreSQL, and Redis operate under permissive MIT / Apache 2.0 open-source licenses."),
            ("Zero Licensing Expenditure", "Requires zero proprietary software purchases or costly commercial 3D engine licenses."),
            ("Manageable Prototype Costs", "The academic prototype can be fully developed and hosted using free developer tiers (Render, Vercel, Supabase, GitHub)."),
            ("Commercial ROI Upside", "For commercial theatres, reducing blind seating directly curtails refund requests and boosts consumer satisfaction.")
        ]),
        ("Operational Feasibility", ACCENT_PURPLE, [
            ("Intuitive Booking Workflow", "CINEVERSE preserves the familiar 5-step booking journey with zero cognitive overload for regular moviegoers."),
            ("Seamless 3D Toggle", "The 3D seat preview operates as a smooth on-demand modal; users can switch between 2D and 3D seamlessly."),
            ("Straightforward Partner Management", "Theatre managers configure auditorium models using standardized JSON matrix definitions without specialized 3D skills."),
            ("Responsive Touch Accessibility", "Optimized controls allow effortless mobile operation using standard touch gestures and single-tap checkout.")
        ])
    ]

    card_w = 3.65
    card_h = 4.0
    start_x = 0.8
    card_y = 1.85

    for idx, (title, color, points) in enumerate(feasibility_data):
        cx = start_x + idx * (card_w + 0.38)
        c = create_card(slide11, cx, card_y, card_w, card_h, bg=CARD_BG, border=CARD_BORDER)

        tb = slide11.shapes.add_textbox(Inches(cx + 0.2), Inches(card_y + 0.18), Inches(card_w - 0.4), Inches(card_h - 0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title.upper()
        p.font.name = FONT_HEADING
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(10)

        for p_title, p_desc in points:
            p_pt = tf.add_paragraph()
            r_t = p_pt.add_run()
            r_t.text = f"•  {p_title}:\n   "
            r_t.font.bold = True
            r_t.font.size = Pt(9)
            r_t.font.color.rgb = TEXT_WHITE

            r_d = p_pt.add_run()
            r_d.text = p_desc
            r_d.font.size = Pt(8.5)
            r_d.font.color.rgb = TEXT_MUTED
            p_pt.space_after = Pt(6)

    # Bottom Feasibility Verdict Banner
    verdict = create_card(slide11, 0.8, 6.0, 11.733, 0.85, bg=CARD_BG_ALT, border=ACCENT_GREEN)
    tb_v = slide11.shapes.add_textbox(Inches(1.0), Inches(6.08), Inches(11.333), Inches(0.7))
    tf_v = tb_v.text_frame
    tf_v.word_wrap = True
    pv = tf_v.paragraphs[0]
    pv.text = "FEASIBILITY CONCLUSION: FULLY VIABLE FOR ACADEMIC PROTOTYPE IMPLEMENTATION"
    pv.font.name = FONT_HEADING
    pv.font.size = Pt(10)
    pv.font.bold = True
    pv.font.color.rgb = ACCENT_GREEN

    pv2 = tf_v.add_paragraph()
    pv2.text = "Based on technical accessibility, zero software licensing barriers, and practical operational usability, CINEVERSE is completely feasible as an academic engineering prototype within the prescribed project timeline and resource constraints."
    pv2.font.name = FONT_BODY
    pv2.font.size = Pt(9)
    pv2.font.color.rgb = TEXT_BODY

    add_footer(slide11, 11)

    # =========================================================================
    # SLIDE 12: SYSTEM WORKFLOW (VISUAL FLOWCHART)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    apply_background(slide12)
    add_header(slide12, "Execution Pipeline", "System Workflow & Transaction Flowchart", "Sequential operational pipeline with backend validation and temporary seat reservation before payment")

    # 12-Step Visual Flowchart in 2 Connected Rows of 6 Steps Each
    row1_steps = [
        ("1. User Login", "Authenticate via JWT or guest session", ACCENT_BLUE),
        ("2. Browse Movies", "Filter catalogue by format & language", ACCENT_BLUE),
        ("3. Select Theatre", "Choose multiplex cinema venue", ACCENT_BLUE),
        ("4. Select Showtime", "Select date & screening time slot", ACCENT_BLUE),
        ("5. Open Seat Map", "Fetch live seat availability matrix", ACCENT_PURPLE),
        ("6. Select Seat", "Choose preferred seat coordinates", ACCENT_PURPLE)
    ]

    row2_steps = [
        ("7. Preview in 3D", "Inspect eye-level view in WebGL", ACCENT_CYAN, True),
        ("8. Backend Validation", "Spring Boot verifies seat eligibility", ACCENT_AMBER, True),
        ("9. 10-Min Redis Hold", "Temporary hold lease before payment", ACCENT_AMBER, True),
        ("10. Confirm & Pay", "Process payment gateway transaction", ACCENT_GREEN, False),
        ("11. Booking Confirmed", "Atomic update: HELD → SOLD in DB", ACCENT_GREEN, False),
        ("12. E-Ticket Issued", "Generate QR e-ticket & dispatch", ACCENT_GREEN, False)
    ]

    card_w = 1.78
    card_h = 2.05
    gap_x = 0.21
    start_x = 0.8
    y1 = 1.95
    y2 = 4.35

    # Draw Row 1
    for idx, (title, desc, col) in enumerate(row1_steps):
        cx = start_x + idx * (card_w + gap_x)
        c = create_card(slide12, cx, y1, card_w, card_h, bg=CARD_BG, border=CARD_BORDER)

        tb = slide12.shapes.add_textbox(Inches(cx + 0.1), Inches(y1 + 0.15), Inches(card_w - 0.2), Inches(card_h - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"STEP {idx+1}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = title.split(". ")[1] if ". " in title else title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_BODY
        p3.font.size = Pt(7.8)
        p3.font.color.rgb = TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    # Draw Row 2
    for idx, (title, desc, col, is_highlight) in enumerate(row2_steps):
        cx = start_x + idx * (card_w + gap_x)
        border_col = col if is_highlight else CARD_BORDER
        c = create_card(slide12, cx, y2, card_w, card_h, bg=CARD_BG, border=border_col, border_width=Pt(1.6 if is_highlight else 1.0))

        tb = slide12.shapes.add_textbox(Inches(cx + 0.1), Inches(y2 + 0.15), Inches(card_w - 0.2), Inches(card_h - 0.3))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = f"STEP {idx+7}"
        p.font.name = FONT_HEADING
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = col
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = title.split(". ")[1] if ". " in title else title
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = ACCENT_CYAN if is_highlight else TEXT_WHITE
        p2.alignment = PP_ALIGN.CENTER
        p2.space_after = Pt(8)

        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.name = FONT_BODY
        p3.font.size = Pt(7.8)
        p3.font.color.rgb = TEXT_MUTED
        p3.alignment = PP_ALIGN.CENTER

    # Bottom Callout Note: Emphasizing the Prompt Requirement
    note_card = create_card(slide12, 0.8, 6.55, 11.733, 0.42, bg=CARD_BG_ALT, border=ACCENT_AMBER)
    tb_n = slide12.shapes.add_textbox(Inches(0.9), Inches(6.58), Inches(11.5), Inches(0.35))
    tf_n = tb_n.text_frame
    p_n = tf_n.paragraphs[0]
    p_n.text = "★ CRITICAL WORKFLOW INVARIANT: Backend availability validation and temporary Redis seat holds occur BEFORE payment to prevent race conditions."
    p_n.font.name = FONT_HEADING
    p_n.font.size = Pt(8.5)
    p_n.font.bold = True
    p_n.font.color.rgb = ACCENT_AMBER
    p_n.alignment = PP_ALIGN.CENTER

    add_footer(slide12, 12)

    # =========================================================================
    # SLIDE 13: EXPECTED OUTCOMES
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    apply_background(slide13)
    add_header(slide13, "Project Deliverables", "Expected Outcomes & Project Deliverables", "Tangible technical deliverables, operational milestones, and experiential benchmarks")

    outcomes = [
        ("1. Working Movie Booking Web Application", ACCENT_BLUE, [
            ("Full-Stack Integration", "Fully operational web application executing seamless booking flow from catalogue browsing to checkout."),
            ("Customer & Admin Portals", "Separate dedicated modules for customer booking and administrative governance."),
            ("Responsive Cross-Platform UI", "Optimized dark-cinema user interface functioning smoothly across desktops, tablets, and smartphones.")
        ]),
        ("2. Virtual 3D Seat Preview Engine", ACCENT_PURPLE, [
            ("Sample Auditorium Model", "Calibrated 3D digital twin of a representative IMAX/multiplex auditorium with realistic screen curvature."),
            ("Dynamic Eye-Level Camera", "Real-time client-side camera projection repositioning to the exact eye-level coordinates of any chosen seat."),
            ("Interactive Seat Battle™", "Functional split-screen module allowing simultaneous visual comparison of two competing seats.")
        ]),
        ("3. Comprehensive Management Modules", ACCENT_GREEN, [
            ("Movie & Show Management", "Admin and partner capabilities to add, edit, and schedule movie screenings with format tags."),
            ("Dynamic Seat Layout Mapping", "Ability to define customized auditorium seating layouts, tier categories, and pricing matrices."),
            ("Booking & Transaction Auditing", "Live administrative dashboard tracking occupancy rates, confirmed bookings, and transaction logs.")
        ]),
        ("4. Enhanced Experience & Future Foundation", ACCENT_AMBER, [
            ("Elimination of Blind Seating", "Substantial improvement in seat-selection confidence by pre-visualizing screen distance and angles."),
            ("Concurrency & Single-Sale Guarantee", "Thread-safe distributed reservation ensuring seats are sold at most once under concurrent rushes."),
            ("Extensible Foundation", "Modular architecture designed for future integration of AI recommendations and WebXR virtual reality.")
        ])
    ]

    card_w = 5.7
    card_h = 2.4
    coords = [
        (0.8, 1.85), (6.833, 1.85),
        (0.8, 4.45), (6.833, 4.45)
    ]

    for idx, (title, color, bullets) in enumerate(outcomes):
        cx, cy = coords[idx]
        c = create_card(slide13, cx, cy, card_w, card_h, bg=CARD_BG, border=CARD_BORDER)
        tb = slide13.shapes.add_textbox(Inches(cx + 0.25), Inches(cy + 0.18), Inches(card_w - 0.5), Inches(card_h - 0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        pt = tf.paragraphs[0]
        pt.text = title
        pt.font.name = FONT_HEADING
        pt.font.size = Pt(12)
        pt.font.bold = True
        pt.font.color.rgb = color
        pt.space_after = Pt(6)

        for b_title, b_desc in bullets:
            pb = tf.add_paragraph()
            rh = pb.add_run()
            rh.text = f"✔  {b_title}: "
            rh.font.bold = True
            rh.font.size = Pt(9.2)
            rh.font.color.rgb = TEXT_WHITE
            
            rt = pb.add_run()
            rt.text = b_desc
            rt.font.size = Pt(8.8)
            rt.font.color.rgb = TEXT_MUTED
            pb.space_after = Pt(3)

    add_footer(slide13, 13)

    # =========================================================================
    # SLIDE 14: CONCLUSION & FUTURE SCOPE
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    apply_background(slide14)
    add_header(slide14, "Looking Forward", "Conclusion & Future Scope", "Transforming conventional movie ticket booking into an immersive, informed spatial experience")

    # Left Card: Academic Conclusion
    card_concl = create_card(slide14, 0.8, 1.85, 5.7, 3.8, bg=CARD_BG, border=CARD_BORDER_ACCENT)
    tb_c = slide14.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.2), Inches(3.5))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p = tf_c.paragraphs[0]
    p.text = "PROJECT SUMMARY & CONCLUSION"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_PURPLE
    p.space_after = Pt(10)

    concl_points = [
        ("Paradigm Shift in Cinema Ticketing", "CINEVERSE redefines movie booking by moving beyond static 2D abstract grids into an interactive, spatial pre-experience."),
        ("Eliminates Spatial Uncertainty", "Directly resolves viewing angle distortion, neck strain, and distance miscalculations by allowing users to 'know their view before they book'."),
        ("Proven Full-Stack Synergy", "Demonstrates the practical viability of combining client-side WebGL (Three.js) 3D graphics with enterprise Java 17 and Spring Boot microservices."),
        ("Defensible Academic Prototype", "Establishes a solid, peer-reviewed engineering title and validated technical architecture for subsequent capstone reviews.")
    ]
    for h, b in concl_points:
        p_p = tf_c.add_paragraph()
        r_h = p_p.add_run()
        r_h.text = f"•  {h}: "
        r_h.font.bold = True
        r_h.font.size = Pt(9.5)
        r_h.font.color.rgb = TEXT_WHITE

        r_b = p_p.add_run()
        r_b.text = b
        r_b.font.size = Pt(9)
        r_b.font.color.rgb = TEXT_MUTED
        p_p.space_after = Pt(5)

    # Right Card: Future Scope
    card_fut2 = create_card(slide14, 6.833, 1.85, 5.7, 3.8, bg=CARD_BG, border=CARD_BORDER)
    tb_f = slide14.shapes.add_textbox(Inches(7.08), Inches(2.0), Inches(5.2), Inches(3.5))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True

    p = tf_f.paragraphs[0]
    p.text = "STRATEGIC FUTURE SCOPE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ACCENT_AMBER
    p.space_after = Pt(10)

    fut_points = [
        ("Full Digital Twin Theatres", "Expand 3D modeling across diverse commercial multiplex architectures with automated CAD ingestion."),
        ("VR Headset Integration", "WebXR immersion in Meta Quest / Apple Vision allowing users to virtually walk through the cinema lobby to their seat."),
        ("AR Theatre Navigation", "Augmented Reality smartphone camera navigation guiding patrons from multiplex entrance to their exact row."),
        ("AI Recommendations", "Machine learning recommendation engine scoring seat satisfaction based on personalized audio and visual preferences."),
        ("Group Payment Splitting", "Collaborative Movie Decision Rooms allowing friend groups to split ticket and food combo payments seamlessly."),
        ("Theatre Partnerships", "Direct API integration with commercial cinema chains (PVR-INOX, Cinepolis) for live automated inventory sync.")
    ]
    for h, b in fut_points:
        p_p = tf_f.add_paragraph()
        r_h = p_p.add_run()
        r_h.text = f"▸  {h}: "
        r_h.font.bold = True
        r_h.font.size = Pt(9.2)
        r_h.font.color.rgb = ACCENT_AMBER

        r_b = p_p.add_run()
        r_b.text = b
        r_b.font.size = Pt(8.6)
        r_b.font.color.rgb = TEXT_MUTED
        p_p.space_after = Pt(4)

    # Grand Thank You Banner
    card_ty = create_card(slide14, 0.8, 5.85, 11.733, 1.05, bg=CARD_BG_ALT, border=ACCENT_CYAN)
    tb_ty = slide14.shapes.add_textbox(Inches(1.0), Inches(5.95), Inches(11.333), Inches(0.85))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True

    p_ty = tf_ty.paragraphs[0]
    p_ty.text = "THANK YOU  ·  QUESTIONS & DISCUSSION"
    p_ty.font.name = FONT_HEADING
    p_ty.font.size = Pt(14)
    p_ty.font.bold = True
    p_ty.font.color.rgb = ACCENT_CYAN
    p_ty.alignment = PP_ALIGN.CENTER

    p_ty2 = tf_ty.add_paragraph()
    p_ty2.text = "CINEVERSE  |  “Know Your View Before You Book.”  |  Academic Engineering Review 1"
    p_ty2.font.name = FONT_BODY
    p_ty2.font.size = Pt(10)
    p_ty2.font.color.rgb = TEXT_MUTED
    p_ty2.alignment = PP_ALIGN.CENTER

    add_footer(slide14, 14)

    # Save presentation
    prs.save(output_path)
    print(f"Presentation successfully created and saved to: {output_path}")

if __name__ == '__main__':
    out_dir = r"C:\Users\Admin\.gemini\antigravity\scratch\A7_AOOP_G13_PROJ"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "CINEVERSE_Review1_Presentation.pptx")
    build_presentation(out_file)
