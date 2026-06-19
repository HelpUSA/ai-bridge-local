/*
 * AI Bridge Local - Route classifier
 *
 * Side-effect free classifier.
 * Micro 1 introduces the contract and smoke tests only.
 */

(function attachRouteClassifier(root) {
  "use strict";

  const ROUTE_DIRECT_INTERCHAT = "direct_interchat";
  const ROUTE_LOCAL_GATEWAY = "local_gateway";

  function normalizeText(value) {
    if (value === null || value === undefined) return "";
    return String(value).trim().toLowerCase();
  }

  function truthy(value) {
    if (value === true) return true;
    if (value === 1) return true;

    const text = normalizeText(value);
    return text === "true" || text === "1" || text === "yes" || text === "y";
  }

  function getEnvelopeValue(envelope, key) {
    if (!envelope || typeof envelope !== "object") return undefined;

    if (Object.prototype.hasOwnProperty.call(envelope, key)) {
      return envelope[key];
    }

    if (
      envelope.payload &&
      typeof envelope.payload === "object" &&
      Object.prototype.hasOwnProperty.call(envelope.payload, key)
    ) {
      return envelope.payload[key];
    }

    return undefined;
  }

  function classifyRoute(envelope) {
    const action = normalizeText(getEnvelopeValue(envelope, "action"));
    const transport = normalizeText(getEnvelopeValue(envelope, "transport"));
    const deliveryKind = normalizeText(getEnvelopeValue(envelope, "delivery_kind"));
    const forceGateway = truthy(getEnvelopeValue(envelope, "force_gateway"));

    if (forceGateway) {
      return ROUTE_LOCAL_GATEWAY;
    }

    if (transport === ROUTE_LOCAL_GATEWAY || transport === "gateway" || transport === "local-gateway") {
      return ROUTE_LOCAL_GATEWAY;
    }

    if (transport === ROUTE_DIRECT_INTERCHAT || transport === "direct-interchat" || transport === "direct") {
      return ROUTE_DIRECT_INTERCHAT;
    }

    if (
      action === "run-command" ||
      action === "run_command" ||
      action === "local-command" ||
      action === "local_command" ||
      action === "smoke" ||
      action === "run-smoke" ||
      action === "run_smoke" ||
      action === "patch" ||
      action === "apply-patch" ||
      action === "apply_patch" ||
      action === "inspect" ||
      action === "inspection" ||
      action === "local-task" ||
      action === "local_task"
    ) {
      return ROUTE_LOCAL_GATEWAY;
    }

    if (action === "send-chat-message" || action === "send_chat_message") {
      return ROUTE_DIRECT_INTERCHAT;
    }

    if (deliveryKind === "inter_agent_message" || deliveryKind === "chat_message") {
      return ROUTE_DIRECT_INTERCHAT;
    }

    return ROUTE_LOCAL_GATEWAY;
  }

  const api = {
    ROUTE_DIRECT_INTERCHAT,
    ROUTE_LOCAL_GATEWAY,
    classifyRoute
  };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }

  root.AIBridgeRouteClassifier = api;
})(typeof globalThis !== "undefined" ? globalThis : window);
