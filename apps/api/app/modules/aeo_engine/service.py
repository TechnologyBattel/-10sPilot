async def check_brand_visibility(brand: str, query: str, provider: str = "openai"):
    mock = f"For {query}, top tools are Ahrefs, SEMrush, {brand}, Moz"
    mentioned = brand.lower() in mock.lower()
    pos = 3 if mentioned else None
    from app.modules.aeo_engine.router import AEOResult
    return AEOResult(brand=brand, query=query, mentioned=mentioned, position=pos, context=mock, provider=provider)
