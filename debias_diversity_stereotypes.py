import json
import os

WORK_DIR = r"C:\Users\sunwo\.gemini\antigravity-ide\scratch\avatar_preset_maker"
GALLERY_DATA = os.path.join(WORK_DIR, "gallery-data.json")
STATUS_FILE = os.path.join(WORK_DIR, "thumbnail_generation_status.json")

# 전방위적 유색인종 및 문화 교차 매핑 정의 (고정관념 완벽 해체)
DEBIAS_MAP = {
    # 90001: 중동 남성 -> 다문화 믹스
    90001: {
        "caption": "다문화 중동계 남성 에디토리얼 포트레이트",
        "prompt": "Cinematic editorial portrait of a distinguished Middle Eastern man of mixed heritage in his mid-30s, sharp jawline, thick well-groomed beard, warm hazel eyes. Wearing a tailored charcoal wool suit with an open collar cream shirt, no tie. Background: warm terracotta studio wall with side rim lighting. Expression: calm, confident, piercing gaze. Skin: warm beige tone, visible texture. Mood: Vogue Men editorial, high-contrast, masculine elegance."
    },
    # 90002: 서아프리카 전통 복식 -> 동아시아계 남성 Kente 복식 착용
    90002: {
        "caption": "서아프리카 전통 복식의 동아시아계 남성 포트레이트",
        "prompt": "Majestic full-body editorial portrait of a tall, broad-shouldered East Asian man of mixed heritage in his 40s. Wearing an elaborate West African Kente cloth boubou in vibrant royal blue, gold, and crimson geometric patterns. Elaborate beaded necklace and wrist cuffs. Expression: regal, serene, direct gaze. Background: clean ivory studio. Lighting: bright even studio with warm golden rim. Skin: warm light-bronze, luminous. Mood: renowned documentary publication meets high fashion."
    },
    # 90003: 북유럽 남성 -> 아시아계 스칸디나비아인 믹스
    90003: {
        "caption": "아시아계 북유럽 남성 자연광 캐주얼",
        "prompt": "Relaxed lifestyle portrait of a Nordic Scandinavian man of East Asian descent in his late 20s, stylish dark textured hair, expressive dark eyes, warm light-caramel skin. Wearing an oversized oatmeal linen shirt, sleeves rolled, light denim. Sitting near a floor-to-ceiling window, soft diffused natural daylight. Expression: easy smile, warm and approachable. Background: minimalist Scandinavian interior, birch wood tones. Mood: Copenhagen street style, effortlessly cool."
    },
    # 90004: 라틴아메리카 여성 -> 아프로-라티나 믹스
    90004: {
        "caption": "아프로-라틴계 여성 비비드 패션",
        "prompt": "Bold editorial portrait of an Afro-Latina Colombian woman in her late 20s, voluminous curly dark coily hair, radiant deep bronze skin, expressive dark eyes with bold cat-eye liner. Wearing a vibrant cobalt-blue off-shoulder ruffled dress. Background: painted mural wall of tropical flowers. Expression: joyful, full laugh, showing teeth. Jewelry: large gold hoop earrings, layered gold chains. Mood: Cartagena street fashion meets editorial."
    },
    # 90005: 남아시아 여성 -> 혼혈 믹스
    90005: {
        "caption": "혼혈 남아시아계 여성 현대 포트레이트",
        "prompt": "Sophisticated close-up editorial portrait of a South Indian woman of mixed South Asian and European heritage in her early 30s, lustrous wavy dark brown hair worn in a loose modern updo. Light golden-brown skin, kohl-lined hazel eyes. Wearing a contemporary silk blouse in deep teal. Background: soft blurred botanical garden. Expression: thoughtful, self-assured. Jewelry: temple-style gold earrings. Mood: modern South Asian luxury editorial."
    },
    # 90007: 동아시아 중년 남성 -> 유라시안 비즈니스 리더
    90007: {
        "caption": "유라시안 중년 남성 사업가 포트레이트",
        "prompt": "Authoritative executive portrait of a Chinese-French businessman of mixed Eurasian heritage in his early 50s, silver-streaked dark hair neatly parted, strong prominent features, slight confident smile. Wearing a precisely tailored dark navy double-breasted blazer over white spread-collar shirt. Background: cool charcoal seamless. Lighting: Rembrandt studio, one strong key light. Expression: composed, trustworthy leadership aura. Mood: Forbes Asia cover shoot."
    },
    # 90008: 유럽 시니어 여성 -> 북아프리카계 프랑스인 믹스
    90008: {
        "caption": "북아프리카계 유럽 시니어 여성 포트레이트",
        "prompt": "Elegant portrait of a French woman of North African descent in her late 60s, silver bob haircut with a subtle wave, warm dark brown eyes, fine laugh lines, radiant olive skin tone. Wearing a cashmere turtleneck in soft ecru and a single strand of pearls. Background: warm Parisian apartment, bookshelves. Lighting: soft window light. Expression: knowing smile, sophisticated serenity. Mood: Vogue Paris silver generation editorial."
    },
    # 90011: 중동 여성 -> 다문화 독일-모로코 믹스
    90011: {
        "caption": "다문화 독일-모로코계 여성 현대적 히잡 패션",
        "prompt": "Contemporary fashion portrait of a Moroccan-German woman of diverse heritage in her early 30s, wearing a modern styled hijab in dusty rose silk, perfectly draped. Radiant warm light-bronze skin, deep green-hazel eyes with precise liner. Wearing a matching rose-toned blazer, minimalist gold jewelry. Background: architectural white Moroccan riad courtyard. Expression: self-assured elegance. Mood: modern global Muslim fashion editorial."
    },
    # 90012: 캐나다 원주민 여성 -> 다문화 믹스
    90012: {
        "caption": "다문화 캐나다 원주민 여성 문화 포트레이트",
        "prompt": "Dignified contemporary portrait of a First Nations Canadian woman of mixed indigenous and African descent in her 40s, textured curly dark hair styled beautifully. Rich warm deep-bronze skin, strong cheekbones, expressive brown eyes. Wearing a modern wool blanket coat with traditional geometric beaded detailing. Background: expansive mountain lake landscape. Lighting: golden hour. Expression: proud, grounded. Mood: National Geographic dignity meets modern indigenous fashion."
    },
    # 90015: 일본 할머니 -> 아프리카계 시니어 여성이 기모노를 입은 모습
    90015: {
        "caption": "일본 전통 의상을 입은 아프리카계 시니어 여성 일러스트",
        "prompt": "Heartwarming hand-painted style illustration of a warm elderly Black grandmother of African descent in her 80s, silver textured bun, rosy cheeks, tiny frame, wearing a traditional indigo kasuri kimono. She kneels in a lush Japanese garden tending to bonsai with small pruning scissors. A tabby cat sleeps on a stone nearby. Style: Studio nostalgic hand-painted anime style watercolor warmth. Mood: quiet, dignified aging, multicultural connection."
    },
    # 90016: 아프리카 전통 문양 -> 동아시아계 소녀가 Kente 복식 세부 디테일을 착용한 모습
    90016: {
        "caption": "아프리카 전통 문양 복식의 동아시아계 소녀 일러스트",
        "prompt": "Bold, graphic illustration of a confident young East Asian girl, approximately 10, with dark textured hair adorned with colorful cowrie shells. Wearing a modern outfit with Kente cloth pattern details. She holds a glowing magical drum. Background: stylized Savannah at sunset with geometric Adinkra pattern borders. Style: Afrofuturism meets children's illustration. Colors: terracotta, gold, deep violet, warm amber."
    },
    # 90017: 수묵화 무사 -> 흑인 사무라이 무사 수묵화
    90017: {
        "caption": "수묵화 스타일 흑인 사무라이 전사 일러스트",
        "prompt": "Expressive East Asian ink wash (sumi-e) style illustration of a lone Black samurai warrior of African descent standing still on a misty mountain peak at dawn. Male figure, powerful silhouette in layered haori armor, one hand on katana handle. Background: sweeping brushstroke mountains, pine trees, rising mist. Colors: monochromatic black ink gradients with a single accent of crimson on his sash. Mood: contemplative, powerful restraint."
    },
    # 90019: 북유럽 신화 Freya 여신 -> 남아시아계 파워풀 여신
    90019: {
        "caption": "남아시아계 북유럽 신화 여신 일러스트",
        "prompt": "Epic Norse mythology illustration of Freya, the goddess of love and war, represented as a powerful South Asian woman with flowing dark wavy hair braided with ravens feathers. Rich golden-bronze skin, fierce dark eyes. Wearing ornate gold-plated armor over fur-trimmed battle dress. Holding a glowing runic spear, a golden necklace Brisingamen glowing at her throat. Background: Asgard rainbow bridge at twilight. Style: fantasy epic illustration, painterly, dramatic lighting."
    },
    # 90021: 인도 신화 영웅 Arjuna -> 동아시아계 남성 영웅
    90021: {
        "caption": "동아시아계 인도 신화 영웅 일러스트",
        "prompt": "Dynamic mythological illustration of Arjuna from the Mahabharata represented as an East Asian warrior man, warm golden skin, decorated with traditional markings, fierce focused eyes. Kneeling drawing a divine golden bow (Gandiva), arrow charged with lightning. Background: vast Kurukshetra battlefield at golden hour with lotus patterns framing the scene. Style: detailed painterly illustration with intricate Indian motif borders. Mood: epic, sacred."
    },
    # 90023: 러시아 발레 -> 흑인 남성 발레리노
    90023: {
        "caption": "흑인 남성 발레리노 예술 일러스트",
        "prompt": "Ethereal illustration of a male ballet dancer mid-leap on a Moscow stage, represented as a tall, muscular Black man of African descent, intense focus. Wearing white and gold theatrical costume, arms extended overhead perfectly. Stage lights create dramatic god-rays. Background: ornate world-class theatrical stage Theatre interior with velvet red curtains. Style: romantic realism illustration with delicate watercolor brushwork. Mood: transcendent artistry, masculine grace."
    },
    # 90028: 남성 스킨케어 -> 아프리카계 스칸디나비아 남성 모델
    90028: {
        "caption": "북유럽 흑인 남성 스킨케어 모델 광고",
        "prompt": "Clean, modern men's skincare advertisement featuring a black Scandinavian man in his late 20s, glowing smooth dark skin, short shaved hair, strong features. Wearing a crisp white tee, holding a minimal skincare serum in both hands, examining it with curious interest. Background: pure white seamless. Lighting: soft diffused front light. Expression: thoughtful consideration, approachable. Mood: premium men's skincare editorial, Shiseido Men aesthetic."
    },
    # 90031: 인도 아유르베다 -> 라틴계/동아시아계 여성
    90031: {
        "caption": "라틴계 여성 인도 아유르베다 제품 광고",
        "prompt": "Luxury Ayurvedic beauty product advertisement featuring a Latina woman in her 30s, traditional jasmine flowers in her long dark wavy hair, radiant light-bronze skin. She pours a golden oil from an ornate terracotta vessel onto her palm. Background: lush Indian botanical garden with marigolds. Lighting: warm golden sunrise. Expression: serene, meditative. Props: turmeric, rose petals, neem leaves surrounding her. Mood: premium Ayurvedic luxury brand meets editorial luxury."
    },
    # 90049: 아프리카 퓨처리즘 전사 -> 중동계 여성
    90049: {
        "caption": "중동계 아프리카 퓨처리즘 전사 캐릭터",
        "prompt": "Afrofuturist warrior character design featuring a Middle Eastern woman in her 30s, shaved head with geometric gold scalp tattoos, piercing hazel eyes, warm beige skin tone. Wearing bio-mechanical armor crafted from futuristic materials merged with traditional Yoruba bronze work and beading. She holds a glowing energy spear. Background: neon-lit Lagos skyline 2187. Style: Black Panther meets Ghost in the Shell. Colors: rich copper, deep violet, electric gold."
    },
    # 90050: 인도 신화 마법사 Brahmin -> 라틴계 시니어 마법사
    90050: {
        "caption": "라틴계 시니어 인도 신화 마법사 캐릭터",
        "prompt": "Epic Indian mythology-inspired male mage character. A commanding Latino senior sage in his 60s, long white flowing beard and hair, wise deep-set eyes, warm golden-brown skin with sacred ash markings. Wearing deep saffron and crimson robes, multiple rudraksha bead strings. Hands raised channeling blue divine flames. Background: ancient Varanasi ghats at dawn with Ganges mist. Style: mythology painterly epic. Colors: gold, crimson, sapphire."
    },
    # 90051: 바이킹 남성 전사 -> 아시아계 남성 바이킹 전사
    90051: {
        "caption": "아시아계 남성 바이킹 전사 캐릭터",
        "prompt": "Imposing Viking warrior character design featuring an East Asian man in his late 30s, thick dark braided beard, fierce dark eyes under a heavy brow, warm light-bronze skin. Battle-worn chainmail under a fur-trimmed cloak. Carrying a double-headed axe with runic engravings glowing faintly. Background: dramatic Norwegian fjord coastline with longships in the mist. Style: epic fantasy painterly. Colors: steel grey, deep crimson, forest green, Norse gold."
    },
    # 90053: 중동 모래 마법사 -> 아프리카계 흑인 여성 마법사
    90053: {
        "caption": "흑인 여성 중동 모래 마법사 캐릭터",
        "prompt": "Mystical sand mage character design featuring a Black woman of African descent in her mid-20s, flowing dark curly hair partially veiled in translucent desert silk, intense kohl-lined golden-brown eyes, rich deep-espresso skin tone. Commanding a vortex of swirling golden sand particles around her hands. Wearing ornate desert warrior robes in deep teal and copper, multiple arm cuffs, ankle bells. Background: vast dune sea under a twin-moon sky. Style: One Thousand and One Nights reimagined as fantasy RPG. Colors: gold, teal, deep amber."
    },
    # 90055: 일본 사무라이 여성 -> 라틴계 여성 사무라이
    90055: {
        "caption": "라틴계 여성 사무라이 캐릭터",
        "prompt": "Fierce female samurai character (kunoichi) design featuring a Latina woman in her late 20s, jet black hair in a warrior's bun with loose strands, intense dark eyes with fierce determination, glowing bronze skin. Wearing partial O-yoroi samurai armor over a crimson hakama, cherry blossom embroidery on sash. Mid-draw sword pose, cherry blossom petals swirling around her blade. Background: burning castle at night. Style: action fantasy anime visual style meets historical cinematic samurai game aesthetic artistic style."
    },
    # 90056: 러시아 빙설 마법사 -> 남아시아계 여성 빙설 마법사
    90056: {
        "caption": "남아시아계 여성 러시아 빙설 마법사 캐릭터",
        "prompt": "Ethereal ice magic character design featuring a South Asian woman in her 30s, long silver-white hair with ice crystal extensions, radiant golden-tan skin tone, luminous frost-blue eyes. She floats above a magical ice fantasy story tundra, commanding ice pillars and blizzard spirals. Wearing an elaborate frost-crystal gown that flows into ice formations. Background: Aurora Borealis lit Siberian winter. Style: magical ice fantasy story meets dark fantasy monster hunter world fantasy. Colors: ice blue, silver, midnight purple."
    },
    # 90133: 세계 무술 -> 교차 인종 수련생들
    90133: {
        "caption": "세계 무술 액션 사진",
        "prompt": "Dynamic martial arts action photograph composite. Four martial artists mid-technique in a 2x2 grid: Brazilian Capoeira practitioner mid-ginga kick (East Asian man), Japanese Kendo master in full armor (Black woman), Indian Kalaripayattu fighter leaping (Nordic Scandinavian man), Scottish Highlander broadsword combatant (Middle Eastern man). Caught in sharp focus with dramatic speed lines. Lighting: intense contrast. Mood: peak athletic discipline."
    },
    # 90134: 전통 음악 -> 교차 인종 연주자들
    90134: {
        "caption": "전통 음악 연주자 콜라주",
        "prompt": "Rich documentary-style collage of traditional musicians from around the world. Four images in a 2x2 grid: elderly West African griot playing kora (East Asian man), Flamenco guitarist passionate performer (Black man), Indian sitar player serene (Latina woman), Japanese shakuhachi player (European man). Focus on hands and instruments, expressive faces. Lighting: warm, intimate stage glow. Mood: universal language of music."
    },
    # 90139: 전통 결혼식 의상 -> 교차 인종 신부들
    90139: {
        "caption": "전통 결혼식 의상 세계 비교",
        "prompt": "Stunning editorial composite of wedding attire from around the world. 2x2 grid: Indian bride in full Kanjeevaram silk sari (Black woman), Nigerian bride in vibrant aso-oke gele (East Asian woman), Japanese bride in white shiromuku kimono (Latina woman), Swedish bride in traditional bridal crown (Middle Eastern woman). Rich fabric textures, metallic threads. Backgrounds: culturally symbolic interiors. Mood: global celebration."
    },
    # 90142: 세계 노인 지혜 -> 교차 인종 시니어들
    90142: {
        "caption": "세계 노인 지혜 포트레이트 시리즈",
        "prompt": "Powerful portrait composite of elders holding wisdom worldwide. 2x2 grid: 90-year-old Japanese ikigai practitioner in Okinawa (Black grandmother), 85-year-old Nigerian griot storyteller (East Asian grandfather), 80-year-old Peruvian weaver (Middle Eastern grandmother), 75-year-old Icelandic fisherman (Latino grandfather). Deeply weathered skin showing lines of lived experience, warm eyes. Mood: universal dignity of aging."
    }
}

def main():
    if not os.path.exists(GALLERY_DATA):
        print("Error: gallery-data.json not found")
        return

    with open(GALLERY_DATA, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts = data.get("posts", [])
    print(f"Loaded {len(posts)} posts for stereotype debiasing.")

    modified_count = 0
    modified_ids = []

    for p in posts:
        pid = p.get("id")
        if pid in DEBIAS_MAP:
            p["caption"] = DEBIAS_MAP[pid]["caption"]
            p["prompt"] = DEBIAS_MAP[pid]["prompt"]
            modified_count += 1
            modified_ids.append(pid)

    print(f"Successfully debiased {modified_count} posts in memory.")

    # Save to gallery-data.json
    with open(GALLERY_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("gallery-data.json updated successfully.")

    # 144개 다양성 포스트 전체에 대해 썸네일 재생성을 보장하기 위해 status 파일에서 이들의 ID를 삭제
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status = json.load(f)
        
        removed_count = 0
        for i in range(90001, 90145):
            spid = str(i)
            if spid in status:
                status.pop(spid)
                removed_count += 1
        
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
        print(f"Cleared {removed_count} diverse posts statuses in {STATUS_FILE} to force fresh generation.")
    else:
        print("No status file found.")

if __name__ == "__main__":
    main()
