
from textwrap import dedent
import os
from typing import List, Tuple, Dict

def reference_discovery_prompt(desc: str) -> str:
    return f"Given this product: '{desc}', find 3 live product URLs of similar tools. Only list working websites, not blogs. Format: Name – URL – short note."


def deep_product_understanding_prompt(desc: str) -> str:
    return f'JSON analysis of product: {desc}\n{{"problem":"Core issue","user":"Who needs it","differentiator":"Why not existing","best_feature":"Most loved","risks":"Possible failure reasons"}}\nRules: Be concise, no fluff, focus on user pain.'


def ux_analysis_prompt(product_desc: str, refs: List[str]) -> str:
    refs_text = "\n".join(
        f"- {screenshot_path.split('/')[-1]}" for screenshot_path in refs
    )

    return f'''UX competitive analysis of: {product_desc}

Read and analyze the following screenshots for UX patterns:
{refs_text}

Respond in JSON:
{{
  "patterns": {{
    "navigation": ["..."],
    "ctas": ["..."],
    "layouts": ["..."],
    "messaging": ["..."]
  }},
  "differentiators": [{{"screenshot":"...","element":"...","why":"..."}}],
  "weaknesses": {{
    "common": ["..."],
    "severe": ["..."]
  }},
  "recommendations": {{
    "adopt": ["..."],
    "avoid": ["..."],
    "innovate": ["..."]
  }},
  "summary": "1-2 sentence takeaway"
}}
Rules: Be concise, specific, mobile-first.'''


def empathize_prompt(product_desc: str, product_understanding: Dict, ux_analysis: Dict) -> str:
    short_problem = str(product_understanding.get("problem", "N/A"))[:200]
    short_user = str(product_understanding.get("user", "N/A"))[:200]
    short_diff = str(product_understanding.get("differentiator", "N/A"))[:200]
    
    nav_patterns = ux_analysis.get("patterns", {}).get("navigation", [])
    adopt = ux_analysis.get("recommendations", {}).get("adopt", [])
    avoid = ux_analysis.get("recommendations", {}).get("avoid", [])
    return f'''Product: {product_desc}

Understanding (trimmed):
- Problem: {short_problem}
- User: {short_user}
- Differentiator: {short_diff}

UX Insights:
- Navigation patterns: {nav_patterns}
- Adopt: {adopt}
- Avoid: {avoid}

Output JSON only:
{{
  "context": {{
    "device": "...",
    "channels": ["...", "...", "..."],
    "immediate_need": "..."
  }},
  "questions": {{
    "identity": ["...", "..."],
    "value": ["...", "..."],
    "trust": ["...", "..."]
  }},
  "conversion": {{
    "primary": "...",
    "secondary": ["...", "..."],
    "required_info": ["...", "..."]
  }},
  "personas": [
    {{
      "name": "...",
      "role": "...",
      "urgency": "...",
      "decision_process": "...",
      "content_needs": ["...", "..."]
    }}
  ],
  "touchpoints": {{
    "first_impression": "...",
    "dropoff_risk": "...",
    "persuasive_element": "..."
  }},
  "research_gaps": ["...", "..."]
}}
Rules: Be concise, quote user questions, focus on behaviors.'''


def define_prompt(product_desc, user_research) -> str:
    return f'''Product: {product_desc}

Research:
- Goal: {user_research.get("conversion",{}).get("primary","N/A")}
- Context: {user_research.get("context",{}).get("immediate_need","N/A")}
- Questions: {user_research.get("questions",{}).get("value",[])}
- Personas: {[p.get("name","N/A")+" ("+p.get("role","")+")" for p in user_research.get("personas",[])]}

Output JSON only:
{{
  "core_pages": {{
    "homepage": {{"job":"...","must_show":["...","..."],"next_step":"..."}},
    "key_secondary": [{{"page":"...","job":"...","exit_risk":"...","recovery":"..."}}]
  }},
  "primary_flow": {{
    "steps":["...","...","..."],
    "dropoff_points":["...","..."],
    "support_elements":["...","..."]
  }},
  "alternate_paths": {{
    "price_concerns":"...",
    "trust_issues":"...",
    "feature_questions":"..."
  }},
  "navigation": {{
    "global_nav":["...","...","..."],
    "mobile_priority":"...",
    "footer_strategy":"..."
  }},
  "conflicts":["...","..."],
  "research_gaps":["...","..."]
}}
Rules: Be concrete, use UI elements, flag conflicts, note missing research.'''

def ideate_prompt(product_desc, user_research, site_flow) -> str:
    return f'''Product: {product_desc}

Research:
- Goal: {user_research.get("conversion",{}).get("primary","N/A")}
- Questions: {user_research.get("questions",{}).get("value",[])}
- Homepage Must Show: {site_flow.get("core_pages",{}).get("homepage",{}).get("must_show",[])}
- Primary Flow: {site_flow.get("primary_flow",{}).get("steps",[])}

Output JSON only:
{{
  "core_messaging": {{
    "value_proposition": "...",
    "unique_angle": "..."
  }},
  "hero": {{
    "headline": "...",
    "subhead": "...",
    "primary_cta": "...",
    "supporting_element": "..."
  }},
  "benefits": [
    {{"headline":"...","proof_point":"...","icon_concept":"..."}},
    {{"headline":"...","proof_point":"...","icon_concept":"..."}},
    {{"headline":"...","proof_point":"...","icon_concept":"..."}}
  ],
  "objections": {{
    "top_3_concerns": ["...","...","..."],
    "faq_answers": [{{"question":"...","answer":"..."}}],
    "trust_elements": ["...","..."]
  }},
  "ctas": {{
    "primary_action":"...",
    "secondary_action":"...",
    "microcopy":"..."
  }},
  "rules": {{
    "tone":"...",
    "avoid":["...","..."],
    "must_include":["...","..."]
  }}
}}
Rules: Be concise, outcome-focused, use real user wording where possible.'''

def wireframe_prompt(product_desc, content_strategy, site_flow) -> str:
    return f'''Product: {product_desc}

Content:
- Hero: {content_strategy.get("hero",{}).get("headline","N/A")}
- Benefits: {[b.get("headline","N/A") for b in content_strategy.get("benefits",[])]}
- CTA: {content_strategy.get("ctas",{}).get("primary_action","N/A")}

Flow:
- Pages: {list(site_flow.get("core_pages",{}).keys())}
- Nav Priority: {site_flow.get("navigation",{}).get("mobile_priority","N/A")}

Output JSON only:
{{
  "layout": {{
    "sections": [
      {{"name":"hero","elements":["..."],"mobile_stack":["..."],"priority":"..."}},
      {{"name":"benefits","elements":["..."],"mobile_stack":["..."],"priority":"..."}}
    ]
  }},
  "mobile_checks": {{
    "critical":["...","...","..."],
    "red_flags":["...","..."]
  }},
  "interactions": {{
    "key":[{{"element":"...","behavior":"...","mobile_consideration":"..."}}]
  }},
  "responsive": {{
    "breakpoints": {{
      "mobile": {{"rules":["...","..."]}},
      "tablet": {{"rules":["...","..."]}}
    }}
  }}
}}
Rules: Be concise, mobile-first, ensure CTA always visible.'''


def design_system_prompt(product_desc, wireframes, content_strategy) -> str:
    return f'''Product: {product_desc}

Wireframes:
- Sections: {[s.get("name","N/A") for s in wireframes.get("layout",{}).get("sections",[])]}
- Mobile Checks: {wireframes.get("mobile_checks",{}).get("critical",[])}

Tone: {content_strategy.get("rules",{}).get("tone","Professional")}

Output JSON only:
{{
  "typography": {{
    "typeface_choice": "...",
    "brand_rationale": "...",
    "heading_hierarchy": {{"h1":"...","h2":"...","h3":"..."}},
    "body_text": "..."
  }},
  "color_tokens": {{
    "primary":"#...","primary_light":"#...","primary_dark":"#...",
    "secondary":"#...","accent":"#...","surface":"#...","background":"#...",
    "success":"#...","warning":"#...","error":"#...",
    "text_primary":"#...","text_secondary":"#...","text_muted":"#...",
    "border":"#...","border_light":"#...","shadow":"#..."
  }},
  "gradients": {{
    "primary_gradient":"linear-gradient(135deg, #... 0%, #... 100%)",
    "hero_gradient":"linear-gradient(180deg, #... 0%, #... 100%)",
    "card_gradient":"linear-gradient(145deg, #... 0%, #... 100%)",
    "button_gradient":"linear-gradient(135deg, #... 0%, #... 100%)"
  }},
  "shadows": {{
    "card_shadow":"0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06)",
    "button_shadow":"0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05)",
    "hover_shadow":"0 20px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04)"
  }},
  "animations": {{
    "duration": {{"fast":"150ms","normal":"300ms","slow":"500ms"}},
    "easing": {{"ease_in":"cubic-bezier(0.4, 0, 1, 1)","ease_out":"cubic-bezier(0, 0, 0.2, 1)","ease_in_out":"cubic-bezier(0.4, 0, 0.2, 1)"}},
    "transforms": {{"scale_hover":"scale(1.05)","scale_click":"scale(0.95)","lift":"translateY(-2px)"}}
  }},
  "wcag_contrast": {{
    "primary_cta":"X.X:1 - PASS/FAIL",
    "body_text":"X.X:1 - PASS/FAIL",
    "secondary_text":"X.X:1 - PASS/FAIL",
    "error_text":"X.X:1 - PASS/FAIL",
    "accessible":"true/false"
  }},
  "signature_elements": [
    {{"element":"...","specification":"...","usage":"..."}},
    {{"element":"...","specification":"...","usage":"..."}}
  ],
  "components": {{
    "buttons": {{
      "primary":{{"default":"...","hover":"...","active":"...","disabled":"...","animation":"transform 300ms ease-out"}},
      "secondary":{{"default":"...","hover":"...","active":"...","disabled":"...","animation":"all 200ms ease-in-out"}},
      "ghost":{{"default":"...","hover":"...","active":"...","disabled":"...","animation":"all 150ms ease-in-out"}}
    }},
    "inputs": {{
      "text_field":{{"default":"...","focus":"...","error":"...","animation":"border-color 200ms ease-in-out"}},
      "select":{{"default":"...","focus":"...","hover":"...","animation":"all 150ms ease-out"}},
      "textarea":{{"default":"...","focus":"...","error":"...","animation":"border-color 200ms ease-in-out"}}
    }},
    "cards": {{
      "content":{{"default":"...","hover":"...","animation":"transform 300ms ease-out, box-shadow 300ms ease-out"}},
      "pricing":{{"default":"...","hover":"...","featured":"...","animation":"transform 200ms ease-in-out"}},
      "testimonial":{{"default":"...","hover":"...","animation":"all 250ms ease-out"}}
    }}
  }},
  "spacing_system": {{"scale":["2px","4px","8px","12px","16px","24px","32px","48px","64px","96px"],"usage":"..."}},
  "border_radius": {{"sm":"4px","md":"8px","lg":"12px","xl":"16px","2xl":"24px","full":"9999px"}},
  "svg_patterns": {{
    "hero_bg":"Complex geometric SVG background pattern with subtle animation",
    "section_divider":"Organic wave or curve SVG divider between sections",
    "decorative_elements":"Abstract shapes, dots, or lines for visual interest"
  }},
  "logo_concept": {{
    "style":"Modern, minimal, geometric/organic",
    "elements":"Icon + wordmark or symbol only",
    "colors":"Uses primary brand colors",
    "usage":"Header, footer, favicon"
  }},
  "summary": "..."
}}
Rules: Modern, animated, gradient-rich, high-contrast, mobile-optimized, includes SVG patterns and logo concept.'''


def high_fidelity_design_prompt(product_desc, design_system, wireframes, content_strategy) -> str:
    return f'''Product: {product_desc}

System:
- Typography: {design_system.get("typography",{}).get("typeface_choice","N/A")}
- Primary Color: {design_system.get("color_tokens",{}).get("primary","N/A")}
- Signature Elements: {[e.get("element","N/A") for e in design_system.get("signature_design_elements",[])]}

Wireframes: {[s.get("name","N/A") for s in wireframes.get("layout",{}).get("sections",[])]}
Tone: {content_strategy.get("rules",{}).get("tone","Professional")}

Output JSON only:
{{
  "design_specifications": {{
    "typography": "...",
    "colors": "...",
    "spacing": "...",
    "components": "..."
  }},
  "interactions": {{
    "hover_states": "...",
    "transitions": "...",
    "responsive": "..."
  }},
  "accessibility": {{
    "contrast": "...",
    "typography": "...",
    "navigation": "..."
  }},
  "implementation_ready": "..."
}}
Rules: Be clean, consistent, accessible, mobile-first.'''


def prototype_prompt(product_desc, content_strategy, design_system, wireframes) -> str:
    return f'''Product: {product_desc}

Content:
- Value Proposition: {content_strategy.get("core_messaging",{}).get("value_proposition","N/A")}
- Hero: {content_strategy.get("hero",{}).get("headline","N/A")}
- CTA: {content_strategy.get("ctas",{}).get("primary_action","N/A")}
- Tone: {content_strategy.get("rules",{}).get("tone","Professional")}

Design:
- Sections: {[s.get("name","N/A") for s in wireframes.get("layout",{}).get("sections",[])]}
- Personality: {design_system.get("typography",{}).get("brand_rationale","Modern and clean")}

Output JSON only:
{{
  "hero": {{"headline":"...","subheadline":"...","cta_primary":"...","cta_secondary":"..."}},
  "problem": {{"headline":"...","description":"...","pain_points":["...","...","..."]}},
  "solution": {{"headline":"...","value_proposition":"...","key_benefits":["...","...","..."]}},
  "features": {{"headline":"...","features":[{{"title":"...","description":"...","benefit":"..."}}]}},
  "social_proof": {{"headline":"...","testimonial":"...","stats":["...","...","..."]}},
  "pricing": {{"headline":"...","plan_name":"...","price":"...","features":["...","..."],"cta":"..."}},
  "footer": {{"cta_headline":"...","cta_description":"...","cta_button":"..."}}
}}
Rules: Use AIDA/PAS style, focus on benefits, strong CTAs, address objections, keep tone consistent.'''

def implementation_prompt(product_description, copy_content, framework, theme, design_data) -> str:
    # Extract key insights concisely
    colors = design_data.get('design_system', {}).get('color_tokens', {})
    gradients = design_data.get('design_system', {}).get('gradients', {})
    shadows = design_data.get('design_system', {}).get('shadows', {})
    animations = design_data.get('design_system', {}).get('animations', {})
    svg_patterns = design_data.get('design_system', {}).get('svg_patterns', {})
    logo_concept = design_data.get('design_system', {}).get('logo_concept', {})
    
    primary_color = colors.get('primary', '#3B82F6')
    typography = design_data.get('design_system', {}).get('typography', {}).get('typeface_choice', 'Inter')
    
    # Key UX patterns from competitive analysis
    ux_adopt = design_data.get('ux_analysis', {}).get('recommendations', {}).get('adopt', [])[:2]
    ux_avoid = design_data.get('ux_analysis', {}).get('recommendations', {}).get('avoid', [])[:2]
    
    # Mobile wireframe priorities
    mobile_critical = design_data.get('wireframes', {}).get('mobile_checks', {}).get('critical', [])[:3]
    
    return f'''You are a senior frontend engineer + modern UX designer. Build a stunning, high-conversion landing page with modern design trends.

Product: {product_description}
Copy (use verbatim, no edits): {copy_content}
Framework: {framework}
Theme: {theme}

Design System:
- Primary Color: {primary_color}
- Typography: {typography}
- Gradients: {gradients}
- Shadows: {shadows}
- Animations: {animations}
- SVG Patterns: {svg_patterns}
- Logo Concept: {logo_concept}
- UX Adopt: {ux_adopt}
- UX Avoid: {ux_avoid}
- Mobile Critical: {mobile_critical}

Output: CODE ONLY (full, runnable). No commentary.

Requirements:
- **Modern Visual Design**: Gradient backgrounds, glass morphism effects, custom SVG patterns, subtle animations
- **Logo & Branding**: Generate inline SVG logo based on logo concept, use in header/footer
- **Advanced Animations**: Smooth transitions (300ms ease-out), hover effects (scale/lift), scroll-triggered animations
- **Rich Components**: Interactive cards with hover shadows, gradient buttons, animated CTAs
- **Visual Hierarchy**: Large typography scale (48px+ headings), generous whitespace, clear content flow
- **Background Patterns**: Custom SVG backgrounds, geometric shapes, organic curves between sections
- **Color Depth**: Use full gradient palette, shadows for depth, borders for definition
- **Micro-interactions**: Button hover states, form focus animations, loading states
- **Modern Layouts**: CSS Grid, Flexbox, asymmetric layouts where appropriate
- **Enhanced Images**: High-quality hero images, testimonial avatars, feature icons (all with proper fallbacks)

Technical Requirements:
- Accessibility: semantic HTML, ARIA as needed, alt text; WCAG AA (4.5:1)
- Layout: mobile-first responsive, clear hierarchy (Z-pattern), generous spacing
- Performance: lazy-load images, minimize CLS, optimized animations (transform/opacity only)
- Meta: viewport, description, Open Graph, Twitter cards, schema markup
- Standards: Modern CSS (Grid, Flexbox, Custom Properties), ES6+, HTML5

Visual Standards:
- Use CSS custom properties for design system tokens
- Implement smooth scroll behavior and focus management
- Add subtle parallax or scroll effects where appropriate
- Include loading states and empty states for better UX
- Use proper typography scale and vertical rhythm

Deliver:
- ONLY the complete, production-ready {framework} code with inline styles
- Include all modern design elements: gradients, animations, SVG backgrounds, custom logo
- Ensure visual impact that stands out from basic templates'''

def landing_prompt(product_description, framework, theme, sections, design_data=None) -> str:
    sections_str = ", ".join(sections) if sections else "hero, features, pricing, footer"
    fw = (framework or "html").lower()
    is_react = fw == "react"
    out = "One React file (App.jsx) plus minimal index.html shell." if is_react else "One complete index.html."
    
    # Extract key insights if design_data available
    design_context = ""
    if design_data:
        primary_cta = design_data.get('content_strategy', {}).get('ctas', {}).get('primary_action', 'Get Started')
        value_prop = design_data.get('content_strategy', {}).get('core_messaging', {}).get('value_proposition', '')[:100]
        primary_color = design_data.get('design_system', {}).get('color_tokens', {}).get('primary', '#3B82F6')
        ux_adopt = design_data.get('ux_analysis', {}).get('recommendations', {}).get('adopt', [])[:2]
        
        design_context = f"""
Strategic Context:
- Primary CTA: {primary_cta}
- Value Prop: {value_prop}
- Brand Color: {primary_color}
- UX Patterns: {ux_adopt}"""

    return f'''You are a senior frontend engineer + modern UX designer.

Goal: Build a stunning, conversion-optimized landing page for: {product_description}
Framework: {fw}; Theme: {theme}{design_context}

Modern Design Requirements:
- **Visual Impact**: Gradient backgrounds, subtle animations, custom SVG patterns, glass morphism
- **Typography**: Large, bold headings (48px+), proper hierarchy, readable line spacing
- **Logo & Branding**: Create inline SVG logo matching the product theme
- **Animations**: Smooth transitions (300ms), hover effects (transform/scale), scroll-triggered animations  
- **Components**: Interactive cards with shadows, gradient buttons, animated CTAs, form validation
- **Backgrounds**: Custom SVG patterns, organic shapes, section dividers, geometric elements
- **Colors**: Rich gradients, proper shadows, depth through layering
- **Images**: High-quality placeholders, proper aspect ratios, lazy loading

Technical Requirements:
- **UX Heuristics**: Large CTAs (Fitts), simple nav (Hick), clear hierarchy, generous whitespace
- **Accessibility**: Semantic HTML, ARIA labels, alt text, WCAG AA contrast (4.5:1)
- **Responsive**: Mobile-first CSS Grid/Flexbox, fluid typography, touch-friendly targets
- **Performance**: Lazy-load images, minimize CLS, optimized animations (transform/opacity only)
- **Modern Standards**: CSS custom properties, ES6+, proper meta tags, schema markup

Content & Structure:
- **Sections**: {sections_str} (with modern styling and animations)
- **Copy**: Benefit-focused, conversion-optimized, no lorem ipsum
- **Images**: Unsplash/Picsum high-quality images with descriptive alt text
- **CTAs**: Multiple conversion points, A/B tested button styles

Visual Style Guide:
- Use CSS custom properties for consistent design tokens
- Implement smooth scroll and focus management
- Add micro-interactions for better engagement
- Include loading and empty states
- Apply proper vertical rhythm and spacing scale

Output:
- {out}
- CODE ONLY with all modern design elements integrated
- Ensure it looks premium and stands out from basic templates'''

def regeneration_prompt(product_desc: str, framework: str, theme: str, section_list: List[str], existing_context: Dict = None) -> str:
    """Generate prompt for regenerating specific sections of a landing page"""
    sections_str = ", ".join(section_list)
    fw = (framework or "html").lower()
    
    context_info = ""
    if existing_context:
        context_info = f"""
Existing Page Context:
- Theme: {existing_context.get('theme', theme)}
- Framework: {existing_context.get('framework', framework)}
- Other sections: {existing_context.get('other_sections', 'Maintain consistency with existing sections')}"""
    
    return f'''You are a senior frontend developer updating a landing page by regenerating specific sections with enhanced visuals.

Context:
- Product: {product_desc}
- Framework: {fw}
- Theme: {theme}
- Sections to regenerate: {sections_str}{context_info}

CRITICAL: The page has an established design system. You MUST follow the exact patterns used by existing sections.

DESIGN SYSTEM ANALYSIS (Follow These Patterns Exactly):
1. **Section Structure**: All sections use `.section` class with `.container` inside
2. **Headers**: Use `.section-header animate-fade-in-up` with `h2.text-5xl.section-title` and `.section-subtitle`
3. **Cards**: Use base `.card` class with simple hover transforms: `translateY(-8px) scale(1.02)`
4. **Icons**: Circular 64px icons with gradient backgrounds, 32px SVGs, placed at top of cards
5. **Typography**: `h3` titles are 1.5rem, 700 weight, `var(--text-primary)` color
6. **Colors**: Use `var(--text-primary)`, `var(--text-secondary)`, and exact hex values like `#EF4444`
7. **Spacing**: `margin-bottom: 24px` for icons, `16px` for titles, standard spacing throughout
8. **Backgrounds**: Simple gradients with opacity, not complex multi-layer effects
9. **Grid**: `repeat(auto-fit, minmax(350px, 1fr))` for card layouts
10. **Animations**: Simple `transition: all 0.3s ease` with basic transforms

EXACT PATTERNS FROM EXISTING SECTIONS:

Problem Section Pattern:
```html
<section class="section problem" style="background: linear-gradient(135deg, #fef7f7 0%, #fef5e7 50%, #fefbf0 100%); position: relative; overflow: hidden;">
<div class="section-pattern">
  <svg viewBox="0 0 100 100" fill="none">
    <pattern id="section-grid" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="currentColor" stroke-width="0.5" opacity="0.3"/>
      <circle cx="10" cy="10" r="1" fill="currentColor" opacity="0.2"/>
    </pattern>
    <rect width="100%" height="100%" fill="url(#section-grid)"/>
  </svg>
</div>
<div class="container" style="position: relative; z-index: 1;">
  <div class="section-header animate-fade-in-up">
    <h2 class="text-5xl section-title">Title with <span style="color: #EF4444;">highlight</span></h2>
    <p class="section-subtitle">Description text</p>
  </div>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 32px; margin-top: 60px;">
    <div class="card" style="border-left: 4px solid #EF4444;" onmouseover="this.style.transform='translateY(-8px) scale(1.02)'" onmouseout="this.style.transform='translateY(0) scale(1)'">
      <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #fee2e2, #fecaca); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px;">
        <svg style="width: 32px; height: 32px; color: #EF4444;">...</svg>
      </div>
      <h3 style="font-size: 1.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 16px;">Card Title</h3>
      <p style="color: var(--text-secondary); line-height: 1.6;">Card description</p>
    </div>
  </div>
</div>
</section>
```

REQUIREMENTS:
1. **Exact Structure**: Follow the pattern above EXACTLY - same classes, same spacing, same element hierarchy
2. **Simple Enhancements**: Only add simple inline styles, no complex multi-layer effects
3. **Consistent Colors**: Use the established color palette and CSS custom properties
4. **Standard Animations**: Use the same hover effects as existing sections
5. **Clean Code**: No overly complex styling or excessive nested elements
6. **Semantic Content**: Make the content relevant to {product_desc} and the section purpose

Instructions:
1. Generate ONLY the requested sections: {sections_str}
2. Follow the EXACT pattern structure shown above
3. Keep styling simple and consistent with existing sections
4. Use appropriate colors and content for each section type
5. Wrap with section markers: <!-- START: {{section_name}} --> ... <!-- END: {{section_name}} -->
6. Return ONLY the code, no explanations

Generate sections that match the existing design system perfectly while adding relevant content for {product_desc}.'''
