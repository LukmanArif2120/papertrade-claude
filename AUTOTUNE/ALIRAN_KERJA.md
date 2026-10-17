# Aliran kerja AUTOTUNE

Sasaran siap: Ahad 18 Okt 2026, 23:59 MYT. Peraturan teknikal: `SPEC.md`. Pengguna membenarkan larian automatik tanpa kelulusan setiap fasa (17 Okt 2026), push ke `main`, workflow baharu `autotune_*.yml`, Release data, dan notifikasi pada titik penting sahaja.

## Peraturan kerja
- Tulis hanya dalam `AUTOTUNE/` dan `.github/workflows/autotune_*.yml`. Fail lain dibaca sahaja.
- Sebelum push: `git pull --rebase origin main`; `git add` laluan sendiri sahaja; ujian `python3 -m unittest discover -s AUTOTUNE/ujian` lulus.
- Data harga mentah tidak dicommit (aset Release `autotune-data`); cache tempatan `AUTOTUNE/.cache/` diabaikan git.
- Jimat token: skrip mencetak ringkasan ≤ 20 baris; jangan baca `SPEC_SEMUA_KAEDAH.md` penuh (grep sahaja); laporan dijana skrip.

## Fasa
| Fasa | Kerja | Di mana | Output |
|---|---|---|---|
| F1 | Senarai calon, muat turun, QC, universe | `AUTOTUNE/data/`, `autotune_data.yml` | Release `autotune-data`, `manifest.json`, `QC.md` |
| F2 | Salinan kaedah berparameter + kesetaraan + julat | `AUTOTUNE/kaedah/` | 134 modul, `param_julat.csv`, `KESETARAAN.md` |
| F3 | Enjin + penala | `AUTOTUNE/teras/`, `AUTOTUNE/tala/`, `autotune_tala.yml` | pekerja shard |
| F4 | Perintis 5 kaedah di Actions | Actions | ukur masa/memori |
| F5 | Tala penuh (20 job serentak) | Actions | `hasil/tala/Mxx.json` |
| F6 | Pengesahan + portfolio gabungan | `AUTOTUNE/sahkan/`, `autotune_sahkan.yml` | `parameter_sedia.csv`, `gabungan.json`, `LAPORAN.md` |
| F7 | Dashboard (terakhir) | artifact sedia ada | tab AUTOTUNE |
| F8 | Tala semula setiap suku | `autotune_suku.yml` | cadangan |

## Status
- 17 Okt 21:47 MYT: spec ditetapkan; F1–F3 dimulakan selari.
