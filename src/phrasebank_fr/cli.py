"""Point d'entrée en ligne de commande : `python -m phrasebank_fr <commande>`."""
import argparse
import json

from .config import load_config
from .extract import extract_all
from .filter import filter_sentences
from .jsonl import read_jsonl, write_jsonl
from .sample import stratified_sample, to_label_studio
from .segment import segment_blocks
from .sources import download_missing, read_sources


def cmd_download(cfg: dict, args: argparse.Namespace) -> None:
    n = download_missing(cfg["paths"]["sources"], cfg["paths"]["raw"])
    print(f"{n} PDF téléchargé(s)")


def cmd_extract(cfg: dict, args: argparse.Namespace) -> None:
    out = cfg["paths"]["interim"] / "blocks.jsonl"
    ext = cfg["extract"]
    blocks = extract_all(
        cfg["paths"]["raw"], cfg["paths"]["sources"], ext["repeated_block_ratio"], ext["margin_ratio"]
    )
    n = write_jsonl(out, blocks)
    print(f"{n} blocs -> {out}")


def cmd_segment(cfg: dict, args: argparse.Namespace) -> None:
    src = cfg["paths"]["interim"] / "blocks.jsonl"
    out = cfg["paths"]["interim"] / "sentences_raw.jsonl"
    n = write_jsonl(out, segment_blocks(read_jsonl(src), cfg["segment"]["language"]))
    print(f"{n} phrases brutes -> {out}")


def cmd_filter(cfg: dict, args: argparse.Namespace) -> None:
    src = cfg["paths"]["interim"] / "sentences_raw.jsonl"
    out = cfg["paths"]["processed"] / "sentences.jsonl"
    n = write_jsonl(out, filter_sentences(read_jsonl(src), cfg["filter"]))
    print(f"{n} phrases retenues -> {out}")


def cmd_run(cfg: dict, args: argparse.Namespace) -> None:
    cmd_extract(cfg, args)
    cmd_segment(cfg, args)
    cmd_filter(cfg, args)


def cmd_sample(cfg: dict, args: argparse.Namespace) -> None:
    sources = {row["doc_id"]: row for row in read_sources(cfg["paths"]["sources"])}
    sector_of = {doc_id: row["sector"] for doc_id, row in sources.items()}
    rows = read_jsonl(cfg["paths"]["processed"] / "sentences.jsonl")
    sample = stratified_sample(rows, sector_of, args.n, args.seed)

    out = cfg["paths"]["annotations"] / f"{args.name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(to_label_studio(sample, sources), f, ensure_ascii=False, indent=2)

    per_sector = {}
    for row in sample:
        sector = sector_of.get(row["doc_id"], "Inconnu")
        per_sector[sector] = per_sector.get(sector, 0) + 1
    print(f"{len(sample)} phrases -> {out}")
    for sector, count in sorted(per_sector.items()):
        print(f"  {sector} : {count}")


COMMANDS = {
    "download": (cmd_download, "télécharge les PDF déclarés dans sources.csv"),
    "extract": (cmd_extract, "PDF -> blocs de texte"),
    "segment": (cmd_segment, "blocs -> phrases"),
    "filter": (cmd_filter, "phrases -> phrases exploitables"),
    "run": (cmd_run, "extract + segment + filter"),
    "sample": (cmd_sample, "tire un échantillon stratifié par secteur, au format Label Studio"),
}


def main() -> None:
    parser = argparse.ArgumentParser(prog="phrasebank", description="Pipeline du PhraseBank FR")
    sub = parser.add_subparsers(dest="command", required=True)
    parsers = {name: sub.add_parser(name, help=help_text) for name, (_, help_text) in COMMANDS.items()}
    parsers["sample"].add_argument("--n", type=int, default=100, help="nombre de phrases (défaut : 100)")
    parsers["sample"].add_argument("--seed", type=int, default=42, help="graine du tirage (défaut : 42)")
    parsers["sample"].add_argument("--name", default="pilot_100", help="nom du fichier de sortie")
    args = parser.parse_args()
    COMMANDS[args.command][0](load_config(), args)


if __name__ == "__main__":
    main()
