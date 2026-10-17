# الريتاج للحلول التقنية

Arabic, right-to-left company website for AlRetaj Technology Solutions. The site presents technology services and EMPID, with contact at [info@alretaj.com](mailto:info@alretaj.com).

## Files

- `index.html`: page content, metadata, social preview, and organization structured data.
- `styles.css`: responsive visual design and locally hosted Tajawal Arabic font.
- `script.js`: mobile navigation and current copyright year.
- `assets/`: supplied badge and banner; `assets/fonts/` includes the Tajawal license.
- `robots.txt` and `sitemap.xml`: search crawler entry points.
- `content/posts.json`: Arabic article source content and related article links.
- `assets/blog/`: lightweight WebP featured images in 1200 px and 480 px sizes for the 12 original articles.
- `content/featured-images.json`: image descriptions, generation prompts, and exported file sizes.
- `tools/build_blog.py`: generates the static blog index, article pages, and sitemap from `content/posts.json`.
- `assets/empid/`: fresh, cropped screenshots from the Arabic Al Ofoq pilot tenant using test records.
- `SEO_STATUS.md`: current search visibility blocker and publication checks.

## Edit the blog

Update `content/posts.json`, then run `python tools/build_blog.py` from this directory. Commit or deploy the generated `blog/` pages with the rest of the site. Each article has its own title, summary, canonical URL, metadata, structured data, and links to related reading. The EMPID guide is at `/blog/empid/`.

The original service articles use generated illustrative photography. The WebP files in `assets/blog/` are the published versions; the large source PNGs are kept outside the site. Cards load 480 px thumbnails lazily, while article pages use responsive `srcset` and 1200 px images for larger screens.

## Preview

Serve this directory at the site root, for example `python -m http.server 4173` from `D:\alretaj`, then open `http://localhost:4173/`. Absolute asset paths assume deployment at the root of `https://alretaj.com/`.

Before publishing, confirm that `alretaj.com` is the final domain and that the described service categories match AlRetaj's actual offerings. The contact action opens the visitor's email client; there is no form or data collection on this site.
