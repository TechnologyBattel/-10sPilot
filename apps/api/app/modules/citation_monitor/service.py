"""Citation monitor service."""

from app.core.errors import EngineError
from app.modules.citation_monitor.engines import ENGINES, EngineAnswer
from app.modules.citation_monitor.schemas import CitationCheck, CitationRequest


def _evaluate(answer: EngineAnswer, request: CitationRequest) -> CitationCheck:
    domain = request.domain.removeprefix("www.").lower()
    brand = (request.brand or domain.split(".")[0]).lower()
    text = answer.text.lower()

    position: int | None = None
    for index, url in enumerate(answer.citations, start=1):
        if domain in url.lower():
            position = index
            break

    return CitationCheck(
        engine=answer.engine,
        prompt=request.prompt,
        cited=position is not None or domain in text,
        mentioned=brand in text or domain in text,
        position=position,
        answer_excerpt=answer.text[:400],
        error=answer.error,
    )


class CitationMonitorService:
    async def check(self, request: CitationRequest) -> list[CitationCheck]:
        checks: list[CitationCheck] = []
        for engine in request.engines:
            probe = ENGINES.get(engine)
            if probe is None:
                checks.append(
                    CitationCheck(engine=engine, prompt=request.prompt, error="unknown engine")
                )
                continue
            try:
                checks.append(_evaluate(await probe(request.prompt), request))
            except EngineError as error:
                checks.append(CitationCheck(engine=engine, prompt=request.prompt, error=str(error)))
        return checks
