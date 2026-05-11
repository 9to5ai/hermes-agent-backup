#!/usr/bin/env python3
import json

# Playlist videos from CDP extraction
playlist_ids = [
    "9Qh4bHqQlnQ", "rQKis2Cfpeo", "J-6pnl5DQg8", "7J5s4U9-1fQ", "HhZXOG7V1MU", "PaKDlUTng5c",
    "lOfUFrNG_W4", "YnoQ8RJbALw", "UV1WDNe4J5w", "ntvkDnk_5jA", "6iB_6_pqvxA", "1bCXCxrDsCs",
    "8gtszunwr9M", "EN7frwQIbKc", "bNdiBwXbLNw", "UZuD8BMjwYI", "tmmPoxSwnq8", "5KQMX6r9FA8",
    "2QDem6-FaFw", "869u8y6yXJ0", "N5KQclvI6aw", "Ds23uX_Ss68", "LDN-CwTSLhQ", "rFBaDKRCmK0",
    "PplmzlgE0kg", "xFJceTJrbWo", "ibVJ-eWMB1Q", "7zCsfe57tpU", "Bj0i-yvIUQs", "YSaww_tepJ4",
    "Io16VZoP4Lg", "67IIjrEM178", "MoR2rG78eP4", "hWWegmAkNwQ", "k0KcsFaXHWk", "9gbwHbIx9UI",
    "T_xyhjfFCdY", "LF3aUIM57uw", "Xwjr_jxGFG8", "WdGSXQPwwmo", "6xdW0bdVkVU", "wkv2ifxPpF8",
    "tNV9_I-zLO0", "MkeNzdbx6VQ", "gUGQb0tPjc0", "hPMN5IiFHLg", "9RRaWDNj3Zk", "NAqvKD9SUZc",
    "IuSilY9v68s", "qO7T5zgRvXM", "Xhl8gVk3yrc", "4zk-hJ50vmU", "jbHB-rzKBAs", "NjJOb1p8QWA",
    "AaPVooZjNbw", "Nac62xsvk0I", "aiiSDXgCVPI", "CvbQmO_--Uw", "NA0CHyjAihc", "YDqqRqqlnJU",
    "xc20ZJMN-JA", "fr78adfAnuA", "YPObBOwIrHk", "_ghw5bwBMjQ", "IVF0nmGsoAQ", "82HsvG1_Nqk",
    "01FfDlraiHc", "51tQHSufJmA", "fdpbHIY-ZMc", "g0MikM4Bsbc", "XwdLT7qF14E", "Qd2Dyr0m3BI",
    "G0LTv8hQ5Cs", "MT78nZvpPOo", "hFf4MLQj6L4", "hrREdNm7vB4", "DiTqa4jAuYI", "rBUfD_wvbhw",
    "hrIY-clbdg8", "M4lqyeA7Vow", "SAjAk1RpA1U", "11PBno-cJ1g", "NCKQL0op30E", "GutMgDwU9Ro",
    "78Vyy_dzWXA", "hrIY-clbdg8", "rTsV52orKOM", "72a1PjnZFIM", "nAFw5i39m9I", "ha4cNZrdo_Y",
    "8ad3L_TkDqk", "7pWFNyQDEbU", "GqygvjpruhM", "ofBXJUE8qEA", "00Y-p62sk0s", "_qZvORxGqI0",
    "tS_fJJxMjn4", "81_W0vzhJdw", "kyz1z2Y5Oe0", "cvq7Nd8qaAo"
]

with open('/Users/momo/.hermes/cron/output/playlist_watcher_log.json') as f:
    tracker = json.load(f)

processed = set(tracker.get('processed_videos', []))
new_videos = [v for v in playlist_ids if v not in processed]

print(f"Playlist count: {len(playlist_ids)}")
print(f"Processed count: {len(processed)}")
print(f"New videos: {len(new_videos)}")
if new_videos:
    print(f"First new: {new_videos[:5]}")
