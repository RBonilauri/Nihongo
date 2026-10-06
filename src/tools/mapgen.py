import os, sys
import json, math, sys
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SRC, 'content'))
from shapely.geometry import shape, Polygon, MultiPolygon
from shapely import affinity
from shapely.ops import unary_union
GJ = os.path.join(SRC, 'build', 'japan.geojson')
if not os.path.exists(GJ):
    import urllib.request
    os.makedirs(os.path.dirname(GJ), exist_ok=True)
    urllib.request.urlretrieve('https://raw.githubusercontent.com/dataofjapan/land/master/japan.geojson', GJ)
src = json.load(open(GJ))
REG = {'hok': ('北海道', 'Hokkaidō'), 'toh': ('東北', 'Tōhoku'), 'kan': ('関東', 'Kantō'), 'chu': ('中部', 'Chūbu'), 'kin': ('近畿', 'Kinki (Kansai)'), 'chg': ('中国', 'Chūgoku'), 'shi': ('四国', 'Shikoku'), 'kyu': ('九州・沖縄', 'Kyūshū et Okinawa')}
# nom court : (région, chef-lieu kanji, kana, spécialité)
I = {
'北海道': ('hok', '札幌', 'さっぽろ', 'Grands espaces et neige, ramen de Sapporo, produits laitiers'),
'青森': ('toh', '青森', 'あおもり', 'Pommes, festival Nebuta'),
'岩手': ('toh', '盛岡', 'もりおか', 'Nouilles wanko-soba, temple Chūson-ji'),
'宮城': ('toh', '仙台', 'せんだい', 'Baie de Matsushima, langue de bœuf grillée'),
'秋田': ('toh', '秋田', 'あきた', 'Chien akita, riz, kiritanpo'),
'山形': ('toh', '山形', 'やまがた', 'Cerises, onsen de Ginzan'),
'福島': ('toh', '福島', 'ふくしま', 'Pêches, château de Tsuruga, saké'),
'茨城': ('kan', '水戸', 'みと', 'Natto, parc de Hitachi'),
'栃木': ('kan', '宇都宮', 'うつのみや', 'Sanctuaires de Nikkō, fraises, gyōza'),
'群馬': ('kan', '前橋', 'まえばし', 'Onsen de Kusatsu'),
'埼玉': ('kan', 'さいたま', 'さいたま', 'Banlieue de Tōkyō, Kawagoe (« petit Edo »)'),
'千葉': ('kan', '千葉', 'ちば', 'Aéroport de Narita, Tōkyō Disneyland'),
'東京': ('kan', '新宿', 'しんじゅく', 'Capitale : Shibuya, Asakusa, Akihabara'),
'神奈川': ('kan', '横浜', 'よこはま', 'Yokohama, Kamakura, Hakone'),
'新潟': ('chu', '新潟', 'にいがた', 'Riz Koshihikari, saké'),
'富山': ('chu', '富山', 'とやま', 'Alpes japonaises, route Tateyama Kurobe'),
'石川': ('chu', '金沢', 'かなざわ', 'Jardin Kenroku-en, feuille d’or de Kanazawa'),
'福井': ('chu', '福井', 'ふくい', 'Falaises de Tōjinbō, musée des dinosaures'),
'山梨': ('chu', '甲府', 'こうふ', 'Mont Fuji (côté nord), raisins et vin'),
'長野': ('chu', '長野', 'ながの', 'Alpes, singes des neiges, soba'),
'岐阜': ('chu', '岐阜', 'ぎふ', 'Shirakawa-gō, Takayama'),
'静岡': ('chu', '静岡', 'しずおか', 'Thé vert, mont Fuji, anguille'),
'愛知': ('chu', '名古屋', 'なごや', 'Nagoya, Toyota, cuisine au miso'),
'三重': ('kin', '津', 'つ', 'Grand sanctuaire d’Ise, ninjas d’Iga'),
'滋賀': ('kin', '大津', 'おおつ', 'Lac Biwa, le plus grand lac du Japon'),
'京都': ('kin', '京都', 'きょうと', 'Temples, geishas, ancienne capitale'),
'大阪': ('kin', '大阪', 'おおさか', 'Takoyaki, okonomiyaki, château d’Ōsaka'),
'兵庫': ('kin', '神戸', 'こうべ', 'Bœuf de Kōbe, château de Himeji'),
'奈良': ('kin', '奈良', 'なら', 'Cerfs de Nara, grand Bouddha'),
'和歌山': ('kin', '和歌山', 'わかやま', 'Mont Kōya, chemins du Kumano Kodō'),
'鳥取': ('chg', '鳥取', 'とっとり', 'Dunes de sable, crabe'),
'島根': ('chg', '松江', 'まつえ', 'Grand sanctuaire d’Izumo'),
'岡山': ('chg', '岡山', 'おかやま', 'Jardin Kōraku-en, légende de Momotarō'),
'広島': ('chg', '広島', 'ひろしま', 'Mémorial de la paix, Miyajima, okonomiyaki'),
'山口': ('chg', '山口', 'やまぐち', 'Fugu de Shimonoseki, grotte d’Akiyoshidō'),
'徳島': ('shi', '徳島', 'とくしま', 'Danse Awa Odori, tourbillons de Naruto'),
'香川': ('shi', '高松', 'たかまつ', 'Udon sanuki'),
'愛媛': ('shi', '松山', 'まつやま', 'Mandarines, onsen de Dōgo'),
'高知': ('shi', '高知', 'こうち', 'Bonite grillée (katsuo no tataki), Sakamoto Ryōma'),
'福岡': ('kyu', '福岡', 'ふくおか', 'Ramen tonkotsu, mentaiko'),
'佐賀': ('kyu', '佐賀', 'さが', 'Porcelaine d’Arita et d’Imari'),
'長崎': ('kyu', '長崎', 'ながさき', 'Histoire des échanges avec l’étranger, castella'),
'熊本': ('kyu', '熊本', 'くまもと', 'Château de Kumamoto, mont Aso, Kumamon'),
'大分': ('kyu', '大分', 'おおいた', 'Onsen de Beppu et de Yufuin'),
'宮崎': ('kyu', '宮崎', 'みやざき', 'Mangues, gorges de Takachiho'),
'鹿児島': ('kyu', '鹿児島', 'かごしま', 'Volcan Sakurajima, patates douces'),
'沖縄': ('kyu', '那覇', 'なは', 'Plages, culture ryūkyū, karaté'),
}
import content
from adjectifs_keigo import rj
from vocab_themes import PREF
PK = {a: b for a, b, c in PREF}
import pykakasi
_kk = pykakasi.kakasi()
def k2r(k):
    r = ''.join(x['hepburn'] for x in _kk.convert(k)).replace('ou', 'ō').replace('oo', 'ō').replace('uu', 'ū').replace('ei', 'ei')
    return r[:1].upper() + r[1:]
cos = math.cos(math.radians(37))
S = 38.0
def prep(geom, name):
    polys = list(geom.geoms) if isinstance(geom, MultiPolygon) else [geom]
    big = max(polys, key=lambda p: p.area)
    keep = [p for p in polys if p.area >= 0.012 or p is big]
    if name == '北海道': keep = [p for p in keep if p is big or p.centroid.x < 145.3]
    if name == '鹿児島': keep = [p for p in keep if p.centroid.y > 29.5]
    if name == '東京': keep = [p for p in keep if p.centroid.y > 35 and p.centroid.x < 140.2]
    return MultiPolygon(keep)
out = []
for f in src['features']:
    ja = f['properties']['nam_ja']; nm = ja if ja == '北海道' else ja[:-1]
    g = prep(shape(f['geometry']), nm)
    if nm == '沖縄':
        g = affinity.scale(g, 1.3, 1.3, origin=g.centroid); c0 = g.centroid; g = affinity.translate(g, 141.8 - c0.x, 30.2 - c0.y)
    g = g.simplify(0.012, preserve_topology=True)
    ps = []
    for p in (g.geoms if hasattr(g, 'geoms') else [g]):
        if p.is_empty: continue
        d = ''
        for ring in [p.exterior] + list(p.interiors):
            pts = [(round(x * cos * S, 1), round(-y * S, 1)) for x, y in ring.coords]
            d += 'M' + 'L'.join('%g,%g' % q for q in pts) + 'Z'
        ps.append(d)
    c = g.centroid
    reg, cap, capk, spe = I[nm]
    out.append({'n': nm, 'r': reg, 'd': ''.join(ps), 'c': [round(c.x * cos * S, 1), round(-c.y * S, 1)], 'cap': cap, 'capk': capk, 'capr': k2r(capk), 'sp': spe, 'k': PK.get(nm, ''), 'ro': k2r(PK.get(nm, ''))})
xs = [];
allp = [o['d'] for o in out]
import re
nums = re.findall(r'M|L|(-?[\d.]+),(-?[\d.]+)', ''.join(allp))
X = [float(a) for a, b in nums if a]; Y = [float(b) for a, b in nums if a]
vb = [round(min(X) - 8), round(min(Y) - 8), round(max(X) - min(X) + 16), round(max(Y) - min(Y) + 16)]
# cadre Okinawa
ok = [o for o in out if o['n'] == '沖縄'][0]
nn = re.findall(r'(-?[\d.]+),(-?[\d.]+)', ok['d']); ox = [float(a) for a, b in nn]; oy = [float(b) for a, b in nn]
frame = [round(min(ox) - 6), round(min(oy) - 6), round(max(ox) - min(ox) + 12), round(max(oy) - min(oy) + 12)]
json.dump({'vb': vb, 'frame': frame, 'reg': {k: list(v) for k, v in REG.items()}, 'p': out}, open(os.path.join(SRC, 'data', 'japanmap.json'), 'w'), ensure_ascii=False, separators=(',', ':'))
import os; print(vb, frame, os.path.getsize(os.path.join(SRC, 'data', 'japanmap.json')), len(out))
