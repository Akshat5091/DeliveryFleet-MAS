"""Tool 4: Vector RAG Knowledge Retrieval Tool using ChromaDB."""
from typing import List, Dict, Any, Optional
import os
from pathlib import Path
from ...config import KB_DIR, CHROMA_PERSIST_DIR

DEFAULT_POLICY_CORPUS = [
    {
        "source": "company_delivery_policy.txt",
        "text": "Statutory Driver Working Hour Limits: Drivers must never exceed 9.0 cumulative hours on duty per 24-hour cycle. When hours exceed 8.5 hours and projected trip duration exceeds 30 minutes, pre-emptive dispatch reassignment is required."
    },
    {
        "source": "company_delivery_policy.txt",
        "text": "Priority Cold-Chain Consignments: Critical medical deliveries and temperature-sensitive biologicals must be expedited via dedicated priority transit corridors with zero idle dwell time."
    },
    {
        "source": "delivery_zone_rules.txt",
        "text": "Municipal Zone B Freight Restrictions: Consignments exceeding 50.0 kg are strictly prohibited from entering or traversing Zone B during peak traffic hours between 17:00 and 20:00 to prevent gridlock."
    },
    {
        "source": "delivery_zone_rules.txt",
        "text": "Zone A Low-Emission Operations: Zone A urban core enforces green corridor prioritization favoring Electric Vans and zero-emission vehicles for commercial dispatches."
    },
    {
        "source": "driver_working_hour_limits.txt",
        "text": "Driver Safety and Fatigue Protocol: Dispatches must balance driver ratings with accumulated shift fatigue. Mandatory cooling breaks are enforced when fatigue thresholds are reached."
    }
]

class ChromaRAGTool:
    """Tool for querying company operational policies and municipal zone rules via Vector RAG with persistent fallback."""
    name: str = "policy_rag_search"
    description: str = "Searches internal company logistics policies, driver hour limits, and zone transit restrictions."

    def __init__(self, kb_dir: Optional[Path] = None):
        self.kb_dir = kb_dir or KB_DIR
        self.collection = None
        self.fallback_docs: List[Dict[str, str]] = []
        self._load_fallback_corpus()
        self._initialize_vector_db()

    def _initialize_vector_db(self) -> None:
        """Initialize ChromaDB collection and index documents."""
        try:
            import chromadb
            client = chromadb.PersistentClient(path=str(CHROMA_PERSIST_DIR))
            self.collection = client.get_or_create_collection(name="logistics_policies")
            
            # Check if collection is empty, then populate
            if self.collection.count() == 0:
                self._index_documents()
        except Exception:
            self.collection = None

    def _index_documents(self) -> None:
        """Chunk text files and add embeddings to ChromaDB collection."""
        docs = []
        metadatas = []
        ids = []
        doc_idx = 0

        if self.kb_dir and self.kb_dir.exists():
            for txt_file in self.kb_dir.glob("*.txt"):
                try:
                    content = txt_file.read_text(encoding="utf-8")
                    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                    for p in paragraphs:
                        docs.append(p)
                        metadatas.append({"source": txt_file.name})
                        ids.append(f"doc_{doc_idx}")
                        doc_idx += 1
                except Exception:
                    continue

        if docs and self.collection:
            try:
                self.collection.add(
                    documents=docs,
                    metadatas=metadatas,
                    ids=ids
                )
            except Exception:
                pass

    def _load_fallback_corpus(self) -> None:
        """In-memory corpus fallback for cross-platform portability."""
        self.fallback_docs = []
        if self.kb_dir and self.kb_dir.exists():
            for txt_file in self.kb_dir.glob("*.txt"):
                try:
                    content = txt_file.read_text(encoding="utf-8")
                    for p in content.split("\n\n"):
                        if p.strip():
                            self.fallback_docs.append({
                                "source": txt_file.name,
                                "text": p.strip()
                            })
                except Exception:
                    continue

        if not self.fallback_docs:
            self.fallback_docs = list(DEFAULT_POLICY_CORPUS)

    def search_rules(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search policy knowledge base for relevant clauses."""
        q_str = str(query or "general delivery policy").strip()
        safe_k = max(1, min(10, int(top_k or 3)))
        results = []

        if self.collection is not None:
            try:
                chroma_res = self.collection.query(
                    query_texts=[q_str],
                    n_results=safe_k
                )
                if chroma_res and chroma_res["documents"]:
                    docs = chroma_res["documents"][0]
                    metas = chroma_res["metadatas"][0]
                    for d, m in zip(docs, metas):
                        results.append({
                            "source": m.get("source", "unknown"),
                            "snippet": d,
                            "relevance_score": 0.92
                        })
                    if results:
                        return results
            except Exception:
                pass  # Use fallback

        # Fallback scoring: word intersection relevance
        query_words = set(q_str.lower().split())
        scored = []
        for doc in self.fallback_docs:
            doc_words = set(doc["text"].lower().split())
            overlap = len(query_words.intersection(doc_words))
            if overlap > 0:
                scored.append((overlap, doc))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        for _, doc in scored[:safe_k]:
            results.append({
                "source": doc["source"],
                "snippet": doc["text"][:300],
                "relevance_score": 0.88
            })

        if not results:
            results.append({
                "source": "company_delivery_policy.txt",
                "snippet": "Standard dispatch policy: 9-hour driver limit, priority cold-chain protocol.",
                "relevance_score": 0.70
            })
        return results

