# Core Service API pack

Public API documentation facts for Convai's external developer surfaces. External developers only.
Enterprise-grade API reference — not backend setup, not internal architecture.
Generic doctrine lives in `references/`.

This is an **API reference pack**, not an SDK or plugin pack. It governs external developer-facing
API documentation at the quality bar of Stripe, OpenAI, Twilio, or AWS public API docs.

Last audited: 2026-08-18 against `502ad7f8`. That commit is the realtime engine only. The API gateway that serves the REST surface is a separate repository with no contract yet, so every REST claim on a page is still verified by hand.

Use the **Convai Unity SDK docs as the internal quality benchmark** for structure, clarity, and
reader guidance. Borrow the relevant practices, not Unity-specific content:
- Start with a direct, outcome-focused lead paragraph that explains what the reader can do.
- Use GitBook-native structure deliberately: card tables for hubs, steppers for short integration
  guides, content-ref blocks for next steps, and hints only for security, beta, or operationally
  important notes.
- Keep page flow narrow and purposeful. Each page should answer one job, then point to the next
  relevant page.
- Require source verification before naming any endpoint, header, field, enum value, default,
  status code, or error response.
- Add `last_reviewed` frontmatter to version-sensitive pages and set it to the API contract version,
  release tag, or maintainer-approved review marker.

**Reader question every page must answer:** "What do I send, what do I get back, and what can go wrong?"

**Every public endpoint page should include (when applicable):**
- HTTP method + full public URL (via GitBook vars, never hard-coded staging URLs)
- Authentication (header name, format, required vs optional)
- Request parameters/body with types, required flags, defaults, constraints
- Response schema with field descriptions and example JSON
- Status codes and error response format
- Beta/stable lifecycle label where relevant
- Minimal copy-pasteable curl or code example (public contract only)
- A realistic usage example that explains when to use the endpoint in a product workflow

**Tone and structure:**
- Contract-first, not implementation-first
- Present tense, imperative for actions ("Send a POST request to…")
- No repo internals, no "how we built this", no ops runbooks
- Consistent terminology across all endpoint pages (same auth header, same error envelope, same session ID naming per surface)

**Usage example guidance:**
- Prefer learning, training, simulation, onboarding, assessment, and enterprise enablement scenarios when
  they fit the feature. This is Convai's primary domain framing for public API examples.
- Gaming and interactive entertainment examples are allowed when they explain the API behavior more
  clearly than a training scenario, or when the feature naturally maps to player/NPC interaction.
- Choose the clearest domain example for the API contract being documented. Do not force a training
  scenario if another domain makes request timing, session state, or response handling easier to
  understand.
- Keep examples product-level and external-facing. Do not mention internal services, private tooling,
  database state, deployment environments, or repo workflows.
- Usage examples should clarify intent, edge cases, and expected outcomes; they should not replace the
  formal request/response schema.

**AAA page-authoring rules for this API:**
- Every page has one primary Diataxis mode. If a draft mixes endpoint reference, usage guide, and
  conceptual explanation, split it into separate pages and link them.
- Hub pages route. They use a short outcome lead, GitBook card tables, and minimal prose.
- Endpoint reference pages state facts. They include exact methods, paths, auth requirements, fields,
  defaults, constraints, status codes, examples, and error behavior. No narrative teaching.
- Usage guides help readers complete one product task. They may use steppers, tabs, verification, and
  next-step content refs, but they must link back to endpoint reference instead of duplicating schemas.
- Concept pages explain behavior such as session lifecycle, realtime events, authentication model,
  versioning, or error strategy. Use Mermaid and tables when they make state or decisions clearer.
- Troubleshooting pages organize by symptom. Each item must include symptom, likely cause, fix, and
  verification.

**Endpoint page anatomy:**
- Frontmatter with `title`, `description`, and `last_reviewed` when the API contract is version-sensitive.
- Headingless lead paragraph: one to three short sentences that state what the endpoint does and when
  to use it.
- `## Endpoint` with method and public URL, using GitBook variables for base URLs.
- `## Authentication` with required headers and token format.
- `## Request` with path parameters, query parameters, headers, and body schema as tables or OpenAPI.
- `## Response` with success schema, example JSON, and field descriptions.
- `## Errors` with status codes, error envelope, retryability, and recovery guidance.
- `## Usage example` with a realistic learning/training-first scenario and copy-pasteable request.
- `## Next steps` with two to five descriptive content refs when a next action exists.

**GitBook block usage for public API docs:**
- Use OpenAPI blocks for REST endpoint reference pages when an OpenAPI source exists. Avoid manually
  duplicating schemas that can drift. Neither source repo ships a checked-in OpenAPI spec today; use
  Pydantic models, handler routes, and source docs as verification sources until an OpenAPI artifact is
  published.
- Use tabs for equivalent request examples such as `curl`, `JavaScript`, and `Python`; do not use tabs
  for unrelated workflows.
- Use code blocks with languages for all requests, responses, JSON, WebSocket messages, and errors.
  Use titled GitBook code blocks when the title clarifies `Request`, `Response`, or a file path.
- Use hints sparingly: `info` for beta/prerequisite context, `success` for observable verification,
  `warning` for compatibility or rate-limit constraints, and `danger` for secrets, destructive actions,
  or production-impacting security risks.
- Use cards for hubs and routing pages only.
- Use content refs for strong next steps after explaining why the linked page matters.
- Use Mermaid for realtime/session state machines, event flows, or auth decision trees.
- Use tables for fields, parameters, status codes, limits, and compatibility matrices. Do not use
  tables for visual layout.
- Use screenshots only if a public dashboard or UI state is necessary to prevent ambiguity. Never use
  screenshots for code, logs, JSON, configuration, or terminal output.

**Examples and validation:**
- Examples must be runnable or clearly scoped as pseudocode.
- Use realistic placeholders such as `YOUR_API_KEY`, `CHARACTER_ID`, `SESSION_ID`, and
  `END_USER_ID`. Do not include real keys, private project names, local usernames, or internal URLs.
- Show expected success output or a verification cue after task examples.
- Prefer this example order when a page needs multiple examples: minimal working request, common
  production-style learning/training scenario, optional advanced variation.
- Keep schemas authoritative. Examples illustrate common use; they do not redefine the contract.

**Final quality gate before handoff:**
- Page has no duplicate Markdown H1 and starts with a headingless lead paragraph.
- Description is outcome-focused, plain English, and 120–160 characters when possible.
- No `## Overview`, `## Introduction`, "click here", "simply", "just", "easy", or marketing filler.
- All public API names, headers, fields, defaults, limits, errors, and status codes are source-verified.
- GitBook variables are used for shared base URLs, versions, and synchronized values.
- A block-fit pass is complete: native GitBook blocks are used where they improve scanning,
  verification, copyability, or navigation.

**Internal content blacklist (never in docs):**
- Python, UV, pip, virtualenv, `uv sync`, `uv run`
- Ray Serve, `serve_config.yaml`, Docker, container images, warm-pool actors
- `stg` / `prod` branch deploy flows, gcp-app-infra-iac, CODEOWNERS
- Alembic, Cloud SQL, `db/models/`, schema migrations
- Pipecat pipelines, processors, internal service classes as doc subjects
- NeuroSync wire protocol, IR/Qdrant/Pinecone internals, usage Pub/Sub protobufs
- Provider SDK adapters (LLM, TTS, STT, OVR, Kokoro downstream clients)
- Telemetry/BQ/turn-trace server internals, `debug_log` gated fields, `server-log` RTVI debug messages
- Internal test client (`client/` submodule) unless promoted as an official public sample
- Private ops playbooks, bastion host access, internal Slack/Atlassian links
- Deprecated gRPC APIs as new documentation subjects, `rpc/internal_service.proto`,
  `SessionCache` / `SessionCacheInternal` payloads
- NLP `/log` (commented "Private-Use"), `/character/test/*`, `/interaction-logs/error-traces`
- Admin/ops payment routes, `settings.toml` internal URLs, PEM certificates, load-balancer plumbing

Both source repos are **verification sources** for public contracts only — not documentation content.

Existing related docs to **not** treat as gold standard: `api-reference/core-api-reference/` (legacy).
Greenfield only — no legacy page reuse.

**Naming and IA are not locked in this pack.** The pack id is `core-service` (for `docs-writer`,
`/plan-docs`, and `/verify-doc`). That id is an internal docs-tool identifier. It is **not** the public
product name, folder path, or sidebar label. All public-facing names and the final page tree are
decided after inspecting the source and running `/plan-docs core-service`.
from a source audit of both backend repositories in an earlier pass, but that audit predates this line
and its commit was not recorded, so its age is unknown. **Run `/audit-pack core-service` against both
backend repositories before writing a batch of API pages**, and record the commits here.

---

## Product naming

- Do **not** guess or lock a canonical public product name in this pack. Derive it during
  `/plan-docs core-service` from public URLs, dashboard copy, SDK references, and maintainer input.
- Do **not** call these APIs a "plugin" or "SDK" unless the public product surface genuinely is one.
- Do **not** expose internal repo or service names (`core-service`, `ConvAI_Middleman`, deploy
  environment names) in public page titles, sidebar labels, or reader-facing prose unless source
  confirms they are official public names.
- Backend phrasing for integrators: refer to **"Convai"** per cross-SDK rules; never "Convai cloud",
  "Convai's servers", or "cloud-powered".
- Two backend codebases back this pack. Public docs may span multiple sections in the documentation
  repo; they do not need to live under one folder or one product label.

## Audience and prerequisites baseline

- Primary audience: public API consumers integrating Convai from applications, backend services, or tooling.
- Baseline prerequisites (API-consumer oriented only): Convai account, API key, character/resource
  identifiers, reachable endpoint URL, and request/response format knowledge.
- Do **not** include Python, UV, Ray Serve, Docker, local server run commands, repo contribution steps,
  or environment setup as reader prerequisites.

## Terminology and concepts

Use exact casing from source. Do not normalize headers across surfaces unless a maintainer confirms a
single public standard.

### Authentication headers

| Surface | Primary API key header | Session token header | Source |
|---|---|---|---|
| Realtime HTTP (`core-service`) | `X-API-Key` | `API-AUTH-TOKEN` | `core-service/auth/dependencies.py` |
| REST gateway (`ConvAI_Middleman`) | `CONVAI-API-KEY` | `API-AUTH-TOKEN` | `ConvAI_Middleman/main/character/resources/blueprint_utils.py` |

Auth precedence on both surfaces: if the API key header is present, use it; else resolve
`API-AUTH-TOKEN` to an API key; else return 401.

### Session and identity terms

| Term | Meaning | Source |
|---|---|---|
| `session_id` | Client session identifier returned after connect or init | `core-service/models/api.py` (`ConnectResponse`), Middleman REST handlers |
| `character_session_id` | Server-side character session row ID | `core-service/models/api.py` (`ConnectResponse`) |
| `character_id` | Character resource identifier | Both repos |
| `end_user_id` | End-user identity for LTM and personalization | Both repos |
| `end_user_metadata` | JSON metadata for end user | Both repos |
| `speaker_id` | Speaker profile identifier (mutually exclusive with `end_user_id` on some surfaces) | Middleman REST handlers; `core-service` connect validation |
| `request_trace_id` | Trace ID for support correlation | `core-service/models/api.py` (`ConnectResponse`) |

### Realtime protocol terms

| Term | Meaning | Source |
|---|---|---|
| RTVI | Realtime Voice Interaction message protocol over LiveKit data channel, WebSocket, or Daily | `core-service/docs/rtvi.md`, `core-service/models/rtvi.py` |
| `transport` | Client transport name on connect (`livekit`, `websocket`; `internal`/`external` map to LiveKit) | `core-service/transport/transport_factory.py` |
| `file-upload` | LiveKit byte-stream topic for client image uploads | `core-service/docs/file-upload.md`, `core-service/transport/services/livekit.py` |

### REST error envelope (Middleman)

| Shape | Example | Source |
|---|---|---|
| Standard REST error | `{"ERROR": "<message>"}` | `ConvAI_Middleman/main/global_resources/response_config.py` (`external_error_message`) |
| With reference ID | `{"ERROR": "<message>", "Reference ID": "<uuid>"}` | Same |
| v2 voices variant | `{"error": "<message>"}` | `ConvAI_Middleman/main/tts/v2_voices_blueprint.py` |

### Stable error codes (core-service HTTP logging)

`ErrorCode` values in `core-service/utils/api_event.py`: `none`, `bad_request`, `invalid_api_key`,
`realtime_access_denied`, `concurrency_limit`, `character_not_found`, `session_not_found`,
`session_forbidden`, `shared_session_conflict`, `missing_end_user_id`, `speaker_limit`,
`speaker_resolution_failed`, `database_unavailable`, `internal_error`.

### Terms to avoid or common mistakes

- Do not write "Convai backend", "cloud backend", or "cloud-powered".
- Do not use `X-API-Key` on Middleman REST pages or `CONVAI-API-KEY` on core-service realtime pages
  unless documenting a cross-surface migration explicitly approved by a maintainer.
- Do not call `internal` or `external` transport names separate public products; both map to LiveKit
  in `transport_factory.py`.
- Do not document deprecated gRPC response-only fields such as `debug_log` — gated/internal behavior is
  not a public REST or realtime contract.
- Reconcile `usage-limit-reached` `quota_type` values against source (`interaction`, `tts`, `error`)
  before publishing; do not copy example values from `docs/rtvi.md` without verification.

## Install and package model

This section documents the **API access model**, not an install step.

- No install model for readers: APIs are consumed over public HTTP, WebSocket, or transport
  endpoints (LiveKit, Daily).
- Canonical docs root path under `api-reference/` is set during `/plan-docs` after the public
  endpoint inventory and product naming are verified. Do not pre-commit a folder name here.
- Leave backend packaging/deployment details out of public docs.
- Base URLs must use GitBook variables. Known production hints from existing SDK docs:
  `live_server_url` → `<code class="expression">space.vars.live_server_url</code>` for realtime
  references. Additional vars (`api_base_url`, `stream_base_url`, and others) must be added to
  `.gitbook/vars.yaml` and verified with a maintainer before publishing endpoint pages.

## GitBook variables

Use `space.vars` for values that must stay synchronized across pages. Do not hard-code URLs or versions.

| Variable | Current value | Used in |
|---|---|---|
| `live_server_url` | `https://live.convai.com` | Realtime endpoint references (existing SDK docs) |
| `dashboard_url` | `https://convai.com` | API key and character ID setup references |

**Owner action before publishing endpoint pages:** add dedicated API vars to `.gitbook/vars.yaml` (for
example `api_base_url`, `stream_base_url`, and any version markers). Reference with
`<code class="expression">space.vars.variable_name</code>`. Do not use `{{ variable_name }}` syntax.

## Gold-standard example pages — READ BEFORE DRAFTING

**Before drafting, open the example whose Diataxis mode matches your task.** Use it as the
quality benchmark for lead paragraph, section count, block selection and prose tone. These are
pages from this subject's own section, chosen because they pass the structure gate and are
substantial enough that there is something to copy.

| Page type | Example page to open |
|---|---|
| Reference (realtime message) | `api-reference/core-api-reference/live-apis-beta/server-to-client-messages.md` |
| Reference (client message) | `api-reference/core-api-reference/live-apis-beta/client-to-server-messages.md` |

Both examples are reference pages, which is what this section is almost entirely made of. There is no how-to or explanation exemplar here yet; the first one written to this bar becomes it.

## Section layout

**Final page tree is built during `/plan-docs core-service`, not preset here.** The planner inspects
the source, inventories public endpoints, groups them by reader intent, proposes folder and file names,
and stops for human approval. This pack defines constraints and quality bar only.

### How naming and structure are decided

1. **Inspect source** — public routes, request/response models, handler modules, auth requirements, beta labels.
2. **Inventory public surface** — list every externally accessible endpoint; mark private/internal as
   out of scope using the classification policy below.
3. **Derive product language** — use names that already appear in public URLs, responses, dashboard, or
   official external copy. Avoid internal repo or module names unless they are verified public terms.
4. **Group by reader intent** — authentication, errors, REST resources, realtime/session, guides,
   troubleshooting. Not by backend package structure or repo boundaries.
5. **Name folders and pages** — lowercase hyphenated slugs; `title` frontmatter matches `SUMMARY.md`
   labels exactly; each name must pass the AAA naming criteria below.
6. **Human approves the plan** — then `/build-docs` writes one work unit at a time.

### AAA naming criteria (every name must pass)

| Name type | Criteria |
|---|---|
| Section folder | Reader-facing, reflects public API grouping, not internal service/module names |
| Page `title` | Sentence case, ≤ 60 characters, keyword-first, unique, matches search intent |
| File slug | Lowercase, hyphenated, stable, readable |
| Endpoint group | Mirrors public resource or capability names from source |
| Guide page | Verb-led task name, not vague labels (`Basics`, `Setup`) |
| Sidebar label | Identical to page `title` frontmatter |

Do **not** pre-commit specific folder paths, page filenames, or product titles in this pack.

### Structural constraints (fixed regardless of final names)

- Lives under `api-reference/`, not `plugins-and-integrations/`.
- Greenfield — do not reuse or mirror legacy `api-reference/core-api-reference/` layout.
- No repo-clone getting-started, no internal operations/architecture sections.
- Public troubleshooting only (auth failures, validation errors, rate limits, realtime session issues).
- Hub pages route with cards; reference pages stay austere; guides hold scenario walkthroughs.
- Max 2 nav levels for non-reference sections; reference may use 3 when the surface is large and stable.
- Multiple documentation sections are allowed when reader intent differs (for example realtime vs REST
  studio vs speech utilities). They do not need to share one sidebar parent.

### Reader paths the final tree must make obvious

- Authenticate and make a first request.
- Look up the contract for a specific endpoint or message type.
- Handle errors, retries, rate limits, and beta behavior.
- Follow a realistic integration example (learning/training-first when it fits).
- Understand realtime/session behavior without reading backend architecture.

---

## Public contract classification policy

Every surface from either source repo must be classified before documentation. The planner and writer
use these tiers; `/verify-doc` rejects anything documented above its approved tier.

| Tier | Definition | Documentation action |
|---|---|---|
| **Public** | Externally intended, stable contract with source-verifiable schema; used by SDKs or integrators | Document in reference pages after maintainer confirms tier |
| **Conditional** | Exists in source but env-gated, diagnostic, mixed dashboard/SDK scope, or proto drift risk | List in pack inventory; document only after explicit maintainer approval per surface |
| **Internal** | Ops, debug, admin, provider plumbing, cache serialization, or implementation detail | Never document; add to blacklist |

**Classification rules:**
- gRPC is deprecated. Do not create new public gRPC reference pages or guides. Use proto files only to
  verify legacy behavior when revising existing deprecated content or migration notes.
- Rate-limit registry (`rate_limit/registry.py`) is supporting evidence only, not publication approval.
- No checked-in OpenAPI exists in either repo. Pydantic models, handler routes, and
  `docs/rtvi.md` are verification sources until an OpenAPI artifact is published.

### When an OpenAPI artifact does exist

Every hand-written endpoint page is a copy of something the code already knows, and a copy drifts.
The moment either repository publishes a spec, the reference pages should be generated from it rather
than maintained, which removes this entire page class from the human pipeline and makes it correct by
construction.

GitBook takes the spec directly. Add this to the repository that owns the spec:

{% code title=".github/workflows/gitbook-openapi.yml" %}
```yaml
name: Publish the OpenAPI spec to GitBook

on:
  push:
    branches: [main]
    paths: ["**/openapi.yaml", "**/openapi.json"]
  workflow_dispatch:

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish
        env:
          GITBOOK_TOKEN: ${{ secrets.GITBOOK_TOKEN }}
        run: |
          npx -y @gitbook/cli@latest openapi publish \
            --spec "${{ vars.GITBOOK_SPEC_NAME }}" \
            --organization "${{ vars.GITBOOK_ORGANIZATION_ID }}" \
            path/to/openapi.yaml
```
{% endcode %}

`GITBOOK_TOKEN` is a repository secret; the spec name and organization id are repository variables.
Once it runs, the pages using OpenAPI blocks refresh from the spec on every merge.

Two rules follow, and CV-73 states them: a page backed by a spec is never hand-edited, and when a fact
on one is wrong the fix belongs in the spec. Editing the page instead produces a correction that the
next publish silently discards, which is worse than the original error because nobody sees it go.
- When proto files and REST/realtime handlers differ, treat REST/realtime handlers as the current
  source of truth unless a maintainer explicitly says a deprecated gRPC contract must be preserved.
- When auth header casing differs between repos, document the header required by that specific surface.

---

## Areas that are deliberately undocumented

Three top-level packages in the realtime engine are internal and no page describes them. They are listed here so the next writer knows the gap is a decision rather than an oversight, and so the drift check stays quiet about them:

| Package | Why it is not documented |
|---|---|
| `frames` | Pipecat frame types used inside the pipeline. A reader never constructs one; the transport contract is what they see. |
| `globals` | Process-wide state and configuration singletons. Implementation detail of how the service boots, with no reader-facing surface. |
| `observers` | Internal instrumentation hooks. Nothing a client can attach to or observe. |

If any of these ever gains a reader-facing surface, document it and remove its row.

## Source of truth — realtime engine (`core-service`)

- Repository: `Conv-AI/core-service`
- Local path: per-machine. Ask for it; never guess it and never copy one from an example.

### Verification files (public contract)

| Purpose | File |
|---|---|
| HTTP/WebSocket routes | `server.py` |
| HTTP request/response models | `models/api.py` |
| RTVI message models | `models/rtvi.py` |
| RTVI wire guide | `docs/rtvi.md` |
| RTVI envelope parsing | `models/rtvi_message_interface.py` |
| Client message handler registry | `handlers/rtvi_client_msg_handler.py` |
| Auth dependency | `auth/dependencies.py` |
| Stable HTTP error codes | `utils/api_event.py` |
| Client transport names | `transport/transport_factory.py` |
| LiveKit file upload | `docs/file-upload.md`, `transport/services/livekit.py` |
| Client action integration | `docs/client-action-integration-guide.md` |
| Client latency events | `docs/latency-instrumentation-v2.md`, `utils/turn_trace.py` |

### Public-tier inventory

| Surface | Method / transport | Auth | Source |
|---|---|---|---|
| Session connect | `POST /connect` | `X-API-Key` or `API-AUTH-TOKEN` | `server.py`, `models/api.py` |
| Session disconnect | `POST /disconnect` | None (`session_id` query) | `server.py` |
| Realtime chat | `WebSocket /chat?session_id=` | Session from `/connect` | `server.py` |
| RTVI client messages | LiveKit topic `rtvi`, WebSocket, Daily | Session | `handlers/rtvi_client_msg_handler.py`, `models/rtvi.py` |
| RTVI server messages | Same transports | Session | `models/rtvi.py`, `docs/rtvi.md` |
| LiveKit file upload | Byte stream topic `file-upload` | LiveKit session | `docs/file-upload.md` |
| HTTP error codes | `ErrorCode` enum | N/A | `utils/api_event.py` |

**RTVI client → server message types** (from `rtvi_client_msg_handler.py`):
`user_text_message`, `trigger-message`, `update-template-keys`, `update-scene-metadata`,
`update-dynamic-info`, `context-update`, `tts-toggle`, `stt-toggle`, `kill-pipeline`,
`interrupt-bot`, `force-user-stopped-speaking`, `reset-idle-timer`.

**RTVI server → client message types** (from `models/rtvi.py` and `docs/rtvi.md`):
`server-response`, `interaction-created`, `usage-limit-reached`, `bot-turn-completed`, `bot-emotion`,
`behavior-tree-response`, `moderation-response`, `action-response`, `final-user-transcription`,
`visemes`, `neurosync-blendshapes`, `chunked-neurosync-blendshapes`, `blendshape-turn-stats`,
`user-idle-warning`, `llm-no-response`, `vad-stt-debug`, `vad-stt-started`, `vad-stt-stopped`,
`turn-trace`, `server-log`, `session-config`, `audio-data`, `bot-started-speaking`,
`bot-stopped-speaking`.

**`/connect` HTTP errors** (from `server.py` handler): 401 `Invalid API key`; 403 realtime access
denied or session forbidden; 404 character or session not found; 400 missing `end_user_id` or VAD
validation; 409 shared-session conflict; 429 concurrency or speaker limit; 503 database unavailable; 500
internal.

**`/chat` WebSocket close codes:** `1008` session not found, expired, transport mismatch, duplicate
connection; `1011` server error.

### Conditional-tier inventory (maintainer approval required)

| Surface | Gate | Source |
|---|---|---|
| Local RAG retrieve | `IR_LOCAL_RAG_FEATURE_ENABLED=true` | `server.py` (`POST /retrieve`) |
| Client latency ingest | Diagnostic instrumentation | `server.py` (`POST /turn_event`) |
| `vad-stt-debug`, `turn-trace`, `server-log` RTVI messages | Debug/operator | `models/rtvi.py` |
| `sse` transport | Implemented but rejected on `/connect` | `transport/transport_factory.py`, `server.py` |
| `StreamingConnectRequest` | Model exists; no HTTP route found | `models/api.py` |

### Internal-tier (never document)

Ray Serve actors, warm pool, `models/internal.py`, `SessionCacheData`, NeuroSync V2 protocol,
IR/Qdrant pipeline, usage Pub/Sub (`ConvaiUsageRecords.proto`), BAML/prompt layers, DB models,
Alembic, provider adapters, telemetry exporters, env-specific deploy config,
`GET /healthz` health check, `POST /character/custom-features`, Daily transport (`daily`).

---

## Source of truth — API gateway (`ConvAI_Middleman`)

- Repository: `ConvAI_Middleman`, maintainer-provided
- Local path: per-machine. Ask for it; never guess it and never copy one from an example.

### Verification files (public contract)

| Purpose | File |
|---|---|
| Deprecated gRPC proto (legacy verification only) | `rpc/public/service.proto` |
| Full deprecated gRPC proto (do not document as current public surface) | `rpc/service.proto` |
| Deprecated gRPC service implementation (legacy verification only) | `rpc/service.py` |
| REST blueprint registration | `main/init_rest.py` |
| Character REST routes | `rest/character_blueprint.py` |
| Auth and API key validation | `main/character/resources/blueprint_utils.py` |
| REST error envelope | `main/global_resources/response_config.py` |
| Status mapping used by REST/gateway errors | `main/global_resources/ResponseObj/convai_status.py` |
| Rate-limit route classification | `main/global_resources/rate_limit/registry.py` |
| STT routes | `main/stt/stt_blueprint.py` |
| TTS routes | `main/tts/tts_blueprint.py` |
| Voice catalog v2 | `main/tts/v2_voices_blueprint.py` |

### Public-tier inventory

| Surface | Method / transport | Auth | Source |
|---|---|---|---|
| Character response (REST) | `POST /character/getResponse` | `CONVAI-API-KEY` or `API-AUTH-TOKEN` | `rest/character_blueprint.py` |
| Init conversation | `POST /character/initConversation` | Same | Same |
| Conversation history | `POST /character/conversationHistory` | Same | Same |
| Speech-to-text | `POST /stt/` | API key | `main/stt/stt_blueprint.py` |
| Text-to-speech | `POST /tts/` | API key | `main/tts/tts_blueprint.py` |
| Voice catalog | `GET /v2/voices`, `GET /v2/voices/<voice_value>` | Unauthenticated read | `main/tts/v2_voices_blueprint.py` |
| Health | `GET /health` | None | `main/init_rest.py` |

**REST/gateway auth errors** (stable strings from `blueprint_utils.py`):
`The request is missing an API key.`, `The request is missing a valid API key.`,
`The request contains an invalid API key.`

**Status mapping** (from `convai_status.py`): document the HTTP equivalents when writing REST
pages — for example `UNAUTHENTICATED` → 401, `PERMISSION_DENIED` → 403,
`RESOURCE_EXHAUSTED` → 429, `UNAVAILABLE` → 503.

**Rate/usage limit messages** (source-verified strings): `API rate limit exceeded. Please try again later.`,
`API usage limit exceeded for current plan.`, `Rate limit exceeded.`

### Conditional-tier inventory (maintainer approval required)

These routes exist in source and may be customer-facing, but scope (SDK-public vs dashboard-only) is
not fully determined from code alone. The planner must confirm each group with a maintainer before
documentation.

| Domain | Route prefix | Source |
|---|---|---|
| Character studio | `/character/*` (create, list, get, update, delete, snapshots, chat history, prompts) | `rest/character_blueprint.py` |
| Knowledge bank | `/character/knowledge-bank/*` | `rest/knowledge_bank_blueprint.py` |
| Avatars | `/character/avatars/*` | `rest/avatar_blueprint.py` |
| Narrative design | `/character/narrative/*` | `rest/narrative_design_blueprint.py` |
| User and API keys | `/user/*` | `main/user/user_blueprint.py` |
| End users and speakers | `/user/end-users/*`, `/user/speaker/*` | Same |
| Memory | `/memory/*` | `main/memory/memory_blueprint.py` |
| Functions | `/functions/*` | `main/functions/functions_blueprint.py` |
| Voice cloning | `/voice-cloning/*` | `main/voiceCloning/voice_cloning_blueprint.py` |
| Experiences / streaming | `/xp/*` | `main/experience/experience_blueprint.py` |
| Assets | `/assets/*` | `main/assets/assets_blueprint.py` |
| Animations | `/animations/*` | `main/animation/animation_blueprint.py` |
| Projects | `/project/*` | `main/project/project_blueprint.py` |
| Payments (customer subset) | `/payments/*` | `main/payments/payments_blueprint.py` |
| NLP utilities | `/nlp/zeroshot`, `/nlp/emotion`, `/nlp/translate` | `main/nlp/nlp_blueprint.py` |

### Internal-tier (never document)

Deprecated gRPC APIs as new documentation subjects, `rpc/internal_service.proto`,
`SessionCacheInternal`, `Hello`/`HelloStream` test RPCs, `/nlp/log`,
`/character/test/*`, `/interaction-logs/error-traces`, admin payment routes, downstream TTS/face/voice
provider protos, usage metering protos, gRPC-Web proxy plumbing, `settings.toml` internal URLs,
eval/ops tooling, PEM certs.

---

## Auth documentation rules

- Document the exact header names required by the surface being documented. Do not collapse
  `X-API-Key` and `CONVAI-API-KEY` into one name.
- Document `API-AUTH-TOKEN` as a UUID session token that resolves to an API key on both surfaces.
- State auth precedence: API key header wins over session token.
- Document that `/disconnect` on the realtime surface accepts `session_id` without an API key; call out
  the security implication in a `warning` hint if the page covers session teardown.
- Never document internal API key bypasses (for example `convai-internal-services`).

## Error documentation rules

- **core-service HTTP:** document HTTP status code, `detail` string, and mapped `ErrorCode` where
  `map_http_exception()` applies. Source: `utils/api_event.py`.
- **Middleman REST:** document `{"ERROR": "<message>"}` envelope and optional `Reference ID`. Source:
  `response_config.py`. Note the `{"error": ...}` variant on v2 voices pages.
- **Deprecated gRPC:** do not create new gRPC docs. If maintaining legacy migration content, mark it
  deprecated and verify against `rpc/public/service.proto` plus maintainer input.
- **RTVI:** document `server-response.status` values (`success`, `error`, `processing`, `pending`),
  `usage-limit-reached` fields, and `bot-turn-completed.error_reason` (for example `audio_delivery_failed`).
- **WebSocket:** document close codes where the transport uses them (`/chat` on core-service).
- Organize troubleshooting by symptom. Quote exact error strings from source.
- Do not document `internal_error_message_*` helpers or `statusCode` pipeline enums.

## REST and realtime documentation rules

- **REST reference pages:** method, path, auth, request/response schema, status codes, error envelope,
  rate-limit behavior when source-verified. Use tables; use OpenAPI block only when a published spec exists.
- **RTVI reference pages:** message `type`, payload schema, direction (client→server or server→client),
  transport applicability (LiveKit, WebSocket). Cross-link concept pages for session lifecycle.
- **Non-HTTP transports:** LiveKit `file-upload` byte stream and RTVI data channel are not HTTP routes.
  Document them as transport contracts, not REST endpoints.
- **Deprecated proto drift:** when proto files differ from current REST/realtime behavior, do not
  document the proto behavior as current public API. Use it only for deprecated legacy notes.

## Platform and version notes

- Document only public endpoint availability, beta/stable status, authentication requirements, and
  version sensitivity visible to API consumers.
- Rate limits and usage quotas: document only source-verified messages and HTTP/status codes. Full plan
  matrices require maintainer input.
- Versioning policy is not defined in source. Most Middleman REST routes are unversioned except
  `/v2/voices`. Flag versioning decisions during `/plan-docs`.
- Do **not** document Python version, UV, Ray Serve, Docker, Cloud SQL, Alembic, or branch deploy flows.
- Require `last_reviewed` on any page whose contract depends on a release, beta state, env gate, or
  schema version. Use an API contract version or maintainer-approved review marker — not Python package
  versions or deployment branch names.

## Tutorials and external sources

No official public API tutorial URLs are registered in this pack yet. Add rows here only when a
maintainer confirms a public, external-facing tutorial. Transcripts (if available) live under
`.convai-docs/sources/core-service/` in the documentation repo.

| Topic | Video URL | Transcript |
|---|---|---|
| — | — | — |

Only include public API tutorials or official public examples — not internal setup or backend
contribution material.

## Bundled sample/demo assets

Not applicable to a public API reference.

| Asset name | Type | Purpose |
|---|---|---|
| N/A | N/A | No bundled demo assets unless a maintainer identifies an official public sample client |
