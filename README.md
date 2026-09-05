# Glitter App Privacy Policies

Unified privacy-policy site for every Android application published by
**Glitter** (Hong Kong). Published with GitHub Pages at
<https://gl1tter25.github.io/privacy/>.

## Layout

- `index.html` — hub page listing all apps
- `<slug>/index.html` — the privacy policy of one app, e.g.
  `poop-loop/index.html` → <https://gl1tter25.github.io/privacy/poop-loop/>

Every policy page is a single self-contained HTML file (inline CSS, no
external resources) and follows the same 13-section structure:

1. Scope and who we are · 2. Information you provide · 3. Local processing
and storage · 4. Advertising and automatically handled information ·
5. Sharing and sale of information · 6. Android permissions and device
features · 7. Security · 8. Retention and deletion · 9. Age and children's
privacy · 10. International processing · 11. Your choices and privacy
rights · 12. Changes to this policy · 13. Contact us

## Apps (30)

| Slug | App | Package |
|---|---|---|
| `poop-loop` | Poop Loop | `com.gl1tt.poop` |
| `brewlog` | BrewLog | `com.glitterfan.brewlog` |
| `cleanloop` | CleanLoop | `com.glitterfan.cleanloop` |
| `coinvault` | CoinVault | `com.glitterfan.coinvault` |
| `expiryloop` | ExpiryLoop | `com.glitterfan.expiryloop` |
| `fuellog` | FuelLog | `com.glitterfan.fuellog` |
| `gamevault` | GameVault | `com.glitterfan.gamevault` |
| `giftloop` | GiftLoop | `com.glitterfan.giftloop` |
| `groceryloop` | GroceryLoop | `com.glitterfan.groceryloop` |
| `homevault` | HomeVault | `com.glitterfan.homevault` |
| `keydateloop` | KeyDateLoop | `com.glitterfan.keydateloop` |
| `labvault` | LabVault | `com.glitterfan.labvault` |
| `leaflog` | LeafLog | `com.glitterfan.leaflog` |
| `lendloop` | LendLoop | `com.glitterfan.lendloop` |
| `meterloop` | MeterLoop | `com.glitterfan.meterloop` |
| `mileageloop` | MileageLoop | `com.glitterfan.mileageloop` |
| `moodloop` | MoodLoop | `com.glitterfan.moodloop` |
| `movieloop` | MovieLoop | `com.glitterfan.movieloop` |
| `pacekeeper` | PaceKeeper | `com.glitterfan.pacekeeper` |
| `packtrail` | PackTrail | `com.glitterfan.packtrail` |
| `petvault` | PetVault | `com.glitterfan.petvault` |
| `quantvault` | QuantVault | `com.glitterfan.quantvault` |
| `readtrail` | ReadTrail | `com.glitterfan.readtrail` |
| `seedvault` | SeedVault | `com.glitterfan.seedvault` |
| `siplog` | SipLog | `com.glitterfan.siplog` |
| `stitchloop` | StitchLoop | `com.glitterfan.stitchloop` |
| `subvault` | SubVault | `com.glitterfan.subvault` |
| `teavault` | TeaVault | `com.glitterfan.teavault` |
| `vitalvault` | VitalVault | `com.glitterfan.vitalvault` |
| `wrenchvault` | WrenchVault | `com.glitterfan.wrenchvault` |

## Rebuilding the pages

`_build/` holds the renderer:

- `_build/apps.json` — per-app parameter table (app name, package, extracted
  section content, theme micro-variables)
- `_build/make_template.py` — regenerates `_build/template.html` from the
  reference Poop Loop layout
- `_build/render.py` — renders every `<slug>/index.html` from template +
  parameters (`python -X utf8 render.py [slug]`)
- `_build/make_index.py` — rebuilds the hub `index.html`
- `_build/console-url-migration.md` — old per-app repo URLs → new unified
  URLs, for the Google Play Console migration

To add a new app: add its entry to `_build/apps.json`, run `render.py` and
`make_index.py`, commit, push. See the `privacy-site-publish` skill for the
full SOP.

## Contact

- **Glitter** (Hong Kong) — williamfan12138@gmail.com
- **Ezra** — zjh020608@gmail.com
