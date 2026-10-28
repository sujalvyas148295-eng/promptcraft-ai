"""
PromptCraft AI - Flask Backend
Universal Prompt Generator & Quality Evaluator
Built for IPE (Introduction to Prompt Engineering)
"""

import os
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'promptcraft-ai-secret-key-2026'

# ---------------------------------------------------------------------------
# STYLE MODIFIERS
# ---------------------------------------------------------------------------
STYLE_PRESETS = {
    "futuristic": {
        "label": "Futuristic",
        "aesthetic": "sleek cyberpunk/solarpunk aesthetics, neon violet and cyan accents, holographic UI elements, advanced futuristic tech motifs",
        "tone": "forward-looking, high-tech, visionary, sleek and modern",
        "tech_focus": "modern reactive architectures, glassmorphism, glowing micro-interactions, next-gen best practices"
    },
    "cinematic": {
        "label": "Cinematic",
        "aesthetic": "dramatic 35mm anamorphic film quality, volumetric lighting, rich chiaroscuro shadows, high dynamic range, storytelling depth",
        "tone": "evocative, atmospheric, emotionally resonant, immersive",
        "tech_focus": "high-impact visual hierarchy, narrative storytelling, dramatic reveal sequences"
    },
    "minimal": {
        "label": "Minimal",
        "aesthetic": "clean negative space, Swiss international typography, monochromatic with subtle accent, essentialist composition",
        "tone": "concise, direct, highly focused, elegant, fluff-free",
        "tech_focus": "lightweight, uncluttered structures, accessible simplicity, zero friction"
    },
    "professional": {
        "label": "Professional",
        "aesthetic": "polished corporate polish, balanced layout, trustworthy muted tones, enterprise-grade elegance",
        "tone": "authoritative, structured, business-ready, objective, articulate",
        "tech_focus": "enterprise architectural patterns, strict standards compliance, maintainable, scalable"
    },
    "technical": {
        "label": "Technical",
        "aesthetic": "blueprint clarity, precision diagrams, terminal-inspired accents, exact dimensional parameters",
        "tone": "analytical, rigorous, deterministic, unambiguous",
        "tech_focus": "strict type-safety, formal specifications, algorithmic efficiency, comprehensive edge cases"
    },
    "creative": {
        "label": "Creative",
        "aesthetic": "expressive avant-garde flair, vivid color theory, unexpected juxtapositions, artistic nuance",
        "tone": "imaginative, captivating, original, emotionally engaging",
        "tech_focus": "experimental patterns, dynamic animations, playful interactive states"
    }
}

# ---------------------------------------------------------------------------
# CATEGORY PROMPT GENERATORS
# ---------------------------------------------------------------------------

def build_image_prompt(idea: str, style_info: dict, instructions: str, variation: int = 0) -> str:
    lighting_options = [
        "Volumetric neon rim lighting with deep violet backlighting and soft cyan fill",
        "Dramatic golden hour cinematic lighting with soft diffused ambient shadows",
        "Crisp studio strobe lighting with high-contrast specular reflections"
    ]
    camera_options = [
        "Shot on 50mm f/1.4 prime lens, shallow depth of field, sharp subject focus, 8K resolution",
        "Wide-angle 24mm perspective, eye-level framing, dynamic diagonal composition, hyper-detailed",
        "Close-up macro perspective, cinematic anamorphic bokeh, rule-of-thirds composition"
    ]
    
    light = lighting_options[variation % len(lighting_options)]
    cam = camera_options[variation % len(camera_options)]
    
    extra = f"\n- Additional Constraints: {instructions.strip()}" if instructions else ""
    
    prompt = f"""# Master Image Generation Prompt (Optimized for Midjourney v6 / DALL-E 3 / Stable Diffusion XL)

**Core Subject & Scene:**
{idea.strip()}

**Visual Style & Art Direction:**
- Aesthetic: {style_info['label']} style ({style_info['aesthetic']})
- Lighting & Atmosphere: {light}
- Camera & Framing: {cam}
- Color Palette: Electric cyan, deep violet, midnight charcoal, and luminous highlights
- Rendering & Quality: Octane Render style, Unreal Engine 5 aesthetic, 8K UHD, masterpiece detail, ray-traced reflections{extra}

**Negative Guidance (Unwanted Elements):**
Avoid low resolution, blurry details, muddy textures, deformed anatomy, bad proportions, unnatural artifacts, watermark, text signatures, washed-out contrast.

---
**Quick Copy-Paste One-Liner (Midjourney / SDXL):**
{idea.strip()}, {style_info['label'].lower()} style, {style_info['aesthetic']}, {light.lower()}, {cam.lower()}, 8k resolution, photorealistic masterpiece, octane render --ar 16:9 --v 6.1 --style raw"""
    return prompt.strip()


def build_video_prompt(idea: str, style_info: dict, instructions: str, variation: int = 0) -> str:
    transitions = [
        "Seamless dolly-in camera tracking smoothly into the primary subject, fluid motion blur at 60fps",
        "Orbiting dynamic camera rotation at eye-level, cinematic slow-motion ramping (120fps feel)",
        "Low-angle drone forward push with volumetric atmospheric fog, stable gimbal motion"
    ]
    movement = transitions[variation % len(transitions)]
    extra = f"\n- Director's Notes: {instructions.strip()}" if instructions else ""

    prompt = f"""# Master Video Generation Prompt (Optimized for Sora / Runway Gen-3 Alpha / Luma Dream Machine)

**Concept Title:**
{idea.strip()}

**Scene Breakdown & Temporal Progression:**
- **Opening (0s - 2s):** Establishing wide shot introducing the setting and primary focal subject with {style_info['tone']} mood.
- **Action Sequence (2s - 6s):** Dynamic progression where the subject engages actively. {movement}.
- **Resolution (6s - 8s+):** Pull-back reveal emphasizing scale, environment detail, and visual impact.

**Cinematography & Visual Parameters:**
- Style & Mood: {style_info['label']} ({style_info['aesthetic']})
- Camera Movement: {movement}
- Lighting & Grading: High-contrast color grade, deep neon shadows, sharp anamorphic highlights
- Aspect Ratio: 16:9 widescreen (cinematic)
- Motion Fidelity: Smooth, physically consistent movement, no morphing artifacts, stable geometry{extra}

**Audio & Atmosphere Cues:**
- Soundscape: Subtle futuristic synth swell, crisp environmental Foley sounds, deep sub-bass undertone.

---
**Runway / Sora Prompt String:**
Cinematic {style_info['label'].lower()} video: {idea.strip()}. {movement}. Lighting: {style_info['aesthetic']}. Photorealistic, 4K 60fps, continuous camera motion, stable geometry, hyper-realistic physics."""
    return prompt.strip()


def build_website_prompt(idea: str, style_info: dict, instructions: str, variation: int = 0) -> str:
    extra = f"\n- Custom Specifications: {instructions.strip()}" if instructions else ""
    
    prompt = f"""# Master Website Design & Code Prompt (Optimized for Claude 3.5 Sonnet / v0.dev / Cursor)

**Project Brief:**
Design and implement a complete, responsive modern web experience for:
"{idea.strip()}"

**Visual Language & Design System:**
- Design Theme: {style_info['label']} ({style_info['aesthetic']})
- Color Palette:
  - Deep Base: Midnight Navy (`#080a14`) & Dark Obsidian (`#0f1224`)
  - Accent Glow: Vivid Violet (`#8b5cf6`) & Neon Cyan (`#06b6d4`)
  - Text & Accents: Crisp White (`#f8fafc`) & Subtle Slate (`#94a3b8`)
- Surfaces: Glassmorphic cards with `backdrop-filter: blur(16px)`, soft 1px border (`rgba(255,255,255,0.08)`), subtle radial neon glows.
- Typography: Modern sans-serif (e.g., Plus Jakarta Sans or Inter) with spacious tracking and high contrast.

**Required Page Architecture & Sections:**
1. **Header / Navbar:** Sticky blurred navigation with glowing brand logo, intuitive nav links, and interactive primary CTA button.
2. **Hero Section:** High-impact punchy headline, descriptive sub-headline, dual CTA buttons (Primary glowing & Secondary glass), and an eye-catching interactive visual element.
3. **Core Features / Content Grid:** 3 to 4 distinct cards detailing unique value points with custom icons, glowing hover states, and concise descriptions.
4. **Interactive Showcase / Demo Module:** A functional, interactive widget or card demonstrating the core product/service utility.
5. **Social Proof & Stats:** Key performance metrics or user testimonials arranged in clean counters.
6. **Footer:** Clean bottom bar with copyright, quick links, and subtle college/author credits.

**Technical & Interaction Requirements:**
- Frontend: Clean semantic HTML5, modern modular CSS3, and lightweight vanilla JavaScript.
- Mobile First & Responsive: Flawless layout adaptivity across mobile (375px+), tablet (768px+), and desktop (1280px+).
- Micro-interactions: Smooth CSS cubic-bezier hover transitions, keyboard focus outlines for accessibility (WCAG 2.1 AA), and zero layout shifts.{extra}

**Deliverable Expected:**
Provide complete, production-ready code with clean inline documentation and zero placeholder lorem-ipsum."""
    return prompt.strip()


def build_code_prompt(idea: str, style_info: dict, instructions: str, variation: int = 0) -> str:
    extra = f"\n- Specific Constraints / Tech Stack: {instructions.strip()}" if instructions else ""
    
    prompt = f"""# Master Software Engineering Prompt (Optimized for Claude 3.5 Sonnet / Cursor / GitHub Copilot)

**Role Definition:**
Act as a Principal Staff Software Engineer and Senior Systems Architect.

**Task & Objective:**
Design and implement a clean, robust, and production-ready solution for:
"{idea.strip()}"

**Architecture & Implementation Standards:**
- Approach: {style_info['label']} engineering ({style_info['tech_focus']})
- Code Quality: Adhere to SOLID principles, DRY, clear separation of concerns, and clean architectural boundaries.
- Type Safety & Documentation: Full type annotations/type hints, expressive variable names, and concise docstrings explaining "why" rather than "what".
- Defensive Design: Validate all incoming arguments and parameters; handle unexpected null/undefined states gracefully.
- Performance: Optimize for predictable time complexity and minimal memory allocations.

**Deliverables Required:**
1. **Technical Overview:** Brief explanation of the architecture, data flow, and trade-offs.
2. **Production Code:** Full, working, dependency-minimal implementation (no pseudocode or truncated snippets).
3. **Edge Case Handling:** Explicit coverage for boundary conditions, empty inputs, network timeouts, or invalid payloads.
4. **Unit Test Suite:** Comprehensive test cases covering standard operation, edge cases, and error assertions.{extra}

**Output Guidelines:**
Write complete runnable code without leaving "TODO" comments. Include instructions on how to execute and verify the solution locally."""
    return prompt.strip()


def build_study_prompt(idea: str, style_info: dict, instructions: str, variation: int = 0) -> str:
    extra = f"\n- Focus Area / Target Audience: {instructions.strip()}" if instructions else ""
    
    prompt = f"""# Master Learning & Mastery Prompt (Optimized for ChatGPT / Claude / Gemini)

**Role Definition:**
Act as a world-class university professor and pedagogical expert specializing in active learning and the Feynman Technique.

**Subject to Master:**
"{idea.strip()}"

**Instructional Framework:**
Adopt a {style_info['label'].lower()} instructional tone ({style_info['tone']}). Structure your teaching into these clear, progressive steps:

1. **The 30-Second Intuitive Mental Model:**
   Explain the concept in simple English using an intuitive, memorable real-world analogy. Avoid heavy jargon at this stage.

2. **Core Mechanics & First Principles:**
   Deconstruct how it actually works step by step. Highlight the essential rules, components, or mathematical/logical foundations.

3. **Concrete Practical Example:**
   Walk through a complete, realistic scenario or code/math demonstration showing the concept in action from start to finish.

4. **Common Pitfalls & Misconceptions:**
   Identify the top 3 mistakes beginners make when learning this topic, and provide clear rules of thumb to prevent them.

5. **Revision Cheat-Sheet:**
   Provide a bulleted summary of key takeaway facts formatted for quick revision flashcards.

6. **Active Recall Knowledge Check:**
   Conclude with 3 conceptual comprehension questions and 1 practical scenario challenge. Include hidden/foldable answer hints.{extra}

**Goal:**
Make the concept crystal-clear, unforgettable, and immediately actionable for revision."""
    return prompt.strip()


def build_writing_prompt(idea: str, style_info: dict, instructions: str, variation: int = 0) -> str:
    extra = f"\n- Specific Format / Audience Constraints: {instructions.strip()}" if instructions else ""
    
    prompt = f"""# Master Content & Presentation Prompt (Optimized for Claude / ChatGPT / Gemini)

**Role Definition:**
Act as an elite executive communications strategist, speechwriter, and content architect.

**Content Mission:**
Create a compelling, structured, and high-impact deliverable based on:
"{idea.strip()}"

**Tone & Editorial Stance:**
- Style: {style_info['label']} ({style_info['tone']})
- Delivery Style: Clear, rhythmically varied sentences, authoritative yet engaging, high signal-to-noise ratio.

**Structured Content Architecture:**
1. **The Narrative Hook:** An arresting opening statement, surprising insight, or provocative question that instantly commands attention.
2. **Context & Problem Statement:** Clearly frame why this topic matters right now, the tension involved, and what is at stake.
3. **Core Argument & Pillar Insights:** Break the subject into 3 to 4 well-reasoned pillars supported by concrete reasoning, real-world examples, or structured data points.
4. **Key Takeaways / Slide Outline:** If presenting, organize as clean sequential slides with Visual Cue, Headline, Bullet Points, and Speaker Notes.
5. **Memorable Call-to-Action:** A forward-looking conclusion that leaves the audience inspired and ready to act.{extra}

**Format Requirement:**
Format with clean Markdown headers, bullet points, callout quotes, and bold highlights for effortless skimming."""
    return prompt.strip()


def build_custom_prompt(idea: str, style_info: dict, instructions: str, variation: int = 0) -> str:
    extra = f"\n- Additional Parameters: {instructions.strip()}" if instructions else ""
    
    prompt = f"""# Universal Meta-Prompt (Universal AI Task Blueprint)

**System Persona:**
You are an expert AI assistant specializing in high-precision execution with a {style_info['label'].lower()} orientation ({style_info['tone']}).

**Core Objective:**
{idea.strip()}

**Operational Context & Constraints:**
- Tone & Voice: {style_info['tone']}
- Focus: Maintain high factual accuracy, systematic structure, and actionable specificity.
- Formatting: Use structured Markdown headings, numbered sequences, and concise summaries where applicable.{extra}

**Step-by-Step Execution Plan:**
1. **Analysis:** Review the requirements and identify all critical components, variables, and potential edge constraints.
2. **Execution:** Produce the primary solution or deliverable with maximum clarity, omitting unnecessary filler or repetition.
3. **Verification:** Self-critique the output against safety, completeness, and practical utility.

**Final Deliverable Requirement:**
Provide a comprehensive, ready-to-use output that directly fulfills the objective with zero conversational fluff."""
    return prompt.strip()


GENERATORS = {
    "image": build_image_prompt,
    "video": build_video_prompt,
    "website": build_website_prompt,
    "code": build_code_prompt,
    "study": build_study_prompt,
    "writing": build_writing_prompt,
    "custom": build_custom_prompt
}

# ---------------------------------------------------------------------------
# PROMPT QUALITY ANALYZER (Transparent Heuristics)
# ---------------------------------------------------------------------------

def evaluate_prompt_quality(idea: str, generated_prompt: str, category: str, style: str) -> dict:
    """
    Transparent rule-based heuristic scoring (0 - 100).
    Evaluates:
      - Clarity (0-25)
      - Context (0-25)
      - Specificity (0-25)
      - Output Format (0-25)
    Returns breakdown, total score, and up to 3 improvement suggestions.
    """
    text = (idea + " " + generated_prompt).lower()
    idea_words = len(re.findall(r'\w+', idea))
    prompt_words = len(re.findall(r'\w+', generated_prompt))
    
    suggestions = []
    
    # 1. Clarity (0 - 25)
    clarity_score = 15
    action_verbs = ['create', 'generate', 'write', 'build', 'explain', 'design', 'implement', 'analyze', 'summarize', 'show', 'produce']
    found_verbs = [v for v in action_verbs if v in text]
    if len(found_verbs) >= 2:
        clarity_score += 6
    elif len(found_verbs) == 1:
        clarity_score += 3
        
    if idea_words >= 5:
        clarity_score += 4
    else:
        suggestions.append("Add a few more descriptive words to your initial idea to clarify the core objective.")
    clarity_score = min(25, max(10, clarity_score))
    
    # 2. Context (0 - 25)
    context_score = 14
    context_markers = ['role', 'persona', 'audience', 'system', 'background', 'context', 'objective', 'overview', 'setting', 'scenario']
    found_context = [m for m in context_markers if m in text]
    if len(found_context) >= 3:
        context_score += 8
    elif len(found_context) >= 1:
        context_score += 4
        
    if any(k in text for k in ['beginner', 'expert', 'client', 'student', 'user', 'audience', 'visitor']):
        context_score += 3
    else:
        suggestions.append("Explicitly state your target audience or user level (e.g., 'for beginners' or 'enterprise scale').")
    context_score = min(25, max(10, context_score))
    
    # 3. Specificity (0 - 25)
    specificity_score = 15
    specific_keywords = [
        'lighting', 'camera', 'resolution', 'palette', 'architecture', 'responsive',
        'syntax', 'error', 'boundary', 'feynman', 'pitfalls', 'tone', 'slide', 'aspect ratio'
    ]
    found_specifics = [s for s in specific_keywords if s in text]
    if len(found_specifics) >= 3:
        specificity_score += 7
    elif len(found_specifics) >= 1:
        specificity_score += 4
        
    if any(char in generated_prompt for char in ['#', '*', '-', '`']):
        specificity_score += 3
        
    if idea_words < 10 and len(suggestions) < 3:
        suggestions.append("Include specific constraints such as color choices, programming languages, or scene details in 'Additional Instructions'.")
    specificity_score = min(25, max(10, specificity_score))
    
    # 4. Output Format (0 - 25)
    format_score = 16
    has_headers = '#' in generated_prompt
    has_bullets = '-' in generated_prompt or '*' in generated_prompt
    has_code_or_mono = '`' in generated_prompt
    
    if has_headers:
        format_score += 3
    if has_bullets:
        format_score += 3
    if has_code_or_mono:
        format_score += 3
        
    if prompt_words > 120:
        format_score += 3
        
    format_score = min(25, max(10, format_score))
    
    total = clarity_score + context_score + specificity_score + format_score
    total = max(35, min(98, total))
    
    # Rating label
    if total >= 88:
        rating_label = "Exceptional Structure"
    elif total >= 75:
        rating_label = "Strong & Actionable"
    elif total >= 60:
        rating_label = "Good Baseline"
    else:
        rating_label = "Needs Specifics"
        
    # Default friendly suggestion if list is empty
    if not suggestions:
        suggestions.append("Optional: You can copy and customize individual sections in the output text to fit your exact model parameters.")
        
    return {
        "total_score": total,
        "rating_label": rating_label,
        "breakdown": {
            "clarity": clarity_score,
            "context": context_score,
            "specificity": specificity_score,
            "output_format": format_score
        },
        "suggestions": suggestions[:3],
        "disclaimer": "Heuristic estimate based on prompt engineering best practices. It is not an AI judgment or a performance guarantee."
    }

# ---------------------------------------------------------------------------
# EXAMPLE PRESETS
# ---------------------------------------------------------------------------
EXAMPLES = [
    {
        "id": "ex-1",
        "title": "Cinematic Futuristic City",
        "category": "image",
        "category_label": "Image Generation",
        "style": "cinematic",
        "idea": "A sprawling neo-Tokyo metropolis in 2099 at midnight, glowing holographic billboards reflecting in wet asphalt streets, flying vehicles gliding between towering skyscrapers, lone cyberpunk traveler in a luminous trench coat looking up.",
        "instructions": "16:9 widescreen aspect ratio, octane render, vivid cyan and magenta lighting accents, sharp volumetric reflections."
    },
    {
        "id": "ex-2",
        "title": "Coffee Shop Promo Video",
        "category": "video",
        "category_label": "Video Generation",
        "style": "cinematic",
        "idea": "An artisanal specialty coffee shop on a rainy autumn morning: barista pouring silky microfoam latte art into a ceramic cup, warm amber indoor light, steam gently rising, cozy customers reading books in the background.",
        "instructions": "Smooth slow-motion macro shot of the pour, 60fps cinematic pacing, warm color temperature, realistic steam physics."
    },
    {
        "id": "ex-3",
        "title": "Futuristic Portfolio Website",
        "category": "website",
        "category_label": "Website Creation",
        "style": "futuristic",
        "idea": "A personal portfolio website for an AI engineer and creative technologist showcasing interactive 3D project cards, experience timeline, skills radar, and a futuristic terminal-style contact form.",
        "instructions": "Dark midnight glassmorphism theme, glowing neon purple borders, fluid mobile responsiveness, smooth hover animations."
    },
    {
        "id": "ex-4",
        "title": "Explain Python Loops to a Beginner",
        "category": "study",
        "category_label": "Study & Learning",
        "style": "minimal",
        "idea": "Explain how 'for' and 'while' loops work in Python to someone who has never written a single line of code before.",
        "instructions": "Use a clear kitchen recipe or conveyor belt analogy, provide 2 short code snippets, and include a 3-question mini quiz."
    },
    {
        "id": "ex-5",
        "title": "Summarize Study Notes into Revision Points",
        "category": "study",
        "category_label": "Study & Learning",
        "style": "professional",
        "idea": "Summarize a 10-page college lecture on Operating System Process Scheduling (FCFS, SJF, Round Robin, and Priority Scheduling) into high-yield exam revision points.",
        "instructions": "Include a comparative Markdown table with pros/cons/time complexity, plus 4 active recall flashcards."
    },
    {
        "id": "ex-6",
        "title": "Presentation on Artificial Intelligence",
        "category": "writing",
        "category_label": "Writing & Presentation",
        "style": "futuristic",
        "idea": "A 5-minute college presentation about 'The Evolution and Future of Generative AI' highlighting text, image, and autonomous agent breakthroughs.",
        "instructions": "Structure as a 6-slide deck with catchy headlines, 3 talking points per slide, speaker notes, and an inspirational closing question."
    }
]

# ---------------------------------------------------------------------------
# FLASK ROUTES
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    """Serves the main single-page application."""
    return render_template('index.html', examples=EXAMPLES, styles=STYLE_PRESETS)


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Returns the list of 6 curated example prompts."""
    return jsonify({"status": "success", "examples": EXAMPLES})


@app.route('/api/generate', methods=['POST'])
def generate():
    """
    Main prompt generation endpoint.
    Accepts JSON:
      - category: str (image|video|website|code|study|writing|custom)
      - idea: str (user's raw idea)
      - style: str (cinematic|minimal|professional|futuristic|technical|creative)
      - instructions: str (optional additional constraints)
      - variation: int (optional integer to produce subtle phrasing variations)
    """
    try:
        data = request.get_json(silent=True) or {}
        category = str(data.get('category', 'image')).strip().lower()
        idea = str(data.get('idea', '')).strip()
        style = str(data.get('style', 'futuristic')).strip().lower()
        instructions = str(data.get('instructions', '')).strip()
        variation = int(data.get('variation', 0))
    except Exception as e:
        return jsonify({"status": "error", "message": f"Malformed request payload: {str(e)}"}), 400

    # Server-side validation
    if not idea:
        return jsonify({
            "status": "error",
            "message": "Please enter an idea in 'Describe what you want to create...'. An idea is required to generate a prompt."
        }), 400

    if len(idea) > 3000:
        return jsonify({
            "status": "error",
            "message": "Input is too long. Please limit your description to 3,000 characters."
        }), 400

    if len(instructions) > 2000:
        return jsonify({
            "status": "error",
            "message": "Additional instructions are too long. Please limit them to 2,000 characters."
        }), 400

    if category not in GENERATORS:
        category = "custom"

    style_info = STYLE_PRESETS.get(style, STYLE_PRESETS["futuristic"])
    generator_fn = GENERATORS[category]

    try:
        generated_prompt = generator_fn(idea, style_info, instructions, variation)
        quality = evaluate_prompt_quality(idea, generated_prompt, category, style)

        return jsonify({
            "status": "success",
            "data": {
                "category": category,
                "category_label": {
                    "image": "Image Generation",
                    "video": "Video Generation",
                    "website": "Website Creation",
                    "code": "Coding & Software",
                    "study": "Study & Learning",
                    "writing": "Writing & Presentation",
                    "custom": "Custom Meta-Prompt"
                }.get(category, "Universal Prompt"),
                "style": style,
                "style_label": style_info["label"],
                "original_idea": idea,
                "instructions": instructions,
                "generated_prompt": generated_prompt,
                "variation": variation,
                "quality": quality,
                "notice": "PromptCraft AI crafts structured prompts to paste into your favorite AI tool (ChatGPT, Midjourney, Claude, v0, etc.). It does not directly generate the final image, video, or site."
            }
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to generate prompt: {str(e)}"
        }), 500


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    On-demand quality scoring endpoint for customized/edited prompts.
    """
    try:
        data = request.get_json(silent=True) or {}
        prompt = str(data.get('prompt', '')).strip()
        idea = str(data.get('idea', '')).strip()
        category = str(data.get('category', 'custom')).strip().lower()
        style = str(data.get('style', 'futuristic')).strip().lower()

        if not prompt:
            return jsonify({"status": "error", "message": "Prompt content is empty."}), 400

        quality = evaluate_prompt_quality(idea or prompt[:100], prompt, category, style)
        return jsonify({"status": "success", "quality": quality})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/health')
def health():
    """Healthcheck endpoint for hosting providers."""
    return jsonify({"status": "ok", "app": "PromptCraft AI", "version": "1.0.0"})


if __name__ == '__main__':
    # Local development server
    port = int(os.environ.get('PORT', 5000))
    print(f">> PromptCraft AI is launching on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)

