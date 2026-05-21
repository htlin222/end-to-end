# NEJM AI Perspective Submission Playbook

Single source of truth for the operator's submission-day actions.
Everything below is YOU (Hsieh-Ting Lin); the Claude side has done
all the upstream work and committed.

## Current state

- Repo public: https://github.com/htlin222/end-to-end ✓
- NEJM AI Perspective manuscript: `manuscript-nejmai/main.pdf` (4 pages,
  620 body words, 5 refs, 1 figure) at tag `viewpoint-nejmai-v1.0.0` ✓
- Cover letter: `manuscript-nejmai/cover-letter.md` (4 `<<INSERT>>`
  placeholders for reviewer names + medRxiv DOI + Zenodo DOI + date) ✓
- medRxiv submission metadata: `manuscript-nejmai/medrxiv-metadata.md` ✓
- Lancet DH fallback: `manuscript/main.pdf` at tag `viewpoint-v1.1.0` ✓
- Case-study v1.0.1 (F1 blocker fixed): tag `case-study-v1.0.1` ✓

## Step 1 — medRxiv preprint posting (operator manual, ~30 min)

1. Go to https://www.medrxiv.org/submit
2. Account: log in with `hsieh.ting.lin@gmail.com` (create one if no
   existing medRxiv account — confirmation email will land in your
   Work Gmail; himalaya can fetch if needed)
3. Follow the 14-step workflow in `medrxiv-metadata.md`
4. Upload `release/viewpoint-nejmai-v1.0.0/end-to-end-nejmai.pdf`
5. Submit; expect DOI within 1–3 business days
6. When DOI arrives, replace `<<INSERT medRxiv DOI>>` in the cover
   letter and re-export the PDF if you reference the DOI in body text

## Step 2 — Zenodo DOI (operator manual, ~10 min once medRxiv lands)

1. Go to https://zenodo.org and log in with your GitHub account
2. Enable the GitHub-Zenodo integration for `htlin222/end-to-end`
   (Settings → Linked accounts → GitHub → flip toggle)
3. Push a new release tag OR trigger a re-sync; Zenodo mints a DOI
4. Cite the Zenodo DOI in the cover letter

## Step 3 — NEJM AI submission via Editorial Manager (operator manual, ~60 min)

NEJM AI does NOT accept pre-submission inquiries; submit directly.

1. Go to https://www.editorialmanager.com/nejmai (or whichever
   submission system NEJM AI uses; verify on the journal's "Author
   Center" page at https://ai.nejm.org/author-center)
2. Create an account with `hsieh.ting.lin@gmail.com` + ORCID
   0009-0002-3974-4528 (the existing eJCRP Editorial Manager account
   does NOT carry over; each journal has its own Aries database)
3. Select "Perspective" article type
4. Fill author block:
   - Hsieh-Ting Lin, MD
   - Koo Foundation Sun Yat-Sen Cancer Center, Hematology and Medical
     Oncology, Taipei, Taiwan
   - ORCID 0009-0002-3974-4528
   - mail@hsiehting.com
5. Title: "The prompt is the protocol: a disclosure standard for
   clinician-investigators using agentic large language models"
6. Abstract: copy the 1-sentence abstract from `manuscript-nejmai/
   main.tex` (or use the 350-word medRxiv abstract if NEJM AI EM asks
   for a longer one at submission)
7. Body word count: 620 (well under 1,200 ceiling)
8. Upload `manuscript-nejmai/main.pdf` as the main manuscript file
9. Upload `manuscript-nejmai/main.tex` and `references.bib` as
   supplementary LaTeX sources
10. Upload `manuscript-nejmai/cover-letter.md` (compile to PDF via
    `pandoc manuscript-nejmai/cover-letter.md -o cover-letter.pdf`)
    as the cover letter file
11. Fill suggested reviewer names (the cover letter has placeholders;
    populate based on your judgement; see "Suggested reviewer
    candidates" below for starting points)
12. Conflicts of interest: declare none
13. Funding: declare none
14. AI usage statement: NEJM AI EM has an explicit AI-disclosure
    field; paste the Acknowledgements paragraph from `main.tex` plus
    "Full per-step log at https://github.com/htlin222/end-to-end/
    blob/main/docs/ai-usage-disclosure.md"
15. Confirm not under consideration elsewhere; click Submit

## Suggested reviewer candidates (you choose; conflict-screen against
Koo Foundation, Anthropic, Google DeepMind, OpenAI, Sakana AI)

Editorial AI policy in biomedical publishing:
- Mohammad Hosseini (Northwestern, ORCID 0000-0002-2820-4592) — published
  "Disclosing generative AI use for writing assistance should be
  voluntary" (Sage 2025; multiple AI-disclosure-policy papers)
- Kristi Holmes (Northwestern Health Sciences Library, ORCID
  0000-0001-8420-5254) — co-author with Hosseini

Agentic LLM scientific discovery:
- James Zou (Stanford, ORCID 0000-0001-8880-4764) — author of
  Lancet 2025 "Rise of agentic AI teammates in medicine"
- Atul Butte (UCSF, ORCID 0000-0002-7433-2740) — broad AI-in-medicine
  policy + Methods voice
- Jeff Clune (UBC / Vector Institute, ORCID 0000-0002-3361-2887) —
  Sakana AI Scientist co-author

Clinical-prediction-model reporting (TRIPOD):
- Karel G. M. Moons (UMC Utrecht, ORCID 0000-0003-2118-004X) — TRIPOD
  steering committee
- Gary S. Collins (Oxford, ORCID 0000-0002-2772-2316) — TRIPOD-AI

Digital-health workflow reproducibility / FAIR:
- Andrew L. Beam (HSPH, ORCID 0000-0001-7989-1923) — multiple
  reproducibility-in-clinical-AI editorials
- Karandeep Singh (UCSD, ORCID 0000-0001-9089-1995) — has Lancet AI
  and JAMA Network Open track record

Diversify: aim for one US, one EU, one Asia-Pacific (non-Taiwan), one
flexible. Exclude any current collaborator and any paid Anthropic /
Google DeepMind / OpenAI / Sakana relationship.

## Step 4 — Wait

NEJM AI decision time: typically 4–8 weeks. If desk-rejected:
- Re-target Lancet DH using `manuscript/main.pdf` at viewpoint-v1.1.0
- Cover letter `manuscript/cover-letter.md` is already drafted
- Repository state does not need to change; just submit through the
  Lancet group Editorial Manager at https://www.editorialmanager.com/landig/

If accepted with revisions: respond per the typical reviewer-loop
workflow; the Disclosure 2.0 manifest in the repo means every
revision is traceable.

## Step 5 — On acceptance (operator)

1. Make the case-study-v1.0.1 release public (already is)
2. Verify the NEJM AI version is consistent with the longer Lancet DH
   companion (viewpoint-v1.1.0); decide whether to retract the
   companion or leave it in the repo as an alternative format
3. Post the final NEJM AI version of the manuscript to medRxiv as a
   v2 of the preprint
4. Publish acceptance in your CV
