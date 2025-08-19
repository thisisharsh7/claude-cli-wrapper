"""
Enhanced Theme System with Modern Design Theory
Comprehensive theme specifications for CCUI
"""

from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ThemeSpec:
    """Theme specification with design theory backing"""
    name: str
    description: str
    use_cases: List[str]
    target_audience: str
    design_philosophy: str
    visual_characteristics: Dict[str, Any]
    accessibility_priority: str
    implementation_notes: str

# Enhanced Theme System based on Modern Design Theory
THEME_SPECIFICATIONS = {
    
    # EXISTING THEMES (Enhanced)
    "minimal": ThemeSpec(
        name="Minimal",
        description="Clean, content-focused design following Dieter Rams' principles of good design",
        use_cases=[
            "B2B SaaS platforms", 
            "Professional services", 
            "Documentation sites",
            "Portfolio websites"
        ],
        target_audience="Professional users who value efficiency and clarity",
        design_philosophy="Less but better - eliminate visual noise to focus on content and functionality",
        visual_characteristics={
            "color_palette": "Monochromatic with single accent color",
            "typography": "Sans-serif, high readability (Inter, System fonts)",
            "spacing": "Generous whitespace, 8px grid system",
            "components": "Flat design, subtle borders, minimal shadows",
            "interactions": "Subtle hover states, no exaggerated animations",
            "layout": "Grid-based, plenty of breathing room"
        },
        accessibility_priority="AAA compliance - highest readability standards",
        implementation_notes="Focus on typography hierarchy, use system fonts, avoid decorative elements"
    ),
    
    "brutalist": ThemeSpec(
        name="Brutalist",
        description="Raw, honest design inspired by Brutalist architecture - bold and uncompromising",
        use_cases=[
            "Creative agencies",
            "Art portfolios", 
            "Experimental products",
            "Bold brand statements"
        ],
        target_audience="Design-forward users who appreciate bold, unconventional aesthetics",
        design_philosophy="Raw materials, honest construction, bold geometric forms",
        visual_characteristics={
            "color_palette": "High contrast, monochrome with bold accent",
            "typography": "Bold sans-serif, chunky fonts (Helvetica Bold, Arial Black)",
            "spacing": "Tight spacing, overlapping elements, asymmetrical layouts",
            "components": "Sharp edges, no rounded corners, heavy borders",
            "interactions": "Abrupt state changes, no easing animations",
            "layout": "Asymmetrical, overlapping sections, raw grid breaks"
        },
        accessibility_priority="AA compliance with high contrast ratios",
        implementation_notes="Use system fonts at heavy weights, avoid gradients, embrace harsh edges"
    ),
    
    "playful": ThemeSpec(
        name="Playful",
        description="Joyful, approachable design using organic shapes and vibrant colors",
        use_cases=[
            "Consumer apps",
            "Children's products",
            "Entertainment platforms",
            "Creative tools"
        ],
        target_audience="General consumers seeking delightful, engaging experiences",
        design_philosophy="Design should spark joy and create emotional connections",
        visual_characteristics={
            "color_palette": "Bright, saturated colors with rainbow gradients",
            "typography": "Rounded fonts, varied weights (Circular, Nunito)",
            "spacing": "Organic spacing, playful asymmetry",
            "components": "Rounded corners, soft shadows, gradient backgrounds",
            "interactions": "Bouncy animations, micro-interactions, spring physics",
            "layout": "Flowing, organic shapes, circular elements"
        },
        accessibility_priority="AA compliance with careful color contrast management",
        implementation_notes="Use CSS custom properties for color variations, implement spring animations"
    ),
    
    "corporate": ThemeSpec(
        name="Corporate",
        description="Traditional, trustworthy design following established business conventions",
        use_cases=[
            "Financial services",
            "Healthcare",
            "Government",
            "Enterprise software"
        ],
        target_audience="Business professionals requiring trust and reliability signals",
        design_philosophy="Established patterns that convey competence and trustworthiness",
        visual_characteristics={
            "color_palette": "Blue-based, conservative palette",
            "typography": "Traditional serif/sans combinations (Georgia, Arial)",
            "spacing": "Structured grid, consistent margins",
            "components": "Traditional buttons, formal layouts, subtle shadows",
            "interactions": "Conservative animations, predictable patterns",
            "layout": "Hierarchical, left-to-right reading flow"
        },
        accessibility_priority="WCAG 2.1 AA compliance minimum",
        implementation_notes="Use established UI patterns, avoid experimental layouts"
    ),
    
    # NEW THEMES (Based on Modern Design Theory)
    "morphism": ThemeSpec(
        name="Morphism",
        description="Soft, tactile design combining neumorphism and glassmorphism principles",
        use_cases=[
            "Mobile apps",
            "Design portfolios",
            "Premium products",
            "UI/UX showcases"
        ],
        target_audience="Design enthusiasts and users of premium digital products",
        design_philosophy="Skeuomorphic elements that feel tangible in digital space",
        visual_characteristics={
            "color_palette": "Soft, muted backgrounds with subtle color shifts",
            "typography": "Soft, rounded fonts (SF Pro, Poppins)",
            "spacing": "Generous padding for tactile feel",
            "components": "Inset/outset shadows, glass effects, soft borders",
            "interactions": "Pressure-sensitive animations, depth changes",
            "layout": "Layered depth, floating elements"
        },
        accessibility_priority="AA compliance with careful contrast on glass elements",
        implementation_notes="Multiple box-shadows for depth, backdrop-filter for glass effects, avoid overuse"
    ),
    
    "animated": ThemeSpec(
        name="Animated",
        description="Motion-first design where animation drives user experience and storytelling",
        use_cases=[
            "Interactive storytelling",
            "Product launches",
            "Creative portfolios",
            "Brand experiences"
        ],
        target_audience="Users seeking engaging, immersive digital experiences",
        design_philosophy="Motion as a design material - guiding attention and creating narrative",
        visual_characteristics={
            "color_palette": "Dynamic colors that change with interactions",
            "typography": "Fonts that support animation (Variable fonts, Web fonts)",
            "spacing": "Fluid spacing that adapts to motion",
            "components": "Elements designed for transformation",
            "interactions": "Choreographed animations, gesture-based interactions",
            "layout": "Scenes that transform based on scroll/interaction"
        },
        accessibility_priority="AA compliance with respect for prefers-reduced-motion",
        implementation_notes="Use CSS animations and transforms, implement proper motion preferences, optimize for performance"
    ),
    
    "terminal": ThemeSpec(
        name="Terminal",
        description="Monospace, CLI-inspired aesthetic appealing to developers and tech enthusiasts",
        use_cases=[
            "Developer tools",
            "Technical documentation",
            "API platforms",
            "Hacker/security tools"
        ],
        target_audience="Developers, system administrators, tech-savvy users",
        design_philosophy="Embrace the aesthetic of command-line interfaces and terminal applications",
        visual_characteristics={
            "color_palette": "Terminal colors: green/amber text on dark backgrounds",
            "typography": "Monospace fonts only (Fira Code, JetBrains Mono)",
            "spacing": "Character-grid based spacing",
            "components": "ASCII art elements, code-block styling",
            "interactions": "Typewriter animations, cursor blinking effects",
            "layout": "Terminal window metaphors, fixed-width layouts"
        },
        accessibility_priority="High contrast mode support, screen reader optimization",
        implementation_notes="Use CSS ch units for spacing, implement typewriter effects, include ASCII art"
    ),
    
    "aesthetic": ThemeSpec(
        name="Aesthetic",
        description="Retro-futuristic design drawing from Y2K, vaporwave, and cyber aesthetics",
        use_cases=[
            "Creative platforms",
            "Music/entertainment",
            "Fashion brands",
            "Art communities"
        ],
        target_audience="Gen Z and millennial users interested in nostalgic digital culture",
        design_philosophy="Nostalgic digital aesthetics reimagined for modern interfaces with modern usability standards",
        visual_characteristics={
            "color_palette": "Dark base (navy/black) with bright neon accents (cyan, magenta, electric blue) for high contrast",
            "typography": "Retro futuristic fonts with excellent readability - white/cyan text on dark backgrounds",
            "spacing": "Modern grid with retro visual elements, generous padding for readability",
            "components": "Neon-outlined components on dark backgrounds, high-contrast interactive states",
            "interactions": "Subtle neon glow effects that enhance rather than reduce readability",
            "layout": "Dark theme with bright accent colors, ensure 4.5:1 minimum contrast ratio"
        },
        accessibility_priority="WCAG AA compliance with high contrast ratios - all text must meet 4.5:1 contrast minimum",
        implementation_notes="CRITICAL: Use dark backgrounds (rgb(15,23,42) or darker) with bright neon text. Never use light backgrounds with light text. Test all color combinations for WCAG compliance. Neon effects should be additive, not replacing proper contrast."
    ),
    
    # ADDITIONAL THEMES
    "dark": ThemeSpec(
        name="Dark",
        description="Modern dark theme optimized for contrast and reduced eye strain",
        use_cases=[
            "Developer tools",
            "Creative portfolios",
            "Entertainment platforms",
            "Productivity apps"
        ],
        target_audience="Night-owl users, developers, gamers, and professionals",
        design_philosophy="Focus on content with reduced luminance for comfort and contrast",
        visual_characteristics={
            "color_palette": "Dark grays and blacks with bright accent colors (teal, purple, green)",
            "typography": "Sans-serif fonts with high readability (Inter, Roboto)",
            "spacing": "Balanced spacing to maintain clarity in dark backgrounds",
            "components": "High-contrast buttons, glowing outlines, subtle elevation",
            "interactions": "Smooth transitions, glowing hover effects",
            "layout": "Dark surfaces with accent highlights"
        },
        accessibility_priority="WCAG AA - focus on 4.5:1 contrast minimum",
        implementation_notes="Always test color contrast, avoid low-contrast grays on dark backgrounds"
    ),

    "vibrant": ThemeSpec(
        name="Vibrant",
        description="Colorful, dopamine-rich design that energizes user interactions",
        use_cases=[
            "Marketing websites",
            "Consumer products",
            "Music apps",
            "Startups"
        ],
        target_audience="Younger audiences, casual consumers, users seeking fun experiences",
        design_philosophy="Bright, bold colors that evoke excitement and energy",
        visual_characteristics={
            "color_palette": "Dopamine-boosting gradients (purple-pink, orange-teal)",
            "typography": "Bold, expressive fonts (Montserrat, Gilroy)",
            "spacing": "Dynamic spacing with asymmetry for energy",
            "components": "Colorful buttons, gradient backgrounds, shadow pops",
            "interactions": "Animated gradients, hover glows, micro-motions",
            "layout": "Hero-first layouts with bold CTA focus"
        },
        accessibility_priority="AA compliance with careful balance of bright colors",
        implementation_notes="Use CSS gradients, avoid oversaturation, test text over gradients"
    ),

    "sustainable": ThemeSpec(
        name="Sustainable",
        description="Nature-inspired design emphasizing eco-conscious branding",
        use_cases=[
            "Environmental organizations",
            "Eco-products",
            "Sustainable brands",
            "Wellness platforms"
        ],
        target_audience="Eco-conscious consumers and businesses promoting sustainability",
        design_philosophy="Natural, calm aesthetics that convey environmental awareness",
        visual_characteristics={
            "color_palette": "Greens, browns, muted earth tones",
            "typography": "Clean, organic fonts (Lora, Poppins)",
            "spacing": "Ample whitespace for calm, airy layouts",
            "components": "Soft corners, natural textures, leaf-like motifs",
            "interactions": "Gentle fades, smooth transitions, nature-inspired patterns",
            "layout": "Grounded, natural hierarchy with open layouts"
        },
        accessibility_priority="AA compliance ensuring readability against muted palettes",
        implementation_notes="Avoid neon greens, prefer muted natural palettes with contrast"
    ),

    "data": ThemeSpec(
        name="Data",
        description="Information-dense design optimized for dashboards and analytics",
        use_cases=[
            "Analytics dashboards",
            "Finance apps",
            "Enterprise SaaS",
            "Developer tools"
        ],
        target_audience="Data-driven professionals, analysts, and technical teams",
        design_philosophy="Clarity and efficiency in presenting high-density information",
        visual_characteristics={
            "color_palette": "Blue/gray neutral palettes with strong accent colors for data highlights",
            "typography": "Readable sans-serif fonts (Roboto, IBM Plex Sans)",
            "spacing": "Tight grid-based spacing for dense data presentation",
            "components": "Charts, tables, cards with strong visual hierarchy",
            "interactions": "Hover tooltips, interactive filtering, sorting transitions",
            "layout": "Modular grid layouts optimized for data clarity"
        },
        accessibility_priority="AAA compliance for clarity in dense information",
        implementation_notes="Ensure chart colors are colorblind-safe, provide text alternatives"
    ),

    "illustrated": ThemeSpec(
        name="Illustrated",
        description="Hand-drawn, custom illustration-driven design for humanized experiences",
        use_cases=[
            "Creative startups",
            "Onboarding flows",
            "Educational platforms",
            "Community websites"
        ],
        target_audience="Casual users, students, creative professionals",
        design_philosophy="Bring warmth and personality through illustration and character",
        visual_characteristics={
            "color_palette": "Soft pastels with playful accents",
            "typography": "Rounded, friendly fonts (Nunito, Quicksand)",
            "spacing": "Organic spacing with flowing shapes",
            "components": "Illustration-heavy components, custom icons",
            "interactions": "Playful micro-interactions, onboarding animations",
            "layout": "Centered layouts, storytelling through visuals"
        },
        accessibility_priority="AA compliance, careful to not rely on illustrations for meaning",
        implementation_notes="SVG illustrations should be lightweight, use Lottie for animations"
    )
}

def get_theme_design_system_rules(theme_name: str) -> str:
    """Generate theme-specific design system rules for prompts"""
    if theme_name not in THEME_SPECIFICATIONS:
        return ""
    
    theme = THEME_SPECIFICATIONS[theme_name]
    
    return f"""
THEME-SPECIFIC DESIGN SYSTEM RULES FOR {theme.name.upper()}:

Philosophy: {theme.design_philosophy}
Target Use: {', '.join(theme.use_cases[:2])}

Visual Requirements:
- Colors: {theme.visual_characteristics['color_palette']}
- Typography: {theme.visual_characteristics['typography']}
- Spacing: {theme.visual_characteristics['spacing']}
- Components: {theme.visual_characteristics['components']}
- Interactions: {theme.visual_characteristics['interactions']}
- Layout: {theme.visual_characteristics['layout']}

Accessibility: {theme.accessibility_priority}
Implementation Notes: {theme.implementation_notes}

CRITICAL: All design tokens must align with these {theme.name} theme characteristics.
"""

def get_theme_choices() -> List[str]:
    """Get all available theme names"""
    return list(THEME_SPECIFICATIONS.keys())

def get_theme_description(theme_name: str) -> str:
    """Get theme description for CLI help"""
    if theme_name not in THEME_SPECIFICATIONS:
        return "Unknown theme"
    
    theme = THEME_SPECIFICATIONS[theme_name]
    return f"{theme.description}"

def detect_theme_from_content(content: str) -> str:
    """Enhanced theme detection from HTML/CSS content with priority-based scoring"""
    content_lower = content.lower()
    
    # Specific theme patterns with higher priority checks first
    
    # 1. Brutalist (check before dark theme since both use bg-black)
    brutalist_score = 0
    if 'brutalist-border' in content_lower: brutalist_score += 10
    if 'brutalist-shadow' in content_lower: brutalist_score += 10
    if 'font-black' in content_lower: brutalist_score += 5
    if 'font-bold uppercase' in content_lower: brutalist_score += 3
    if 'bg-red-600' in content_lower and 'bg-yellow-400' in content_lower: brutalist_score += 5
    if 'jetbrains mono' in content_lower: brutalist_score += 3
    
    # 2. Morphism
    morphism_score = 0
    if 'backdrop-filter' in content_lower: morphism_score += 10
    if 'glassmorphism' in content_lower: morphism_score += 10
    if 'neumorphism' in content_lower: morphism_score += 10
    if 'bg-white/20' in content_lower or 'bg-opacity-' in content_lower: morphism_score += 5
    
    # 3. Terminal
    terminal_score = 0
    if 'font-mono' in content_lower: terminal_score += 5
    if 'text-green-400' in content_lower or 'text-green-500' in content_lower: terminal_score += 5
    if 'border-green-500' in content_lower: terminal_score += 5
    if 'animate-pulse' in content_lower and 'green' in content_lower: terminal_score += 3
    if 'terminal' in content_lower: terminal_score += 3
    
    # 4. Playful
    playful_score = 0
    if 'rounded-xl' in content_lower or 'rounded-2xl' in content_lower: playful_score += 5
    if 'bg-pink-' in content_lower or 'bg-purple-' in content_lower: playful_score += 5
    if 'hover:scale-' in content_lower: playful_score += 3
    if 'gradient' in content_lower and ('pink' in content_lower or 'purple' in content_lower): playful_score += 5
    
    # 5. Corporate
    corporate_score = 0
    if 'bg-blue-900' in content_lower or 'bg-blue-800' in content_lower: corporate_score += 5
    if 'shadow-lg' in content_lower or 'shadow-xl' in content_lower: corporate_score += 3
    if 'corporate' in content_lower or 'professional' in content_lower: corporate_score += 5
    
    # 6. Dark theme (check after brutalist to avoid conflicts)
    dark_score = 0
    if ('dark' in content_lower and 'theme' in content_lower): dark_score += 10
    if 'bg-gray-900' in content_lower: dark_score += 5
    if 'text-gray-100' in content_lower or 'text-white' in content_lower: dark_score += 3
    if 'border-gray-700' in content_lower: dark_score += 3
    
    # Return theme with highest score
    scores = {
        'brutalist': brutalist_score,
        'morphism': morphism_score,
        'terminal': terminal_score,
        'playful': playful_score,
        'corporate': corporate_score,
        'dark': dark_score
    }
    
    # Get theme with highest score (minimum threshold of 5)
    max_theme = max(scores, key=scores.get)
    if scores[max_theme] >= 5:
        return max_theme
    
    # Fallback patterns for other themes
    if 'neon' in content_lower or 'cyber' in content_lower or 'retro' in content_lower:
        return 'aesthetic'
    elif 'vibrant' in content_lower or 'dopamine' in content_lower:
        return 'vibrant'
    elif 'sustainable' in content_lower or 'eco' in content_lower:
        return 'sustainable'
    elif 'data' in content_lower or 'dashboard' in content_lower or 'analytics' in content_lower:
        return 'data'
    elif 'illustrated' in content_lower or 'illustration' in content_lower:
        return 'illustrated'
    elif 'animation' in content_lower and ('transform' in content_lower or 'keyframes' in content_lower):
        return 'animated'
    else:
        return 'minimal'