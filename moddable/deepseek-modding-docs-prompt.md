# DeepSeek Prompt: Rewrite Modding Documentation for New Modders

## Target Audience

New game modders who will be editing exposed XML/YAML game files. They know basic HTML/XML syntax but nothing about this game's content pipeline.

## Files to Rewrite

All 7 HTML files in `/mnt/fire/StarDrive/docs/kit/moddable/` share the same structure, CSS, navigation, and documentation patterns:

| File | Topic | Families | Files | Tags |
|------|-------|----------|-------|------|
| [`colonies.html`](colonies.html) | Colonies, economy and ground war | 6 | 141 | 132 |
| [`game-options.html`](game-options.html) | General game options | 4 | 4 | 99 |
| [`ships.html`](ships.html) | Ships, modules and designs | 6 | 1,778 | 264 |
| [`tech.html`](tech.html) | Tech tree and research | 3 | 192 | 88 |
| [`map-creation.html`](map-creation.html) | Map creation and solar systems | 6 | 43 | 85 |
| [`races-diplomacy.html`](races-diplomacy.html) | Races, diplomacy and events | 6 | 152 | 258 |
| [`ui-assets.html`](ui-assets.html) | UI modding and assets | 14 | 3,425 | 139 |

## Common Problems Across All Files

1. **Undocumented tags**: Many tags are marked as "index entries" with notes like "the guide has not yet documented its unit, accepted range or failure symptom. Do not infer a bound from the vanilla values." These are useless to a modder trying to change values.

2. **No getting-started section**: No information about where files live, what file extension to use, how to name them, or where to place them.

3. **No worked examples**: No complete, minimal XML/YAML file a modder can copy and modify.

4. **Buried critical warnings**: Warnings like "capital, outpost, spaceport, terraformer, biosphere are hardcoded by name — renaming removes behaviour" are buried in the middle of tag lists instead of being prominent upfront.

5. **No override/unification explanation**: The "XML unifies by file name" concept is not explained in plain language.

6. **No troubleshooting**: No section on what happens if a tag is misspelled, missing, or out of range.

7. **No testing workflow**: No guidance on how to verify changes took effect.

8. **Undefined terminology**: Terms like "BID," "UID," "pacing," "fertility," "richness" used without definition.

## Required Improvements (Apply to Each File)

- Add a "Getting Started" section at the top: file locations, naming conventions, required fields vs optional fields, how to create a new entry.
- Add a complete, minimal XML/YAML example for each family that a modder can copy-paste and edit.
- Replace all "index entry / not yet documented" placeholder text with either documented defaults/ranges or an explicit "safe to leave at vanilla value" note.
- Promote hardcoded-by-name warnings to a prominent "⚠️ Critical" callout box near the top of each affected family.
- Explain the override/unification system in plain language.
- Add a "Common Mistakes & Troubleshooting" section.
- Add a "How to Test Your Changes" section.
- Define all game-specific terms on first use.
- Keep the existing HTML structure and CSS classes so the page still renders correctly.
- Preserve the existing tag reference tables but make each tag entry include: what it does, valid range/type, default if omitted, and what breaks if set wrong.

## Output Format

Return the complete rewritten HTML file for each of the 7 files, ready to save. Include comments marking sections that still need game-engine verification (e.g., tag ranges not yet confirmed).

## Example Prompt to Send to DeepSeek

```
You are a technical writer specializing in game modding documentation. Your task is to rewrite the modding reference HTML files in /mnt/fire/StarDrive/docs/kit/moddable/ so that a brand-new modder with no prior knowledge of the codebase can understand them.

Files to rewrite:
- colonies.html — Colonies, economy and ground war (6 families, 141 files, 132 tags)
- game-options.html — General game options (4 families, 4 files, 99 tags)
- ships.html — Ships, modules and designs (6 families, 1,778 files, 264 tags)
- tech.html — Tech tree and research (3 families, 192 files, 88 tags)
- map-creation.html — Map creation and solar systems (6 families, 43 files, 85 tags)
- races-diplomacy.html — Races, diplomacy and events (6 families, 152 files, 258 tags)
- ui-assets.html — UI modding and assets (14 families, 3,425 files, 139 tags)

Target audience: New game modders who will be editing exposed XML/YAML game files. They know basic HTML/XML syntax but nothing about this game's content pipeline.

Common problems across all files:
1. Many tags are marked as "index entries" with notes like "the guide has not yet documented its unit, accepted range or failure symptom. Do not infer a bound from the vanilla values."
2. No getting-started section: where do files live, what file extension to use, how to name them, where to place them.
3. No worked example showing a complete, minimal XML/YAML file a modder can copy and modify.
4. Critical warnings are buried in the middle of tag lists instead of being prominent upfront.
5. No explanation of the override/unification system ("XML unifies by file name").
6. No troubleshooting section: what happens if a tag is misspelled, missing, or out of range.
7. No testing workflow: how to verify changes took effect.
8. Terminology like "BID," "UID," "pacing," "fertility," "richness" used without definition.

Required improvements (apply to each file):
- Add a "Getting Started" section at the top: file locations, naming conventions, required fields vs optional fields, how to create a new entry.
- Add a complete, minimal XML/YAML example for each family that a modder can copy-paste and edit.
- Replace all "index entry / not yet documented" placeholder text with either documented defaults/ranges or an explicit "safe to leave at vanilla value" note.
- Promote hardcoded-by-name warnings to a prominent "⚠️ Critical" callout box near the top of each affected family.
- Explain the override/unification system in plain language.
- Add a "Common Mistakes & Troubleshooting" section.
- Add a "How to Test Your Changes" section.
- Define all game-specific terms on first use.
- Keep the existing HTML structure and CSS classes so the page still renders correctly.
- Preserve the existing tag reference tables but make each tag entry include: what it does, valid range/type, default if omitted, and what breaks if set wrong.

Output format: Return the complete rewritten HTML file for each of the 7 files, ready to save. Include comments marking sections that still need game-engine verification.