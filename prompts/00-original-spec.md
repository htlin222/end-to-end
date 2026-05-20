# `00-original-spec.md` — Operator-Supplied Orchestration Spec

**Protocol artefact.** Verbatim record of the orchestration spec supplied
by the operator (Hsieh-Ting Lin MD) on the first day of this study. The
spec is preserved as it was written, including phrasing the operator
would now revise, because the integrity rule of this repository is that
the artefact is preserved as it was *used*, not as the operator wishes
it had been.

## Preamble — model identifier and snapshot

- **Model**: Anthropic Claude `claude-opus-4-7` (1M-context variant),
  accessed via the Claude Code CLI.
- **Snapshot date**: 2026-05-20.
- **Sampling parameters**: default Claude Code values; no temperature
  override.
- **Tool envelope**: Read, Edit, Write, Bash, WebSearch, WebFetch, Agent
  (sub-agent dispatch with `general-purpose` and `Explore` subagent
  types), MCP `claude_ai_PubMed`, MCP `claude_ai_bioRxiv`, TaskCreate /
  TaskUpdate / TaskList, ToolSearch.

## Spec (verbatim, original language)

> 我想做個跟 ___ 有關的題目，請幫我看一下最近發表過的類似主題，以 High
> IF 期刊為偏好及審美。開始幫我想這個題目，設計方法、研究，再依據結果，
> 以它的 novelty、robustness 的程度來看適合哪間期刊、去參考他們的寫作
> 規範，latex + csl + bib ，寫完初稿後，需要請 4 位 subagents 提出
> revision 意見，然我們修改，這樣要至少四輪以上，直到所有 reviewer 都
> "ACCEPT"，記得加上 AI usage disclaimer 。最終要交付的東西是一個
> github private repo 、所有的 preprint 的素材都要提交要在 release 中

## Spec (operator-confirmed English rendering)

> I want to work on a topic related to ___. Please scan recently published
> work on similar topics, with a preference for high-impact-factor journals.
> Help me develop the topic, design the methods and the study, and based on
> the results, judge by novelty and robustness which journal it fits; consult
> that journal's writing conventions; use LaTeX + CSL + BibTeX. After the
> first draft, dispatch four subagents to provide revision opinions; we then
> revise. Iterate at least four rounds until every reviewer says "ACCEPT".
> Remember to add an AI usage disclaimer. The final deliverable is a private
> GitHub repository; all preprint materials must be attached to the release.

## Subsequent operator clarifications (recorded verbatim, in order)

These clarifications were issued during the same dialogue and have been
folded into the downstream pipeline prompts. They are recorded here so
that the entire human-supplied input envelope is auditable in one file.

1. **Submission target.** "我想把這個 prompt 投稿到 NEJM AI 適合怎麼寫？
   Letter to Editor ? Lancet ? 之類的
   https://www.nature.com/articles/s41586-026-10644-y 參考一下別人的"
   *Rendering:* the operator asked which venue the methodology itself should
   be submitted to, supplying the *Nature* "Co-Scientist" article as a
   benchmark.

2. **Article type.** "我就是想投 Perspective 的那種 不用比，只是要提出，
   未來的研究都要這樣開場"
   *Rendering:* the operator confirmed the article type should be a
   Perspective / Viewpoint, manifesto-shaped, with no requirement to
   benchmark against centralised agentic systems.

3. **Realism guardrail.** "你覺得有機會高分 IF 嗎？"
   *Rendering:* the operator asked for an honest probability estimate of
   acceptance at high-IF venues. This conversation produced the decision
   to target Lancet Digital Health Viewpoint with a backing case study.

4. **Path commitment.** "先做 case study，目標 Lancet Digital Health"
   *Rendering:* the operator committed to the path: build a case study,
   then write the Viewpoint pointing to it.

5. **Execution mandate.** "你要: 照我們的價構 做出一個研究，讓這個研究的
   過程在一個 git repo 有 commit 有 meta data 有審計 有 reviewr AI agent
   的意見版本，等等等，讓大家看到，一個個體怎麼用 agent 做研究，然後我們
   投稿的文章就要來 show 這個"
   *Rendering:* the repository's commit history, metadata, audit trail and
   reviewer-AI-agent versioned opinions are themselves the submission
   payload. The submitted article is not merely supported by the repo;
   the repo is the substrate the article displays.

6. **Final deliverable + author + best-practice guidance.** "你最後要交付的:
   一個準備投 lancet 的文章，(請看投稿規定) 作者是
   https://lin.hsiehting.com/cv/ alwasy follow the ultimate goal: increase
   the sucessful rate for hight IF paper best practice"
   *Rendering:* the final deliverable is a Lancet-Digital-Health-ready
   manuscript with Hsieh-Ting Lin MD as the author of record; every
   downstream decision should optimise for the best-practice probability
   of acceptance at high-IF venues.

7. **Domain commitment.** During interactive scoping the operator confirmed
   the case-study domain stays at HCC TCGA-LIHC + GEO validation cohorts
   (not pivoted to the operator's primary hematologic-malignancy
   specialty), explicitly accepting that the cross-domain demonstration
   doubles as a domain-portability argument in the Viewpoint.

8. **Autonomy commitment.** The operator confirmed the case study runs in
   "fully autonomous + transparent ledger" mode. The operator does not
   pre-screen Layer 1's claim selection, does not intervene during the
   reviewer loop, and reports negative results if they emerge from Layer
   3 external validation.

## Status

This file is **closed for edits**. Any superseding instruction is recorded
as `00-original-spec-amend-NN.md` with its own preamble. The integrity
rule applies: prior versions are not removed.
