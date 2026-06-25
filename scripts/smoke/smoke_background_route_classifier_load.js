const assert = require("assert");
const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "../..");
const backgroundPath = path.join(root, "extension", "background.js");
const classifierPath = path.join(root, "extension", "route_classifier.js");

const background = fs.readFileSync(backgroundPath, "utf8");
const classifier = fs.readFileSync(classifierPath, "utf8");

assert(background.includes("AIBRIDGE_ROUTE_CLASSIFIER_LOAD_START"), "missing load start marker");
assert(background.includes("importScripts(\"route_classifier.js\")"), "missing importScripts for route_classifier.js");
assert(background.includes("globalThis.aiBridgeClassifyRouteSafe"), "missing safe classifier helper");
assert(classifier.includes("function classifyRoute"), "missing classifyRoute implementation");

console.log("OK smoke_background_route_classifier_load");