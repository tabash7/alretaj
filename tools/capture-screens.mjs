// Captures demo-workspace screens for the AlRetaj EMPID articles.
// Run from any folder:  node D:\alretaj\tools\capture-screens.mjs
// A visible browser opens. Sign in yourself (email, password, 2FA code). The script waits, then captures.
// No credentials are stored or read by this script. Avatars are hidden so no faces appear.
import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
const require = createRequire('D:/hrms/package.json');
const { chromium } = require('playwright');

const BASE = process.env.EMPID_BASE || 'http://localhost:5173';
const OUT = 'D:/alretaj/tools/capture-review/raw';
mkdirSync(OUT, { recursive: true });

// name, route, optional clicks (visible text, in order), optional scrollY
const SHOTS = [
  ['dashboard', '/dashboard'],
  ['command-center', '/workforce-command-center'],
  ['employees', '/employees'],
  ['employee-360', '/employees', { openFirstEmployee: true }],
  ['documents', '/documents'],
  ['contracts', '/contracts'],
  ['attendance', '/attendance'],
  ['team-attendance', '/team/attendance'],
  ['reports-attendance', '/reports/attendance'],
  ['admin-shifts', '/admin/shifts'],
  ['leave', '/leave'],
  ['leave-approvals', '/leave/approvals'],
  ['admin-settings-leave', '/admin/settings', { clicks: ['سياسات الإجازات'] }],
  ['admin-settings-email', '/admin/settings?tab=email'],
  ['timetracking', '/timetracking'],
  ['timetracking-approvals', '/timetracking/approvals'],
  ['timetracking-overtime', '/timetracking/overtime'],
  ['payroll', '/payroll'],
  ['payroll-statements', '/payroll/statements'],
  ['payroll-readiness', '/payroll-readiness'],
  ['my-payslips', '/my-payslips'],
  ['benefits-available', '/benefits', { clicks: ['المزايا المتاحة'] }],
  ['benefits-mine', '/benefits', { clicks: ['مزاياي'] }],
  ['benefits-leave-balance', '/benefits', { clicks: ['رصيد الإجازات'] }],
  ['expenses', '/expenses'],
  ['expenses-reports', '/expenses', { clicks: ['التقارير'] }],
  ['assets', '/assets'],
  ['my-assets', '/my-assets'],
  ['projects', '/projects'],
  ['tasks', '/tasks'],
  ['reports-project-time', '/reports/project-time'],
  ['reports-project-time-rates', '/reports/project-time', { scrollY: 900 }],
  ['performance', '/performance'],
  ['performance-goals', '/performance/goals'],
  ['onboarding', '/onboarding'],
  ['onboarding-documents', '/onboarding?tab=documents'],
  ['onboarding-progress', '/onboarding?tab=progress'],
  ['employee-relations', '/employee-relations'],
  ['employee-relations-separation', '/employee-relations', { clicks: ['الانفصال'] }],
  ['surveys', '/surveys'],
  ['appreciations', '/appreciations'],
  ['referrals', '/referrals'],
  ['gcc-obligations', '/compliance/gcc-obligations'],
  ['gcc-data-quality', '/compliance/gcc-data-quality'],
  ['gcc-audit-readiness', '/reports/gcc-compliance/audit-readiness'],
  ['reports', '/reports'],
  ['reports-lower', '/reports', { scrollY: 900 }],
  ['analytics', '/analytics'],
  ['email', '/email'],
  ['email-scheduled', '/email/scheduled'],
  ['settings-sso', '/settings?tab=sso'],
  ['settings-security', '/settings?tab=security'],
];

const HIDE_FACES = `
  img[src*="avatar" i], img[alt*="avatar" i], [class*="avatar" i] img, [data-avatar] img, header img[src^="blob:"], img[src*="photo" i], img[src*="profile" i] { visibility: hidden !important; }
  [class*="toast" i], [role="status"][class*="toast" i] { display: none !important; }
`;

const browser = await chromium.launch({ headless: false });
const ctx = await browser.newContext({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1, locale: 'ar-SA', timezoneId: 'Asia/Riyadh', colorScheme: 'light' });
const page = await ctx.newPage();
await page.goto(`${BASE}/login`);
console.log('>>> Sign in in the browser window (email, password, 2FA). Waiting up to 10 minutes...');
await page.waitForURL((u) => !u.pathname.startsWith('/login'), { timeout: 600000 });
await page.waitForLoadState('networkidle').catch(() => {});
console.log('Signed in. Capturing...');

// force light theme + Arabic where the app stores it
await page.evaluate(() => { try { localStorage.setItem('theme', 'light'); } catch {} }).catch(() => {});

const log = [];
for (const [name, route, opts = {}] of SHOTS) {
  const rec = { name, route, status: 'ok', note: '' };
  try {
    await page.goto(`${BASE}${route}`, { waitUntil: 'domcontentloaded' });
    await page.waitForLoadState('networkidle', { timeout: 15000 }).catch(() => {});
    await page.addStyleTag({ content: HIDE_FACES });
    await page.waitForTimeout(1800);
    for (const label of opts.clicks || []) {
      const el = page.getByText(label, { exact: false }).first();
      if (await el.count()) { await el.click({ timeout: 3000 }).catch(() => (rec.note += ` noclick:${label}`)); await page.waitForTimeout(1200); }
      else rec.note += ` missing:${label}`;
    }
    if (opts.openFirstEmployee) {
      const link = page.locator('a[href^="/employees/"]').first();
      if (await link.count()) { await link.click().catch(() => {}); await page.waitForLoadState('networkidle').catch(() => {}); await page.addStyleTag({ content: HIDE_FACES }); await page.waitForTimeout(1800); }
      else rec.note += ' no-employee-link';
    }
    if (opts.scrollY) { await page.evaluate((y) => window.scrollTo(0, y), opts.scrollY); await page.waitForTimeout(600); }
    rec.url = page.url();
    rec.textLength = (await page.locator('main').innerText().catch(() => '')).length;
    await page.screenshot({ path: `${OUT}/${name}.png` });
  } catch (e) { rec.status = 'error'; rec.note += ' ' + String(e).slice(0, 120); }
  console.log(rec.status.padEnd(5), name, rec.note);
  log.push(rec);
}
writeFileSync(`${OUT}/_capture-log.json`, JSON.stringify(log, null, 1));
console.log('Done. Files are in', OUT);
await browser.close();
