# Kekuatan sektor & industri bagi SELURUH pasaran AS (bukan Shariah sahaja).
# Sumber: screener Moomoo semua saham AS harga >= USD5 (perubahan 5/21/63 hari, nilai pasaran) dan
# papertrade/peta_industri.csv (ticker -> industri Moomoo). Sektor = pemetaan industri Moomoo ke 11 sektor
# Morningstar (SEKTOR di bawah).
#
# Guna:
#   python3 sektor_pasaran.py --skrin <fail1.json> <fail2.json> ... --peta papertrade/peta_industri.csv \
#       --tarikh YYYY-MM-DD --out papertrade/sektor_pasaran.csv [--json sektor_pasaran.json]
# Skrin: quote_stock_screen dengan screen_queries
#   [{"simple_field_query":{"simple_field":1,"screen_value_list":[2]}},
#    {"simple_property_query":{"property":{"name":2201},"lower":{"value":5000,"includes":true}}}]
# dan retrieve_queries
#   [{"basic_property":{"name":1101}},{"cumulative_property":{"name":3102,"days":5}},
#    {"cumulative_property":{"name":3102,"days":21}},{"cumulative_property":{"name":3102,"days":63}},
#    {"simple_property":{"name":2301}}]
# limit 300, ulang next_key hingga has_more=false (~21 halaman).
import sys, os, csv, json, argparse
import numpy as np
import pandas as pd

SEKTOR = {
    'Basic Materials': ['Agricultural Inputs', 'Aluminum', 'Building Materials', 'Chemicals', 'Coking Coal', 'Copper',
                        'Gold', 'Lumber & Wood Production', 'Other Industrial Metals & Mining',
                        'Other Precious Metals & Mining', 'Paper & Paper Products', 'Silver', 'Specialty Chemicals',
                        'Steel'],
    'Communication Services': ['Advertising Agencies', 'Broadcasting', 'Electronic Gaming & Multimedia', 'Entertainment',
                               'Internet Content & Information', 'Publishing', 'Telecom Services'],
    'Consumer Cyclical': ['Apparel Manufacturing', 'Apparel Retail', 'Auto & Truck Dealerships', 'Auto Manufacturers',
                          'Auto Parts', 'Department Stores', 'Footwear & Accessories', 'Furnishings, Fixtures & Appliances',
                          'Gambling', 'Home Improvement Retail', 'Internet Retail', 'Leisure', 'Lodging', 'Luxury Goods',
                          'Packaging & Containers', 'Personal Services', 'Recreational Vehicles', 'Residential Construction',
                          'Resorts & Casinos', 'Restaurants', 'Specialty Retail', 'Textile Manufacturing', 'Travel Services'],
    'Consumer Defensive': ['Beverages - Brewers', 'Beverages - Non-Alcoholic', 'Beverages - Wineries & Distilleries',
                           'Confectioners', 'Discount Stores', 'Education & Training Services', 'Farm Products',
                           'Food Distribution', 'Grocery Stores', 'Household & Personal Products', 'Packaged Foods',
                           'Tobacco'],
    'Energy': ['Oil & Gas Drilling', 'Oil & Gas E&P', 'Oil & Gas Equipment & Services', 'Oil & Gas Integrated',
               'Oil & Gas Midstream', 'Oil & Gas Refining & Marketing', 'Thermal Coal', 'Uranium'],
    'Financial Services': ['Asset Management', 'Banks - Diversified', 'Banks - Regional', 'Capital Markets', 'Credit Services',
                           'Financial Conglomerates', 'Financial Data & Stock Exchanges', 'Insurance - Diversified',
                           'Insurance - Life', 'Insurance - Property & Casualty', 'Insurance - Reinsurance',
                           'Insurance - Specialty', 'Insurance Brokers', 'Mortgage Finance', 'Shell Companies'],
    'Healthcare': ['Biotechnology', 'Diagnostics & Research', 'Drug Manufacturers - General',
                   'Drug Manufacturers - Specialty & Generic', 'Health Information Services', 'Healthcare Plans',
                   'Medical Care Facilities', 'Medical Devices', 'Medical Distribution', 'Medical Instruments & Supplies',
                   'Pharmaceutical Retailers'],
    'Industrials': ['Aerospace & Defense', 'Airlines', 'Airports & Air Services', 'Building Products & Equipment',
                    'Business Equipment & Supplies', 'Conglomerates', 'Consulting Services', 'Electrical Equipment & Parts',
                    'Engineering & Construction', 'Farm & Heavy Construction Machinery', 'Industrial Distribution',
                    'Infrastructure Operations', 'Integrated Freight & Logistics', 'Marine Shipping', 'Metal Fabrication',
                    'Pollution & Treatment Controls', 'Railroads', 'Rental & Leasing Services',
                    'Security & Protection Services', 'Specialty Business Services', 'Specialty Industrial Machinery',
                    'Staffing & Employment Services', 'Tools & Accessories', 'Trucking', 'Waste Management'],
    'Real Estate': ['REIT - Diversified', 'REIT - Healthcare Facilities', 'REIT - Hotel & Motel', 'REIT - Industrial',
                    'REIT - Mortgage', 'REIT - Office', 'REIT - Residential', 'REIT - Retail', 'REIT - Specialty',
                    'Real Estate - Development', 'Real Estate - Diversified', 'Real Estate Services'],
    'Technology': ['Communication Equipment', 'Computer Hardware', 'Consumer Electronics', 'Electronic Components',
                   'Electronics & Computer Distribution', 'Information Technology Services', 'Scientific & Technical Instruments',
                   'Semiconductor Equipment & Materials', 'Semiconductors', 'Software - Application',
                   'Software - Infrastructure', 'Solar'],
    'Utilities': ['Utilities - Diversified', 'Utilities - Independent Power Producers', 'Utilities - Regulated Electric',
                  'Utilities - Regulated Gas', 'Utilities - Regulated Water', 'Utilities - Renewable'],
}
SEKTOR_INDUSTRI = {i: s for s, L in SEKTOR.items() for i in L}
MIN_SAHAM = 3          # industri dengan < 3 saham tidak diberi skor
LAJUR = ['tarikh', 'jenis', 'nama', 'sektor', 'n', 'prestasi_1w', 'prestasi_1m', 'prestasi_3m', 'breadth',
         'rel_1m', 'rel_3m', 'fasa', 'skor_panas', 'mcap_bilion', 'teratas', 'alam']


def baca_skrin(fail):
    """Fail keputusan quote_stock_screen -> DataFrame ticker, r1w, r1m, r3m (%), mcap (USD)."""
    rows = []
    for f in fail:
        d = json.load(open(f, encoding='utf-8'))
        if isinstance(d, list) and d and isinstance(d[0], dict) and 'text' in d[0]:
            d = json.loads(d[0]['text'])
        for it in d.get('data', {}).get('items', []):
            v = {}
            for r in it.get('results', []):
                for k, x in r.items():
                    if not isinstance(x, dict) or 'property' not in x:
                        continue
                    p = x['property']; res = x.get('res', {})
                    val = res.get('sval') if res.get('result_type') == 3 else res.get('ival')
                    v[(p.get('name'), p.get('days'))] = val
            t = (it.get('code') or '').replace('US.', '')
            if not t:
                continue
            f_ = lambda key, sk: None if v.get(key) in (None, '') else float(v[key]) / sk
            rows.append(dict(ticker=t, r1w=f_((3102, 5), 1000), r1m=f_((3102, 21), 1000), r3m=f_((3102, 63), 1000),
                             mcap=f_((2301, None), 1000)))
    df = pd.DataFrame(rows).drop_duplicates('ticker', keep='last')
    # buang saham tanpa dagangan (perubahan 0 pada ketiga-tiga tempoh) dan nilai melampau (> 500%)
    tiada = (df[['r1w', 'r1m', 'r3m']].fillna(0) == 0).all(axis=1)
    df = df[~tiada]
    for c in ['r1w', 'r1m', 'r3m']:
        df.loc[df[c].abs() > 500, c] = np.nan
    return df


def fasa(rel3, rel1):
    if rel3 is None or rel1 is None or np.isnan(rel3) or np.isnan(rel1):
        return ''
    return 'Leading' if rel3 >= 0 and rel1 >= 0 else 'Improving' if rel3 < 0 <= rel1 else \
        'Weakening' if rel3 >= 0 > rel1 else 'Lagging'


def kumpulan(df, kunci, jenis, pasaran):
    out = []
    for nama, g in df.groupby(kunci):
        if len(g) < MIN_SAHAM:
            continue
        m1w, m1m, m3m = g.r1w.median(), g.r1m.median(), g.r3m.median()
        top = g.sort_values('r1m', ascending=False).head(3)
        out.append(dict(jenis=jenis, nama=nama, sektor=g.sektor.iloc[0] if jenis == 'Industri' else nama, n=len(g),
                        prestasi_1w=m1w, prestasi_1m=m1m, prestasi_3m=m3m,
                        breadth=round(100 * (g.r1m > 0).mean(), 1),
                        rel_1m=m1m - pasaran['r1m'], rel_3m=m3m - pasaran['r3m'],
                        mcap_bilion=round(g.mcap.sum() / 1e9, 1),
                        teratas=' '.join(f'{r.ticker}({r.r1m:+.1f}%)' for r in top.itertuples() if pd.notna(r.r1m))))
    k = pd.DataFrame(out)
    if k.empty:
        return k
    # skor panas 0–100: pangkat persentil antara kumpulan jenis yang sama
    pk = lambda s: s.rank(pct=True).fillna(0.5)
    k['skor_panas'] = (100 * (0.30 * pk(k.prestasi_1m) + 0.25 * pk(k.prestasi_3m) + 0.15 * pk(k.prestasi_1w)
                              + 0.30 * pk(k.breadth))).round(1)
    k['fasa'] = [fasa(a, b) for a, b in zip(k.rel_3m, k.rel_1m)]
    for c in ['prestasi_1w', 'prestasi_1m', 'prestasi_3m', 'rel_1m', 'rel_3m']:
        k[c] = k[c].round(2)
    return k


def bina(skrin, peta_csv):
    df = baca_skrin(skrin)
    peta = pd.read_csv(peta_csv)[['ticker', 'industri']]
    df = df.merge(peta, on='ticker', how='inner')
    df['sektor'] = df.industri.map(SEKTOR_INDUSTRI).fillna('Lain-lain')
    pasaran = dict(r1m=df.r1m.median(), r3m=df.r3m.median(), r1w=df.r1w.median(), n=len(df),
                   breadth=round(100 * (df.r1m > 0).mean(), 1))
    s = kumpulan(df, 'sektor', 'Sektor', pasaran)
    i = kumpulan(df, 'industri', 'Industri', pasaran)
    return pd.concat([s, i], ignore_index=True), pasaran


def main(argv=None):
    ap = argparse.ArgumentParser(description='Kekuatan sektor/industri seluruh pasaran AS')
    ap.add_argument('--skrin', nargs='+', required=True)
    ap.add_argument('--peta', required=True)
    ap.add_argument('--tarikh', required=True)
    ap.add_argument('--out', required=True, help='CSV sejarah (ditambah; snapshot tarikh sama diganti)')
    ap.add_argument('--json', help='JSON snapshot untuk db dashboard sektor/pasaran')
    a = ap.parse_args(argv)
    k, pas = bina(a.skrin, a.peta)
    k.insert(0, 'tarikh', a.tarikh)
    k['alam'] = 'US penuh (harga >= USD5)'
    lama = pd.read_csv(a.out) if os.path.exists(a.out) else pd.DataFrame(columns=LAJUR)
    lama = lama[lama.tarikh != a.tarikh]
    pd.concat([lama, k[LAJUR]], ignore_index=True).to_csv(a.out, index=False)
    if a.json:
        json.dump({'tarikh': a.tarikh, 'pasaran': pas, 'rows': json.loads(k[LAJUR].to_json(orient='records'))},
                  open(a.json, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print(f"Pasaran: {pas['n']} saham, median 1M {pas['r1m']:.2f}%, breadth {pas['breadth']}%")
    for j in ['Sektor', 'Industri']:
        t = k[k.jenis == j].sort_values('skor_panas', ascending=False)
        print(j, len(t), '| teratas:', ', '.join(f'{r.nama} {r.skor_panas}' for r in t.head(5).itertuples()))


if __name__ == '__main__':
    main()
