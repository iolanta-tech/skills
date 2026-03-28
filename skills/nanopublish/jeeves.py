"""Nanopublication publish: Markdown-LD via yaml-ld -> nanopub."""

from __future__ import annotations

import re
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import rdflib
import sh
import yaml
import yaml_ld
from rdflib import Dataset, Graph, Literal, Namespace, URIRef
from yaml_ld.to_rdf import ToRDFOptions


NP = Namespace("http://www.nanopub.org/nschema#")
PROV = Namespace("http://www.w3.org/ns/prov#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
TEMP_NP = Namespace("http://purl.org/nanopub/temp/np/")
PROFILE_PATH = Path.home() / ".nanopub" / "profile.yml"
PRODUCTION_REGISTRY = "https://registry.knowledgepixels.com/np/"
TEST_REGISTRY = "https://test.registry.knowledgepixels.com/np/"


def _assertion_from_markdown_ld(path: Path) -> Graph:
    path = path.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(path)

    nq = yaml_ld.to_rdf(path, ToRDFOptions(format="application/n-quads"))
    return Graph().parse(data=nq, format="nquads")


def _load_profile() -> dict:
    return yaml.safe_load(PROFILE_PATH.read_text())


def _now_literal() -> Literal:
    return Literal(datetime.now(timezone.utc).replace(tzinfo=None), datatype=XSD.dateTime)


def _build_nanopub(path: str, derived_from: str = "") -> Dataset:
    profile = _load_profile()
    assertion_source = _assertion_from_markdown_ld(Path(path))
    creation_time = _now_literal()

    dataset = Dataset()
    dataset.bind("np", NP)
    dataset.bind("prov", PROV)
    dataset.bind("xsd", XSD)

    for prefix, namespace in assertion_source.namespaces():
        dataset.bind(prefix, namespace)

    nanopub_uri = TEMP_NP[""]
    head_uri = TEMP_NP["Head"]
    assertion_uri = TEMP_NP["assertion"]
    provenance_uri = TEMP_NP["provenance"]
    pubinfo_uri = TEMP_NP["pubinfo"]

    head = Graph(dataset.store, head_uri)
    head.add((nanopub_uri, rdflib.RDF.type, NP.Nanopublication))
    head.add((nanopub_uri, NP.hasAssertion, assertion_uri))
    head.add((nanopub_uri, NP.hasProvenance, provenance_uri))
    head.add((nanopub_uri, NP.hasPublicationInfo, pubinfo_uri))

    assertion = Graph(dataset.store, assertion_uri)
    for triple in assertion_source:
        assertion.add(triple)

    provenance = Graph(dataset.store, provenance_uri)
    provenance.add((assertion_uri, PROV.generatedAtTime, creation_time))
    if derived_from.strip():
        provenance.add((assertion_uri, PROV.wasDerivedFrom, URIRef(derived_from.strip())))

    pubinfo = Graph(dataset.store, pubinfo_uri)
    pubinfo.add((nanopub_uri, PROV.generatedAtTime, creation_time))
    pubinfo.add((nanopub_uri, PROV.wasAttributedTo, URIRef(profile["orcid_id"])))

    return dataset


def _store_dataset(dataset: Dataset, destination: Path) -> None:
    destination.write_text(dataset.serialize(format="trig"))


def _default_signed_output_path(source_path: str) -> Path:
    source = Path(source_path).expanduser().resolve()
    return source.with_name(f"signed.{source.stem}.trig")


def _sign_with_rust_cli(dataset: Dataset) -> tuple[Path, str]:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        unsigned_path = tmpdir_path / "unsigned.trig"
        signed_path = tmpdir_path / f"signed.{unsigned_path.name}"
        _store_dataset(dataset, unsigned_path)

        output = str(sh.nanopub("sign", str(unsigned_path)))
        match = re.search(r"^URI:\s+(https://w3id\.org/np/\S+)$", output, re.MULTILINE)
        if not match:
            raise RuntimeError(f"Could not parse signed nanopub URI from output:\n{output}")
        if not signed_path.is_file():
            raise RuntimeError(f"Signed nanopub not created at {signed_path}")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".trig", prefix="signed-nanopub-") as handle:
            persisted_signed_path = Path(handle.name)
        shutil.copyfile(signed_path, persisted_signed_path)
        return persisted_signed_path, match.group(1)


def _publish_signed_file(signed_path: Path, test_server: bool = False) -> None:
    registry = TEST_REGISTRY if test_server else PRODUCTION_REGISTRY
    sh.curl(
        "--silent",
        "--show-error",
        "--fail-with-body",
        "-H",
        "Content-Type: application/trig",
        "--data-binary",
        f"@{signed_path}",
        registry,
    )


def publish(
    path: str,
    test_server: bool = False,
    derived_from: str = "",
    dry_run: bool = False,
    output: str = "",
):
    """Build a nanopub from a Markdown-LD file (yaml-ld), sign, publish or write TriG."""
    dataset = _build_nanopub(path, derived_from=derived_from)

    if output and output.strip():
        out_path = Path(output).expanduser().resolve()
        signed_path, source_uri = _sign_with_rust_cli(dataset)
        try:
            shutil.copyfile(signed_path, out_path)
        finally:
            signed_path.unlink(missing_ok=True)
        print(source_uri)
        print(f"Wrote {out_path}")
        return

    if dry_run:
        print(dataset.serialize(format="trig"))
        return

    signed_path, source_uri = _sign_with_rust_cli(dataset)
    out_path = _default_signed_output_path(path)
    try:
        shutil.copyfile(signed_path, out_path)
        _publish_signed_file(signed_path, test_server=test_server)
    finally:
        signed_path.unlink(missing_ok=True)
    print(source_uri)
    print(f"Wrote {out_path}")


def check(path: str):
    """Validate a signed nanopublication TriG using the Rust nanopub CLI."""
    output = str(sh.nanopub("check", str(Path(path).expanduser().resolve()))).strip()
    if output:
        print(output)
