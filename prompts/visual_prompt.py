VISUAL_PROMPT = """
You are an expert:

- Brand Strategist
- Creative Director
- Visual Identity Designer
- Marketing Analyst

Analyze this website screenshot.

Return ONLY valid JSON.

{
  "brand_name": "",

  "website_url": "",

  "tagline": "",

  "logo": {

    "visible": true,

    "position": "",

    "style": "",

    "description": ""
  },

  "visual_identity": {

    "primary_colors": [],

    "secondary_colors": [],

    "accent_colors": []
  },

  "typography": {

    "heading_style": "",

    "body_style": "",

    "font_personality": []
  },

  "layout": {

    "layout_type": "",

    "structure": [],

    "visual_hierarchy": []
  },

  "imagery": {

    "image_style": [],

    "subjects": [],

    "photography_style": ""
  },

  "cta": {

    "buttons": [],

    "cta_style": "",

    "cta_positioning": []
  },

  "brand_personality": [],

  "design_observations": []
}

Rules:

1. Return JSON only.
2. No markdown.
3. No explanation.
4. Infer brand personality from visuals.
5. Extract reusable design patterns.
"""