import json
from pathlib import Path

from services.playwright_service import PlaywrightService
from services.gemini_service import GeminiService
from services.groq_service import GroqService
from services.product_discovery_service import ProductDiscoveryService

from agents.visual_analysis_agent import VisualAnalysisAgent
from agents.content_analysis_agent import ContentAnalysisAgent
from agents.product_analysis_agent import ProductAnalysisAgent

from agents.pattern_extraction_agent import PatternExtractionAgent
from agents.audience_dna_agent import AudienceDNAAgent
from agents.product_dna_agent import ProductDNAAgent
from agents.creative_rules_agent import CreativeRulesAgent

from agents.brand_fusion_agent import BrandFusionAgent
from agents.brand_memory_builder import BrandMemoryBuilder

from agents.page_summary_agent import PageSummaryAgent
from agents.reduce_summary_agent import ReduceSummaryAgent

def save_json(
    filepath,
    data
):

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )


def main():

    website_url = input(
        "Website URL: "
    ).strip()

    Path(
        "outputs"
    ).mkdir(
        exist_ok=True
    )

    gemini = GeminiService()
    groq = GroqService()

    print("\nCrawling Website...")

    crawler = PlaywrightService()

    pages = crawler.capture_brand_pages(
        website_url,
        max_pages=3
    )

    print(
        f"\nPages Captured: {len(pages)}"
    )

    # --------------------
    # Visual Analysis
    # --------------------

    visual_agent = VisualAnalysisAgent(
        gemini
    )

    visual_results = []

    if len(pages) > 0:

        visual_results.append(
            visual_agent.analyze(
                pages[0]["screenshot"]
            )
        )

    save_json(
        "outputs/visual_analysis.json",
        visual_results
    )

    # --------------------
    # Content Analysis
    # --------------------

    content_agent = ContentAnalysisAgent(
        groq
    )

    content_results = []

    for page in pages:

        content_results.append(
            content_agent.analyze(
                page
            )
        )

    save_json(
        "outputs/content_analysis.json",
        content_results
    )

    print("\nCreating Page Summaries...")

    page_summary_agent = PageSummaryAgent(
        groq
    )

    page_summaries = []

    homepage_visual = (
        visual_results[0]
        if visual_results
        else {}
    )

    for i in range(len(content_results)):

        page_payload = {

            "content":
            content_results[i],

            "visual":
            homepage_visual
        }

        page_summaries.append(
            page_summary_agent.summarize(
                page_payload
            )
        )

    save_json(
        "outputs/page_summaries.json",
        page_summaries
    )

    print("\nReducing Summaries...")

    reduce_agent = ReduceSummaryAgent(
        groq
    )

    compressed_brand_data = (
        reduce_agent.reduce(
            page_summaries
        )
    )

    save_json(
        "outputs/compressed_brand_data.json",
        compressed_brand_data
    )


    # --------------------
    # Product Analysis
    # --------------------

    print("\nRunning Product Analysis...")

    product_agent = ProductAnalysisAgent(
        groq
    )

    product_results = []

    # Homepage skip
    for page in pages[1:4]:

        result = product_agent.analyze(
            page
        )

        product_results.append(
            result
        )

    save_json(
        "outputs/product_analysis.json",
        product_results
    )

    print(
        f"\nProducts Analyzed: {len(product_results)}"
    )
    
    # --------------------
    # Pattern Extraction
    # --------------------

    combined = {

        "compressed_brand_data":
        compressed_brand_data,

        "products":
        product_results
    }
    
    pattern_agent = (
        PatternExtractionAgent(
            groq
        )
    )

    patterns = (
        pattern_agent.extract_patterns(
            combined
        )
    )

    save_json(
        "outputs/patterns.json",
        patterns
    )

    # --------------------
    # Audience DNA
    # --------------------

    audience_agent = (
        AudienceDNAAgent(
            groq
        )
    )

    audience_dna = (
        audience_agent.extract(
            patterns
        )
    )

    save_json(
        "outputs/audience_dna.json",
        audience_dna
    )

    # --------------------
    # Product DNA
    # --------------------

    product_dna_agent = (
        ProductDNAAgent(
            groq
        )
    )

    product_dna = (
        product_dna_agent.extract(
            patterns
        )
    )

    save_json(
        "outputs/product_dna.json",
        product_dna
    )

    # --------------------
    # Creative Rules
    # --------------------

    creative_agent = (
        CreativeRulesAgent(
            groq
        )
    )

    creative_rules = (
        creative_agent.extract(
            patterns
        )
    )

    save_json(
        "outputs/creative_rules.json",
        creative_rules
    )

    # --------------------
    # Brand Fusion
    # --------------------

    brand_brain = {

        "patterns":
        patterns,

        "audience_dna":
        audience_dna,

        "product_dna":
        product_dna,

        "creative_rules":
        creative_rules
    }

    fusion_agent = (
        BrandFusionAgent(
            groq
        )
    )

    brand_dna = (
        fusion_agent.fuse(
            brand_brain
        )
    )

    save_json(
        "outputs/brand_dna.json",
        brand_dna
    )

    # --------------------
    # Brand Memory
    # --------------------

    memory_builder = (
        BrandMemoryBuilder(
            groq
        )
    )

    brand_memory = (
        memory_builder.build(
            brand_dna
        )
    )

    save_json(
        "memory/brand_memory.json",
        brand_memory
    )

    print(
        "\n===================="
    )

    print(
        "BRAND INTELLIGENCE COMPLETE"
    )

    print(
        "===================="
    )


if __name__ == "__main__":
    main()