import pymupdf

from phrasebank_fr.extract import extract_blocks
from phrasebank_fr.filter import filter_sentences
from phrasebank_fr.sample import stratified_sample
from phrasebank_fr.segment import segment_blocks
from phrasebank_fr.sources import parse_pages

FILTER_CFG = {
    "min_words": 6,
    "max_words": 60,
    "min_alpha_ratio": 0.6,
    "max_digit_ratio": 0.25,
    "require_final_punctuation": True,
    "exclude_patterns": [
        r"\(en (milliers|millions|milliards) de (dirhams|DH|MAD)\)",
        r"^\d+(\.\d+)+\s",
        r"^[IVX]+(\.\d+)+\s*[-–.]",
        r"^\d+\s*\*",
    ],
}


def _make_pdf(path, n_pages=3):
    doc = pymupdf.open()
    for i in range(1, n_pages + 1):
        page = doc.new_page()
        page.insert_text((72, 40), "Communication financiere T3 2024")
        page.insert_text((72, 400), f"Le chiffre d'affaires progresse de {i},5 % sur la periode.")
        page.insert_text((72, 800), f"Page {i}")
    doc.save(path)


def test_extract_removes_headers_and_footers(tmp_path):
    pdf = tmp_path / "doc.pdf"
    _make_pdf(pdf)
    texts = [b["text"] for b in extract_blocks(pdf, repeated_block_ratio=0.5, margin_ratio=0.12)]
    assert len(texts) == 3
    assert all("progresse" in t for t in texts)


def test_extract_keeps_only_selected_pages(tmp_path):
    pdf = tmp_path / "doc.pdf"
    _make_pdf(pdf)
    blocks = extract_blocks(pdf, repeated_block_ratio=0.5, margin_ratio=0.12, keep_pages={2, 3})
    assert [b["page"] for b in blocks] == [2, 3]


def test_stratified_sample_balances_sectors_and_is_reproducible():
    rows = (
        [{"id": f"a{i}", "doc_id": "bank", "sentence": "x"} for i in range(50)]
        + [{"id": f"b{i}", "doc_id": "mine", "sentence": "x"} for i in range(50)]
        + [{"id": f"c{i}", "doc_id": "telco", "sentence": "x"} for i in range(3)]  # secteur trop petit
    )
    sector_of = {"bank": "Banques", "mine": "Mines", "telco": "Télécoms"}
    sample = stratified_sample(rows, sector_of, n=21, seed=1)
    counts = {d: sum(r["doc_id"] == d for r in sample) for d in sector_of}
    assert counts == {"bank": 9, "mine": 9, "telco": 3}
    assert sample == stratified_sample(rows, sector_of, n=21, seed=1)


def test_parse_pages():
    assert parse_pages("") is None
    assert parse_pages("2;6-8") == {2, 6, 7, 8}
    assert parse_pages("1, 3") == {1, 3}


def test_segment_keeps_decimal_numbers():
    blocks = [{"doc_id": "d", "page": 1,
               "text": "Le PNB progresse de 8,2 % à 14,3 MMDH. Le RNPG recule de 3 %."}]
    sentences = [s["sentence"] for s in segment_blocks(blocks)]
    assert sentences == ["Le PNB progresse de 8,2 % à 14,3 MMDH.", "Le RNPG recule de 3 %."]


def test_segment_splits_bullets():
    blocks = [{"doc_id": "d", "page": 1, "text": "• Hausse du CA. • Baisse de la dette.  Dividende stable. › Marge en repli."}]
    assert [s["sentence"] for s in segment_blocks(blocks)] == [
        "Hausse du CA.", "Baisse de la dette.", "Dividende stable.", "Marge en repli."
    ]


def test_segment_strips_leading_markers_but_keeps_numbers():
    blocks = [{"doc_id": "d", "page": 1, "text": (
        "3 La distribution des dividendes pour un effet de -547.8 MDH. "
        "5-4-1 Le résultat d'exploitation progresse. "
        "2 482 millions de dirhams de résultat net."
    )}]
    assert [s["sentence"] for s in segment_blocks(blocks)] == [
        "La distribution des dividendes pour un effet de -547.8 MDH.",
        "Le résultat d'exploitation progresse.",
        "2 482 millions de dirhams de résultat net.",
    ]


def test_filter_drops_noise_and_assigns_ids():
    rows = [{"doc_id": "iam", "page": 1, "sentence": s} for s in [
        "Le chiffre d'affaires consolidé progresse de 3,1 % sur le trimestre.",
        "Le chiffre d'affaires consolidé progresse de 3,1 % sur le trimestre.",  # doublon
        "Faits marquants",                                                     # titre
        "2023 2024 12 450 13 210 6,1 % 8 900 9 100.",                          # ligne de tableau
        "Les dossiers physiques de la clientèle comprennent :",                # début de liste
        "2.10 Dettes envers la clientèle au 31 décembre 2023 (en milliers de dirhams)",  # titre de tableau
        "III.2.1 - Diversification par contrepartie et par secteur d'activité.",         # titre numéroté
        "L'endettement net augmente sensiblement à fin septembre.",
    ]]
    kept = list(filter_sentences(rows, FILTER_CFG))
    assert [r["id"] for r in kept] == ["iam_0001", "iam_0002"]
    assert "endettement" in kept[1]["sentence"]
