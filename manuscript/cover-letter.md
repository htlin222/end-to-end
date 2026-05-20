# Cover Letter — Viewpoint submission to *The Lancet Digital Health*

[Operator: this is the draft submission cover letter. Replace dated
fields and the `<<INSERT...>>` placeholders at final submission. The
Lancet group's Editorial Manager accepts cover letters as plain text or
PDF; submit this as PDF generated from `pandoc cover-letter.md -o
cover-letter.pdf`.]

---

**Date.** `<<INSERT submission date in YYYY-MM-DD format>>`

**To.** The Editors, *The Lancet Digital Health*

**Subject.** Submission of an unsolicited Viewpoint manuscript: "The
prompt is the protocol: a disclosure standard for clinician-investigators
using agentic large language models".

Dear Editors,

I am pleased to submit the enclosed unsolicited **Viewpoint** for
consideration in *The Lancet Digital Health*. The Viewpoint addresses a
question your editorial team has engaged with publicly through your AI
policy and through the Lancet group's editorial policies: what disclosure
standard should accompany manuscripts whose preparation involved
generative-AI tooling at depth?

I argue that the current Lancet group policy, calibrated for a 2023
generation of LLM use, has not kept pace with what individual clinician-
investigators are doing in 2026. The same year that Google's Co-Scientist
multi-agent system was published in *Nature* (\texttt{10.1038/s41586-026-
10644-y}), a single clinician with no large-lab affiliation can today
assemble an end-to-end agentic workflow on commodity tooling. The current
policy classifies most of what such a workflow does (argument development,
methods drafting, literature scoping, claim selection) as prohibited;
that classification has predictable equilibrium consequences neither side
wants.

The Viewpoint proposes a Disclosure 2.0 standard whose minimum unit is
\{prompt, model identifier, tool envelope, commit history, reviewer-
subagent transcripts, audit log, tagged release\}. Critically, the
manuscript and its supporting case study are themselves produced under
exactly that standard: every artefact the standard would require is
publicly archived at the GitHub repository linked in the manuscript's
Data Sharing statement. The reviewer's task is to adjudicate the policy
argument; the repository disposes of any factual dispute about whether
such a workflow exists.

I have made no formal commitment to the standard's adoption beyond
publishing the present submission under it. The submission is therefore
both an argument and a working example.

## Submission metadata

| Item                  | Value                                                         |
|-----------------------|---------------------------------------------------------------|
| Article type          | Viewpoint                                                     |
| Body word count       | 2 428 (texcount, body sections only; under the 2 500 ceiling) |
| References            | 14 (Vancouver superscript-numeric; ceiling 30)                |
| Display items         | 2 (Figure 1, artefact ledger; Figure 2, policy gap)           |
| Preprint              | medRxiv DOI to be inserted after preprint posting             |
| Repository            | `https://github.com/htlin222/end-to-end` (tag `viewpoint-v1.0.0`) |
| Persistent code DOI   | Zenodo DOI to be inserted after GitHub-Zenodo deposit         |

## Generative-AI background of the author

My prior LLM-adjacent work (theory-of-mind-like behaviour in LLM poker
agents, arXiv 2026, sole author) informs this Viewpoint's framing of
agentic-LLM disclosure. My day job is as a haematology and medical
oncology fellow; I am not an LLM researcher, and the present manuscript
reflects a clinician-investigator's practical encounter with agentic
tooling rather than a methods-paper contribution.

## Originality and exclusivity

This manuscript is original, has not been published, and is not under
consideration at another journal. The repository it links to is published
under the MIT licence; no other party holds rights that would conflict
with publication.

## Suggested reviewers

I respectfully suggest the following independent reviewers, none of whom
have a current collaboration, mentorship, or institutional relationship
with the author. Suggestions are offered to assist the editorial team and
are not binding.

1. `<<INSERT reviewer 1 name, affiliation, e-mail>>` — expertise:
   editorial policy on generative-AI in biomedical publishing.
2. `<<INSERT reviewer 2 name, affiliation, e-mail>>` — expertise:
   agentic LLM systems for scientific discovery.
3. `<<INSERT reviewer 3 name, affiliation, e-mail>>` — expertise:
   clinical-prediction-model reporting (TRIPOD).
4. `<<INSERT reviewer 4 name, affiliation, e-mail>>` — expertise:
   digital-health workflow reproducibility and FAIR principles.

I have no individuals to declare as preferred non-reviewers.

## Conflicts of interest

The author declares no competing interests. The author does not hold
equity, employment or paid advisory roles with Anthropic, Google, OpenAI,
or any other company whose generative-AI tools are discussed in the
manuscript. The author is a salaried haematology and medical oncology fellow at the Koo
Foundation Sun Yat-Sen Cancer Center, Taipei, Taiwan.

## Funding

This work received no specific funding. The Anthropic Claude subscription
used to operate the workflow is the author's personal expense.

## Generative-AI use

The manuscript and the supporting case study were prepared using
Anthropic Claude (Opus 4.7, 1M-context variant) via the Claude Code CLI
for argument development, methodology drafting, literature scoping,
claim selection and reviewer-subagent orchestration. Per the Lancet
group's current AI policy, this disclosure is reproduced verbatim in
the Acknowledgements section of the manuscript and is documented in
full at `docs/ai-usage-disclosure.md` in the linked repository. No AI
tool is listed as an author. No AI-generated figures are included.

## Closing

I would be grateful for consideration in *The Lancet Digital Health*. I
welcome correspondence at \texttt{mail@hsiehting.com}, and I am
available to revise the manuscript in response to editorial or peer
review.

Sincerely,

Hsieh-Ting Lin, M.D.
Department of Hematology and Medical Oncology
Koo Foundation Sun Yat-Sen Cancer Center
Taipei, Taiwan
ORCID: 0009-0002-3974-4528
