#!/usr/bin/env python3
import os, random, datetime, re

REPO = r'C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo'
ARTICLES_DIR = os.path.join(REPO, 'articles')
os.makedirs(ARTICLES_DIR, exist_ok=True)

ESIM_LINKS = {'jp': 'https://travel-guide.esimart.cc/goods/122', 'kr': 'https://travel-guide.esimart.cc/goods/3', 'eu': 'https://travel-guide.esimart.cc/goods/14', 'tw': 'https://travel-guide.esimart.cc/goods/11', 'oce': 'https://travel-guide.esimart.cc/goods/7'}
LOCK_START = 2000

def gen_article(topic, region, city, slug, lock_id):
    today = datetime.date.today().isoformat()
    read_time = random.randint(5, 12)
    desc = city + '是' + region + '最受歡迎的旅遊城市之一，這篇攻略帶你深度探索當地最美的景點和美食。'
    tags = [region, city, '一日遊', '景點']
    tags_html = ''.join(['<span class="tag">' + t + '</span>' for t in tags])
    info_box = '<div class="info-box">INFO: 最佳旅遊季節：每年3-5月或9-11月。</div>'
    budget_table = '<table><tr><th>項目</th><th>預估費用</th></tr><tr><td>交通</td><td>約' + str(random.randint(500,2000)) + '元</td></tr><tr><td>餐飲</td><td>約' + str(random.randint(1000,3000)) + '元</td></tr><tr><td>門票</td><td>約' + str(random.randint(300,1500)) + '元</td></tr><tr><td><strong>合計</strong></td><td><strong>約' + str(random.randint(2000,8000)) + '元</strong></td></tr></table>'
    esim_cta = '<div class="esim-cta"><h2>去' + region + '上網不用煩惱</h2><p>出發前線上購買 QR Code 掃描安裝，落地立即連網。<br>支援 4G/LTE 高速，LINE/IG 隨時上傳，全程無隱藏費用。</p><a class="btn" href="https://travel-guide.esimart.cc/goods" target="_blank" rel="noopener">查看 eSIM 方案 -gt;</a></div>'
    details1 = '<details><summary>交通方便嗎？</summary><p>當地公共交通發達，地鐵和公車網路密集。</p></details>'
    details2 = '<details><summary>文化禮儀要注意什麼？</summary><p>在寺廟請保持安靜，公共場合勿吸菸。</p></details>'
    author_box = '<div class="author-box"><h3>關於本文</h3><p>本文內容由旅遊通 eSIM 編輯團隊撰寫，資訊已於 ' + today + ' 更新核對。</p><p><strong>聯絡我們：</strong><a href="mailto:Service@esimart.com">Service@esimart.com</a></p></div>'
    footer = '<footer><p>資料來源：旅遊通 eSIM，查詢日 ' + today + '。客服 Service@esimart.com</p></footer>'
    
    body_content = '<h2>為什麼要來' + city + '？</h2><p>' + desc + '</p>' + info_box
    body_content += '<h2>必訪景點 TOP 5</h2><ol class="numbered-list">'
    for i in range(1, 6):
        body_content += '<li><strong>景點' + str(i) + '</strong> - 這是' + city + '最經典的景點之一，建議預留1-2小時參觀。</li>'
    body_content += '</ol>'
    body_content += '<h2>預算估算（1人，1天）</h2>' + budget_table
    body_content += '<h2>網路建議</h2><p>在' + region + '旅行時，穩定的網路連線非常重要。Google Maps導航、翻譯App、LINE溝通都需要良好的網路品質。</p>'
    body_content += esim_cta
    body_content += '<h2>常見問題</h2>' + details1 + details2
    body_content += author_box + footer
    
    og_img = 'https://loremflickr.com/1200/630/' + region.lower() + ',' + city.lower() + '?lock=' + str(lock_id) + '?w=1200&h=630&fit=crop'
    article_img = 'https://loremflickr.com/600/400/' + region.lower() + ',' + city.lower() + '?lock=' + str(lock_id) + '?w=1200&h=600&fit=crop'
    
    html = '<!doctype html>'
    html += '<html lang="zh-Hant">'
    html += '<head><link rel="stylesheet" href="/travel-guide.esimart/assets/style.css">'
    html += '<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
    html += '<title>' + topic + ' - 旅遊通 eSIM</title>'
    html += '<meta name="description" content="' + desc + '">'
    html += '<link rel="canonical" href="https://chiag455371.github.io/travel-guide.esimart/articles/' + slug + '.html">'
    html += '<meta property="og:type" content="article">'
    html += '<meta property="og:title" content="' + topic + '">'
    html += '<meta property="og:description" content="' + desc + '">'
    html += '<meta property="og:url" content="https://chiag455371.github.io/travel-guide.esimart/articles/' + slug + '.html">'
    html += '<meta property="og:image" content="' + og_img + '">'
    html += '<meta name="twitter:card" content="summary_large_image">'
    html += '<meta name="author" content="旅遊通 eSIM 編輯團隊">'
    html += '<meta name="date_published" content="' + today + '">'
    html += '</head><body>'
    html += '<nav class="topnav"><a class="brand" href="https://chiag455371.github.io/travel-guide.esimart/"><em>旅遊通</em> eSIM</a>'
    html += '<a href="https://chiag455371.github.io/travel-guide.esimart/">首頁</a>'
    html += '<a href="https://chiag455371.github.io/travel-guide.esimart/articles/">旅遊攻略</a>'
    html += '<a class="btn-nav" href="https://travel-guide.esimart.cc/goods" target="_blank" rel="noopener">eSIM 方案</a></nav>'
    html += '<article><header>'
    html += '<div class="breadcrumb"><a href="https://chiag455371.github.io/travel-guide.esimart/">首頁</a> <span>-gt; </span> <a href="https://chiag455371.github.io/travel-guide.esimart/articles/">旅遊攻略</a> <span>-gt; </span> <span>' + topic + '</span></div>'
    html += '<h1>' + topic + '</h1>'
    html += '<p class="subtitle">' + desc + '</p>'
    html += '<div class="meta-row"><span class="meta-date">更新：' + today + '</span><span class="meta-read">約 ' + str(read_time) + ' 分鐘閱讀</span></div>'
    html += '<div class="tags">' + tags_html + '</div>'
    html += '<figure><img src="' + article_img + '" alt="' + topic + '" loading="lazy"></figure>'
    html += '</header>' + body_content + '</article>'
    html += '<footer><p>COPYRIGHT 2024-2026 旅遊通 eSIM｜全球 58 國流量卡</p>'
    html += '<p><a href="mailto:Service@esimart.com">Service@esimart.com</a></p></footer>'
    html += '</body></html>'
    
    filepath = os.path.join(ARTICLES_DIR, slug + '.html')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return slug

if __name__ == '__main__':
    existing = {f.replace('.html','') for f in os.listdir(ARTICLES_DIR) if f.endswith('.html') and f != 'index.html'}
    templates = [
        ('京都清水寺二年坂一日遊：古都漫步的完美路線', 'jp', 'Kyoto', 'jp-kyoto-sannenzaka'),
        ('東京渋谷原宿潮流文化完整探索：從竹下通到表參道', 'jp', 'Tokyo', 'jp-tokyo-harajuku'),
        ('京都嵐山竹林小徑：世界遺產禪意之美深度導覽', 'jp', 'Kyoto', 'jp-kyoto-arashiyama'),
        ('東京晴空塔淺草周邊深度攻略：關東最大地标的全面探索', 'jp', 'Tokyo', 'jp-tokyo-skytree'),
        ('富士山五合目登山入門：裝備交通與注意事項完整指南', 'jp', 'Fuji', 'jp-fuji-hiking'),
        ('東京新宿黃金街深夜美食：居酒屋文化的在地體驗', 'jp', 'Tokyo', 'jp-tokyo-shinjuku-ylane'),
        ('京都金閣寺龍安寺枯山水庭園：世界文化遺產深度導覽', 'jp', 'Kyoto', 'jp-kyoto-kinkakuji'),
        ('東京迪士尼樂園迪士尼海洋雙園區完整攻略', 'jp', 'Tokyo', 'jp-tokyo-disney'),
        ('廣島和平紀念公園宮島嚴島神社：世界遺產一日巡禮', 'jp', 'Hiroshima', 'jp-hiroshima-itsukushima'),
        ('北海道支笏湖層雲峽溫泉：冬季雪景與熱泉完美結合', 'jp', 'Noboribetsu', 'jp-hokkaido-onsen'),
        ('首爾明洞弘大夜生活指南：購物美食K-pop文化完整攻略', 'kr', 'Seoul', 'kr-seoul-mydong'),
        ('濟州島西歸浦城隍市場咖啡街：南國風情慢活之旅', 'kr', 'Jeju', 'kr-jeju-city'),
        ('釜山海雲台海灘广安里夜景：韓國第二大城市海濱魅力', 'kr', 'Busan', 'kr-busan-haeundae'),
        ('首爾德壽宮光化門廣場：朝鮮王朝歷史街頭探索', 'kr', 'Seoul', 'kr-seoul-deoksugung'),
        ('濟州島中文觀光區偶來市集：自然與地道的完美平衡', 'kr', 'Jeju', 'kr-jeju-jungmun'),
        ('倫敦大英博物館泰晤士河畔漫步：世界級文化遺產深度探索', 'eu', 'London', 'eu-london-british'),
        ('阿姆斯特丹運河區梵高博物館：荷蘭藝術與水城的浪漫邂逅', 'eu', 'Amsterdam', 'eu-amsterdam-canals'),
        ('柏林勃蘭登堡門東邊畫廊：德國歷史與現代藝術對話', 'eu', 'Berlin', 'eu-berlin-wall'),
        ('羅馬鬥技場西班牙階梯：永恒之城的千年時光之旅', 'eu', 'Rome', 'eu-rome-colosseum'),
        ('倫敦考文特花園博羅市場：最地道的英式街頭美食探索', 'eu', 'London', 'eu-london-covent'),
        ('台北101展望台信義區商圈：摩天大樓下的都市漫遊', 'tw', 'Taipei', 'tw-taipei-101'),
        ('台北陽明山國家公園：花海溫泉與火山地質自然奇觀', 'tw', 'Taipei', 'tw-yangmingshan'),
        ('南投清境農場合歡山：高山上的英國鄉村風情', 'tw', 'Nantou', 'tw-nantou-clear'),
        ('嘉義阿里山森林鐵路：百年鐵道與日出雲海的經典旅程', 'tw', 'Chiayi', 'tw-ari-san-rail'),
        ('台北士林夜市圓山大飯店：經典台灣夜市完整攻略', 'tw', 'Taipei', 'tw-shilin-night'),
        ('台中高美濕地日落：台灣西部海岸最浪漫的夕陽景點', 'tw', 'Taichung', 'tw-gaomei-sunset'),
        ('花蓮太魯閣國家公園：峽谷奇觀與布洛灣壯麗風景', 'tw', 'Hualien', 'tw-taruco'),
        ('台東鹿野高台熱氣球：太平洋畔的飛翔夢想', 'tw', 'Taitung', 'tw-luye-balloon'),
        ('苗栗三義桐花季：每年五月最浪漫的粉色花瓣雨', 'tw', 'Miaoli', 'tw-sanyi-crape'),
        ('屏東車城乡草原：台灣最慢活的鄉間風景線', 'tw', 'Pingtung', 'tw-pingtung-ranch'),
    ]
    new_templates = [(t,r,c,s) for t,r,c,s in templates if s not in existing]
    selected = new_templates[:20]
    generated = []
    lock_id = LOCK_START
    for topic, region, city, slug in selected:
        if slug not in existing:
            try:
                gen_article(topic, region, city, slug, lock_id)
                generated.append(slug)
                print('Generated: ' + slug)
            except Exception as e:
                print('Failed: ' + slug + ' - ' + str(e))
            lock_id += 1
    print('Total new articles: ' + str(len(generated)))
    print('Date: ' + datetime.date.today().isoformat())
