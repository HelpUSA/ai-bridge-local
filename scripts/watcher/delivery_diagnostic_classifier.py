# -*- coding: utf-8 -*-
"""Delivery diagnostic classifier for AI Bridge Local.

This module is intentionally pure/read-only: it does not send messages,
touch the browser, mutate the queue, or execute inter-chat delivery tests.
It converts observed delivery/error text into stable diagnostic codes.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryDiagnostic:
    code: str
    confidence: str
    summary: str
    next_action: str


DIAGNOSTIC_CODES = (
    "target_chat_not_registered",
    "target_tab_not_open",
    "composer_not_found",
    "modal_blocking",
    "send_button_disabled",
    "inject_timeout",
    "submit_not_confirmed",
    "delivery_not_acked",
    "unknown_delivery_failure",
)


_RULES: tuple[tuple[str, tuple[str, ...], str, str], ...] = (
    (
        "submit_not_confirmed",
        (
            "submit_not_confirmed",
            "composer_still_has_text",
            "compositor ainda tem texto",
            "composer still has text",
        ),
        "Envio tentado, mas o texto continuou no composer.",
        "Revalidar seletor/botao de envio e se ha modal bloqueante antes de reenviar.",
    ),
    (
        "modal_blocking",
        (
            "modal_blocking",
            "share modal",
            "compartilhar",
            "share/compartilhar",
            "blocking modal",
            "modal bloqueante",
        ),
        "Um modal ou overlay provavelmente bloqueou a injecao ou o envio.",
        "Fechar modal/overlay e repetir somente depois de confirmar composer livre.",
    ),
    (
        "send_button_disabled",
        (
            "send_button_disabled",
            "submit_button_not_found_or_disabled",
            "send button disabled",
            "botao de envio desabilitado",
            "button disabled",
        ),
        "Botao de envio nao encontrado ou indisponivel.",
        "Inspecionar seletor do botao e estado do composer antes de nova tentativa.",
    ),
    (
        "composer_not_found",
        (
            "composer_not_found",
            "composer not found",
            "campo de composicao nao foi encontrado",
            "textarea not found",
            "contenteditable not found",
        ),
        "Campo de composicao nao foi encontrado no chat destino.",
        "Confirmar se a aba esta no chat correto e se a UI terminou de carregar.",
    ),
    (
        "target_chat_not_registered",
        (
            "target_chat_not_registered",
            "source_chat_id_mismatch",
            "target chat not registered",
            "chat destino nao registrado",
            "destino nao localizado",
        ),
        "Chat destino nao esta registrado de forma confiavel no bridge local.",
        "Confirmar chat_id destino, aba aberta e extensao ativa antes de reenviar.",
    ),
    (
        "target_tab_not_open",
        (
            "target_tab_not_open",
            "tab not found",
            "no tab",
            "aba destino nao esta aberta",
            "aba suspensa",
            "could not establish connection",
        ),
        "Aba destino nao parece aberta, ativa ou alcançavel.",
        "Abrir/ativar a aba destino e confirmar registro no dashboard/local bridge.",
    ),
    (
        "delivery_not_acked",
        (
            "delivery_not_acked",
            "not acked",
            "nao recebeu ack",
            "sem ack",
            "marked as delivering",
        ),
        "Entrega ficou em delivering sem ack dentro do limite.",
        "Verificar aba destino e reemitir com command_id novo se necessario.",
    ),
    (
        "inject_timeout",
        (
            "inject_timeout",
            "injection timeout",
            "inject timeout",
            "timeout apos tentativa de injecao",
            "timeout",
        ),
        "Timeout generico durante ou apos a tentativa de injecao.",
        "Coletar contexto de aba/composer/modal para classificar melhor antes de reenviar.",
    ),
)


def normalize_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def classify_delivery_failure(value: object) -> DeliveryDiagnostic:
    text = normalize_text(value)
    if not text:
        return DeliveryDiagnostic(
            code="unknown_delivery_failure",
            confidence="low",
            summary="Nao ha texto de erro suficiente para classificar a falha.",
            next_action="Coletar stderr/stdout, status da aba destino e ultimo delivery_result.",
        )

    for code, needles, summary, next_action in _RULES:
        for needle in needles:
            if needle in text:
                confidence = "high" if code != "inject_timeout" else "medium"
                return DeliveryDiagnostic(
                    code=code,
                    confidence=confidence,
                    summary=summary,
                    next_action=next_action,
                )

    return DeliveryDiagnostic(
        code="unknown_delivery_failure",
        confidence="low",
        summary="Falha de entrega nao mapeada pela taxonomia atual.",
        next_action="Adicionar uma regra readonly ao classifier antes de alterar entrega real.",
    )


def format_diagnostic(value: object) -> str:
    diagnostic = classify_delivery_failure(value)
    return (
        "tipo=" + diagnostic.code + "\n"
        "confianca=" + diagnostic.confidence + "\n"
        "resumo=" + diagnostic.summary + "\n"
        "correcao=" + diagnostic.next_action
    )


__all__ = [
    "DIAGNOSTIC_CODES",
    "DeliveryDiagnostic",
    "classify_delivery_failure",
    "format_diagnostic",
    "normalize_text",
]
