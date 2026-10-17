"""Build the Arabic blog as static HTML for deployment at alretaj.com."""

from __future__ import annotations

import html
import json
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
POSTS = json.loads((ROOT / "content" / "posts.json").read_text(encoding="utf-8"))
SITE = "https://alretaj.com"
BRAND = "الريتاج للحلول التقنية"
EXTERNAL_READING = {
    "multi-branch-operations": (
        "كيف تنقل طريقة تشغيل نجحت من فرع إلى آخر؟",
        "https://orkeed.com/blog/multi-branch-operations/",
        "دليل من أوركيد لتجهيز حزمة تشغيل تراعي الاختلافات المحلية قبل توسيع التجربة.",
        "أوركيد",
    ),
    "cloud-readiness-for-business": (
        "قائمة جاهزية السحابة قبل النقل",
        "https://bsmah.com/blog/cloud-readiness-for-business/",
        "دليل من بصمة لمراجعة الاعتماديات والتكلفة وخطة الرجوع قبل التنفيذ.",
    ),
    "empid-attendance-visibility": (
        "خمس خطوات لمراجعة الحضور قبل اعتماد الشهر",
        "https://bsmah.com/blog/empid-attendance-visibility/",
        "قائمة من بصمة لتحويل شاشة الحضور إلى إجراء مراجعة واضح للفريق.",
    ),
    "systems-integration-without-duplicate-work": (
        "خريطة ربط الأنظمة قبل كتابة التكامل",
        "https://bsmah.com/blog/systems-integration-without-duplicate-work/",
        "ورقة عمل من بصمة لتحديد مصدر البيانات وقواعد التعارض بين الأنظمة.",
    ),
}


PRODUCT_READING = {
    "empid-hr-operations": ("كيف يرتبط ملف الموظف بالخدمات اليومية؟", "https://www.empid.com/employee-management/", "دليل EMPID الرسمي لملف الموظف ومسارات العمل المرتبطة به."),
    "empid-attendance-visibility": ("شاهد طريقة مراجعة الحضور في EMPID", "https://www.empid.com/attendance-management/", "شرح رسمي للشاشات والخطوات التي تعرض سجل الحضور والاستثناءات."),
    "empid-leave-requests": ("تعرّف إلى إدارة الإجازات في EMPID", "https://www.empid.com/leave-management/", "دليل المنتج لطلبات الإجازة والأرصدة ومسار الموافقة."),
    "empid-employee-self-service": ("استكشف الخدمة الذاتية للموظف", "https://www.empid.com/employee-self-service/", "شرح رسمي للطلبات التي يستطيع الموظف متابعتها من حسابه."),
    "empid-reports-for-hr": ("اطلع على تقارير وتحليلات EMPID", "https://www.empid.com/reports-analytics/", "دليل المنتج لقراءة المؤشرات والتقارير بحسب صلاحيات الفريق."),
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def page_head(title: str, description: str, path: str, schema: object, og_type: str = "article", visual: dict | None = None) -> str:
    canonical = f"{SITE}{path}"
    image_url = f"{SITE}{visual['src']}" if visual else f"{SITE}/assets/alretaj-badge.png"
    image_alt = visual["alt"] if visual else BRAND
    return f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#071a34">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" type="image/png" href="/assets/alretaj-badge.png">
  <link rel="preload" href="/assets/fonts/tajawal-arabic-400.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/styles.css">
  <meta property="og:type" content="{og_type}">
  <meta property="og:locale" content="ar_AR">
  <meta property="og:site_name" content="{BRAND}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{esc(image_url)}">
  <meta property="og:image:alt" content="{esc(image_alt)}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
  <a class="skip-link" href="#main">انتقل إلى المحتوى</a>
  <header class="site-header" id="top">
    <div class="wrap header-inner">
      <a class="brand" href="/" aria-label="الريتاج للحلول التقنية، الصفحة الرئيسية">
        <img src="/assets/alretaj-badge.png" alt="" width="48" height="48">
        <span class="brand-copy"><strong>الريتاج</strong><small>للحلول التقنية</small></span>
      </a>
      <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="افتح القائمة"><span></span><span></span><span></span></button>
      <nav id="site-nav" class="site-nav" aria-label="التنقل الرئيسي">
        <a href="/#about">من نحن</a><a href="/#services">خدماتنا</a><a href="/#empid">EMPID</a><a href="/blog/">المدونة</a><a class="nav-contact" href="/#contact">تواصل معنا <span aria-hidden="true">↗</span></a>
      </nav>
    </div>
  </header>
"""


def footer() -> str:
    return f"""  <footer class="site-footer">
    <div class="wrap footer-main">
      <div class="footer-brand"><img src="/assets/alretaj-badge.png" alt="" width="52" height="52"><div><strong>{BRAND}</strong><span>AlRetaj Technology Solutions</span></div></div>
      <div class="footer-links"><a href="/">الرئيسية</a><a href="/#services">خدماتنا</a><a href="/blog/">المدونة</a><a href="mailto:info@alretaj.com">البريد الإلكتروني</a></div>
    </div>
    <div class="wrap footer-bottom"><span>© <span id="year">2026</span> {BRAND}</span><a href="#top">العودة للأعلى ↑</a></div>
  </footer>
  <script src="/script.js" defer></script>
</body>
</html>
"""


def breadcrumb_schema(title: str, path: str) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "الرئيسية", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "المدونة", "item": f"{SITE}/blog/"},
            {"@type": "ListItem", "position": 3, "name": title, "item": f"{SITE}{path}"},
        ],
    }


def article_card(post: dict) -> str:
    thumb = ""
    if post.get("featured"):
        thumb = f'<a class="blog-card-image" href="/blog/{esc(post["slug"])}/" tabindex="-1" aria-hidden="true"><img src="{esc(post["featured"]["thumb"])}" alt="" width="480" height="270" loading="lazy" decoding="async"></a>'
    elif post.get("visual"):
        thumb = f'<a class="blog-card-image" href="/blog/{esc(post["slug"])}/" tabindex="-1" aria-hidden="true"><img src="{esc(post["visual"]["src"])}" alt="" width="1360" height="794" loading="lazy" decoding="async"></a>'
    return f"""<article class="blog-card">
      {thumb}
      <p class="blog-card-category">{esc(post['category'])}</p>
      <h3><a href="/blog/{esc(post['slug'])}/">{esc(post['title'])}</a></h3>
      <p>{esc(post['summary'])}</p>
      <a class="blog-card-link" href="/blog/{esc(post['slug'])}/" aria-label="اقرأ: {esc(post['title'])}">اقرأ المقال <span aria-hidden="true">←</span></a>
    </article>"""


def build_index() -> None:
    title = f"مدونة الأعمال والتقنية | {BRAND}"
    description = "مقالات عملية عن تطوير المواقع والتطبيقات، تكامل الأنظمة، السحابة، الدعم التقني، نقل البيانات، التحول الرقمي، ومنصة EMPID للموارد البشرية."
    schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "مدونة الريتاج للحلول التقنية",
        "url": f"{SITE}/blog/",
        "description": description,
        "inLanguage": "ar",
        "publisher": {"@type": "Organization", "name": BRAND, "url": f"{SITE}/"},
    }
    cards = "\n".join(article_card(post) for post in POSTS)
    body = f"""<main id="main">
  <section class="blog-landing-hero">
    <div class="wrap">
      <nav class="breadcrumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">/</span><span>المدونة</span></nav>
      <p class="section-kicker">أفكار للعمل اليومي</p>
      <h1>التقنية أوضح حين تبدأ من سؤال جيد.</h1>
      <p>هنا نكتب عن القرارات التي تواجه فرق الأعمال: متى نطوّر نظاماً؟ كيف ننقل بياناتنا؟ وما الذي يجعل التشغيل أكثر استقراراً؟ مقالات قصيرة تقرأها قبل أن تبدأ مشروعك.</p>
      <a class="blog-empid-link" href="/blog/empid/">شاهد دليل EMPID بالصور ←</a>
    </div>
  </section>
  <section class="blog-list-section section" aria-labelledby="blog-list-title">
    <div class="wrap">
      <div class="blog-list-heading"><div><p class="section-kicker">من المدونة</p><h2 id="blog-list-title">موضوعات تساعدك على الاختيار.</h2></div><span>{len(POSTS)} مقالة</span></div>
      <div class="blog-grid">{cards}</div>
    </div>
  </section>
  <section class="blog-contact"><div class="wrap"><div><p class="section-kicker">لديك تحدٍ محدد؟</p><h2>لننظر إليه معاً.</h2></div><a class="button button-gold" href="mailto:info@alretaj.com">راسلنا <span aria-hidden="true">↗</span></a></div></section>
</main>
"""
    dest = ROOT / "blog" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page_head(title, description, "/blog/", schema, "website") + body + footer(), encoding="utf-8")


def build_empid_hub() -> None:
    title = "EMPID بالعربية: الحضور والإجازات والتقارير | الريتاج"
    description = "تعرّف إلى EMPID من خلال لقطات حقيقية من التطبيق العربي: الحضور والانصراف، إدارة الإجازات، الخدمة الذاتية، وتقارير الموارد البشرية."
    posts = [post for post in POSTS if post.get("visual")]
    cards = "\n".join(article_card(post) for post in posts)
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "دليل EMPID",
        "description": description,
        "url": f"{SITE}/blog/empid/",
        "inLanguage": "ar",
        "hasPart": [{"@type": "BlogPosting", "name": post["title"], "url": f"{SITE}/blog/{post['slug']}/"} for post in posts],
    }
    body = f"""<main id="main">
  <section class="blog-landing-hero empid-hub-hero"><div class="wrap empid-hub-hero-grid"><div>
    <nav class="breadcrumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">/</span><a href="/blog/">المدونة</a><span aria-hidden="true">/</span><span>EMPID</span></nav>
    <p class="section-kicker">دليل المنتج</p><h1>EMPID في يوم العمل الحقيقي.</h1>
    <p>شاهد كيف تبدو مهام الموارد البشرية داخل التطبيق العربي. اللقطات مأخوذة من بيئة عرض الأفق ببيانات اختبار، ونشرح ما يمكن أن يستفيد منه فريقك وما يحتاج إلى إعداد قبل التشغيل.</p>
  </div><div class="empid-hub-preview"><a href="/assets/empid/attendance.png" data-lightbox aria-label="تكبير لقطة شاشة الحضور والانصراف"><img src="/assets/empid/attendance.png" alt="لقطة من شاشة الحضور والانصراف العربية في EMPID" width="1360" height="794" fetchpriority="high"></a><span>شاشة فعلية · بيئة عرض تجريبية</span></div></div></section>
  <section class="blog-list-section section"><div class="wrap">
    <div class="blog-list-heading"><div><p class="section-kicker">من داخل التطبيق</p><h2>ابدأ بالمسار الذي يهمك.</h2></div><span>{len(posts)} مقالات</span></div>
    <div class="blog-grid">{cards}</div>
    <p class="empid-hub-more">تبحث عن الصورة العامة؟ <a href="/blog/empid-hr-operations/">اقرأ كيف يجمع EMPID أعمال الموارد البشرية اليومية ←</a></p>
  </div></section>
</main>"""
    dest = ROOT / "blog" / "empid" / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page_head(title, description, "/blog/empid/", schema, "website", posts[0]["visual"]) + body + footer(), encoding="utf-8")


def build_article(post: dict, posts_by_slug: dict[str, dict]) -> None:
    slug = post["slug"]
    path = f"/blog/{slug}/"
    title = f"{post.get('seo_title', post['title'])} | الريتاج"
    description = post["summary"]
    preview = post.get("featured") or post.get("visual")
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "headline": post["title"],
                "description": description,
                "mainEntityOfPage": f"{SITE}{path}",
                "url": f"{SITE}{path}",
                "inLanguage": "ar",
                "author": {"@type": "Organization", "name": BRAND},
                "publisher": {"@type": "Organization", "name": BRAND, "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/alretaj-badge.png"}},
                **({"image": f"{SITE}{preview['src']}"} if preview else {}),
                **({"datePublished": post["published"], "dateModified": post["published"]} if post.get("published") else {}),
            },
            breadcrumb_schema(post["title"], path),
        ],
    }
    paragraphs = "\n".join(f"<p>{esc(p)}</p>" for p in post["intro"])
    visual = post.get("visual")
    featured = post.get("featured")
    figure = ""
    if visual:
        figure = f"""<figure class="empid-figure">
          <div class="empid-figure-top"><span class="empid-live-dot"></span>من شاشة EMPID العربية <span>لقطة فعلية</span></div>
          <div class="empid-image-frame"><a href="{esc(visual['src'])}" data-lightbox aria-label="تكبير لقطة شاشة EMPID"><img src="{esc(visual['src'])}" alt="{esc(visual['alt'])}" width="1360" height="{600 if visual['src'].endswith('self-dashboard.png') else 794}" loading="eager" fetchpriority="high"></a><span class="empid-figure-pointer" style="left:{visual.get('focus_x', 40)}%;top:{visual.get('focus_y', 38)}%" aria-hidden="true">↘</span></div>
          <figcaption><strong>{esc(visual['focus'])}</strong><span>{esc(visual['caption'])}</span></figcaption>
        </figure>"""
    featured_figure = ""
    if featured:
        featured_figure = f"""<figure class="article-featured wrap">
          <a href="{esc(featured['src'])}" data-lightbox aria-label="تكبير الصورة التوضيحية للمقال">
            <img src="{esc(featured['src'])}" srcset="{esc(featured['thumb'])} 480w, {esc(featured['src'])} 1200w" sizes="(max-width: 760px) calc(100vw - 36px), 1100px" alt="{esc(featured['alt'])}" width="1200" height="675" fetchpriority="high" decoding="async">
          </a>
          <figcaption>صورة توضيحية للمقال</figcaption>
        </figure>"""
    sections = []
    for index, section in enumerate(post["sections"], 1):
        section_paragraphs = "\n".join(f"<p>{esc(p)}</p>" for p in section["paragraphs"])
        bullets = ""
        if section.get("bullets"):
            bullets = "<ul>" + "".join(f"<li>{esc(item)}</li>" for item in section["bullets"]) + "</ul>"
        sections.append(f'<section id="section-{index}"><h2>{esc(section["heading"])}</h2>{section_paragraphs}{bullets}</section>')
    related = "\n".join(article_card(posts_by_slug[slug]) for slug in post["related"])
    external = EXTERNAL_READING.get(slug)
    external_reading = (
        f'<aside class="external-reading"><span>قراءة مرتبطة من {esc(external[3] if len(external) > 3 else "بصمة")}</span><a href="{esc(external[1])}">{esc(external[0])} ←</a><p>{esc(external[2])}</p></aside>'
        if external else ""
    )
    product = PRODUCT_READING.get(slug)
    product_reading = (
        f'<aside class="external-reading"><span>من دليل EMPID الرسمي</span><a href="{esc(product[1])}">{esc(product[0])} ←</a><p>{esc(product[2])}</p></aside>'
        if product else ""
    )
    body = f"""<main id="main">
  <article>
    <header class="article-hero{' empid-article-hero' if visual else ''}"><div class="wrap article-hero-inner">
      <nav class="breadcrumbs" aria-label="مسار الصفحة"><a href="/">الرئيسية</a><span aria-hidden="true">/</span><a href="/blog/">المدونة</a><span aria-hidden="true">/</span><span>{esc(post['category'])}</span></nav>
      <p class="section-kicker">{esc(post['category'])}</p>
      <h1>{esc(post['title'])}</h1>
      <p class="article-summary">{esc(post['summary'])}</p>
    </div></header>
    {featured_figure}
    <div class="wrap article-layout">
      <aside class="article-aside"><span>في هذا المقال</span><nav aria-label="أقسام المقال">{''.join(f'<a href="#section-{i}">{esc(s["heading"])}</a>' for i,s in enumerate(post['sections'],1))}<a href="#next-step">خطوة عملية</a></nav></aside>
      <div class="article-body">{paragraphs}{figure}{''.join(sections)}<section class="article-next" id="next-step"><p class="section-kicker">خطوة عملية</p><h2>{esc(post['takeaway_title'])}</h2><p>{esc(post['takeaway'])}</p></section>{external_reading}{product_reading}
        <div class="article-cta"><p>إذا كان هذا التحدي قريباً من واقع عملك، اكتب لنا ما تحتاجه.</p><a class="button button-gold" href="mailto:info@alretaj.com?subject={quote(post['subject'])}">تحدث مع الريتاج <span aria-hidden="true">↗</span></a></div>
      </div>
    </div>
  </article>
  <section class="related-section section" aria-labelledby="related-title"><div class="wrap"><div class="related-heading"><div><p class="section-kicker">اقرأ أيضاً</p><h2 id="related-title">موضوعات مرتبطة.</h2></div><a href="/blog/">كل المقالات ←</a></div><div class="blog-grid related-grid">{related}</div></div></section>
</main>
"""
    dest = ROOT / "blog" / slug / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(page_head(title, description, path, schema, visual=preview) + body + footer(), encoding="utf-8")


def build_sitemap() -> None:
    urls = ["/", "/blog/", "/blog/empid/"] + [f"/blog/{post['slug']}/" for post in POSTS]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines += [f"  <url><loc>{SITE}{url}</loc></url>" for url in urls]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    slugs = [post["slug"] for post in POSTS]
    if len(slugs) != len(set(slugs)):
        raise ValueError("Duplicate blog slugs")
    posts_by_slug = {post["slug"]: post for post in POSTS}
    for post in POSTS:
        if not all(slug in posts_by_slug and slug != post["slug"] for slug in post["related"]):
            raise ValueError(f"Invalid related post in {post['slug']}")
    build_index()
    build_empid_hub()
    for post in POSTS:
        build_article(post, posts_by_slug)
    build_sitemap()
    print(f"Built blog index and {len(POSTS)} articles")


if __name__ == "__main__":
    main()
