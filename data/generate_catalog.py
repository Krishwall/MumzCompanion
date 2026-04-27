import json
import random

stage_buckets = [
    "early_pregnancy", "mid_pregnancy", "late_pregnancy",
    "newborn", "infant", "older_infant"
]

templates = {
    "early_pregnancy": [
        ("Prenatal Vitamins", "فيتامينات ما قبل الولادة", ["prenatal", "vitamins", "health"], "Essential vitamins for early pregnancy.", "فيتامينات أساسية في بداية الحمل."),
        ("Morning Sickness Tea", "شاي غثيان الصباح", ["morning_sickness", "tea", "relief"], "Herbal tea to soothe morning sickness.", "شاي عشبي لتهدئة غثيان الصباح."),
        ("Pregnancy Journal", "مذكرات الحمل", ["journal", "memory", "pregnancy"], "Track your pregnancy journey.", "تتبعي رحلة حملك."),
        ("Stretch Mark Oil", "زيت لعلامات التمدد", ["skincare", "stretch_marks", "oil"], "Nourishing oil for stretching skin.", "زيت مغذي للبشرة المتمددة."),
        ("Nausea Wristbands", "أساور الغثيان", ["nausea", "relief", "travel"], "Acupressure bands for nausea relief.", "أساور العلاج بالضغط لتخفيف الغثيان.")
    ],
    "mid_pregnancy": [
        ("Maternity Leggings", "سراويل حمل", ["maternity", "clothing", "comfort"], "Comfortable leggings for growing bump.", "سراويل مريحة للبطن المتنامي."),
        ("Pregnancy Pillow", "وسادة الحمل", ["sleep", "pillow", "comfort", "back_pain"], "U-shaped pillow for better sleep.", "وسادة على شكل حرف U لنوم أفضل."),
        ("Belly Support Band", "حزام دعم البطن", ["support", "band", "back_pain"], "Provides support for your lower back.", "يوفر الدعم لأسفل الظهر."),
        ("Doppler Fetal Monitor", "جهاز دوبلر لمراقبة الجنين", ["monitor", "health", "doppler"], "Listen to your baby's heartbeat.", "استمعي لنبضات قلب طفلك."),
        ("Maternity Dress", "فستان حمل", ["maternity", "clothing", "dress"], "Elegant and comfortable maternity dress.", "فستان حمل أنيق ومريح.")
    ],
    "late_pregnancy": [
        ("Hospital Bag Organizer", "منظم حقيبة المستشفى", ["hospital", "organizer", "preparation"], "Get ready for the big day.", "استعدي لليوم الكبير."),
        ("Nursing Bras 3-Pack", "حمالات صدر للرضاعة", ["nursing", "clothing", "bra"], "Comfortable bras for nursing.", "حمالات صدر مريحة للرضاعة."),
        ("Perineal Spray", "بخاخ العجان", ["postpartum", "recovery", "spray"], "Cooling spray for postpartum recovery.", "بخاخ مبرد للتعافي بعد الولادة."),
        ("Birthing Ball", "كرة الولادة", ["birth", "exercise", "ball"], "Helps with labor positioning.", "يساعد في وضعيات المخاض."),
        ("Maternity Pads", "فوط صحية للولادة", ["postpartum", "hygiene", "pads"], "Extra absorbent for postpartum use.", "فائقة الامتصاص للاستخدام بعد الولادة.")
    ],
    "newborn": [
        ("Ergobaby Newborn Carrier", "حامل المواليد", ["carrier", "travel", "bonding"], "Hands-free carrier for newborns.", "حامل للمواليد بدون استخدام اليدين."),
        ("Newborn Diapers Pack", "حفاضات حديثي الولادة", ["diapers", "hygiene"], "Soft diapers for sensitive skin.", "حفاضات ناعمة للبشرة الحساسة."),
        ("Swaddle Blankets", "بطانيات التقميط", ["swaddle", "sleep", "blanket"], "Organic cotton swaddles.", "قماطات من القطن العضوي."),
        ("White Noise Machine", "آلة الضوضاء البيضاء", ["sleep", "sound", "machine"], "Helps newborn sleep soundly.", "تساعد حديثي الولادة على النوم بعمق."),
        ("Diaper Rash Cream", "كريم طفح الحفاض", ["skincare", "cream", "healing"], "Soothes and protects baby skin.", "يهدئ ويحمي بشرة الطفل.")
    ],
    "infant": [
        ("Activity Gym", "صالة ألعاب للرضع", ["play", "development", "gym"], "Interactive play mat for tummy time.", "سجادة لعب تفاعلية لوقت الاستلقاء على البطن."),
        ("Teething Toys", "ألعاب التسنين", ["teething", "toys", "relief"], "Silicone toys to soothe gums.", "ألعاب سيليكون لتهدئة اللثة."),
        ("High Chair", "كرسي طعام", ["feeding", "chair", "solids"], "Easy-to-clean high chair.", "كرسي طعام سهل التنظيف."),
        ("Soft Spoons", "ملاعق ناعمة", ["feeding", "utensils", "solids"], "Gentle on infant gums.", "لطيفة على لثة الرضع."),
        ("Baby Monitor", "جهاز مراقبة الطفل", ["safety", "monitor", "camera"], "Keep an eye on your infant.", "راقبي طفلك الرضيع.")
    ],
    "older_infant": [
        ("Walker Toy", "لعبة مشاية", ["walking", "development", "toy"], "Helps baby take first steps.", "تساعد الطفل على اتخاذ خطواته الأولى."),
        ("Sippy Cups", "أكواب الشرب", ["feeding", "cup", "transition"], "Spill-proof transition cups.", "أكواب انتقال مانعة للانسكاب."),
        ("Stacking Blocks", "مكعبات التكديس", ["play", "development", "blocks"], "Develops fine motor skills.", "تطور المهارات الحركية الدقيقة."),
        ("Baby Proofing Kit", "مجموعة حماية الطفل", ["safety", "proofing", "home"], "Childproof your home.", "اجعلي منزلك آمناً للطفل."),
        ("Bath Toys Set", "مجموعة ألعاب الاستحمام", ["bath", "toys", "fun"], "Makes bath time fun.", "تجعل وقت الاستحمام ممتعاً.")
    ]
}

catalog = []
id_counter = 1

for stage in stage_buckets:
    items = templates[stage]
    # We want ~13-14 items per bucket to reach 80 total
    # Let's generate variations
    for i in range(14):
        base_item = items[i % len(items)]
        variation = i // len(items)
        
        name_en = f"{base_item[0]} (Option {variation+1})" if variation > 0 else base_item[0]
        name_ar = f"{base_item[1]} (خيار {variation+1})" if variation > 0 else base_item[1]
        
        price = random.randint(30, 400)
        
        catalog.append({
            "id": f"P{id_counter:03d}",
            "name_en": name_en,
            "name_ar": name_ar,
            "stage_tags": [stage],
            "price_aed": price,
            "tags": base_item[2],
            "description_en": base_item[3],
            "description_ar": base_item[4],
            "in_stock": True
        })
        id_counter += 1

with open("d:/MumzCompanion/data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print(f"Generated {len(catalog)} products.")
