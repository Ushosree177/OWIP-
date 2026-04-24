import tldextract
from ddgs import DDGS
from rapidfuzz import fuzz
import subprocess
import re

BAD_DOMAINS = [
    "wikipedia.org", "youtube.com", "facebook.com",
    "linkedin.com", "instagram.com", "twitter.com",
    "t.me", "reuters.com", "forbes.com"
]

SUSPICIOUS_KEYWORDS = [
    "movie", "torrent", "download", "watch",
    "stream", "free", "hd", "1080p"
]

STOPWORDS = ["university", "institute", "of", "the", "and"]

def clean_query(q):
    words = q.lower().split()
    return " ".join([w for w in words if w not in STOPWORDS])

def get_canonical_domain(url):
    if not url:
        return ""
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}".lower()

def classify_site(link):
    link = link.lower()

    if any(word in link for word in SUSPICIOUS_KEYWORDS):
        return "⚠️ Suspicious / Media"

    if any(bad in link for bad in BAD_DOMAINS):
        return "ℹ️ Informational"

    return "✅ Official / Likely Official"

def llm_choose_best(query, candidates):
    prompt = f"""
Choose the most likely official website for: {query}

Options:
{chr(10).join(candidates)}

Rules:
- choose main homepage only
- prefer official institutional domain
- avoid wiki, news, social, mirror, subpages
- return only one URL
"""

    try:
        result = subprocess.run(
            ["ollama", "run", "link-ai"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            timeout=40
        )

        output = result.stdout
        match = re.search(r'https?://\S+', output)

        if match:
            return match.group(0)

    except:
        pass

    return candidates[0]

def identify_official_website(user_query):
    query_clean = clean_query(user_query.strip())

    search_results = []
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(f"{query_clean} official website", max_results=8))
    except:
        try:
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query_clean, max_results=8))
        except:
            search_results = []

    if not search_results:
        return {
            "link": "https://www.google.com/search?q=" + query_clean,
            "category": "No data"
        }

    scored_candidates = []

    for i, res in enumerate(search_results):
        link = res["href"].lower()
        domain = get_canonical_domain(link)

        if not domain:
            continue

        if any(bad in link for bad in BAD_DOMAINS):
            continue

        score = 0
        score += (10 - i) * 2

        if domain.endswith(".gov") or domain.endswith(".gov.uk"):
            score += 25
        elif domain.endswith(".edu") or ".ac." in domain:
            score += 20
        elif domain.endswith(".org"):
            score += 10

        score += fuzz.token_set_ratio(domain, query_clean) / 5

        for w in query_clean.split():
            if w in domain:
                score += 2

        if link.count("/") > 3:
            score -= 5

        if any(word in link for word in SUSPICIOUS_KEYWORDS):
            score -= 20

        scored_candidates.append({
            "link": "https://" + domain,
            "score": score
        })

    finalists = sorted(scored_candidates, key=lambda x: x["score"], reverse=True)
    top3 = [x["link"] for x in finalists[:3]]

    best_link = llm_choose_best(query_clean, top3)
    category = classify_site(best_link)

    return {
        "link": best_link,
        "category": category
    }