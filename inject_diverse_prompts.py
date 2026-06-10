#!/usr/bin/env python3
"""
inject_diverse_prompts.py
- gallery-data.json에 글로벌 다양성 프롬프트 144개 주입
- 젠더/민족/연령/문화권 균형 설계
- 카테고리별 12개 신규 포스트 추가
"""
import json, os, time

WORK_DIR  = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
GALLERY   = os.path.join(WORK_DIR, "gallery-data.json")

# ─── Diverse Prompts by Category ────────────────────────────────────────────
NEW_POSTS = [

  # ═══════════════════════════════════════════════════════════
  # PORTRAIT — 12 new: global gender/ethnicity/age diversity
  # ═══════════════════════════════════════════════════════════
  {"id": 90001, "tags": ["portrait"], "shortcode": "div_portrait_01",
   "caption": "중동 남성 에디토리얼 포트레이트",
   "prompt": "Cinematic editorial portrait of a distinguished Middle Eastern man in his mid-30s, sharp jawline, thick well-groomed beard, dark expressive eyes. Wearing a tailored charcoal wool suit with an open collar cream shirt, no tie. Background: warm terracotta studio wall with side rim lighting. Expression: calm, confident, piercing gaze. Skin: deep olive tone, visible texture. Mood: Vogue Men editorial, high-contrast, masculine elegance."},

  {"id": 90002, "tags": ["portrait"], "shortcode": "div_portrait_02",
   "caption": "서아프리카 남성 전통 복식 포트레이트",
   "prompt": "Majestic full-body editorial portrait of a tall, broad-shouldered West African man in his 40s. Wearing an elaborate Kente cloth boubou in vibrant royal blue, gold, and crimson geometric patterns. Elaborate beaded necklace and wrist cuffs. Expression: regal, serene, direct gaze. Background: clean ivory studio. Lighting: bright even studio with warm golden rim. Skin: rich deep ebony, luminous. Mood: National Geographic meets high fashion."},

  {"id": 90003, "tags": ["portrait"], "shortcode": "div_portrait_03",
   "caption": "북유럽 남성 자연광 캐주얼",
   "prompt": "Relaxed lifestyle portrait of a Nordic Scandinavian man in his late 20s, sandy blond tousled hair, light blue eyes, warm freckled fair skin. Wearing an oversized oatmeal linen shirt, sleeves rolled, light denim. Sitting near a floor-to-ceiling window, soft diffused natural daylight. Expression: easy smile, warm and approachable. Background: minimalist Scandinavian interior, birch wood tones. Mood: Copenhagen street style, effortlessly cool."},

  {"id": 90004, "tags": ["portrait"], "shortcode": "div_portrait_04",
   "caption": "라틴아메리카 여성 비비드 패션",
   "prompt": "Bold editorial portrait of a Colombian woman in her late 20s, voluminous dark curly hair, radiant warm caramel skin, expressive dark eyes with bold cat-eye liner. Wearing a vibrant cobalt-blue off-shoulder ruffled dress. Background: painted mural wall of tropical flowers. Expression: joyful, full laugh, showing teeth. Jewelry: large gold hoop earrings, layered gold chains. Mood: Cartagena street fashion meets editorial."},

  {"id": 90005, "tags": ["portrait"], "shortcode": "div_portrait_05",
   "caption": "남아시아 여성 현대 포트레이트",
   "prompt": "Sophisticated close-up editorial portrait of a South Indian woman in her early 30s, lustrous jet-black hair worn in a loose modern updo with loose tendrils. Rich warm brown skin, naturally full lips with plum-tinted gloss, kohl-lined dark eyes. Wearing a contemporary silk blouse in deep teal. Background: soft blurred botanical garden. Expression: thoughtful, self-assured. Jewelry: temple-style gold earrings. Mood: modern South Asian luxury editorial."},

  {"id": 90006, "tags": ["portrait"], "shortcode": "div_portrait_06",
   "caption": "흑인 여성 뷰티 에디토리얼",
   "prompt": "Ultra-close-up beauty editorial portrait of a Black American woman in her mid-20s. Natural 4C coily hair, styled in a sculptural high puff crown. Skin: flawless deep espresso with warm undertones, glass-skin finish. Bold fuschia lip, defined cheekbones with highlight dusting. Background: gradient deep plum to midnight black. Lighting: dramatic split Rembrandt light. Mood: Black beauty magazine — Essence meets Vogue."},

  {"id": 90007, "tags": ["portrait"], "shortcode": "div_portrait_07",
   "caption": "동아시아 중년 남성 사업가 포트레이트",
   "prompt": "Authoritative executive portrait of a Chinese man in his early 50s, silver-streaked black hair neatly parted, strong prominent features, slight confident smile. Wearing a precisely tailored dark navy double-breasted blazer over white spread-collar shirt. Background: cool charcoal seamless. Lighting: Rembrandt studio, one strong key light. Expression: composed, trustworthy leadership aura. Mood: Forbes Asia cover shoot."},

  {"id": 90008, "tags": ["portrait"], "shortcode": "div_portrait_08",
   "caption": "유럽 시니어 여성 우아한 포트레이트",
   "prompt": "Elegant portrait of a French woman in her late 60s, silver bob haircut with a subtle wave, brilliant blue-grey eyes, fine laugh lines that speak of a life well-lived. Wearing a cashmere turtleneck in soft ecru and a single strand of pearls. Background: warm Parisian apartment, bookshelves. Lighting: soft window light. Expression: knowing smile, sophisticated serenity. Mood: Vogue Paris silver generation editorial."},

  {"id": 90009, "tags": ["portrait"], "shortcode": "div_portrait_09",
   "caption": "논바이너리 앤드로지너스 패션 포트레이트",
   "prompt": "High-fashion editorial portrait of a non-binary individual in their mid-20s, androgynous features, shaved sides with a dramatic swooped platinum blonde top. Sharp cheekbones, neutral expression. Wearing a sculptural avant-garde black and white asymmetric jacket. Background: pure white studio. Lighting: hard directional overhead spot. Makeup: sharp graphic eyeliner, no other makeup. Mood: Dazed & Confused editorial, gender-fluid luxury."},

  {"id": 90010, "tags": ["portrait"], "shortcode": "div_portrait_10",
   "caption": "어린이 순수한 자연 포트레이트",
   "prompt": "Joyful lifestyle portrait of a mixed-heritage boy approximately 7 years old, curly brown hair, warm honey-toned skin, bright gap-toothed smile with sparkling brown eyes. Wearing a striped cotton tee and denim overalls. Location: sunlit garden with golden hour light filtering through oak leaves. Expression: mid-laugh, candid and carefree. Mood: natural child photography, pure innocence, warm editorial."},

  {"id": 90011, "tags": ["portrait"], "shortcode": "div_portrait_11",
   "caption": "중동 여성 현대적 히잡 패션",
   "prompt": "Contemporary fashion portrait of a Moroccan woman in her early 30s, wearing a modern styled hijab in dusty rose silk, perfectly draped. Radiant warm olive-bronze skin, deep hazel eyes with precise liner, defined brows. Wearing a matching rose-toned blazer, minimalist gold jewelry. Background: architectural white Moroccan riad courtyard. Expression: self-assured elegance. Mood: modern global Muslim fashion editorial."},

  {"id": 90012, "tags": ["portrait"], "shortcode": "div_portrait_12",
   "caption": "원주민 문화 존중 포트레이트",
   "prompt": "Dignified contemporary portrait of a First Nations Canadian woman in her 40s, long straight black hair with a single braid adorned with a turquoise bead. Rich warm umber skin, strong cheekbones. Wearing a modern wool blanket coat with traditional geometric beaded detailing. Background: expansive mountain lake landscape. Lighting: golden hour. Expression: proud, grounded. Mood: National Geographic dignity meets modern indigenous fashion."},

  # ═══════════════════════════════════════════════════════════
  # ILLUSTRATION — 12 new: diverse characters and styles
  # ═══════════════════════════════════════════════════════════
  {"id": 90013, "tags": ["illustration"], "shortcode": "div_illus_01",
   "caption": "소년 주인공 모험 일러스트",
   "prompt": "Vibrant anime-style adventure illustration of a brave young boy protagonist, approximately 12, with spiky dark hair and determined amber eyes. Wearing a worn travel cloak, leather satchel across his chest. Pose: leaping forward with a wooden staff raised, mid-action. Background: vast fantasy landscape with floating islands and glowing aurora. Style: Studio Ghibli warmth meets modern shonen manga energy."},

  {"id": 90014, "tags": ["illustration"], "shortcode": "div_illus_02",
   "caption": "다인종 우정 그룹 일러스트",
   "prompt": "Warm, joyful friendship group illustration featuring five children of diverse ethnicities — East Asian, Black, South Asian, Latina, Middle Eastern — aged 8-10. All laughing together under a rainbow while holding hands. Flat vector art style with bold, cheerful colors. Each child in culturally resonant but modern casual clothes. Background: sunny park with stylized trees. Mood: inclusive, celebratory, children's book editorial illustration."},

  {"id": 90015, "tags": ["illustration"], "shortcode": "div_illus_03",
   "caption": "시니어 할머니 따뜻한 일러스트",
   "prompt": "Heartwarming hand-painted style illustration of a warm elderly Japanese grandmother (obaachan) in her 80s, silver bun, rosy cheeks, tiny frame, wearing a traditional indigo kasuri kimono. She kneels in a lush garden tending to bonsai with small pruning scissors. A tabby cat sleeps on a stone nearby. Style: Studio Ghibli watercolor warmth. Mood: quiet, dignified aging, intergenerational connection."},

  {"id": 90016, "tags": ["illustration"], "shortcode": "div_illus_04",
   "caption": "아프리카 전통 문양 일러스트 캐릭터",
   "prompt": "Bold, graphic illustration of a confident young West African girl, approximately 10, with large natural afro puffs adorned with colorful cowrie shells. Wearing a modern outfit with Kente cloth pattern details. She holds a glowing magical drum. Background: stylized Savannah at sunset with geometric Adinkra pattern borders. Style: Afrofuturism meets children's illustration. Colors: terracotta, gold, deep violet, warm amber."},

  {"id": 90017, "tags": ["illustration"], "shortcode": "div_illus_05",
   "caption": "수묵화 스타일 무사 일러스트",
   "prompt": "Expressive East Asian ink wash (sumi-e) style illustration of a lone samurai warrior standing still on a misty mountain peak at dawn. Male figure, powerful silhouette in layered haori armor, one hand on katana handle. Background: sweeping brushstroke mountains, pine trees, rising mist. Colors: monochromatic black ink gradients with a single accent of crimson on his sash. Mood: contemplative, powerful restraint."},

  {"id": 90018, "tags": ["illustration"], "shortcode": "div_illus_06",
   "caption": "중남미 카니발 축제 일러스트",
   "prompt": "Explosive, joyful carnival illustration capturing the energy of Rio Carnival. A non-binary performer in an elaborate feathered headdress, sequined bodysuit in electric teal and gold, arms outstretched mid-spin. Confetti and fireworks burst around them. Background: packed stadium with blurred crowd. Style: bold flat graphic illustration, vibrant vector. Mood: pure celebratory joy, inclusive festival energy."},

  {"id": 90019, "tags": ["illustration"], "shortcode": "div_illus_07",
   "caption": "북유럽 신화 여신 일러스트",
   "prompt": "Epic Norse mythology illustration of Freya, the goddess of love and war. Tall, powerful warrior woman with flowing amber hair braided with ravens feathers. Wearing ornate gold-plated armor over fur-trimmed battle dress. Holding a glowing runic spear, a golden necklace Brisingamen glowing at her throat. Background: Asgard rainbow bridge at twilight. Style: fantasy epic illustration, painterly, dramatic lighting."},

  {"id": 90020, "tags": ["illustration"], "shortcode": "div_illus_08",
   "caption": "귀여운 남자아이 스티커 일러스트",
   "prompt": "Adorable chibi-style boy character sticker illustration. A chubby-cheeked Korean boy approximately 6 years old, round face, bowl cut black hair, big sparkly eyes, wearing a tiny dinosaur hoodie. Poses: waving hello, sleeping, crying dramatically, eating ramen — all arranged as a cute sticker sheet on white background. Style: LINE Friends meets Kakao Friends. Colors: warm, bright pastels."},

  {"id": 90021, "tags": ["illustration"], "shortcode": "div_illus_09",
   "caption": "인도 신화 영웅 일러스트",
   "prompt": "Dynamic mythological illustration of Arjuna from the Mahabharata. Noble warrior man, dark brown skin, decorated with traditional markings, fierce focused eyes. Kneeling drawing a divine golden bow (Gandiva), arrow charged with lightning. Background: vast Kurukshetra battlefield at golden hour with lotus patterns framing the scene. Style: detailed painterly illustration with intricate Indian motif borders. Mood: epic, sacred."},

  {"id": 90022, "tags": ["illustration"], "shortcode": "div_illus_10",
   "caption": "퀴어 프라이드 따뜻한 커플 일러스트",
   "prompt": "Tender, warm illustration of two men in their late 20s sharing a quiet moment at a café table. One man is Black with short natural hair and a warm smile, wearing a yellow sweater. The other is South Asian with glasses and a plaid shirt. They are laughing together over coffee, hands touching on the table. Style: soft watercolor with gentle linework, pastel warm tones. Mood: everyday love, gentle and joyful."},

  {"id": 90023, "tags": ["illustration"], "shortcode": "div_illus_11",
   "caption": "러시아 발레 일러스트",
   "prompt": "Ethereal illustration of a male ballet dancer mid-leap on a Moscow stage. Tall, lean, Eastern European features, intense focus. Wearing white and gold theatrical costume, arms extended overhead perfectly. Stage lights create dramatic god-rays. Background: ornate Bolshoi Theatre interior with velvet red curtains. Style: romantic realism illustration with delicate watercolor brushwork. Mood: transcendent artistry, masculine grace."},

  {"id": 90024, "tags": ["illustration"], "shortcode": "div_illus_12",
   "caption": "장애인 슈퍼히어로 일러스트",
   "prompt": "Empowering superhero illustration of a teenage girl wheelchair user. She has natural dark curls, South Asian heritage, determined expression. Her wheelchair transforms into a sleek chrome rocket platform. She wears a vibrant turquoise and silver supersuit with glowing gauntlets. Background: city skyline at night with neon lights reflecting below. Style: bold comic book illustration, dynamic composition, inclusive heroism."},

  # ═══════════════════════════════════════════════════════════
  # PRODUCT — 12 new: global diverse model representation
  # ═══════════════════════════════════════════════════════════
  {"id": 90025, "tags": ["product"], "shortcode": "div_product_01",
   "caption": "남성 그루밍 제품 광고",
   "prompt": "Premium men's grooming product advertisement. A well-groomed Black man in his early 30s, clean shaved head, strong jaw, confident expression. Holding a sleek matte black skincare serum bottle near his jaw. Background: cool slate gray studio. Lighting: three-point studio, crisp shadows. Skin: rich mahogany, freshly moisturized glow. Styling: fitted dark turtleneck. Mood: luxury men's editorial, GQ meets Tom Ford Beauty."},

  {"id": 90026, "tags": ["product"], "shortcode": "div_product_02",
   "caption": "남성 향수 광고 에디토리얼",
   "prompt": "Cinematic fragrance advertisement featuring a Spanish man in his mid-30s, dark wavy hair, olive skin, chiseled Mediterranean features. Standing shirtless in a sunlit Iberian stone courtyard, holding an amber glass perfume bottle at chest height. Background: terracotta walls, climbing bougainvillea. Lighting: golden afternoon sun with deep shadows. Expression: mysterious, magnetic. Mood: luxury masculine fragrance — Dior Homme meets Valentino Uomo."},

  {"id": 90027, "tags": ["product"], "shortcode": "div_product_03",
   "caption": "다크 스킨톤 화장품 광고",
   "prompt": "Beauty product advertisement celebrating deep skin tones. A Nigerian model in her mid-20s, stunning dark chocolate skin with natural luminosity. She holds a luxury foundation bottle in her exact shade. Close-up beauty shot with impeccable natural makeup. Background: warm gold leaf texture. Lighting: ring light + warm gels, maximum skin radiance. Expression: proud, glowing. Text prop: 'YOUR SHADE EXISTS' in elegant serif. Mood: Fenty Beauty aesthetic."},

  {"id": 90028, "tags": ["product"], "shortcode": "div_product_04",
   "caption": "남성 스킨케어 어성 모델 광고",
   "prompt": "Clean, modern men's skincare advertisement. A Japanese man in his late 20s, smooth glass skin, neat black hair, warm beige tone. Wearing a crisp white tee, holding a minimal skincare serum in both hands, examining it with curious interest. Background: pure white seamless. Lighting: soft diffused front light. Expression: thoughtful consideration, approachable. Mood: KOSE Men's / Shiseido Men — K-beauty meets J-beauty men's skincare."},

  {"id": 90029, "tags": ["product"], "shortcode": "div_product_05",
   "caption": "운동화 광고 남성 모델",
   "prompt": "High-energy sneaker advertisement featuring a lean athletic Black teen male, approximately 16, mid-air dunk jump in an urban basketball court at golden hour. Wearing bold electric orange performance sneakers, matching shorts. Droplets of sweat caught in the air. Background: chain-link fence, urban skyline blurred. Lighting: dramatic backlight rim creating a glowing silhouette. Mood: Nike Air Jordan energy, raw street athleticism."},

  {"id": 90030, "tags": ["product"], "shortcode": "div_product_06",
   "caption": "고령자 헬스케어 제품 광고",
   "prompt": "Empowering healthcare product advertisement. A vital, active Japanese woman in her 70s — silver bob, radiant smile, healthy posture. She is demonstrating an ergonomic health device while standing in a bright modern kitchen. Background: warm white kitchen with natural plants. Lighting: cheerful daylight. Expression: genuine satisfaction, active independence. Mood: premium senior wellness brand, dignified and energetic."},

  {"id": 90031, "tags": ["product"], "shortcode": "div_product_07",
   "caption": "인도 아유르베다 제품 광고",
   "prompt": "Luxury Ayurvedic beauty product advertisement. A South Indian woman in her 30s, traditional jasmine flowers in her long oiled hair, deep warm copper skin. She pours a golden oil from an ornate terracotta vessel onto her palm. Background: lush Indian botanical garden with marigolds. Lighting: warm golden sunrise. Expression: serene, meditative. Props: turmeric, rose petals, neem leaves surrounding her. Mood: Forest Essentials meets editorial luxury."},

  {"id": 90032, "tags": ["product"], "shortcode": "div_product_08",
   "caption": "스포츠웨어 여성 다양성 광고",
   "prompt": "Powerful sportswear advertisement featuring a group of three diverse women of different body types — athletic, curvy, petite — all in matching bold red sportswear. Three women: a tall Black woman, a plus-size Latina, and a lean East Asian woman. All mid-action in a dynamic choreographed jump pose. Background: clean white studio. Lighting: high-key bright, energetic. Mood: celebratory body diversity, Adidas / Nike inclusive energy."},

  {"id": 90033, "tags": ["product"], "shortcode": "div_product_09",
   "caption": "중동 남성 럭셔리 시계 광고",
   "prompt": "Ultra-premium luxury watch advertisement. A distinguished Emirati man in his 50s, silver-streaked beard, commanding presence. Close-up of his wrist wearing an intricate gold chronograph watch. Background: polished dark marble surface. Lighting: single dramatic spotlight highlighting the watch face. Skin: warm olive, manicured hands. Clothing visible: crisp white kandura sleeve. Mood: Rolex meets Gulf luxury — timeless masculine prestige."},

  {"id": 90034, "tags": ["product"], "shortcode": "div_product_10",
   "caption": "어린이 장난감 광고 혼혈 아이",
   "prompt": "Bright, joyful toy product advertisement featuring a mixed-race boy, approximately 5, with curly sandy-brown hair, huge sparkling green eyes, and warm golden-honey skin. He holds up a colorful building block set with pure delight, eyes wide with excitement. Background: cozy, warm playroom with wooden toys. Lighting: warm, soft. Expression: pure unfiltered joy. Mood: premium children's toy editorial, inclusive family advertising."},

  {"id": 90035, "tags": ["product"], "shortcode": "div_product_11",
   "caption": "젠더뉴트럴 향수 광고",
   "prompt": "Avant-garde gender-neutral fragrance advertisement. Two models — one feminine presenting person with short platinum hair, one masculine presenting person with long dark waves — both wearing all-white minimal clothing. They hold opposite ends of an elegant minimalist clear glass bottle. Background: pure white studio with soft gradient. Lighting: ethereal even light. Expression: serene, unified. Mood: Byredo / Le Labo gender-fluid luxury fragrance editorial."},

  {"id": 90036, "tags": ["product"], "shortcode": "div_product_12",
   "caption": "라틴 남성 패션 광고",
   "prompt": "Vibrant fashion editorial advertisement featuring a charismatic Brazilian man in his late 20s, bronze warm skin, curly dark hair, infectious confident smile. Wearing a bold tropical print silk shirt unbuttoned at chest, tailored cream linen trousers. Background: Copacabana beach promenade, blue sky. Lighting: bright tropical midday sun. Mood: luxury Latin lifestyle brand — São Paulo meets Milan fashion week."},

  # ═══════════════════════════════════════════════════════════
  # FOOD — 12 new: global cuisine diversity
  # ═══════════════════════════════════════════════════════════
  {"id": 90037, "tags": ["food"], "shortcode": "div_food_01",
   "caption": "인도 탈리 정식 푸드 포토",
   "prompt": "Stunning overhead editorial food photograph of a traditional South Indian banana leaf meal (Sadya). On a fresh green banana leaf: steaming white rice mound surrounded by 12+ small portions of colorful curries, chutneys, papadum, banana chips, payasam. Rich turmeric yellows, vibrant greens, deep reds. Props: brass water vessel, lotus flower garnish on side. Mood: Kerala harvest festival feast, Bon Appétit meets National Geographic."},

  {"id": 90038, "tags": ["food"], "shortcode": "div_food_02",
   "caption": "멕시코 타코 스트리트 푸드",
   "prompt": "Vibrant close-up food photograph of authentic Mexican al pastor tacos on a rustic tin plate. Three tacos: double corn tortillas, glistening charred pork with achiote marinade, fresh diced pineapple, white onion, cilantro, bright green salsa. Charred lime wedge on side. Background: sizzling comal, smoky street food atmosphere. Colors: warm amber, bright citrus, vibrant green. Lighting: dramatic warm street lamp glow. Mood: Mexico City taqueria midnight."},

  {"id": 90039, "tags": ["food"], "shortcode": "div_food_03",
   "caption": "에티오피아 인제라 전통 음식",
   "prompt": "Beautiful overhead editorial photograph of Ethiopian Injera feast spread on a large communal plate. Spongy grey-brown injera flatbread topped with colorful mounds of: rich red berbere beef tibs, creamy yellow atayef lentils, vibrant green gomen (collard greens), deep red misir wot. All presented on a traditional woven colorful Ethiopian basket plate. Mood: communal sharing, cultural dignity, National Geographic food editorial."},

  {"id": 90040, "tags": ["food"], "shortcode": "div_food_04",
   "caption": "이탈리아 파스타 장인 요리",
   "prompt": "Intimate editorial food photograph of freshly made Italian pasta carbonara in a copper pan. Glossy silky sauce coating bronze spaghetti, crispy guanciale pieces golden and translucent, freshly cracked black pepper, dusting of Pecorino romano. A wooden spoon mid-twirl. Background: worn marble Italian kitchen counter. Steam rising. Lighting: warm golden bistro light. Mood: Trattoria Roma — Casa Mia meets Bon Appétit."},

  {"id": 90041, "tags": ["food"], "shortcode": "div_food_05",
   "caption": "일본 라멘 명장 그릇",
   "prompt": "Perfect editorial close-up of a rich tonkotsu ramen bowl. Creamy opaque pork bone broth, perfectly coiled chashu pork slices with caramelized edges, soft ramen noodles, marinated soy egg cut perfectly in half showing golden jammy yolk, bamboo shoots, green onion, sheet of crispy nori. Ceramic bowl on dark wood. Background: blurred ramen shop interior with noren curtains. Lighting: warm amber overhead. Mood: Michelin ramen temple."},

  {"id": 90042, "tags": ["food"], "shortcode": "div_food_06",
   "caption": "모로코 타진 향신료 요리",
   "prompt": "Exotic overhead editorial photograph of a Moroccan lamb tagine in its traditional conical clay pot. Tender slow-cooked lamb with preserved lemons, green olives, harissa, saffron-tinged broth. Surrounding the pot: scattered rose petals, cinnamon sticks, star anise, fresh mint. Resting on hand-painted blue and white Fez ceramic tiles. Background: Marrakech riad atmosphere. Lighting: warm lantern glow. Mood: luxury North African dining."},

  {"id": 90043, "tags": ["food"], "shortcode": "div_food_07",
   "caption": "프랑스 파티스리 크루아상",
   "prompt": "Exquisite editorial photograph of freshly baked French croissants at a Parisian boulangerie. Multiple golden croissants arranged with their characteristic laminated honeycomb layers visible in cross-section cut. Butter pooling, steam wisping. One croissant on a white ceramic plate with a small ramekin of dark apricot jam. Background: marble counter, worn copper weighing scale. Lighting: soft morning Paris sunlight. Mood: luxury Parisian morning ritual."},

  {"id": 90044, "tags": ["food"], "shortcode": "div_food_08",
   "caption": "중국 딤섬 브런치",
   "prompt": "Elegant dim sum brunch editorial from above. Bamboo steamers stacked artfully revealing: har gow (shrimp dumplings) with translucent wrappers, siu mai with quail egg, turnip cake, char siu bao. Accompanied by: pu-erh tea in a delicate celadon teapot, dipping sauces, gold chopsticks. Background: dark wood Hong Kong tea house table. Lighting: warm overhead soft. Colors: jade greens, ivory, amber, pink. Mood: yum cha luxury Cantonese."},

  {"id": 90045, "tags": ["food"], "shortcode": "div_food_09",
   "caption": "페루 세비체 신선한 해산물",
   "prompt": "Vibrant editorial food photograph of Peruvian ceviche in a white ceramic bowl. Fresh tiger shrimp and sea bass marinated in tiger's milk (leche de tigre), bright yellow ají amarillo leche, red onion rings, giant Peruvian corn (choclo), sweet potato slice, crispy cancha corn. Garnish: micro cilantro, thin lime slice. Background: coastal restaurant with Pacific ocean blur. Lighting: bright tropical daylight. Colors: electric citrus, cool ocean blues."},

  {"id": 90046, "tags": ["food"], "shortcode": "div_food_10",
   "caption": "중동 샤와르마 길거리 음식",
   "prompt": "Dramatic editorial close-up of a perfectly assembled Levantine shawarma wrap. Flatbread with swirls of creamy garlic toum sauce, tightly packed layers of golden spiced chicken shawarma, pickled turnips (vibrant fuchsia), fresh parsley, tomato. Wrapped in butcher paper partially peeled. Background: busy Beirut street food stall, charcoal brazier glow. Lighting: warm night street light. Mood: authentic street food documentary."},

  {"id": 90047, "tags": ["food"], "shortcode": "div_food_11",
   "caption": "나이지리아 졸로프 라이스",
   "prompt": "Bold, celebratory overhead editorial of West African Jollof rice. Vibrant deep orange-red rice in a large cast iron pot, steaming. Surrounded by: roasted whole chicken pieces with crispy skin, fried ripe plantains, Nigerian pepper soup, fresh sliced tomatoes and onions. Side: cold Supermalt bottle. Background: bright wax print tablecloth in bold yellow/orange/green patterns. Lighting: bright cheerful daylight. Mood: West African celebration feast."},

  {"id": 90048, "tags": ["food"], "shortcode": "div_food_12",
   "caption": "비건 레인보우 볼 건강식",
   "prompt": "Stunning, vibrant overhead editorial of a vegan rainbow poke bowl. Perfect concentric color arrangement: purple beet hummus, orange sweet potato cubes, golden turmeric tofu, emerald edamame, red watermelon radish slices, white cauliflower rice base. Black and white sesame seeds scattered, microgreens crown. Background: light grey concrete surface. Lighting: clean even natural light. Mood: wholesome inclusive nutrition, clean wellness editorial."},

  # ═══════════════════════════════════════════════════════════
  # CHARACTER — 12 new: diverse global characters
  # ═══════════════════════════════════════════════════════════
  {"id": 90049, "tags": ["character"], "shortcode": "div_char_01",
   "caption": "아프리카 퓨처리즘 전사 캐릭터",
   "prompt": "Afrofuturist warrior character design. A powerful Black woman in her 30s, shaved head with geometric gold scalp tattoos, piercing amber eyes. Wearing bio-mechanical armor crafted from futuristic materials merged with traditional Yoruba bronze work and beading. She holds a glowing energy spear. Background: neon-lit Lagos skyline 2187. Style: Black Panther meets Ghost in the Shell. Colors: rich copper, deep violet, electric gold."},

  {"id": 90050, "tags": ["character"], "shortcode": "div_char_02",
   "caption": "인도 신화 마법사 남성 캐릭터",
   "prompt": "Epic Indian mythology-inspired male mage character. A commanding Brahmin sage in his 60s, long white flowing beard and hair, wise deep-set eyes, warm dark brown skin with sacred ash markings. Wearing deep saffron and crimson robes, multiple rudraksha bead strings. Hands raised channeling blue divine flames. Background: ancient Varanasi ghats at dawn with Ganges mist. Style: mythology painterly epic. Colors: gold, crimson, sapphire."},

  {"id": 90051, "tags": ["character"], "shortcode": "div_char_03",
   "caption": "바이킹 남성 전사 캐릭터",
   "prompt": "Imposing Viking warrior character design. A massive Norse man in his late 30s, fiery red braided beard, ice-blue eyes under a heavy brow. Battle-worn chainmail under a fur-trimmed cloak. Carrying a double-headed axe with runic engravings glowing faintly. Background: dramatic Norwegian fjord coastline with longships in the mist. Style: epic fantasy painterly. Colors: steel grey, deep crimson, forest green, Norse gold."},

  {"id": 90052, "tags": ["character"], "shortcode": "div_char_04",
   "caption": "라틴 뱀파이어 귀족 캐릭터",
   "prompt": "Gothic aristocrat vampire character. A pale Argentinian man in his apparent 30s (ageless vampire), sharp aristocratic features, slicked black hair, deep crimson eyes. Wearing an 18th-century Baroque velvet coat in midnight black with gold brocade, lace cravat, ornate walking cane. Standing in a baroque Buenos Aires mansion. Style: Anne Rice gothic romance meets anime villain. Colors: black, deep crimson, antique gold."},

  {"id": 90053, "tags": ["character"], "shortcode": "div_char_05",
   "caption": "중동 모래 마법사 여성 캐릭터",
   "prompt": "Mystical sand mage character design. An Arabian woman in her mid-20s, flowing dark hair partially veiled in translucent desert silk, intense kohl-lined golden eyes. Commanding a vortex of swirling golden sand particles around her hands. Wearing ornate desert warrior robes in deep teal and copper, multiple arm cuffs, ankle bells. Background: vast dune sea under a twin-moon sky. Style: One Thousand and One Nights reimagined as fantasy RPG. Colors: gold, teal, deep amber."},

  {"id": 90054, "tags": ["character"], "shortcode": "div_char_06",
   "caption": "LGBT 프라이드 파티 그룹 캐릭터",
   "prompt": "Joyful group character illustration of diverse LGBTQ+ friends at a pride parade. Five characters: a tall drag queen in rainbow sequins, a nonbinary person with colorful hair in overalls, a butch lesbian woman, a gay couple (one Black, one Asian). All surrounded by confetti, balloons, rainbow flags. Style: bright modern illustration, inclusive and celebratory. Colors: full rainbow spectrum, vivid and warm. Mood: community, love, visibility."},

  {"id": 90055, "tags": ["character"], "shortcode": "div_char_07",
   "caption": "사무라이 여성 전사 캐릭터",
   "prompt": "Fierce female samurai character (kunoichi) design. A Japanese woman in her late 20s, jet black hair in a warrior's bun with loose strands, intense dark eyes with fierce determination. Wearing partial O-yoroi samurai armor over a crimson hakama, cherry blossom embroidery on sash. Mid-draw sword pose, cherry blossom petals swirling around her blade. Background: burning castle at night. Style: Fate/Stay Night meets Ghost of Tsushima artistic style."},

  {"id": 90056, "tags": ["character"], "shortcode": "div_char_08",
   "caption": "러시아 빙설 마법사 캐릭터",
   "prompt": "Ethereal ice magic character design. A Russian woman in her 30s, long silver-white hair with ice crystal extensions, pale cool skin with blue-tinted undertones, luminous frost eyes. She floats above a frozen tundra, commanding ice pillars and blizzard spirals. Wearing an elaborate frost-crystal gown that flows into ice formations. Background: Aurora Borealis lit Siberian winter. Style: Frozen meets Witcher fantasy. Colors: ice blue, silver, midnight purple."},

  {"id": 90057, "tags": ["character"], "shortcode": "div_char_09",
   "caption": "유튜버 게이머 남성 캐릭터",
   "prompt": "Energetic gaming content creator character design. A young Korean-American man in his early 20s, stylish faded undercut, warm honey skin, bright expressive brown eyes behind gaming glasses. Wearing a hoodie with a YouTube play button logo, headphones around neck. Surrounded by floating gaming icons, controller in hand, victory pose. Background: colorful streaming setup with LED lights. Style: modern chibi-realistic hybrid. Mood: Gen-Z gaming culture."},

  {"id": 90058, "tags": ["character"], "shortcode": "div_char_10",
   "caption": "장애인 휠체어 미래 스포츠 선수",
   "prompt": "Dynamic sports character design of a Paralympic sprinter. A South Asian man in his 30s, powerful muscular upper body, determined focused expression, wearing a cutting-edge lightweight racing prosthetic. Wearing a Team India athletics uniform, mid-race at a futuristic Olympic stadium. Background: packed stadium with glowing holographic scoreboards. Style: dynamic sports illustration with motion blur. Mood: triumph, human capability, inclusion."},

  {"id": 90059, "tags": ["character"], "shortcode": "div_char_11",
   "caption": "성별 변환 판타지 정령 캐릭터",
   "prompt": "Otherworldly spirit character that transcends gender. A luminous being with androgynous features, shifting between masculine and feminine, with flowing iridescent silver hair. Their form is partially translucent, revealing shifting starscapes within. Wearing flowing robes that blend into aurora light trails. Eyes: shifting between gold and violet. Background: cosmic void with planetary rings. Style: ethereal celestial anime art meets concept art. Colors: iridescent, shifting opalescent tones."},

  {"id": 90060, "tags": ["character"], "shortcode": "div_char_12",
   "caption": "원주민 샤먼 할머니 캐릭터",
   "prompt": "Powerful shaman elder character design. An Andean Quechua grandmother in her 70s, deeply weathered warm brown skin with smile lines of wisdom, long silver braids wrapped with colorful woven threads and feathers. Wearing layered traditional Bolivian pollera skirts with intricate woven patterns. She calls spirit animals with a sacred staff. Background: Machu Picchu summit in morning mist. Style: magical realism illustration. Mood: ancestral wisdom, matriarchal power."},

  # ═══════════════════════════════════════════════════════════
  # PLUSH — 12 new: global cultural plush designs
  # ═══════════════════════════════════════════════════════════
  {"id": 90061, "tags": ["plush"], "shortcode": "div_plush_01",
   "caption": "아프리카 코끼리 봉제 인형",
   "prompt": "Adorably cute plush toy of an African savannah elephant. Chunky round proportions, oversized floppy ears, tiny tusks in cream felt. Fabric: warm grey ultra-plush minky velvet with slightly lighter belly patch. Accessories: a tiny woven Kente cloth blanket on its back. Eyes: big glossy black button eyes with embroidered lashes. Style: high-end designer plush, Jellycat quality. Background: white studio product shot."},

  {"id": 90062, "tags": ["plush"], "shortcode": "div_plush_02",
   "caption": "인도 코끼리 가네샤 인형",
   "prompt": "Charming plush toy interpretation of Ganesha, the Hindu elephant deity. Cute chibi proportions, four tiny soft arms each holding miniature accessories (lotus, sweet modak). Wearing a tiny fabric crown (mukut) and a golden dhoti. Fabric: warm coral pink velvet with gold thread embroidery details on the costume. Expression: joyful, benevolent smile embroidered. Background: white studio on a small embroidered cushion."},

  {"id": 90063, "tags": ["plush"], "shortcode": "div_plush_03",
   "caption": "아이슬란드 북극여우 봉제 인형",
   "prompt": "Incredibly soft and fluffy Arctic fox plush toy. Winter white coloring with subtle ice-blue shadow undertones. Massive fluffy tail curled around its feet. Tiny black button nose, embroidered whiskers, big round glass-like eyes with starry reflection. Fabric: premium long-pile white faux fur. Style: Jellycat Bashful quality. The fox holds a tiny felted snowflake. Background: white studio with snowflake scatter."},

  {"id": 90064, "tags": ["plush"], "shortcode": "div_plush_04",
   "caption": "멕시코 아홀로틀 귀여운 인형",
   "prompt": "Irresistibly cute axolotl (ajolote) plush toy. Plump round body, feathery external gill branches in bubblegum pink, wide perpetual smile, stubby legs. Fabric: soft minky fabric in peach-pink with pink gills in fluffy chenille. Expression: the classic axolotl smile embroidered with love. Size: 30cm. Big oval black glossy eyes. Style: collector-quality designer plush. Background: turquoise water-colored paper background."},

  {"id": 90065, "tags": ["plush"], "shortcode": "div_plush_05",
   "caption": "중국 판다 봉제 인형 전통의상",
   "prompt": "Giant panda plush toy dressed in miniature traditional Chinese Tang dynasty clothing. Classic black and white panda coloring. Wearing a tiny embroidered red silk changshan with gold cloud motifs, a small scholar's cap. Sitting cross-legged holding a tiny bamboo stalk. Fabric: super soft bamboo fiber velvet. Eyes: embroidered with warm expression. Style: Beijing Silk Road collectible plush. Background: white with subtle Chinese lattice pattern."},

  {"id": 90066, "tags": ["plush"], "shortcode": "div_plush_06",
   "caption": "스칸디나비아 무스 봉제 인형",
   "prompt": "Tall, gangly, absolutely adorable moose plush toy. Comically long thin legs, disproportionately large antlers in brown felted wool. Warm tawny brown minky body with cream belly. Big goofy stitched smile, shiny black nose. Wearing a tiny Nordic sweater in red and white snowflake pattern. Style: Danish design, Maileg aesthetic. Background: white studio with pine branch prop."},

  {"id": 90067, "tags": ["plush"], "shortcode": "div_plush_07",
   "caption": "오스트레일리아 코알라 인형",
   "prompt": "Supremely huggable koala plush toy. Plump round body with oversized fluffy grey ears, tiny eucalyptus sprig clutched in its paws. Fabric: the plushest grey mohair-style faux fur with a white fluffy chest. Large round black velvet nose, tiny embroidered black dot eyes with long lashes. Expression: utterly serene and sleepy. Style: NICI quality plush. Background: pale eucalyptus green paper background."},

  {"id": 90068, "tags": ["plush"], "shortcode": "div_plush_08",
   "caption": "브라질 투칸 새 봉제 인형",
   "prompt": "Vibrant toucan plush toy inspired by the Toco Toucan of the Amazon. Dramatically oversized orange and yellow beak in soft felt. Jet black body in smooth velvet, white throat patch, bright red undertail in felt. Round googly eyes with gold rings. Perched on a small branch prop. Style: WWF conservation plush meets designer toy. Colors: vivid tropical. Background: lush green tropical leaf backdrop."},

  {"id": 90069, "tags": ["plush"], "shortcode": "div_plush_09",
   "caption": "이집트 파라오 고양이 봉제 인형",
   "prompt": "Regal Egyptian cat plush toy inspired by Bastet. Sleek sand-golden colored cat with elegant Siamese-like proportions. Adorned with miniature gold jewelry: collar with scarab pendant, anklet bracelets, tiny blue lotus crown. Eyes: brilliant blue glass eyes with dark kohl-effect stitching. Fabric: smooth velvet in golden tan. Seated in classic Egyptian statue pose. Background: sandy desert beige with hieroglyph pattern."},

  {"id": 90070, "tags": ["plush"], "shortcode": "div_plush_10",
   "caption": "러시아 마트로시카 곰 봉제 인형",
   "prompt": "Adorable matryoshka-inspired teddy bear plush. Classic golden-brown bear wearing a hand-painted fabric matryoshka doll body costume in traditional Russian folk art style — red with white/black floral folk patterns. Painted-on facial design resembling a Russian beauty. Inside hint: a tiny baby bear peeking from a front pocket. Fabric: soft chenille. Style: cultural collector plush. Background: deep red background with folk art motifs."},

  {"id": 90071, "tags": ["plush"], "shortcode": "div_plush_11",
   "caption": "케냐 기린 봉제 인형",
   "prompt": "Charming tall giraffe plush toy. Signature long neck, warm amber and cream patchwork pattern, tiny felt ossicones (horns) in brown. Long flutter lash embroidery over big doe brown eyes. Soft suede-touch fabric in warm honey gold and caramel. Optional tiny Maasai bead necklace accessory. Style: KEEL Toys / Wild Republic quality. Background: warm savannah golden hour orange and gold paper."},

  {"id": 90072, "tags": ["plush"], "shortcode": "div_plush_12",
   "caption": "발리 원숭이 사원 봉제 인형",
   "prompt": "Cheeky Balinese macaque monkey plush toy. Warm tawny grey-brown body, pinkish face with embroidered cheeky grin, long curling tail. Dressed in a tiny handmade Balinese ceremonial sarong in gold and black checkered pattern (saput poleng). Holding a miniature banana. Fabric: plush velvet body, felt face. Style: souvenir quality meets designer plush. Background: tropical palm leaf texture background."},

  # ═══════════════════════════════════════════════════════════
  # POSTER — 12 new: global city / cultural posters
  # ═══════════════════════════════════════════════════════════
  {"id": 90073, "tags": ["poster"], "shortcode": "div_poster_01",
   "caption": "라고스 나이지리아 여행 포스터",
   "prompt": "Vibrant travel poster for Lagos, Nigeria. Art deco influenced with bold Afrocentric geometric patterns. Key visual elements: Victoria Island skyline, Bar Beach waves, sprawling Night Market, Jollof rice steam. Typography: 'LAGOS — CITY OF ENERGY' in bold modern sans-serif with Adinkra symbol borders. Colors: electric Lagos yellow, deep forest green, vibrant red of Nigerian flag. Style: 1960s Soviet travel poster meets Afrofuturism graphic."},

  {"id": 90074, "tags": ["poster"], "shortcode": "div_poster_02",
   "caption": "뭄바이 인도 시티 포스터",
   "prompt": "Dynamic Mumbai travel poster in Art Nouveau style with Indian floral motifs. Key visuals: Gateway of India arch, Mumbai local train network diagram, Dharavi colors, Bollywood film reel. 'MUMBAI — MAXIMUM CITY' typography in Devanagari script alongside English. Colors: deep saffron orange, peacock teal, Rajasthani pink, turmeric yellow. Intricate Rangoli border patterns framing the composition. Style: elegant Indo-Art Nouveau."},

  {"id": 90075, "tags": ["poster"], "shortcode": "div_poster_03",
   "caption": "상파울루 브라질 도시 포스터",
   "prompt": "Bold São Paulo cultural poster in Brazilian Concrete Art style. Elements: Paulista Avenue skyscraper geometry, Oscar Niemeyer curves, Ibirapuera Park greenery, street art murals. 'SÃO PAULO — NÃO PARA' typography in Brazilian design style. Colors: verde e amarelo (green, yellow) with deep black metropolitan energy. Geometric grid composition inspired by Hélio Oiticica and Brazilian Tropicália aesthetics."},

  {"id": 90076, "tags": ["poster"], "shortcode": "div_poster_04",
   "caption": "이스탄불 터키 여행 포스터",
   "prompt": "Mystical Istanbul travel poster in Byzantine-Ottoman fusion style. Visual elements: Blue Mosque silhouette with six minarets, Bosphorus Strait boat traffic, Grand Bazaar lanterns, traditional tilework patterns. 'İSTANBUL — WHERE WORLDS MEET' in elegant calligraphy. Colors: deep Ottoman blue, Turkish tile turquoise, antique gold, warm terracotta. Iznik tile geometric borders framing the image. Style: luxury Ottoman meets modern graphic."},

  {"id": 90077, "tags": ["poster"], "shortcode": "div_poster_05",
   "caption": "케이프타운 남아프리카 포스터",
   "prompt": "Dramatic Cape Town travel poster in bold mid-century South African style. Key elements: Table Mountain flat top silhouette, Boulders Beach penguin colony, Bo-Kaap rainbow houses, Cape Winelands. 'CAPE TOWN — AT THE TIP OF AFRICA' typography. Colors: deep Cape ocean navy, Table Mountain terracotta, Bo-Kaap vibrant primary colors, fynbos botanical illustration border. Style: Cape Dutch Art Deco with modern African energy."},

  {"id": 90078, "tags": ["poster"], "shortcode": "div_poster_06",
   "caption": "멕시코시티 문화 포스터",
   "prompt": "Rich Mexico City cultural poster in Diego Rivera mural style. Elements: Teotihuacan pyramids, Zócalo cathedral, Lucha libre mask, agave plant, Day of the Dead skull floral. 'CIUDAD DE MÉXICO — CORAZÓN DE MÉXICO' typography. Colors: Diego Rivera earth tones — terracotta, ochre, cobalt blue, revolutionary red, corn gold. Hand-painted texture style. Aztec calendar sun border detail."},

  {"id": 90079, "tags": ["poster"], "shortcode": "div_poster_07",
   "caption": "두바이 미래도시 포스터",
   "prompt": "Futuristic Dubai travel poster in sleek contemporary Arab luxury style. Key visuals: Burj Khalifa rising from desert sands, Palm Jumeirah aerial shape, desert dunes transforming into glass towers, camel and sports car silhouette together. 'DUBAI — THE FUTURE, TODAY' typography in Arabic and English. Colors: desert gold, electric blue Persian Gulf, chrome silver, deep Arabian night purple. Style: luxury Arab futurism."},

  {"id": 90080, "tags": ["poster"], "shortcode": "div_poster_08",
   "caption": "교토 일본 전통 여행 포스터",
   "prompt": "Exquisite Kyoto travel poster in traditional Nihonga woodblock print style. Elements: Fushimi Inari torii gates in vermillion, Arashiyama bamboo grove, maiko with elaborate kanzashi hair ornaments, sakura blossom reflections in Kinkakuji pond. 'KYOTO — 千年の都' typography in elegant Japanese calligraphy. Colors: deep vermillion, gold leaf, pine green, soft sakura pink, indigo. Style: Hokusai meets luxury Japanese publishing."},

  {"id": 90081, "tags": ["poster"], "shortcode": "div_poster_09",
   "caption": "베를린 독일 전위예술 포스터",
   "prompt": "Avant-garde Berlin culture poster in Bauhaus design style. Elements: Brandenburg Gate abstract geometry, Berlin Wall graffiti fragments, Ampelmann traffic man symbol, techno club underground, Berlin Bear (Bär). 'BERLIN — JUNG. WILD. FREI.' bold Bauhaus typography. Colors: Bauhaus primaries — pure red, blue, yellow on white with black — plus neon techno accents. Grid-based geometric Bauhaus layout. Style: pure Bauhaus 1920s meets Berlin techno."},

  {"id": 90082, "tags": ["poster"], "shortcode": "div_poster_10",
   "caption": "아테네 그리스 클래식 포스터",
   "prompt": "Timeless Athens travel poster in classic Greek illustration style. Elements: Parthenon on Acropolis golden hour silhouette, ancient Greek amphora illustration, olive branch wreath border, Aegean Sea waves in Greek key pattern, Evzone soldier. 'ΑΘΗΝΑ — ATHENS — BIRTHPLACE OF DEMOCRACY' typography. Colors: Aegean cobalt blue, Cycladic white, ancient terracotta, olive gold. Style: 1950s Olympic Games vintage poster aesthetic."},

  {"id": 90083, "tags": ["poster"], "shortcode": "div_poster_11",
   "caption": "뉴욕 힙합 문화 포스터",
   "prompt": "Bold New York City hip-hop culture celebration poster. Elements: Brooklyn Bridge, subway graffiti art style, breakdancer silhouette, boombox, 'I ♥ NY' reimagined. 'NEW YORK CITY — BORN TO BE WILD' in bold graffiti-influenced typography. Colors: subway car silver, graffiti rainbow brights, NYC taxi yellow, midnight black. Layer: overlapping magazine cut-out aesthetic. Style: Jean-Michel Basquiat energy meets modern graphic design."},

  {"id": 90084, "tags": ["poster"], "shortcode": "div_poster_12",
   "caption": "서울 한국 K-컬처 미래 포스터",
   "prompt": "Dynamic Seoul K-Culture future city poster. Elements: Gyeongbokgung palace juxtaposed with Gangnam glass towers, BTS billboard, K-beauty cosmetics, hanbok merged with streetwear, Han River drone view. 'SEOUL — 서울 — WHERE PAST MEETS FUTURE' dual-language typography. Colors: royal Korean red and blue (taeguk) with neon pink K-beauty and midnight blue. Style: neo-traditional Korean graphic design with K-pop energy."},

  # ═══════════════════════════════════════════════════════════
  # STICKER — 12 new: diverse cultural and gender-inclusive stickers
  # ═══════════════════════════════════════════════════════════
  {"id": 90085, "tags": ["sticker"], "shortcode": "div_sticker_01",
   "caption": "다양한 피부톤 하이파이브 스티커",
   "prompt": "Cute inclusive sticker sheet featuring 6 pairs of hands in all skin tones giving high-fives. Arranged in a rainbow pattern. Style: simple bold vector sticker illustration with thick black outline. Each pair has different skin tones — from pale ivory to deep ebony. Above: 'WE ARE ONE' in fun lettering. Colors: joyful rainbow spectrum with thick white border sticker cut. Background: white. Mood: inclusive, celebratory."},

  {"id": 90086, "tags": ["sticker"], "shortcode": "div_sticker_02",
   "caption": "글로벌 음식 스티커 팩",
   "prompt": "Adorable world food sticker pack with thick white die-cut borders. 12 mini food stickers: sushi, tacos, injera, croissant, dim sum, jollof rice, shawarma, ramen, naan, pierogi, arepas, bibimbap. Each food item has a cute face with happy expression. Style: LINE sticker quality, flat cute illustration with bold outlines. Colors: each food in its authentic vibrant color. Background: white sticker sheet layout."},

  {"id": 90087, "tags": ["sticker"], "shortcode": "div_sticker_03",
   "caption": "프라이드 무지개 표정 스티커",
   "prompt": "Vibrant Pride celebration sticker sheet. 8 round emoji-style stickers featuring diverse faces in rainbow expressions: laughing, heart-eyes, crying happy tears, proud fist, dancing, hugging, star-struck, celebrating. Each face has different skin tone and hair type. Some with pride flags on cheeks. Background: white sticker sheet with rainbow die-cut border. Style: iOS emoji meets Pride art, inclusive and joyful."},

  {"id": 90088, "tags": ["sticker"], "shortcode": "div_sticker_04",
   "caption": "세계 국기 하트 스티커",
   "prompt": "Charming world flags heart sticker collection. 16 country flags each reshaped into a heart: South Korea, USA, Japan, Brazil, Ghana, India, Mexico, France, Nigeria, Indonesia, Turkey, South Africa, Germany, Australia, Egypt, Argentina. All with thick white sticker borders, slightly rounded. Style: clean flat illustration. Arranged in a 4x4 grid on white background. Each heart flag has a tiny cute face expression. Mood: global love."},

  {"id": 90089, "tags": ["sticker"], "shortcode": "div_sticker_05",
   "caption": "남성 표정 이모티콘 스티커",
   "prompt": "Expressive male character sticker sheet. A charming young Black man character in 8 different emotional states: excited, embarrassed, thinking, crying, angry, laughing, shy, sleepy. Bold round sticker shape, thick black outline. Each emotion dramatically exaggerated in cute chibi style. Colors: warm, vibrant. Style: KakaoTalk meets LINE sticker male character. Background: white sticker sheet arranged in 2x4 grid."},

  {"id": 90090, "tags": ["sticker"], "shortcode": "div_sticker_06",
   "caption": "귀여운 할머니 할아버지 스티커",
   "prompt": "Adorable grandparents character sticker sheet. An Asian grandmother with silver bun and apron, and a Western grandfather with white mustache and suspenders — both in 6 cute poses each: cooking, napping, gardening, video calling, dancing, smiling. Chibi proportions, soft warm colors. Style: children's book illustration meets sticker design. Mood: intergenerational warmth and humor. Background: white sticker sheet."},

  {"id": 90091, "tags": ["sticker"], "shortcode": "div_sticker_07",
   "caption": "글로벌 직업 캐릭터 스티커",
   "prompt": "Diverse occupation character sticker pack. 8 chibi characters of different genders and ethnicities: Black female doctor, Asian male chef, Latina female engineer, Middle Eastern male teacher, White female astronaut, South Asian male artist, Indigenous female scientist, European male nurse. Each in their uniform, cute and proud. Style: flat vector sticker illustration. Colors: bright, celebratory. Promotes all genders in all professions."},

  {"id": 90092, "tags": ["sticker"], "shortcode": "div_sticker_08",
   "caption": "세계 전통 의상 캐릭터 스티커",
   "prompt": "Beautiful traditional costume character sticker sheet. 8 chibi characters each in traditional dress: Korean hanbok girl, Indian sari woman, African kente man, Japanese yukata boy, Mexican huipil girl, Moroccan djellaba figure, Scottish kilt man, Andean pollera woman. Each with a happy expression and a small cultural prop. Style: clean vector sticker illustration, cultural respect. Background: white sticker sheet."},

  {"id": 90093, "tags": ["sticker"], "shortcode": "div_sticker_09",
   "caption": "스포츠 남녀 챔피언 스티커",
   "prompt": "Champion sports sticker pack celebrating diverse athletes. 8 stickers: Black female sprinter mid-race, Asian male gymnast, Latina female footballer, Middle Eastern male swimmer, Indigenous female archer, European male weightlifter, South Asian male cricket player, mixed-race female basketball player. Each with dynamic pose and gold champion star burst. Style: bold sports illustration sticker. Colors: gold, silver, vibrant team colors."},

  {"id": 90094, "tags": ["sticker"], "shortcode": "div_sticker_10",
   "caption": "연애 다양성 커플 스티커",
   "prompt": "Sweet inclusive couple sticker pack showing diverse love. 6 sticker pairs: Asian heterosexual couple, Black same-sex female couple, interracial straight couple (South Asian man + European woman), same-sex male couple, non-binary couple, senior East Asian couple. All in the same cute chibi art style doing sweet activities: holding hands, sharing food, hugging, reading together. Style: warm, soft illustration sticker. Mood: love is universal."},

  {"id": 90095, "tags": ["sticker"], "shortcode": "div_sticker_11",
   "caption": "장애 인식 포용 스티커",
   "prompt": "Empowering disability inclusion sticker sheet. 8 chibi character stickers: cheerful wheelchair user, deaf person signing, blind person with white cane, prosthetic arm athlete, person with vitiligo, autistic child happily stimming, Down syndrome teen with thumbs up, person with hearing aid. All with warm smiles and proud expressions. Colors: bright, celebrating diversity. Style: inclusive illustration with thick sticker borders. Mood: visibility and pride."},

  {"id": 90096, "tags": ["sticker"], "shortcode": "div_sticker_12",
   "caption": "날씨와 자연 지구 문화 스티커",
   "prompt": "Global nature and weather sticker pack with cultural twist. 12 mini stickers: Japanese cherry blossom, Amazon rainforest, Sahara dunes, Arctic aurora, Indian monsoon, Caribbean hurricane, African savannah sunset, New Zealand glacier, Amazon river dolphin, Alpine snow, Korean autumn maple, Andean condor. Each with cute face expression on the natural element. Style: flat vector sticker. Colors: natural world palette. Mood: global nature appreciation."},

  # ═══════════════════════════════════════════════════════════
  # PHOTO — 12 new: diverse lifestyle photography
  # ═══════════════════════════════════════════════════════════
  {"id": 90097, "tags": ["photo"], "shortcode": "div_photo_01",
   "caption": "흑인 남성 스트리트 패션",
   "prompt": "Confident street style editorial photograph of a tall Black Nigerian-British man in his mid-20s, sharp angular jawline, short tapered fade. Wearing oversized cream Valentino logo tee layered under a tan camel overcoat, slim black trousers, white AF1 sneakers. Background: London Shoreditch brick street, golden sunset. Expression: composed, magnetic. Mood: Black male fashion editorial, Highsnobiety meets i-D magazine."},

  {"id": 90098, "tags": ["photo"], "shortcode": "div_photo_02",
   "caption": "라틴 가족 사진 따뜻한 일상",
   "prompt": "Warm, candid lifestyle photograph of a three-generation Mexican-American family at a Sunday carne asada barbecue. Grandfather (70s, cowboy hat, mustache), parents (40s), and three children (5-12) laughing around a table full of food. Background: backyard with string lights, colorful papel picado banners. Golden hour lighting. Expression: genuine laughter, love. Mood: family photojournalism, Getty Images editorial."},

  {"id": 90099, "tags": ["photo"], "shortcode": "div_photo_03",
   "caption": "인도 남성 요가 명상 사진",
   "prompt": "Serene lifestyle photograph of a fit South Indian man in his 30s practicing yoga at dawn. Warrior III pose on a hilltop above Mysore city, the ancient Mysore Palace visible in the misty valley below. Wearing simple white cotton yoga pants, bare-chested. Golden morning light catches his warm brown skin. Expression: total meditative peace. Mood: Yoga Journal editorial meets National Geographic."},

  {"id": 90100, "tags": ["photo"], "shortcode": "div_photo_04",
   "caption": "중동 청년 음악가 사진",
   "prompt": "Intimate documentary photograph of a young Iraqi man in his early 20s playing an Oud (Arabic lute) in a dimly lit Baghdad café. Soft lamplight illuminates his concentrated expression. He wears a casual white shirt, warm olive skin. Background: ornate wooden mashrabiya screen, tea glasses glowing amber on table. Other patrons softly blurred in background. Mood: National Geographic human story, cultural intimacy."},

  {"id": 90101, "tags": ["photo"], "shortcode": "div_photo_05",
   "caption": "북유럽 여성 자연 하이킹",
   "prompt": "Adventurous lifestyle photograph of a Norwegian woman in her 30s hiking in dramatic Trolltunga fjord landscape. Athletic build, blonde hair in a practical braid, sun-kissed rosy fair skin. Wearing quality technical hiking gear in teal and grey. Sitting on the iconic cliff edge rock with legs dangling over the fjord 700m below. Expression: pure exhilaration. Mood: REI adventure editorial meets Conde Nast Traveler."},

  {"id": 90102, "tags": ["photo"], "shortcode": "div_photo_06",
   "caption": "나이지리아 여성 직장인 사진",
   "prompt": "Powerful professional portrait of a Nigerian corporate executive woman in her 40s in Lagos. Commanding presence, natural two-strand twist hair, radiant deep brown skin. Wearing a bespoke Ankara print blazer over a crisp white silk blouse, pearl earrings. Background: modern glass office building in Victoria Island. Expression: decisive leadership. Mood: Forbes Africa, Black female excellence editorial."},

  {"id": 90103, "tags": ["photo"], "shortcode": "div_photo_07",
   "caption": "시니어 커플 여행 사진",
   "prompt": "Joyful travel photograph of a senior interracial couple in their late 60s exploring Rome together. Japanese woman and Italian man — both silver-haired, active, glowing with vitality. She photographs the Trevi Fountain; he laughs at something she said. She wears a floral scarf; he's in a cream linen jacket. Warm Italian midday sun. Mood: luxury mature travel editorial, AARP meets Conde Nast."},

  {"id": 90104, "tags": ["photo"], "shortcode": "div_photo_08",
   "caption": "케냐 소년 축구 스트리트 사진",
   "prompt": "Energetic documentary photograph of a group of Kenyan boys, ages 8-12, playing barefoot football on a red earth pitch in Kibera, Nairobi at sunset. Joyful, sweaty, completely absorbed in the game. Silhouetted against a dramatic African orange-red sky. The worn football is mid-kick. Background: corrugated iron rooflines of the neighborhood. Mood: National Geographic joy of childhood, pure documentary."},

  {"id": 90105, "tags": ["photo"], "shortcode": "div_photo_09",
   "caption": "동남아 시장 상인 사진",
   "prompt": "Vibrant photojournalistic photograph of a Vietnamese market vendor woman in her 50s in Hội An. Wearing traditional nón lá (conical hat), arranging a beautiful pyramid display of dragon fruit, rambutans, and lotus flowers. Her warm sun-bronzed face shows pride in her display. Background: ancient Hội An lantern-lit marketplace. Morning light cutting through the alley. Colors: stunning tropical fruit rainbow. Mood: National Geographic, human dignity."},

  {"id": 90106, "tags": ["photo"], "shortcode": "div_photo_10",
   "caption": "유럽 아버지와 딸 사진",
   "prompt": "Tender family moment photograph. A French single father in his mid-30s, warm olive skin, dark stubble, sitting cross-legged on a Parisian park floor helping his mixed-race daughter (4 years old, curly hair, enormous brown eyes) build a LEGO castle. Soft afternoon dappled park light. Background: Luxembourg Gardens, blurred. Expression: completely absorbed, loving. Mood: parenting editorial, Similac / Dove family warmth."},

  {"id": 90107, "tags": ["photo"], "shortcode": "div_photo_11",
   "caption": "중년 남성 아티스트 스튜디오",
   "prompt": "Intimate studio portrait of a Brazilian male painter in his 50s, salt-and-pepper beard, warm medium brown skin, paint-covered hands. Standing before a large abstract canvas in his São Paulo studio. He looks at the camera with quiet confidence. Wearing a splattered linen shirt. Natural north-light studio windows. Background: canvases stacked everywhere, paint tubes on shelves. Mood: artist profile editorial, New York Times Magazine."},

  {"id": 90108, "tags": ["photo"], "shortcode": "div_photo_12",
   "caption": "성별 포용적 커플 산책 사진",
   "prompt": "Natural lifestyle photograph of a gender-fluid couple walking hand-in-hand through autumn Kyoto. One person: tall, Korean, masculine-presenting in an oversized camel coat. Other person: petite, European, feminine-presenting with short pixie cut in a plaid blazer. Both mid-laugh, autumn maple leaves falling around them. Background: Philosopher's Path canal in peak autumn red. Lighting: golden afternoon. Mood: inclusive love story, Vogue living."},

  # ═══════════════════════════════════════════════════════════
  # INFOGRAPHIC — 12 new: diverse subjects
  # ═══════════════════════════════════════════════════════════
  {"id": 90109, "tags": ["infographic"], "shortcode": "div_info_01",
   "caption": "세계 언어 다양성 인포그래픽",
   "prompt": "Elegant infographic visualizing global language diversity. World map with bubble sizes showing native speaker counts for top 20 languages. Language families shown in color-coded tree diagram below. Key facts: '7,139 languages exist worldwide', 'Top 5 languages spoken by 40% of humanity'. Typography: clean sans-serif. Colors: warm earth tones — terracotta, sage, warm sand, deep navy. Style: National Geographic information design quality."},

  {"id": 90110, "tags": ["infographic"], "shortcode": "div_info_02",
   "caption": "글로벌 젠더 평등 데이터 인포그래픽",
   "prompt": "Impactful infographic on global gender equality progress. Data visualizations: progress bar chart for female representation in government by region, pay gap comparison circles, education access by gender globe, icons for milestones. Icons use diverse non-gendered figure designs. Colors: empowering purple, sky blue, warm coral. Clean modern layout with generous white space. Style: UN Women meets Economist data journalism."},

  {"id": 90111, "tags": ["infographic"], "shortcode": "div_info_03",
   "caption": "세계 커피 생산 국가 인포그래픽",
   "prompt": "Warm, rich infographic about global coffee production. Illustrated world map with top coffee producing countries highlighted. Coffee cherry to cup journey diagram. Fun facts about coffee culture per country. Icon illustrations: Brazilian fazenda, Ethiopian ceremony, Vietnamese ca phe, Italian espresso machine, Colombian picker. Colors: rich coffee browns, warm creams, forest green, cherry red. Style: Bon Appétit meets National Geographic beautiful data."},

  {"id": 90112, "tags": ["infographic"], "shortcode": "div_info_04",
   "caption": "기후 변화 글로벌 영향 인포그래픽",
   "prompt": "Urgent but beautiful climate change impact infographic. Globe divided into regions showing temperature change data with thermometer icons. Timeline of key climate events 1900-2024. Icons: polar bear, coral reef, glacier, drought, flood. CO2 rising chart. 'What You Can Do' action list. Colors: urgent red gradients to cool blues, hope-green for solutions. Style: scientific accuracy meets design excellence, IPCC report quality."},

  {"id": 90113, "tags": ["infographic"], "shortcode": "div_info_05",
   "caption": "세계 종교 다양성 인포그래픽",
   "prompt": "Respectful, balanced infographic on world religious diversity. Circular Voronoi diagram showing proportional adherent populations. Key facts about each major faith: Christianity, Islam, Hinduism, Buddhism, Judaism, Sikhism, indigenous traditions, non-religious. Sacred symbols illustrated with care. 'Shared Values Across Traditions' section showing commonalities. Colors: each faith in a distinct respectful palette. Style: Pew Research meets respectful design."},

  {"id": 90114, "tags": ["infographic"], "shortcode": "div_info_06",
   "caption": "AI 기술 발전 타임라인 인포그래픽",
   "prompt": "Sleek modern infographic of AI technology timeline. From Turing Test 1950 to GPT-4 2023 and beyond. Key milestones as floating nodes on a neural network visual path. Side panels: AI applications in healthcare, creative arts, science. Diverse human figures interacting with AI systems. Colors: deep midnight navy, electric blue, neon white, warm human gold. Style: Wired magazine meets MIT Technology Review premium design."},

  {"id": 90115, "tags": ["infographic"], "shortcode": "div_info_07",
   "caption": "전통 치유 방법 세계 비교 인포그래픽",
   "prompt": "Fascinating infographic comparing traditional healing practices worldwide. World map with illustrated icons: Chinese acupuncture meridians, Indian Ayurvedic doshas, Indigenous sweat lodge, African herbal medicine, Andean curandera, Amazonian plant medicine, Celtic herbalism, Korean haneuihak. Each with key principles. Colors: natural botanical palette — sage, bark brown, flower pink, sky blue. Style: educational and respectful ethnobotanical illustration."},

  {"id": 90116, "tags": ["infographic"], "shortcode": "div_info_08",
   "caption": "글로벌 음악 장르 맵 인포그래픽",
   "prompt": "Dynamic infographic mapping global music genres by origin. World map with illustrated instruments per region: West African djembe drum, Indian sitar, Brazilian berimbau, Scottish bagpipes, Japanese koto, Andean pan pipes, American guitar, Middle Eastern oud. Connecting lines showing genre cross-pollination. Music genre evolution tree. Colors: vibrant festival spectrum. Style: Rolling Stone meets Spotify data visualization. Fun and educational."},

  {"id": 90117, "tags": ["infographic"], "shortcode": "div_info_09",
   "caption": "세계 결혼 문화 비교 인포그래픽",
   "prompt": "Beautifully illustrated infographic comparing wedding traditions worldwide. 8 featured traditions: Korean hanbok ceremony, Indian Hindu mandap, Nigerian traditional engagement, Mexican Catholic fiesta, Jewish chuppah, Japanese Shinto san-san-kudo, West African kente ceremony, Scandinavian midsummer wedding. Each illustrated with loving care and cultural accuracy. Colors: celebration spectrum — gold, red, white, floral. Style: respectful cultural celebration."},

  {"id": 90118, "tags": ["infographic"], "shortcode": "div_info_10",
   "caption": "세계 수명 건강 데이터 인포그래픽",
   "prompt": "Clean public health infographic on global life expectancy and health factors. Bar chart ranking countries by life expectancy with flag icons. Factors contributing to longevity: diet (Blue Zones illustrated), healthcare access, social connection, purpose. Human figure icons for different body types, ages. Colors: fresh health-positive palette — mint green, sky blue, sunshine yellow. Style: WHO meets clean modern health editorial design."},

  {"id": 90119, "tags": ["infographic"], "shortcode": "div_info_11",
   "caption": "교육 격차 전세계 인포그래픽",
   "prompt": "Thoughtful infographic on global education access disparities. World choropleth map showing literacy rates by country. Illustrated comparison: school day in Finland vs Bangladesh vs USA vs Ghana. Girl's education access by region bar chart. Key facts: '258 million children out of school'. Call to action. Colors: education hope palette — sky blue, sunshine, warm orange, deep navy. Style: UNICEF design excellence meets data journalism."},

  {"id": 90120, "tags": ["infographic"], "shortcode": "div_info_12",
   "caption": "글로벌 SNS 사용 패턴 인포그래픽",
   "prompt": "Fresh digital infographic on global social media usage patterns by region. Bubble chart: platform size by region user count — TikTok in Asia, WhatsApp in South Asia/Latin America, Facebook in Africa, WeChat in China, Instagram globally. Cultural usage patterns: what's posted, hours per day, age demographics. Colors: each platform in its brand color family. Style: tech data journalism, Morning Consult meets The Verge design."},

  # ═══════════════════════════════════════════════════════════
  # DESIGN — 12 new: diverse global graphic design styles
  # ═══════════════════════════════════════════════════════════
  {"id": 90121, "tags": ["design"], "shortcode": "div_design_01",
   "caption": "아프리카 전통 문양 모던 디자인",
   "prompt": "Bold modern graphic design poster inspired by West African Adinkra symbols and Kente cloth geometric patterns. Large-scale repeating Adinkra symbols (Sankofa bird, Gye Nyame) arranged in a dynamic contemporary grid layout. Typography: 'UBUNTU — I AM BECAUSE WE ARE' in a modern sans-serif. Colors: authentic Kente palette — black, gold, deep green, crimson. Style: contemporary Afrocentric graphic design meeting Swiss grid typography."},

  {"id": 90122, "tags": ["design"], "shortcode": "div_design_02",
   "caption": "인도 만다라 현대 디자인",
   "prompt": "Exquisite Indian mandala-inspired modern design composition. An intricate geometric mandala built from traditional kolam/rangoli patterns, digitally refined with mathematical precision. Symmetrical eight-fold geometry with lotus, elephant, peacock motifs. Typography integrated within the mandala geometry. Colors: Rajasthani festival palette — deep fuchsia, saffron orange, peacock teal, pure white, gold. Style: Indian heritage meets Swiss modernism."},

  {"id": 90123, "tags": ["design"], "shortcode": "div_design_03",
   "caption": "일본 와비사비 미니멀 디자인",
   "prompt": "Serene Japanese wabi-sabi inspired minimal design composition. Single imperfect ceramic tea bowl rendered in detailed illustration, positioned off-center per Zen asymmetry principles. Dry ink brushstroke borders. Falling cherry blossom petals arranged in golden ratio spiral. Japanese kanji 不完全 (imperfection) in elegant Sosho calligraphic style. Colors: natural — aged clay, moss green, charcoal ink, paper cream. Style: pure Japanese aesthetics."},

  {"id": 90124, "tags": ["design"], "shortcode": "div_design_04",
   "caption": "러시아 구성주의 현대 포스터",
   "prompt": "Bold Russian Constructivist-style modern design poster. Dynamic diagonal composition with strong geometric shapes — triangles, circles, rectangles — in pure primary colors. Inspired by Rodchenko and El Lissitzky. Central graphic: a diverse fist raised with symbols of global unity. Typography: bold condensed geometric sans-serif in Cyrillic and Latin. Colors: pure Soviet Constructivist palette — red, black, white with minimal yellow accent. Pure graphic power."},

  {"id": 90125, "tags": ["design"], "shortcode": "div_design_05",
   "caption": "멕시코 오아하카 민속 디자인",
   "prompt": "Vibrant Mexican Oaxacan folk art-inspired design. An imaginary alebrijes fantastical creature — part jaguar, part eagle, part serpent — hand-illustrated with traditional Zapotec patterning. Every surface covered in intricate patterns of dots, flowers, geometric shapes. Colors: the full Oaxacan palette — electric pink, neon yellow, deep turquoise, hot orange, lime green. Style: traditional Oaxacan craftsmanship meets contemporary illustration."},

  {"id": 90126, "tags": ["design"], "shortcode": "div_design_06",
   "caption": "스칸디나비아 미드센추리 디자인",
   "prompt": "Classic Scandinavian mid-century modern design composition. Clean grid layout with organic Alvar Aalto-inspired furniture silhouettes illustrated in flat color. Marimekko-style large-scale botanical pattern in the background. Typography: elegant Scandinavian humanist typeface. Colors: Nordic nature palette — pine forest green, birch white, fjord blue, warm wood tan, berry red. Style: pure 1960s Danish design golden age, Finland meets Sweden."},

  {"id": 90127, "tags": ["design"], "shortcode": "div_design_07",
   "caption": "이슬람 기하학 패턴 현대 디자인",
   "prompt": "Breathtakingly intricate Islamic geometric pattern design. Complex 12-fold star pattern (Girih tiles) constructed with mathematical perfection, inspired by the Alhambra Palace tile work. The pattern radiates from a central star through infinite recursion. Colors: Andalusian palace palette — lapis lazuli blue, terracotta, gold, emerald, white. Style: traditional Islamic geometric art meets contemporary luxury design. Sacred geometry."},

  {"id": 90128, "tags": ["design"], "shortcode": "div_design_08",
   "caption": "중국 수묵 캘리그라피 디자인",
   "prompt": "Masterful Chinese ink wash calligraphy design composition. Large-scale Chinese character 和 (harmony/peace) in bold Kaishu calligraphy style dominates the composition, executed with simulated ink brush texture. Surrounding negative space features subtle ink wash mountain mist forms. Red official seal (chop) in the corner. Colors: pure monochromatic ink black to grey with single vermillion red chop seal. Style: Song Dynasty scholar aesthetics meet contemporary minimal design."},

  {"id": 90129, "tags": ["design"], "shortcode": "div_design_09",
   "caption": "브라질 구체주의 예술 디자인",
   "prompt": "Vibrant Brazilian Concretist art-inspired graphic design. Inspired by Lygia Clark and Hélio Oiticica. Dynamic geometric composition with interlocking colored planes that create optical depth and movement. Pure geometric shapes — no representational elements. Colors: Tropicália palette — electric yellow, tropical green, warm red, sky blue, brilliant white. Bold graphic energy with mathematical precision. Style: 1960s São Paulo Concrete Art movement."},

  {"id": 90130, "tags": ["design"], "shortcode": "div_design_10",
   "caption": "한국 단청 전통 문양 디자인",
   "prompt": "Contemporary Korean Dancheong-inspired design composition. Traditional Korean palace wood painting patterns (dancheong) digitally reinterpreted in a modern grid layout. Five traditional colors (obangsaek: blue, red, yellow, white, black) arranged in geometric Tanchukum and Geumdancheong pattern systems. Typography: elegant Hangul and English typeset in harmony. Style: Korean national cultural heritage meets K-contemporary graphic design excellence."},

  {"id": 90131, "tags": ["design"], "shortcode": "div_design_11",
   "caption": "아르데코 다문화 럭셔리 디자인",
   "prompt": "Glamorous Art Deco design composition celebrating multicultural luxury. Central medallion featuring stylized faces from multiple ethnicities — Egyptian, East Asian, European, African — all integrated symmetrically in pure Deco graphic style. Gold sunburst rays, Egyptian lotus column details, geometric jewel accents. Colors: 1920s Deco palette — gold, jet black, cream ivory, deep teal, sunburst orange. Style: Chrysler Building meets Jazz Age global cosmopolitan vision."},

  {"id": 90132, "tags": ["design"], "shortcode": "div_design_12",
   "caption": "원주민 예술 현대 캔버스 디자인",
   "prompt": "Respectful contemporary reinterpretation of Australian Aboriginal dot painting in a modern design context. Traditional X-ray art style animals (kangaroo, emu, serpent, echidna) built from intricate dot patterns. Colors: traditional ochre, white, red earth, deep black — authentic natural pigment palette. Geometric songline path connecting the animals. Style: contemporary Indigenous Australian art collaboration, dignified and authentic cultural expression. Medium: canvas texture background."},

  # ═══════════════════════════════════════════════════════════
  # OTHER — 12 new: miscellaneous diverse global content
  # ═══════════════════════════════════════════════════════════
  {"id": 90133, "tags": ["other"], "shortcode": "div_other_01",
   "caption": "세계 무술 액션 사진",
   "prompt": "Dynamic martial arts action photograph composite. Four martial artists mid-technique in a 2x2 grid: Brazilian Capoeira practitioner mid-ginga kick (Afro-Brazilian man), Japanese Kendo master in full armor mid-strike (Japanese woman), Chinese Wushu performer mid-aerial (Chinese man), Indian Kalaripayattu warrior mid-leap (South Indian teen). Each has perfect explosive form. Background: atmospheric training environments. Style: Sports Illustrated action meets National Geographic."},

  {"id": 90134, "tags": ["other"], "shortcode": "div_other_02",
   "caption": "전통 음악 연주자 콜라주",
   "prompt": "Rich documentary-style collage of traditional musicians from around the world. Four images in a 2x2 grid: elderly West African griot playing kora (Senegalese man), Flamenco guitarist passionate performance (Spanish woman), Indian classical musician playing sarod (elderly South Indian man), Celtic fiddler at Irish session (young Irish woman). Each photo has depth and cultural authenticity. Warm editorial documentary style. Mood: UNESCO world heritage of music."},

  {"id": 90135, "tags": ["other"], "shortcode": "div_other_03",
   "caption": "세계 어린이 놀이 사진",
   "prompt": "Joyful photojournalistic composite of children playing worldwide. A 2x2 grid: Kenyan children playing soccer in a dusty field (golden hour), Japanese children in school uniforms playing in a park (cherry blossom season), Brazilian favela children splashing in a water fountain (hot day), Norwegian children building a massive snowman (winter). All pure unscripted joy. Style: National Geographic Children's Edition, UNICEF annual report dignity and joy."},

  {"id": 90136, "tags": ["other"], "shortcode": "div_other_04",
   "caption": "전통 주거 공간 세계 비교",
   "prompt": "Architectural documentary editorial comparing traditional homes worldwide. A 2x2 grid: Mongolian yurt interior (warm felt, painted wood furniture), Moroccan riad courtyard (tilework, fountain), Japanese machiya townhouse (tatami, shoji screens), West African adobe compound (terracotta, geometric patterns). Each image lit perfectly showing cultural design wisdom. Colors: each space in its authentic material palette. Mood: Architectural Digest cultural homes series."},

  {"id": 90137, "tags": ["other"], "shortcode": "div_other_05",
   "caption": "세계 축제 에너지 모음",
   "prompt": "Explosive documentary composite of global festivals at their peak moment. 2x2 grid: Indian Holi (color powder explosion, diverse participants laughing), Brazilian Carnival (elaborate feathered samba performers), South Korean Boryeong Mud Festival (muddy laughing crowd), Rio de Janeiro NYE fireworks over Copacabana beach (massive crowd). Each image at absolute peak energy. Style: Getty Images editorial best, pure human joy documentation."},

  {"id": 90138, "tags": ["other"], "shortcode": "div_other_06",
   "caption": "전세계 출퇴근 교통 사진",
   "prompt": "Fascinating documentary composite of global commuting. 2x2 grid: Mumbai morning local train (dangerously packed, hands on bars), Amsterdam bicycle rush hour (thousands of bikes), Mexico City Metro (colorful crowded underground), Seoul subway (quiet, everyone on phone). Each captures the human energy of urban life. Style: documentary photography, Martin Parr meets National Geographic urban life series."},

  {"id": 90139, "tags": ["other"], "shortcode": "div_other_07",
   "caption": "전통 결혼식 의상 세계 비교",
   "prompt": "Stunning editorial composite of wedding attire from around the world. 2x2 grid: Indian bride in full Kanjeevaram silk sari with gold Jadau jewelry (Tamil Nadu), Nigerian bride in vibrant aso-oke gele headwrap (Lagos), Japanese bride in Shiromuku pure white uchikake kimono (Kyoto), Maasai bride in elaborate beaded wedding jewelry (Kenya). All dignified, beautiful, authentic. Mood: global wedding magazine editorial excellence."},

  {"id": 90140, "tags": ["other"], "shortcode": "div_other_08",
   "caption": "세계 장인 기술 다큐 사진",
   "prompt": "Intimate documentary composite of master craftspeople at work. 2x2 grid: Japanese Nishijin loom weaver's hands on silk threads (Kyoto), Moroccan leatherworker in Fez tannery (terracotta vats), Colombian Wayuu artisan weaving a mochila bag (La Guajira desert), Indian Varanasi Banarasi silk weaver at handloom (hands and threads). Extreme close-up detail shots. Colors: each craft's material palette. Mood: UNESCO Master of Intangible Heritage."},

  {"id": 90141, "tags": ["other"], "shortcode": "div_other_09",
   "caption": "글로벌 스트리트 아트 벽화",
   "prompt": "Vivid street art documentary composite from global cities. 2x2 grid: São Paulo Vila Madalena beco do batman murals (abstract colorful), Berlin East Side Gallery (political historical murals), Los Angeles Arts District Chicano murals (cultura celebration), Johannesburg Maboneng murals (Afrofuturist themes). Artists photographed mid-creation in scale with their works. Style: street photography documentary, Los Angeles Times Arts meets Bloomberg Pursuits."},

  {"id": 90142, "tags": ["other"], "shortcode": "div_other_10",
   "caption": "세계 노인 지혜 포트레이트 시리즈",
   "prompt": "Powerful portrait composite of elders holding wisdom worldwide. 2x2 grid: 90-year-old Japanese ikigai practitioner (Okinawa, still working in field), 85-year-old Nigerian griot storyteller (hand-carved staff), 80-year-old Tibetan Buddhist nun (Dharamsala monastery), 75-year-old Indigenous Amazonian healer (jungle backdrop). All face the camera with complete dignity and presence. Style: Humans of New York depth meets National Geographic dignity."},

  {"id": 90143, "tags": ["other"], "shortcode": "div_other_11",
   "caption": "미래 도시 생활 다문화 비전",
   "prompt": "Optimistic futuristic illustration of a diverse multicultural mega-city in 2080. Aerial view of a sustainable city with: rooftop vertical farms, solar panel arrays, community water features. Streets filled with people of every ethnicity and background living together — walking, cycling, conversing. Architecture blending futuristic design with cultural heritage elements from multiple civilizations. Colors: hopeful green and blue futurism with warm human tones. Mood: solarpunk utopia."},

  {"id": 90144, "tags": ["other"], "shortcode": "div_other_12",
   "caption": "세계 스포츠 영웅들 모자이크",
   "prompt": "Inspiring mosaic portrait of global sporting legends from diverse backgrounds, genders, and disciplines. Arranged as a large mosaic: Serena Williams (tennis), Pelé (football), Yuna Kim (figure skating), Usain Bolt (sprinting), Simone Biles (gymnastics), Naomi Osaka (tennis), Lionel Messi (football), Novak Djokovic (tennis), Marta (football), Neeraj Chopra (javelin). Rendered in bold graphic illustration style. Colors: gold medal glory, diverse national flag accents. Style: Olympic Games celebration art."},
]

# ─── Load and inject ──────────────────────────────────────────────────────────
with open(GALLERY, "r", encoding="utf-8") as f:
    gallery = json.load(f)

existing_ids = {p.get("id") for p in gallery.get("posts", [])}

added = 0
for post in NEW_POSTS:
    if post["id"] not in existing_ids:
        gallery["posts"].append(post)
        existing_ids.add(post["id"])
        added += 1

print(f"Added {added} new diverse posts. Total posts: {len(gallery['posts'])}")

with open(GALLERY, "w", encoding="utf-8") as f:
    json.dump(gallery, f, indent=2, ensure_ascii=False)

print("gallery-data.json updated successfully.")
