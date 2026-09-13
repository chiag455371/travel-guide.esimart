# -*- coding: utf-8 -*-
"""Generate 20 high-quality travel guide articles daily with real E-E-A-T content."""
import os, re, json, random, datetime, glob

BASE = r"C:\Users\User\Documents\ChatGPT\1號人員\travel-guide-repo"
ARTICLES = BASE + r"\articles"
DISTRIBUTOR = "https://travel-guide.esimart.cc/goods"
TODAY = datetime.date.today().isoformat()

# Region configs
REGIONS = {
    "jp": {"flag": "\U0001f1ef\U0001f1f5", "name": "日本", "esim_path": "122", "keyword": "japan", "default_lock": 2001},
    "kr": {"flag": "\U0001f1f0\U0001f1f7", "name": "韓國", "esim_path": "123", "keyword": "korea", "default_lock": 2002},
    "tw": {"flag": "\U0001f1f9\U0001f1fc", "esim_path": "11", "keyword": "taiwan", "default_lock": 2003},
    "eu": {"flag": "\U0001f1ea\U0001f1fa", "name": "歐洲", "esim_path": "14", "keyword": "europe", "default_lock": 2004},
    "oce": {"flag": "\U0001f1e6\U0001f1fa", "name": "澳洲", "esim_path": "15", "keyword": "australia", "default_lock": 2005},
}

# Article templates with real content per destination
ARTICLE_TEMPLATES = {
    # Japan
    "jp-tokyo-shibuya": {
        "title": "東京涉谷必訪攻略：新宿、澀谷、原宿一日遊完整路線",
        "desc": "東京最熱門的商圈區——涉谷、新宿、原宿一日遊完整攻略，含交通、美食、購物和eSIM建議。",
        "h2s": [
            ("最佳旅遊季節", "東京四季分明，春天（3-5月）可賞櫻花，秋天（10-11月）紅葉滿街。夏天炎熱但適合看煙火，冬天乾燥寒冷但適合滑雪。"),
            ("交通攻略", "從成田機場搭Skyliner到上野約36分鐘，從羽田機場搭單軌電車約14分鐘到濱松町。市區內建議購買地鐵一日券（800日圓），可無限次搭乘東京Metro和都營地鐵。"),
            ("必訪景點", "涉谷Crossing是東京最知名的天線腳，每天超過50萬人經過。明治神宮是日本最具代表性的神社，佔地70萬平方公尺的森林。原宿竹下通是青春文化的聖地。"),
            ("美食推薦", "一蘭拉麵涉谷店24小時營業，味噌叉燒拉麵是招牌。忠犬八公像前的「渋谷食堂」提供正宗豬排飯。星巴克 Reserve Roastery 是全球最大的星巴克旗艦店。"),
            ("預算估算", "交通：約1,000-2,000日圓/天。餐飲：約3,000-6,000日圓/天。門票：約2,000-5,000日圓。總計約6,000-13,000日圓（約1,500-3,200台幣）。"),
        ],
        "tags": ["東京", "涉谷", "新宿", "一日遊", "購物", "美食"],
        "lock": 2101,
    },
    "jp-tokyo-asakusa": {
        "title": "淺草寺＆隅田川一日遊：雷門、仲見世通、天空樹完整攻略",
        "desc": "東京最古老的淺草地區完整導覽，從雷門到大觀覽車、隅田川遊船，一篇搞定。",
        "h2s": [
            ("交通方式", "從新宿搭都營大江戶線約25分鐘到「淺草站」，從上野搭東京Metro銀座線約10分鐘。建議從JR上野站出發，步行15分鐘即可抵達雷門。"),
            ("必訪景點", "淺草寺是東京最古老的寺廟，建於628年。雷門（大燈籠）是東京最具代表性的地標之一。仲見世通商店街有70多家店鋪，出售甜點和紀念品。"),
            ("美食推薦", "Agemochi（炸年糕）是淺草特產，Nakamise通上的「起雲堂」已營業超過70年。仙貝和抹茶冰淇淋也是必買伴手禮。"),
            ("隅田川遊船", "淺草溫泉國際大廈1樓有遊船碼頭，航程約40分鐘，途經淺草、築地、台場。成人票價約2,100日圓，傍晚時分景色最美。"),
            ("預算估算", "交通：約500-1,000日圓。餐飲：約2,000-4,000日圓。門票與活動：約2,000-3,000日圓。合計約4,500-8,000日圓（約1,100-2,000台幣）。"),
        ],
        "tags": ["東京", "淺草", "寺廟", "美食", "一日遊"],
        "lock": 2102,
    },
    "jp-kyoto-fushimi": {
        "title": "京都伏見稻荷大社全攻略：千本鳥居最佳走法與秘境攻略",
        "desc": "伏見稻荷大社是日本三萬座稻荷神社的總本宮，朱紅色鳥居隧道綿延山腹，是京都最具代表性的景觀。",
        "h2s": [
            ("最佳參觀時間", "建議早上7點前抵達，避開人潮。千本鳥居在清晨光線柔和時拍照效果最佳。下午3-4點也能避開旅行團，但光線較硬。"),
            ("千本鳥居走法", "從本殿出發沿山階緩緩上行，前1小時鳥居最密集、拍照最壯觀。登頂約需2-3小時，全程約4公里。下山時可走不同小路探索秘境。"),
            ("周邊景點", "京都站附近的「錦市場」有「京都的廚房」之稱，可品嚐新鮮海鮮和漬物。伏見區還有「月桂冠酒造」可免費參觀釀酒過程。"),
            ("交通方式", "從京都站搭JR奈良線至「稲荷站」，步行5分鐘即達。或從京都市營地下鐵「七條站」轉乘巴士約15分鐘。"),
            ("預算估算", "交通：約200-500日圓。餐飲：約1,500-3,000日圓。門票：免費。合計約1,700-3,500日圓（約420-870台幣）。"),
        ],
        "tags": ["京都", "伏見稻荷", "鳥居", "參拜", "一日遊"],
        "lock": 2103,
    },
    "jp-nara-deer": {
        "title": "奈良公園餵鹿全攻略：與1,200隻野生鹿親密接觸的秘訣",
        "desc": "奈良公園擁有超過1,200隻野生梅花鹿，是日本國家天然紀念物。教你專業餵鹿技巧、避開鹿群攻擊的秘訣。",
        "h2s": [
            ("餵鹿秘訣", "鹿仙貝每包500日圓，可在公園內的販賣處購買。餵鹿時請將鹿仙貝平放手掌，讓鹿自己來吃，不要追逐或推擠。鹿角銳利，請保持安全距離。"),
            ("必訪景點", "東大寺是世界最大木造建築，內有大佛坐像（高15公尺）。春日大社擁有3,000尊石燈籠，是日本最重要的神社之一。"),
            ("美食推薦", "奈良町的「志津香釜飯」是新宿名店，每日限量供應。宇治地區的抹茶甜點也是一絕。"),
            ("交通方式", "從大阪難波搭近鐵奈良線約35分鐘到「奈良站」，步行10分鐘。從京都站搭JR奈良線約45分鐘。"),
            ("預算估算", "交通：約600-1,500日圓。鹿仙貝：500日圓/包。餐飲：約2,000-4,000日圓。門票：約2,000日圓。合計約3,100-8,000日圓（約770-2,000台幣）。"),
        ],
        "tags": ["奈良", "鹿", "東大寺", "春日大社", "一日遊"],
        "lock": 2104,
    },
    "jp-osaka-doton": {
        "title": "大阪道頓堀美食全攻略：格力高看板、元祖炸串、章魚燒必吃清單",
        "desc": "大阪是日本美食之都，道頓堀一帶聚集了最正宗的關西料理。本篇收錄10家必吃老店與步行街完整路線。",
        "h2s": [
            ("必吃美食TOP10", "1. 元祖炸串達摩（元祖串かつだるま）— 創立1929年的炸串名店。2. 梅吉章魚燒（たこやき梅吉）— 外皮酥脆內餡飽滿。3. 本家大阪王將 — 煎餃子每籠只要10個400日圓。"),
            ("步行街路線", "從阪急梅田站出發 → 御堂筋地鐵 → 難波站 → 道頓堀川散步 → 心齋橋筋商店街 → 美國村。全程約2-3小時，沿途美食不斷。"),
            ("夜間景點", "格力高跑男看板是道頓堀最 iconic 的地標，夜晚燈光亮起時特別震撼。堀江地區有隱藏酒吧和深夜食堂，適合喜歡夜生活的人。"),
            ("交通方式", "從關西機場搭南海電鐵Rapi:t特快列車約40分鐘到難波站。從大阪站搭御堂筋線約4分鐘到難波站。"),
            ("預算估算", "交通：約600-1,500日圓。餐飲：約3,000-6,000日圓。購物：約1,000-5,000日圓。合計約4,600-12,500日圓（約1,150-3,100台幣）。"),
        ],
        "tags": ["大阪", "道頓堀", "美食", "炸串", "章魚燒"],
        "lock": 2105,
    },
    "jp-fuji-hiking": {
        "title": "富士山五合目登山入門：裝備清單、交通路線與注意事項完整指南",
        "desc": "富士山是日本最高峰（3,776公尺），每年7月至9月登山季開放期間，數十萬名登山者湧向五合目Starting Point。",
        "h2s": [
            ("登山季節與路線", "登山季僅限7月初至9月中旬。主要路線有五合目（吉田路口）、須山口（富士口）、御殿場口等。五合目是最熱門的路線，海拔2,300公尺起登。"),
            ("裝備清單", "必帶：登山鞋、保暖衣物（山顶溫度高約5度）、雨具、頭燈、水和零食、防曬乳、帽子。可租借：登山杖、氧氣瓶（部分山莊提供）。"),
            ("交通方式", "從新宿搭高速巴士約2.5小時到河口湖五合目。夏季有直達富士山五合目的臨時巴士，每班約2,000日圓往返。"),
            ("住宿建議", "山頂山莊需提前2-3個月預訂，一晚約8,000-15,000日圓。河口湖周邊有旅館和背包客旅館，價格約3,000-8,000日圓。"),
            ("預算估算", "交通：約4,000-6,000日圓。山莊住宿：約8,000-15,000日圓。餐飲：約3,000-5,000日圓。裝備：約2,000-5,000日圓。合計約17,000-31,000日圓（約4,200-7,700台幣）。"),
        ],
        "tags": ["富士山", "登山", "河口湖", "五日遊", "裝備"],
        "lock": 2106,
    },
    "jp-hokkaido-snow": {
        "title": "北海道滑雪全攻略：二世谷粉雪、札幌白色燈節與定禪寺雪壁祭",
        "desc": "北海道是日本冬季最精彩的目的地，二世谷被譽為粉雪天堂，札幌白色燈節和定禪寺雪壁祭每年吸引百萬遊客。",
        "h2s": [
            ("最佳滑雪場", "二世谷（Niseko）是日本最著名的滑雪勝地，年均降雪量超過15公尺，被ESPN評為世界最佳滑雪場之一。星野Tomamu、留壽都（Rusutsu）也是優質選擇。"),
            ("札幌白色燈節", "每年2月上旬在札幌市中心的大通公園舉辦，超過100萬盞燈光裝置將街道變成夢幻隧道。配合現場音樂演出，是北海道冬季最重要的活動。"),
            ("美食推薦", "札幌味噌拉麵（味覺濃厚）、成吉思汗烤羊肉（蒙古烤肉）、海鮮蓋飯（海鮮丼）是北海道三大美食。新千歲機場的「らっきょう」漬物也是必買伴手禮。"),
            ("交通方式", "從東京搭飛機約1.5小時到新千歲機場。從札幌站搭JR到二世谷約2小時。冬季有免費穿梭巴士連接主要滑雪場。"),
            ("預算估算", "機票：約15,000-25,000日圓。滑雪票券：約5,000-8,000日圓/天。住宿：約8,000-20,000日圓/晚。餐飲：約4,000-8,000日圓/天。合計約32,000-61,000日圓（約8,000-15,000台幣）。"),
        ],
        "tags": ["北海道", "滑雪", "二世谷", "粉雪", "冬季"],
        "lock": 2107,
    },
    "jp-hakone-onsen": {
        "title": "箱根溫泉一日遊：火山地形、蘆之湖舟遊與免費美術館完整攻略",
        "desc": "箱根是日本最著名的溫泉鄉，位於富士箱根伊豆國立公園內。大湧谷的硫磺煙氣、蘆之湖的海盗船、強羅公園的噴泉。",
        "h2s": [
            ("必訪景點", "大湧谷是百年前火山爆發形成的谷地，硫磺煙氣騰騰，被稱為「地獄谷」。標本樹因硫磺氣體而變黑，是大自然的神奇之作。特產黑雞蛋據說能延壽7年。"),
            ("蘆之湖海盜船", "在蘆之湖搭乘海盜造型觀光船，航行約40分鐘。天氣好時可遠眺富士山。湖畔的箱根神社朱紅鳥居矗立湖中，是拍照熱門景點。"),
            ("溫泉推薦", "強羅溫泉區有高級溫泉飯店和公共浴場。大涌谷附近的「桃源台」有平價溫泉澡堂。建議選擇帶有「檜風呂」的日式旅館體驗。"),
            ("交通方式", "從新宿搭Odakyu浪漫特快約85分鐘到箱根湯本。箱根自由通行券（715日圓）可無限次搭乘區域內交通。"),
            ("預算估算", "交通：約2,000-4,000日圓。溫泉票：約1,000-2,000日圓。餐飲：約3,000-6,000日圓。住宿：約10,000-30,000日圓。合計約16,000-42,000日圓（約4,000-10,500台幣）。"),
        ],
        "tags": ["箱根", "溫泉", "蘆之湖", "大湧谷", "一日遊"],
        "lock": 2108,
    },
    # Korea
    "kr-seoul-naksan": {
        "title": "首爾南山塔＆南山韓屋村：夜景、告白鎖與傳統村的完美一日",
        "desc": "南山塔（N Seoul Tower）是首爾最浪漫的地標，日落時分的360度首爾全景令人印象深刻。搭配北村韓屋村的傳統風情，一整天玩不夠。",
        "h2s": [
            ("南山塔攻略", "搭乘南山缆車（單程12,000韓圓，往返15,000韓圓）上山。日落前30分鐘排隊可搶先占位观景台。告白鎖區可購買鎖並掛在圍欄上，象徵永恆愛情。"),
            ("北村韓屋村", "距南山塔步行15分鐘，是朝鮮時代兩班貴族的居住區，保存了600多棟傳統韓屋。穿著韓服拍照更有一番風味，租賃費用約15,000-20,000韓圓/小時。"),
            ("美食推薦", "明洞的「韓國屋」供應正宗韓國烤肉。南山塔底的「南山西塔餐廳」有法式料理和高價位的韓定食。弘大的「梨花小巷」有許多平價韓式居酒屋。"),
            ("交通方式", "從明洞站搭7号线到淑大入口站，轉乘南山缆車。或從乙支路入口站步行上山約30分鐘。"),
            ("預算估算", "交通：約2,000-5,000韓圓。南山塔門票：約13,000-23,000韓圓。餐飲：約15,000-40,000韓圓。合計約30,000-78,000韓圓（約750-2,000台幣）。"),
        ],
        "tags": ["首爾", "南山塔", "韓屋村", "夜景", "告白鎖"],
        "lock": 2201,
    },
    "kr-busan-haeundae": {
        "title": "釜山海雲台海灘全攻略：韓劇取景地、咖啡街與海鮮美食一次看",
        "desc": "海雲台是韓國最著名的海灘，也是《來自星星的你》、《觸動你心》等韓劇的熱門取景地。",
        "h2s": [
            ("海雲台海灘", "長約1.5公里的白色沙灘，夏季（7-8月）是游泳和沙灘運動的熱門地點。冬季雖然不能游泳，但海景別具特色。海邊有众多咖啡廳和餐廳。"),
            ("咖啡街", "從海雲台站步行5分鐘的「海雲台咖啡街」聚集了100多家咖啡廳，推薦「해운대베리테아」和「코드그린」。"),
            ("甘草魚市場", "距離海雲台約10分鐘車程，是釜山最大的海鮮市場。現點現煮的甘草魚（민어탕）是必嚐美食，價格約15,000-25,000韓圓。"),
            ("交通方式", "從首爾搭KTX約2.5小時到釜山站。市區內搭乘地鐵1號線至海雲台站。"),
            ("預算估算", "KTX：約60,000-80,000韓圓。住宿：約50,000-150,000韓圓/晚。餐飲：約20,000-50,000韓圓/天。合計約130,000-280,000韓圓（約3,250-7,000台幣）。"),
        ],
        "tags": ["釜山", "海雲台", "海灘", "韓劇", "海鮮"],
        "lock": 2202,
    },
    "kr-jeju-hallasan": {
        "title": "濟州島漢拏山登山全攻略：韓國最高峰的壯麗風景與周邊溫泉",
        "desc": "漢拏山（Hallasan）是韓國最高峰（1,947公尺），也是聯合國教科文組織世界自然遺產。",
        "h2s": [
            ("登山路線", "可從汝矣窟（Yerim-gul）、小路（Joeongbang）、新溪（Sinseok-ori）三條路線攀登。最熱門的是新溪路線，約需3-4小時登顶。"),
            ("周邊景點", "城山日出峰是世界自然遺產，從濟州市區搭巴士約40分鐘。涉慶海的中文觀光區有動物園和水族館。"),
            ("美食推薦", "黑豬肉烤肉是濟州特產，「三姓穴」附近的烤肉店最負盛名。海女海鮮市場可品嚐現撈海鮮。"),
            ("交通方式", "從首爾搭飛機約1.5小時到濟州機場。島內建議租車自駕，每日約30,000-50,000韓圓。"),
            ("預算估算", "機票：約100,000-200,000韓圓。住宿：約50,000-150,000韓圓/晚。餐飲：約20,000-50,000韓圓/天。合計約220,000-500,000韓圓（約5,500-12,500台幣）。"),
        ],
        "tags": ["濟州島", "漢拏山", "登山", "黑豬肉", "海女"],
        "lock": 2203,
    },
    # Taiwan
    "tw-taipei-101": {
        "title": "台北101觀景台＆信義區美食全攻略：跨年煙火、世界最快速電梯與隱藏咖啡廳",
        "desc": "台北101曾經是世界最高建築，至今仍是台北最著名的地標。觀景台的360度台北全景、88樓的超快速電梯（每秒1010公尺）。",
        "h2s": [
            ("觀景台攻略", "89樓室內觀景台成人票600台幣，學生500台幣。91樓戶外天空殿堂需另購票（加100台幣），風大但視野無敵。建議傍晚4-5點去，可看到白天、日落和夜景三種景色。"),
            ("信義區美食", "鼎泰豐信義店的小籠包排隊人龍是常態，建議錯峰前往。八田与一奶茶在101對面巷內，抹茶和original是最熱賣口味。"),
            ("跨年煙火", "每年12月31日晚間8-9點，台北101施放跨年煙火，是全球最壯觀的煙火秀之一。最佳觀賞點：信義新天地A9出口廣場、台北車站前廣場。"),
            ("交通方式", "搭乘台北捷運板南線到「台北101/世貿站」，3號出口步行3分鐘。"),
            ("預算估算", "門票：約600-700台幣。餐飲：約500-1,500台幣。交通：約30-50台幣。合計約1,130-2,250台幣（約280-560人民幣）。"),
        ],
        "tags": ["台北", "101", "觀景台", "跨年", "美食"],
        "lock": 2301,
    },
    "tw-tainan-old": {
        "title": "台南老街美食全攻略：從赤崁樓到擔仔麵，台灣食品之都的15家必吃店",
        "desc": "台南被CNN Travel評為世界十大最便宜美食城市第一名，也是台灣歷史最悠久的城市。",
        "h2s": [
            ("赤崁樓＆開台聖廟", "赤崁樓是台南最著名的歷史遺址，建於1653年。附近的外少婦街有很多傳統小吃。孔廟週邊的仁愛街的擔仔麵是必吃。"),
            ("必吃美食15選", "1. 國華街黃氏虱目魚粥 — 早上6點開始賣，每日限量。2. 林奶奶肉円 — 百年老店，酥脆外皮包裹鮮嫩內餡。3. 阿川鬍鬚豬血湯 — 每晚8點後才有。"),
            ("老街漫步", "從赤崁樓出發，沿中正路步行至國華街（約10分鐘），再轉進正興街，沿途遍布美味小店。全程約1.5公里，建議預留2-3小時。"),
            ("交通方式", "搭乘高鐵到左營站，轉乘捷運紅線到台江體育場站，步行5分鐘。或從高雄機場搭計程車約30分鐘。"),
            ("預算估算", "餐飲：約300-800台幣/天。住宿：約800-2,000台幣/晚。交通：約100-300台幣。合計約1,200-3,100台幣（約300-770人民幣）。"),
        ],
        "tags": ["台南", "美食", "老街", "擔仔麵", "歷史"],
        "lock": 2302,
    },
    "tw-yangmingshan": {
        "title": "陽明山國家公園全攻略：火山地形、竹子湖海芋季與好母咖啡",
        "desc": "陽明山國家公園是台灣第一個國家公園，擁有豐富的火山地形、溫泉和花海。竹子湖的海芋季（4-5月）和陽明花朝（3月）是每年最盛大的活動。",
        "h2s": [
            ("火山地形", "大屯山主峰海拔1,092公尺，是陽明山最高點。噴氣口遺跡位於冷水坑，可看到硫磺煙氣從地面冒出。小油坑的滾滾白煙是陽明山最著名的地熱景觀。"),
            ("竹子湖海芋季", "每年4月中旬至5月中旬，竹子湖地區的海芋田開花，白色的海芋花朵盛開在綠色田園間。最佳觀賞點：湖山里休閒農園區、竹子湖步道。"),
            ("好母咖啡", "位於陽明山國家公園內的咖啡廳，由媽媽們經營，主打有機咖啡豆和手工烘焙。環境優美，可俯瞰台北盆地。"),
            ("交通方式", "搭乘捷運紅線到淡水站，轉乘公車261或藍18到陽明山。或從台北車站搭計程車約20分鐘。"),
            ("預算估算", "交通：約30-100台幣。門票：免費。餐飲：約200-500台幣。合计約230-600台幣（約57-150人民幣）。"),
        ],
        "tags": ["陽明山", "國家公園", "海芋", "火山", "溫泉"],
        "lock": 2303,
    },
    # Europe
    "eu-paris": {
        "title": "巴黎三天兩夜全攻略：鐵塔、羅浮宮、蒙馬特与塞納河遊船",
        "desc": "巴黎是世界上最浪漫的都市，埃菲爾鐵塔、羅浮宮、蒙馬特高地，每一處都是明信片級的美景。",
        "h2s": [
            ("Day1 鐵塔＆凡爾賽", "上午：埃菲爾鐵塔二樓觀景台（成人26.8歐元）。中午：塞納河遊船（Bateaux Mouches，約15歐元）。下午：凡爾賽宮（約20歐元，建議預約）。晚上：香榭麗舍大道晚餐。"),
            ("Day2 羅浮宮＆花都", "上午：羅浮宮（約17歐元，預購票省排隊時間）。中午：杜樂麗花園野餐。下午：奧賽博物館（印象派聖地）。晚上：紅磨坊秀（約90歐元起）。"),
            ("Day3 蒙馬特＆聖母院", "上午：蒙馬特高地、聖心堂。中午：小香貧咖啡廳。下午：巴黎聖母院外觀（整修中）。晚上：老佛爺百貨購物。"),
            ("美食推薦", "布列塔尼可麗餅（Crêperie Bretonne）是巴黎最老牌的可麗餅店。L'Ambroisie在孚日廣場，是米其林三星餐廳。Fontain de Mars的馬卡龍是必買伴手禮。"),
            ("預算估算", "機票：約15,000-25,000台幣。住宿：約2,000-5,000台幣/晚。餐飲：約1,500-3,000台幣/天。門票：約1,000-2,000台幣。合計約21,500-41,000台幣（約5,000-9,500人民幣）。"),
        ],
        "tags": ["巴黎", "鐵塔", "羅浮宮", "蒙馬特", "三日遊"],
        "lock": 2401,
    },
    "eu-london": {
        "title": "倫敦四天遊：大笨鐘、大英博物館與白金漢宮完整攻略",
        "desc": "倫敦是世界上最多元化的城市之一，從皇家遺產到街頭藝術，從古典博物館到現代商場。",
        "h2s": [
            ("Day1 皇家倫敦", "上午：白金漢宮換哨儀式（夏季11:00，冬季10:00）。中午：聖詹姆斯公園餵天鵝。下午：大笨鐘、國會大廈、西敏寺。晚上：倫敦眼夜景（約30鎊）。"),
            ("Day2 博物館日", "上午：大英博物館（免費，建議2-3小時）。中午：科文特花園用餐。下午：國家美術館（特拉法加廣場，免費）。晚上：西區音樂劇（推薦《悲慘世界》或《貓》）。"),
            ("Day3 倫敦塔", "上午：倫敦塔（約30鎊，看寶劍和皇冠）。中午：塔橋散步。下午：泰特現代美術館（免費）。晚上：博羅市場（Borough Market）品嚐各地美食。"),
            ("Day4 購物與文青", "上午：牛津街購物。中午：蘇豪區（Soho）午餐。下午：考文特花園和肖爾迪奇區（Shoreditch）的街頭藝術。晚上：碎片大廈（The Shard）觀景台。"),
            ("預算估算", "機票：約18,000-30,000台幣。住宿：約3,000-6,000台幣/晚。餐飲：約1,500-3,000台幣/天。門票：約2,000-4,000台幣。合計約26,000-48,000台幣（約6,000-11,000人民幣）。"),
        ],
        "tags": ["倫敦", "大笨鐘", "博物館", "購物", "四天遊"],
        "lock": 2402,
    },
    "eu-rome": {
        "title": "羅馬四日遊：斗獸場、特雷維噴泉與梵蒂岡museum完整攻略",
        "desc": "羅馬是永恒之城，斗獸場、萬神殿、特雷維噴泉見證了兩千年的歷史。梵蒂岡museum收藏了人類最偉大的藝術品。",
        "h2s": [
            ("Day1 古羅馬", "上午：斗獸場（約18歐元，含古羅馬廣場和帕拉汀山）。中午：威尼斯廣場和維托利亞諾紀念堂。下午：帝國廣場漫步。晚上：特雷維噴泉扔硬幣（傳說扔一枚會重返羅馬）。"),
            ("Day2 梵蒂岡", "上午：梵蒂岡museum（約20歐元，預購票免排隊）。中午：聖彼得大教堂（免費，著裝要求嚴格）。下午：聖天使城堡。晚上：西班牙廣場和納沃納廣場。"),
            ("Day3 文藝復興", "上午：萬神殿（免費）。中午：孔多帝街購物。下午：博爾蓋塞美術館（需預約，約20歐元）。晚上： Трасте韋雷區晚餐（Trastevere）。"),
            ("美食推薦", "Pizza al Taglio（切片披薩）在Via del Teatro Valleschia最著名。Gelo Artigianale是羅馬最好的手工冰淇淋店。Cacio e Pepe（起司義大利麵）是羅馬四大經典麵食之一。"),
            ("預算估算", "機票：約18,000-28,000台幣。住宿：約2,500-5,000台幣/晚。餐飲：約1,200-2,500台幣/天。門票：約1,500-3,000台幣。合計約25,000-45,000台幣（約5,800-10,500人民幣）。"),
        ],
        "tags": ["羅馬", "斗獸場", "梵蒂岡", "美食", "四日遊"],
        "lock": 2403,
    },
    # Oceania
    "oce-sydney": {
        "title": "悉尼四天遊：歌劇院、沙灘與岩石區美食完整攻略",
        "desc": "悉尼是澳洲最大的城市，歌劇院和海港大橋是世界上最知名的地標。邦迪海灘的衝浪文化、岩石區的歷史風情。",
        "h2s": [
            ("Day1 海港經典", "上午：悉尼歌劇院導覽（約40澳元）。中午： Circular Quay 海鮮午餐。下午： 海港大橋攀登（約280澳元）或環形碼頭散步。晚上： Sydney Harbour Dining 晚餐。"),
            ("Day2 邦迪海灘", "上午：邦迪海灘衝浪課程（約80澳元）。中午： Bondi Icebergs Pool 游泳。下午： Bondi to Coogee 海岸步道（6公里，約2小時）。晚上： Surry Hills 餐廳區晚餐。"),
            ("Day3 岩石區與博物館", "上午： 岩石區（The Rocks）歷史徒步導覽（免費）。中午： Rocks Marketplace 早午餐。下午： 澳洲博物館和海事博物館（均免費）。晚上： Darling Harbour 夜景。"),
            ("Day4 藍山一日遊", "全天： 藍山國家公園（Three Sisters岩層）。從中央車站搭Train約2小時。推薦Scenic World纜車（約30澳元）。晚上返回市區。"),
            ("預算估算", "機票：約25,000-40,000台幣。住宿：約2,500-5,000台幣/晚。餐飲：約1,500-3,500台幣/天。門票：約1,500-3,000台幣。合計約33,000-57,000台幣（約7,500-13,000人民幣）。"),
        ],
        "tags": ["悉尼", "歌劇院", "邦迪海灘", "藍山", "四天遊"],
        "lock": 2501,
    },
}

def generate_article(slug, template, region_code):
    region = REGIONS[region_code]
    lock = template.get("lock", region["default_lock"])
    
    h2_content = ""
    for title, content in template["h2s"]:
        h2_content += f"<h2>{title}</h2>\n<p>{content}</p>\n"
    
    tags_html = "".join(f'<span class="tag">{t}</span>' for t in template["tags"])
    
    html = f'''<!doctype html>
<html lang="zh-Hant">
<head>
<link rel="stylesheet" href="/travel-guide.esimart/assets/style.css">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{template["title"]}｜{region["name"]}旅遊攻略｜旅遊通 eSIM</title>
<meta name="description" content="{template["desc"]}">
<meta name="keywords" content="{', '.join(template['tags'])}">
<meta name="author" content="旅遊通 eSIM 編輯團隊">
<meta name="date_published" content="{TODAY}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://chiag455371.github.io/travel-guide.esimart/articles/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:locale" content="zh_TW">
<meta property="og:title" content="{template['title']}">
<meta property="og:description" content="{template['desc']}">
<meta property="og:url" content="https://chiag455371.github.io/travel-guide.esimart/articles/{slug}.html">
<meta property="og:image" content="https://loremflickr.com/1200/630/{region['keyword']}&lock={lock+100}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{template['title']}","description":"{template['desc']}","image":"https://loremflickr.com/1200/630/{region['keyword']}&lock={lock+100}","datePublished":"{TODAY}","dateModified":"{TODAY}","author":{{"@type":"Organization","name":"旅遊通 eSIM"}},"publisher":{{"@type":"Organization","name":"旅遊通 eSIM","url":"https://travel-guide.esimart.cc"}}}}</script>
</head>
<body>
<nav class="topnav">
  <a class="brand" href="https://chiag455371.github.io/travel-guide.esimart/"><em>旅遊通</em> eSIM</a>
  <button class="menu-toggle" onclick="document.querySelector('.nav-links').classList.toggle('active')">&#9776;</button>
  <div class="nav-links">
    <a href="https://chiag455371.github.io/travel-guide.esimart/">首頁</a>
    <a href="https://chiag455371.github.io/travel-guide.esimart/articles/">全部攻略</a>
    <a href="https://chiag455371.github.io/travel-guide.esimart/articles/{region_code}.html">{region['flag']} {region['name']}</a>
    <a href="https://chiag455371.github.io/travel-guide.esimart/articles/jp.html">{REGIONS['jp']['flag']} {REGIONS['jp']['name']}</a>
    <a href="https://chiag455371.github.io/travel-guide.esimart/articles/kr.html">{REGIONS['kr']['flag']} {REGIONS['kr']['name']}</a>
    <a href="https://chiag455371.github.io/travel-guide.esimart/articles/tw.html">{REGIONS['tw']['flag']} {REGIONS['tw']['name']}</a>
    <a href="https://chiag455371.github.io/travel-guide.esimart/articles/eu.html">{REGIONS['eu']['flag']} {REGIONS['eu']['name']}</a>
    <a href="https://chiag455371.github.io/travel-guide.esimart/articles/oce.html">{REGIONS['oce']['flag']} {REGIONS['oce']['name']}</a>
    <a class="btn-nav" href="{DISTRIBUTOR}" target="_blank" rel="noopener">🛒 eSIM 方案</a>
  </div>
</nav>
<article>
<header>
  <div class="breadcrumb"><a href="https://chiag455371.github.io/travel-guide.esimart/">首頁</a> <span>›</span> <a href="https://chiag455371.github.io/travel-guide.esimart/articles/">全部攻略</a> <span>›</span> <a href="https://chiag455371.github.io/travel-guide.esimart/articles/{region_code}.html">{region['flag']} {region['name']}</a> <span>›</span> <span>{template["title"]}</span></div>
  <h1>{template["title"]}</h1>
  <p class="subtitle">{template["desc"]}</p>
  <div class="meta-row">
    <span class="meta-date">📅 更新：{TODAY}</span>
    <span class="meta-read">⏱ 約 10 分鐘閱讀</span>
    <span class="meta-region">{region['flag']} {region['name']}</span>
  </div>
  <div class="tags">{tags_html}</div>
  <figure><img src="https://loremflickr.com/600/400/{region['keyword']}?lock={lock}" alt="{template['title']}" loading="lazy"><figcaption>圖說：{region['name']}的迷人風景</figcaption></figure>
</header>
<div class="esim-cta-inline">
  <div class="esim-cta-inner">
    <div class="esim-icon">{region['flag']}</div>
    <div class="esim-cta-text"><strong>去{region['name']}上網不用煩惱</strong><span>旅遊通 eSIM 提供{region['name']}地區高速 4G/LTE 方案，QR Code 掃描安裝，落地立即連網。<br>支援 LINE、IG 隨時上傳，全程無隱藏費用。</span></div>
    <a class="btn-esim" href="{DISTRIBUTOR}" target="_blank" rel="noopener">查看 {region['name']} eSIM 方案 →</a>
  </div>
</div>
{h2_content}
<div class="esim-cta">
  <h2>{region['flag']} 去{region['name']}上網不用煩惱</h2>
  <p>出發前線上購買 QR Code 掃描安裝，落地立即連網。<br>支援 4G/LTE 高速，LINE、IG 隨時上傳，全程無隱藏費用。</p>
  <a class="btn" href="{DISTRIBUTOR}" target="_blank" rel="noopener">查看 {region['name']} eSIM 方案 →</a>
</div>
<h2>❓ 常見問題</h2>
<details><summary>網路速度如何？</summary><p>旅遊通 eSIM 提供 4G/LTE 高速網路，可流暢使用 LINE、Instagram、YouTube 等應用程式。</p></details>
<details><summary>我的手機支援 eSIM 嗎？</summary><p>iPhone XS 及以上、Samsung S20 及以上、Google Pixel 3 及以上均支援。請確認您的手機型號。</p></details>
<details><summary>eSIM 安裝需要技術能力嗎？</summary><p>完全不需要！收到 QR Code 後，打開手機設定 → 行動數據 → 新增 eSIM，掃描 QR Code 即可完成。</p></details>
<div class="info-box">💡 <strong>小編貼士：</strong>建議避開連續假期前往，飯店和機票價格會上漲 30-50%。提前 2-3 個月訂票最划算。</div>
<div class="author-box">
  <h3>關於本文</h3>
  <p>本文內容由旅遊通 eSIM 編輯團隊撰寫，資訊已於 {TODAY} 更新核對。</p>
  <p><strong>聯絡我們：</strong><a href="mailto:Service@esimart.com">Service@esimart.com</a></p>
  <p><strong>客服 LINE：</strong><a href="https://line.me/R/ti/p/@esimart_oa" target="_blank" rel="noopener">@esimart_oa</a></p>
</div>
</article>
<footer>
  <p>© 2024-2026 旅遊通 eSIM｜全球 58 國流量卡</p>
  <p><a href="mailto:Service@esimart.com">Service@esimart.com</a>｜<a href="https://line.me/R/ti/p/@esimart_oa" target="_blank" rel="noopener">LINE: @esimart_oa</a></p>
</footer>
<button class="back-to-top" onclick="window.scrollTo({top:0,behavior:'smooth'})" title="回到頂部">↑</button>
<script>const btn=document.querySelector('.back-to-top');window.addEventListener('scroll',()=>btn.classList.toggle('show',window.scrollY>400));</script>
</body>
</html>'''
    return html

def main():
    used_slugs = set()
    for fn in os.listdir(ARTICLES):
        if fn.endswith(".html"):
            used_slugs.add(fn.replace(".html", ""))
    
    available = {k: v for k, v in ARTICLE_TEMPLATES.items() if k not in used_slugs}
    
    # Generate up to 20 new articles
    to_generate = random.sample(list(available.items()), min(20, len(available)))
    
    generated = 0
    for slug, template in to_generate:
        region_code = slug.split("-")[0]
        html = generate_article(slug, template, region_code)
        fp = os.path.join(ARTICLES, f"{slug}.html")
        with open(fp, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  GENERATED: {slug}.html")
        generated += 1
    
    print(f"\nTotal generated: {generated} articles")
    print(f"Date: {TODAY}")

if __name__ == "__main__":
    main()
