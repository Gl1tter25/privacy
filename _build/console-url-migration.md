# Console 隐私政策 URL 迁移清单（Glitter Fan 30 件）

生成：2026-09-05 · 新站已全量上线（31/31 HTTP 200，证据见 `http-status.json` 与 `SUMMARY.md`）

- **旧 URL（当前 Console 商品详情在用）**：`https://gl1tter25.github.io/<slug>-privacy/`（30 件全部实测 200，旧仓冻结保留、不删不改）
- **新 URL（迁移目标）**：`https://gl1tter25.github.io/privacy/<slug>/`（31 件含根页全部实测 200）
- 迁移动作＝Console → 商品详情 → 隐私政策字段换新 URL。**一次一件，逐件核。**
- **铁律：迁移某件前先确认该 app 在 Console 无任何在审/待审更改**（有则等落地）；换 URL 会与既有更改并批送审，勿打断在跑审核。
- 本清单只列对照与状态，Console 侧尚未做任何改动。

## 暂缓（有在审/送审活动证据，等落地后再换）

| Slug | App | 旧 URL → 新 URL | 暂缓原因 |
|---|---|---|---|
| poop-loop | Poop Loop | `/poop-loop-privacy/` → `/privacy/poop-loop/` | 9/4 工厂台账：本轮审核在跑，勿打断 |
| vitalvault | VitalVault | `/vitalvault-privacy/` → `/privacy/vitalvault/` | 9/4 决策：022 testers 补配挂 pending 等审核落地 |
| subvault | SubVault | `/subvault-privacy/` → `/privacy/subvault/` | 2026-09-05 正在全链送审中（另一任务） |
| lendloop | LendLoop | `/lendloop-privacy/` → `/privacy/lendloop/` | 2026-09-05 排在 subvault 后全链送审（另一任务） |

## 待迁移（无已知在审活动；换前仍须逐件核 Console）

| Slug | App | 旧 URL → 新 URL |
|---|---|---|
| brewlog | BrewLog | `/brewlog-privacy/` → `/privacy/brewlog/` |
| cleanloop | CleanLoop | `/cleanloop-privacy/` → `/privacy/cleanloop/` |
| coinvault | CoinVault | `/coinvault-privacy/` → `/privacy/coinvault/` |
| expiryloop | ExpiryLoop | `/expiryloop-privacy/` → `/privacy/expiryloop/` |
| fuellog | FuelLog | `/fuellog-privacy/` → `/privacy/fuellog/` |
| gamevault | GameVault | `/gamevault-privacy/` → `/privacy/gamevault/` |
| giftloop | GiftLoop | `/giftloop-privacy/` → `/privacy/giftloop/` |
| groceryloop | GroceryLoop | `/groceryloop-privacy/` → `/privacy/groceryloop/` |
| homevault | HomeVault | `/homevault-privacy/` → `/privacy/homevault/` |
| keydateloop | KeyDateLoop | `/keydateloop-privacy/` → `/privacy/keydateloop/` |
| labvault | LabVault | `/labvault-privacy/` → `/privacy/labvault/` |
| meterloop | MeterLoop | `/meterloop-privacy/` → `/privacy/meterloop/` |
| mileageloop | MileageLoop | `/mileageloop-privacy/` → `/privacy/mileageloop/` |
| movieloop | MovieLoop | `/movieloop-privacy/` → `/privacy/movieloop/` |
| packtrail | PackTrail | `/packtrail-privacy/` → `/privacy/packtrail/` |
| petvault | PetVault | `/petvault-privacy/` → `/privacy/petvault/` |
| quantvault | QuantVault | `/quantvault-privacy/` → `/privacy/quantvault/` |
| seedvault | SeedVault | `/seedvault-privacy/` → `/privacy/seedvault/` |
| stitchloop | StitchLoop | `/stitchloop-privacy/` → `/privacy/stitchloop/` |
| teavault | TeaVault | `/teavault-privacy/` → `/privacy/teavault/` |
| wrenchvault | WrenchVault | `/wrenchvault-privacy/` → `/privacy/wrenchvault/` |
| leaflog | LeafLog | `/leaflog-privacy/` → `/privacy/leaflog/` |
| moodloop | MoodLoop | `/moodloop-privacy/` → `/privacy/moodloop/` |
| pacekeeper | PaceKeeper | `/pacekeeper-privacy/` → `/privacy/pacekeeper/` |
| readtrail | ReadTrail | `/readtrail-privacy/` → `/privacy/readtrail/` |
| siplog | SipLog | `/siplog-privacy/` → `/privacy/siplog/` |

## 旧仓冻结纪律

- 30 个 `<slug>-privacy` 分仓：**不删、不改、不 push**。在 Console URL 全部迁完之前它们是在用资产；迁完后仍保留作历史存档（Pages 继续挂着不影响新站）。
- 任何 app 的隐私内容变更**只改统一仓**（`_build/apps.json` → render → push），不要再碰旧仓。

## 备注

- quantvault / vitalvault 新页在标准双联系卡之外保留了旧页的联系邮箱 `glitterfan27@gmail.com`（旧页唯一列出的地址），迁移后 Console 侧无需改联系方式。
- 新站根页 `https://gl1tter25.github.io/privacy/` 为 30 件索引，可作开发者的统一隐私政策主页引用。
