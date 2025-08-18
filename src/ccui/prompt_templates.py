
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
    "secondary":"#...","surface":"#...","background":"#...",
    "success":"#...","error":"#...",
    "text_primary":"#...","text_secondary":"#...","text_muted":"#..."
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
    "buttons": {{"primary":{{"default":"...","hover":"...","active":"...","disabled":"..."}}}},
    "inputs": {{"text_field":{{"default":"...","focus":"...","error":"..."}}}},
    "cards": {{"content":"...","pricing":"...","testimonial":"..."}}
  }},
  "spacing_system": {{"scale":["4px","8px","16px","24px"],"usage":"..."}},
  "summary": "..."
}}
Rules: Ensure uniqueness + consistency, mobile-first, contrast accessible.'''


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
    primary_color = colors.get('primary', '#3B82F6')
    typography = design_data.get('design_system', {}).get('typography', {}).get('typeface_choice', 'Inter')
    
    # Key UX patterns from competitive analysis
    ux_adopt = design_data.get('ux_analysis', {}).get('recommendations', {}).get('adopt', [])[:2]
    ux_avoid = design_data.get('ux_analysis', {}).get('recommendations', {}).get('avoid', [])[:2]
    
    # Mobile wireframe priorities
    mobile_critical = design_data.get('wireframes', {}).get('mobile_checks', {}).get('critical', [])[:3]
    
    return f'''You are a senior frontend engineer. Build a high-conversion landing page.

Product: {product_description}
Copy (use verbatim, no edits): {copy_content}
Framework: {framework}
Theme: {theme}

Design System:
- Primary Color: {primary_color}
- Typography: {typography}
- UX Adopt: {ux_adopt}
- UX Avoid: {ux_avoid}
- Mobile Critical: {mobile_critical}

Output: CODE ONLY (full, runnable). No commentary.

Requirements:
- Accessibility: semantic HTML, ARIA as needed, alt text; WCAG AA (4.5:1).
- Layout: mobile-first flex/grid; max ~75ch text; 8px spacing; clear hierarchy (Z-pattern).
- Nav: ≤5 items (Hick's Law).
- Performance: lazy-load offscreen images; minimize CLS; prefer WebP.
- Images: placeholders (https://placeholder.com or https://picsum.photos), alt="Example [type] image".
- Meta: include viewport, description, basic Open Graph/Twitter.
- Standards: ES6+, CSS3, HTML5.

Deliver:
- ONLY the complete HTML/CSS/JS (or single {framework} file if applicable).'''

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

    return f'''You are a senior frontend engineer + UX designer.

Goal: Build a modern, responsive landing page for: {product_description}
Framework: {fw}; Theme: {theme}{design_context}

Requirements:
- Heuristics: large primary CTA (Fitts), simple nav (Hick), clear hierarchy, whitespace.
- Accessibility: semantic HTML, roles/labels, alt text, WCAG AA.
- Responsive: mobile-first flex/grid; ~75ch text; 8px spacing.
- Sections: {sections_str}
- Content: no lorem ipsum; align to product; concise, benefit-led.
- Images: placeholder.com or picsum.photos via URLs; descriptive alt.
- Performance: lazy-load offscreen images; minimize CLS; prefer WebP.

Output:
- {out}
- CODE BLOCKS ONLY. No explanations.'''
