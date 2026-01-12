# Project Context

## Purpose
**Touzubaike (投資百科)** is a one-stop guide for investment and financial management, covering Cryptocurrency, Stocks, ETFs, and Credit Cards.
The project is a high-performance, SEO-optimized static site built with Astro, designed to provide accessible financial knowledge.

## Tech Stack
- **Framework:** Astro 5.x
- **Language:** TypeScript (Strict Mode)
- **Styling:** Tailwind CSS 4.x (via Vite plugin)
- **Content:** MDX, Astro Content Collections
- **Build Tool:** Vite
- **Deployment:** Static (likely Cloudflare Pages based on `.pages.dev` domain)

## Project Conventions

### Code Style
- **TypeScript:** Strict type checking enabled (`astro/tsconfigs/strict`).
- **Components:** `.astro` components for layout and UI.
- **CSS:** Utility-first with Tailwind CSS.
- **Formatting:** Prettier (implied by standard Astro setup).

### Architecture Patterns
- **Static Site Generation (SSG):** Default Astro behavior for maximum performance.
- **File-based Routing:** Routes defined in `src/pages`.
- **Content Collections:** Blog posts and structured content stored in `src/content` (e.g., `src/content/blog`).
- **Layouts:** Shared page wrappers in `src/layouts` (e.g., `BlogPost.astro`).

### Testing Strategy
- **Type Checking:** `npm run astro check` (Astro check + TypeScript).
- **Performance:** 100/100 Lighthouse score goal.
- **Linting:** Standard Astro linting.

### Git Workflow
- Standard feature-branch workflow.
- Commit messages should be descriptive.

## Domain Context
- **Target Audience:** Users interested in financial management and investment in Taiwan (implied by TWD mentions and Traditional Chinese).
- **Key Topics:** Crypto exchanges (Binance, MAX), Stablecoins (USDT), ETFs, Credit Cards.
- **Language:** Traditional Chinese (繁體中文).

## SEO Agent System
The project includes an automated SEO content factory powered by Python and Google Gemini.

### Agent Skills
1.  **Keyword Mining:** Analyzes GSC data (`查詢.csv`) to find high-potential keywords (Rank 1-20).
2.  **SERP Analysis:** Scrapes top 3 competitors to build winning content outlines.
3.  **Content Drafting:** Uses Gemini to write articles based on outlines and SEO best practices.
4.  **SEO Audit:** Automates the "SEO Checklist" verification (keyword density, structure).

## Important Constraints
- **Performance:** Must maintain high Core Web Vitals (Lighthouse 100/100).
- **SEO:** Critical requirement. Canonical URLs, OpenGraph data, Sitemap, and RSS are implemented.
- **Static Nature:** Dynamic features should be client-side only.

## External Dependencies
- **Cloudflare Pages:** Target deployment platform.
- **NPM Packages:** `@astrojs/mdx`, `@astrojs/rss`, `@astrojs/sitemap`, `tailwindcss`, `sharp`.
