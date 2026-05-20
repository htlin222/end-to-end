# Layer-2 Audit — Citation veracity log

**Tag**: `case-study-v1.0.0`
**Bib file**: `case-study/manuscript/references.bib` (30 `@article` entries)
**Method**: each entry resolved against the Crossref REST API
(`https://api.crossref.org/works/<DOI>`), cross-checked against PubMed
via the `claude_ai_PubMed` MCP server where the DOI did not match the
cited title.
**Audit date**: 2026-05-21

## Per-entry table

`Status` is `RESOLVED` (DOI returns the cited work),
`WRONG-TARGET` (DOI returns a real but different work),
`UNRESOLVED` (DOI does not resolve), `META-MISMATCH`
(DOI returns the work but the bib entry has misleading metadata
— e.g., a fabricated title or wrong year).

| Key | DOI | Status | Notes |
|-----|-----|--------|-------|
| cancer2017comprehensive | 10.1016/j.cell.2017.05.046 | RESOLVED | Cell 2017 TCGA-LIHC characterisation. **Uncited in main.tex.** |
| collins2015tripod | 10.7326/M14-0697 | RESOLVED | TRIPOD 2015 statement. Cited. |
| harrell1996multivariable | 10.1002/(SICI)1097-0258(19960229)15:4<361::AID-SIM168>3.0.CO;2-4 | RESOLVED | Harrell-Lee-Mark 1996. Cited. |
| hoshida2008gene | 10.1056/NEJMoa0804525 | RESOLVED | NEJM 2008. Cited. |
| boyault2007transcriptome | 10.1002/hep.21467 | RESOLVED | Hepatology 2007. **Uncited.** |
| roessler2010unique | 10.1158/0008-5472.CAN-10-2607 | RESOLVED | Cancer Res 2010. Cited. |
| villanueva2019hepatocellular | 10.1056/NEJMra1713263 | RESOLVED | NEJM 2019. Cited. |
| llovet2018hepatocellular | 10.1038/s41572-020-00240-3 | META-MISMATCH | DOI resolves correctly to Llovet et al., *Nat Rev Dis Primers* 2021 (PMID 33479224). Bib **key** says "2018" but `year=2021`. Citation works; key string is misleading. Cited. |
| rich2017quality | 10.6004/jnccn.2017.0117 | **WRONG-TARGET** | DOI resolves to "NCCN Guidelines Insights: Antiemesis, Version 2.2017" by Berger et al., **not** Rich/Yopp/Singal. PubMed search for `Rich NE quality survivorship hepatocellular` returns zero hits, and `Rich Yopp Singal quality survivorship hepatocellular carcinoma` returns zero hits. No JNCCN 2017 paper by Rich/Yopp/Singal on HCC survivorship care exists in PubMed. The bib entry appears to be hallucinated. **Uncited in main.tex.** |
| vickers2006decision | 10.1177/0272989X06295361 | RESOLVED | MDM 2006. Cited. |
| vickers2019simple | 10.1186/s41512-019-0064-7 | RESOLVED | Diagn Progn Res 2019. Cited. |
| steyerberg2010assessing | 10.1097/EDE.0b013e3181c30fb2 | RESOLVED | Epidemiology 2010. **Uncited.** |
| calderaro2019molecular | 10.1016/j.jhep.2019.06.001 | RESOLVED | J Hepatol 2019. Cited. |
| nault2013novel | 10.1053/j.gastro.2013.03.051 | META-MISMATCH | DOI resolves to Nault et al., *Gastroenterology* 2013, 145:176-187 — but the actual paper title is **"A Hepatocellular Carcinoma 5-Gene Score Associated With Survival of Patients After Liver Resection"** (PMID 23567350), not the bib's "A novel prognostic gene signature in early-stage hepatocellular carcinoma". Same authors, same DOI, same year, same journal, but the title in references.bib is paraphrased/incorrect (the 5-gene score paper is not specifically about early-stage HCC; it is about HCC resection). **Uncited in main.tex.** |
| wolbers2014concordance | 10.1093/biostatistics/kxt059 | RESOLVED | Biostatistics 2014. **Uncited.** |
| moons2015transparent | 10.7326/M14-0698 | RESOLVED | TRIPOD E&E 2015. Cited. |
| collins2024tripodai | 10.1136/bmj-2023-078378 | RESOLVED | TRIPOD+AI 2024. Cited. |
| villa2016neoangiogenesis | 10.1136/gutjnl-2014-308483 | RESOLVED | Gut 2016 (Crossref records first-online 2015; bib year 2016 = print year). **Uncited.** |
| singal2023aasld | 10.1097/HEP.0000000000000466 | RESOLVED | AASLD Guidance, Hepatology 2023. Cited. |
| vogel2022hepatocellular | 10.1016/S0140-6736(22)01200-4 | RESOLVED | Lancet 2022. Cited. |
| simon2011regularization | 10.18637/jss.v039.i05 | RESOLVED | JSS 2011. Cited. |
| davidson2019lifelines | 10.21105/joss.01317 | RESOLVED | JOSS 2019. Cited. |
| grossman2016toward | 10.1056/NEJMp1607591 | RESOLVED | NEJM 2016. Cited. |
| barrett2013ncbi | 10.1093/nar/gks1193 | RESOLVED | NAR 2012 (database issue) — bib year 2013 corresponds to the print issue. **Uncited.** |
| forner2018hepatocellular | 10.1016/S0140-6736(18)30010-2 | RESOLVED | Lancet 2018. Cited. |
| benjamini1995controlling | 10.1111/j.2517-6161.1995.tb02031.x | RESOLVED | JRSS-B 1995. **Uncited.** |
| uno2011c | 10.1002/sim.4154 | RESOLVED | Stat Med 2011. Cited. |
| pencina2012evaluating | 10.1093/aje/kws207 | RESOLVED | AJE 2012. Cited. |
| cox1972regression | 10.1111/j.2517-6161.1972.tb00899.x | RESOLVED | JRSS-B 1972. Cited. |
| pencina2008evaluating | 10.1002/sim.2929 | RESOLVED | Stat Med 2007 online / 2008 print. Cited. |

## Citation usage cross-check

21 of the 30 entries are cited at least once via `\citep{...}` in
`case-study/manuscript/main.tex`. Nine are present in the bib file but
never cited:

- `cancer2017comprehensive`, `boyault2007transcriptome`,
  `rich2017quality`, `steyerberg2010assessing`, `nault2013novel`,
  `wolbers2014concordance`, `villa2016neoangiogenesis`,
  `barrett2013ncbi`, `benjamini1995controlling`.

The two integrity-sensitive entries (`rich2017quality`,
`nault2013novel`) are both in the uncited set, so neither one
propagates a wrong claim into the manuscript text. They are however
shipped with the release, will appear in the `.bbl` if anything in a
later round adds a `\cite{}`, and document a Layer-1 failure mode
(citation hallucination during bib drafting that was not pruned before
the tag).

## Resolution summary

- 28 / 30 entries resolve to the correct work.
- 1 / 30 (`rich2017quality`) is a wrong-target / likely fabricated
  citation; the DOI points to an NCCN antiemesis guideline. No real
  matching paper found on PubMed.
- 1 / 30 (`nault2013novel`) has a correct DOI but an incorrect bib
  title; the actual paper is the Nault 5-gene score, not a "novel
  prognostic gene signature in early-stage HCC".
- 1 / 30 (`llovet2018hepatocellular`) has a misleading key (says 2018
  but the cited work is 2021); the bib `year` field is correct.

Both `rich2017quality` and `nault2013novel` are uncited in the
manuscript, so neither error reaches the reader of `main.pdf`. The
errors are however part of the published release artefact and are
recorded here for the ledger.
