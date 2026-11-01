"""
Agronomic Crop Information Knowledge Base.
Provides verified agronomic profiles, cultivation guides, climatic requirements,
and empirical dataset statistics for all 22 supported crops.
"""

from typing import Dict, Any, Optional
import os
import pandas as pd

# Comprehensive Agronomic Profiles for all 22 Crops
CROP_DATABASE: Dict[str, Dict[str, Any]] = {
    "rice": {
        "common_name": "Rice (Paddy)",
        "scientific_name": "Oryza sativa",
        "family": "Poaceae (Gramineae)",
        "category": "Cereal Grain / Staple Food",
        "season": "Kharif (Monsoon)",
        "growth_duration": "100 - 150 days",
        "soil_types": ["Deep clayey loam", "Silty clay", "Alluvial soil with low permeability"],
        "ideal_temp_range": "20°C - 35°C",
        "ideal_humidity_range": "80% - 90%",
        "suitable_ph_range": "5.5 - 7.5",
        "rainfall_requirement": "1500 - 2500 mm (or 180 - 300 mm in intensive irrigation)",
        "description": "Rice is the primary dietary staple for more than half of the global population. It thrives in hot, humid climates with standing water during early vegetative phases.",
        "cultivation_practices": [
            "Land Preparation: Puddle the soil thoroughly to create an impermeable layer that holds standing water.",
            "Water Management: Maintain 2-5 cm of standing water during vegetative and tillering stages.",
            "Nutrient Needs: High requirement of Nitrogen and moderate Phosphorus and Potassium.",
            "Harvesting: Harvest when 80-85% of panicles turn golden brown and grain moisture drops to ~20%."
        ],
        "icon": "🌾"
    },
    "maize": {
        "common_name": "Maize (Corn)",
        "scientific_name": "Zea mays",
        "family": "Poaceae",
        "category": "Cereal / Coarse Grain",
        "season": "Kharif / Rabi",
        "growth_duration": "90 - 120 days",
        "soil_types": ["Well-drained fertile loam", "Silt loam", "Rich sandy loam"],
        "ideal_temp_range": "18°C - 30°C",
        "ideal_humidity_range": "55% - 75%",
        "suitable_ph_range": "5.8 - 7.2",
        "rainfall_requirement": "600 - 1000 mm",
        "description": "Maize is recognized as the 'Queen of Cereals' due to its high genetic yield potential. It is utilized for human food, livestock feed, and industrial starch/biofuel.",
        "cultivation_practices": [
            "Soil Prep: Requires deep plowing and well-aerated seedbeds; susceptible to waterlogging.",
            "Tasseling & Silking: Critical moisture-sensitive stages; drought during flowering causes drastic yield loss.",
            "Fertilizer: Split application of Nitrogen ensures vigorous cobs and robust stalks.",
            "Harvest: Harvest when husk leaves dry out and kernel moisture reduces below 25%."
        ],
        "icon": "🌽"
    },
    "chickpea": {
        "common_name": "Chickpea (Gram)",
        "scientific_name": "Cicer arietinum",
        "family": "Fabaceae (Leguminosae)",
        "category": "Pulse / Legume",
        "season": "Rabi (Winter)",
        "growth_duration": "90 - 110 days",
        "soil_types": ["Deep black soils", "Loamy sand to sandy clay loam"],
        "ideal_temp_range": "15°C - 25°C",
        "ideal_humidity_range": "15% - 40%",
        "suitable_ph_range": "6.0 - 7.5",
        "rainfall_requirement": "60 - 90 mm",
        "description": "Chickpea is a major cool-season grain legume known for its high protein content and atmospheric nitrogen-fixing root nodules.",
        "cultivation_practices": [
            "Root Nodules: Inoculate seed with Rhizobium to maximize biological nitrogen fixation.",
            "Moisture: Excessive soil moisture promotes root rot and wilt; requires dry weather during maturity.",
            "Nipping: Pruning apical shoots after 30-40 days encourages lateral branching and pod yield.",
            "Harvesting: Pods rattle when mature and dry; cut close to the ground."
        ],
        "icon": "🌱"
    },
    "kidneybeans": {
        "common_name": "Kidney Beans (Rajma)",
        "scientific_name": "Phaseolus vulgaris",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Rabi / Early Spring",
        "growth_duration": "90 - 130 days",
        "soil_types": ["Light sandy loam", "Well-drained alluvial soil"],
        "ideal_temp_range": "15°C - 25°C",
        "ideal_humidity_range": "50% - 65%",
        "suitable_ph_range": "5.5 - 6.5",
        "rainfall_requirement": "60 - 150 mm",
        "description": "Kidney beans are large, kidney-shaped beans rich in iron, dietary fiber, and plant protein. Unlike most pulses, they are inefficient nitrogen fixers and respond well to basal nitrogen.",
        "cultivation_practices": [
            "Nutrient Management: Apply basal chemical nitrogen as natural Rhizobial symbiosis is weak.",
            "Irrigation: Sensitive to both water deficiency during podding and water stagnation.",
            "Staking: Pole varieties require trellises; bush types require raised beds.",
            "Harvest: Harvest when pods become parchment-like and brittle."
        ],
        "icon": "🫘"
    },
    "pigeonpeas": {
        "common_name": "Pigeon Peas (Arhar / Red Gram)",
        "scientific_name": "Cajanus cajan",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Kharif",
        "growth_duration": "150 - 240 days",
        "soil_types": ["Deep well-drained loamy soils", "Black cotton soils with good drainage"],
        "ideal_temp_range": "20°C - 35°C",
        "ideal_humidity_range": "40% - 65%",
        "suitable_ph_range": "6.0 - 7.5",
        "rainfall_requirement": "600 - 1000 mm",
        "description": "Pigeon pea is an important drought-tolerant tropical pulse crop. Its deep taproot system penetrates compact subsoils and enriches the earth with organic leaf fall.",
        "cultivation_practices": [
            "Cropping System: Frequently intercropped with sorghum, pearl millet, or cotton.",
            "Drought Resistance: Highly drought-tolerant once established due to extensive taproots.",
            "Pod Borer Control: Monitor helicoverpa pod borers during flowering stage.",
            "Harvest: Harvest when 75-80% pods turn brown and dry."
        ],
        "icon": "🌿"
    },
    "mothbeans": {
        "common_name": "Moth Bean (Matki)",
        "scientific_name": "Vigna aconitifolia",
        "family": "Fabaceae",
        "category": "Arid Pulse",
        "season": "Kharif (Semi-arid)",
        "growth_duration": "75 - 90 days",
        "soil_types": ["Sandy arid soil", "Light sandy loam with porous subsoil"],
        "ideal_temp_range": "24°C - 32°C",
        "ideal_humidity_range": "30% - 60%",
        "suitable_ph_range": "5.5 - 7.5",
        "rainfall_requirement": "30 - 70 mm",
        "description": "Moth bean is one of the most drought-hardy pulses known in arid and semi-arid agro-ecologies. It forms dense ground cover that prevents soil erosion.",
        "cultivation_practices": [
            "Erosion Control: Spreading prostrate habit prevents wind and water soil erosion.",
            "Water Efficiency: Can survive prolonged dry spells and erratic monsoon precipitation.",
            "Nutrient Supply: Highly self-sufficient with native soil microbes; minimal inputs required.",
            "Harvest: Pods shatter easily when fully dry; harvest in early morning dew."
        ],
        "icon": "🫛"
    },
    "mungbean": {
        "common_name": "Mung Bean (Green Gram)",
        "scientific_name": "Vigna radiata",
        "family": "Fabaceae",
        "category": "Short-Duration Pulse",
        "season": "Kharif / Zaid (Summer)",
        "growth_duration": "60 - 75 days",
        "soil_types": ["Well-drained loam", "Sandy loam", "Alluvial soil"],
        "ideal_temp_range": "25°C - 35°C",
        "ideal_humidity_range": "60% - 85%",
        "suitable_ph_range": "6.2 - 7.2",
        "rainfall_requirement": "40 - 60 mm",
        "description": "Green gram is an easily digestible pulse rich in proteins, minerals, and antioxidants. Because of its fast 60-day maturity, it fits perfectly as a catch crop in multi-cropping rotations.",
        "cultivation_practices": [
            "Catch Crop: Ideal for rotation between wheat and rice to break disease cycles and restore nitrogen.",
            "Water Management: 2-3 light irrigations; never allow water stagnation.",
            "Pest Management: Watch for whiteflies which transmit yellow mosaic virus (YMV).",
            "Harvest: Multiple hand pickings as pods mature asynchronously."
        ],
        "icon": "🌱"
    },
    "blackgram": {
        "common_name": "Black Gram (Urad)",
        "scientific_name": "Vigna mungo",
        "family": "Fabaceae",
        "category": "Pulse / Legume",
        "season": "Kharif / Spring",
        "growth_duration": "70 - 90 days",
        "soil_types": ["Heavy loams", "Black cotton soils", "Well-aerated alluvial clay"],
        "ideal_temp_range": "25°C - 35°C",
        "ideal_humidity_range": "60% - 75%",
        "suitable_ph_range": "6.5 - 7.8",
        "rainfall_requirement": "60 - 80 mm",
        "description": "Black gram is prized for its culinary elasticity, forming the base of fermented batter for idlis and dosas. It has heavier soil tolerance than green gram.",
        "cultivation_practices": [
            "Seed Inoculation: Treat with Rhizobium leguminosarum and Trichoderma prior to sowing.",
            "Weed Control: Maintain weed-free conditions during the first 30 days after germination.",
            "Irrigation: Pre-flowering and pod-filling irrigations maximize pod weight.",
            "Harvest: Harvest when 80% pods turn blackish and dry."
        ],
        "icon": "🫘"
    },
    "lentil": {
        "common_name": "Lentil (Masoor)",
        "scientific_name": "Lens culinaris",
        "family": "Fabaceae",
        "category": "Cool Season Pulse",
        "season": "Rabi (Winter)",
        "growth_duration": "100 - 130 days",
        "soil_types": ["Light loam", "Silty clay", "Alluvial soils"],
        "ideal_temp_range": "15°C - 25°C",
        "ideal_humidity_range": "55% - 70%",
        "suitable_ph_range": "5.5 - 7.0",
        "rainfall_requirement": "40 - 60 mm",
        "description": "Lentil is an ancient pulse renowned for its quick cooking properties and high prebiotic carbohydrate and iron density. It requires mild winter temperatures.",
        "cultivation_practices": [
            "Seedbed: Requires fine, level, weed-free seedbed with conserved moisture.",
            "Cold Tolerance: Moderately tolerant to mild frost during vegetative growth.",
            "Disease Control: Rust and collar rot should be prevented with well-drained beds.",
            "Harvest: Harvest before pods become over-dry to minimize shattering losses."
        ],
        "icon": "🥣"
    },
    "pomegranate": {
        "common_name": "Pomegranate",
        "scientific_name": "Punica granatum",
        "family": "Lythraceae",
        "category": "Fruit / Horticulture",
        "season": "Perennial (Ambe / Mrig / Hasta bahar)",
        "growth_duration": "Perennial (Commercial harvest from 3rd year)",
        "soil_types": ["Deep loamy or alluvial soil", "Gravelly well-drained soil"],
        "ideal_temp_range": "20°C - 38°C",
        "ideal_humidity_range": "15% - 40%",
        "suitable_ph_range": "6.5 - 7.5",
        "rainfall_requirement": "100 - 150 mm",
        "description": "Pomegranate is a commercially lucrative fruit crop that thrives in semi-arid and arid regions. It produces juicy arils dense with polyphenol antioxidants.",
        "cultivation_practices": [
            "Bahar Treatment: Induce concentrated flowering by withholding irrigation for 30-45 days before flower bud emergence.",
            "Pruning: Regular removal of suckers, deadwood, and cross branches improves air circulation.",
            "Bacterial Blight: Practice orchard sanitation and timely copper-based sprays.",
            "Harvesting: Tap fruit; ripe pomegranates emit a distinct metallic sound and color turns bright yellowish-red."
        ],
        "icon": "🍎"
    },
    "banana": {
        "common_name": "Banana",
        "scientific_name": "Musa acuminata / Musa balbisiana",
        "family": "Musaceae",
        "category": "Tropical Fruit / High-Calorie Cash Crop",
        "season": "Perennial (11 - 14 months crop cycle)",
        "growth_duration": "300 - 365 days",
        "soil_types": ["Deep fertile clayey loam", "Rich alluvial soil high in organic matter"],
        "ideal_temp_range": "25°C - 35°C",
        "ideal_humidity_range": "75% - 85%",
        "suitable_ph_range": "6.0 - 7.5",
        "rainfall_requirement": "100 - 150 mm (Monthly) / 1200 - 2000 mm",
        "description": "Banana is a giant herbaceous perennial plant requiring heavy nutrient and water inputs. It produces sweet, energy-rich fruit fingers year-round in the tropics.",
        "cultivation_practices": [
            "Potassium Hunger: Heavy consumer of Potassium; K is critical for bunch weight and sweetness.",
            "Propping: Support bunch-bearing pseudostems with bamboo poles to prevent wind lodging.",
            "Desuckering: Remove unwanted side suckers so mother plant directs energy to bunch development.",
            "Bunch Covering: Cover hanging bunches with perforated polythene sleeves for uniform color."
        ],
        "icon": "🍌"
    },
    "mango": {
        "common_name": "Mango",
        "scientific_name": "Mangifera indica",
        "family": "Anacardiaceae",
        "category": "Tropical Fruit (King of Fruits)",
        "season": "Perennial (Flowering in winter, fruiting in summer)",
        "growth_duration": "Perennial (Lifespan > 40 years)",
        "soil_types": ["Deep, well-drained alluvial loam", "Lateritic soils with permeable substratum"],
        "ideal_temp_range": "24°C - 35°C",
        "ideal_humidity_range": "50% - 60%",
        "suitable_ph_range": "5.5 - 7.5",
        "rainfall_requirement": "80 - 120 mm",
        "description": "Mango is acclaimed as the 'King of Fruits' in India and tropical Asia. It demands a distinct dry winter spell to induce abundant blossom formation.",
        "cultivation_practices": [
            "Flower Induction: Requires 2-3 months of dry weather and cooler night temperatures.",
            "Irrigation Restraint: Stop irrigation before flowering; resume during marble-sized fruit expansion.",
            "Powdery Mildew: Spray wettable sulfur during panicle emergence.",
            "Harvest: Harvest with 1-2 cm pedicel using fruit pickers when fruit shoulders broaden."
        ],
        "icon": "🥭"
    },
    "grapes": {
        "common_name": "Grapes",
        "scientific_name": "Vitis vinifera",
        "family": "Vitaceae",
        "category": "Vine Fruit / Commercial Viticulture",
        "season": "Perennial (Pruned twice a year in tropics)",
        "growth_duration": "Perennial (Annual vine cycle)",
        "soil_types": ["Well-drained sandy loam", "Red loam with gravelly subsoil"],
        "ideal_temp_range": "15°C - 35°C",
        "ideal_humidity_range": "80% - 85%",
        "suitable_ph_range": "5.5 - 7.0",
        "rainfall_requirement": "60 - 80 mm",
        "description": "Grapes are woody perennial deciduous vines producing berry clusters for fresh table consumption, raisins, and winemaking. Vines require structured trellis training.",
        "cultivation_practices": [
            "Trellis Training: Bower or Y-trellis systems optimize canopy sunlight and air circulation.",
            "Pruning: Foundation pruning (April) and forward fruit pruning (October) dictate harvest timing.",
            "Berry Thinning: Apply Gibberellic Acid (GA3) to elongate clusters and enhance berry sizing.",
            "Rain Protection: Rainfall during ripening causes berry cracking and fungal mildew outbreaks."
        ],
        "icon": "🍇"
    },
    "watermelon": {
        "common_name": "Watermelon",
        "scientific_name": "Citrullus lanatus",
        "family": "Cucurbitaceae",
        "category": "Cucurbit / Summer Fruit",
        "season": "Zaid (Summer)",
        "growth_duration": "80 - 100 days",
        "soil_types": ["Deep sandy loam", "Riverbed sandy deposits with organic mulch"],
        "ideal_temp_range": "24°C - 30°C",
        "ideal_humidity_range": "85% - 90%",
        "suitable_ph_range": "6.0 - 7.0",
        "rainfall_requirement": "40 - 60 mm",
        "description": "Watermelon is a warm-season vining annual producing refreshing fruits with over 92% water content. It demands long warm sunny days and low ambient moisture.",
        "cultivation_practices": [
            "Mulching: Black silver plastic mulch warms rootzones and prevents weed competition.",
            "Pollination: Honeybee activity is vital for pollinating male and female flowers.",
            "Irrigation Tapering: Reduce water supply 10-14 days before harvest to concentrate sugar brix.",
            "Ripeness: Ground spot turns buttery yellow and tendril adjacent to fruit stem dries out."
        ],
        "icon": "🍉"
    },
    "muskmelon": {
        "common_name": "Muskmelon (Cantaloupe)",
        "scientific_name": "Cucumis melo",
        "family": "Cucurbitaceae",
        "category": "Cucurbit / Summer Fruit",
        "season": "Zaid (Summer)",
        "growth_duration": "75 - 90 days",
        "soil_types": ["Sandy loam", "Fertile alluvial soil with porous drainage"],
        "ideal_temp_range": "25°C - 32°C",
        "ideal_humidity_range": "90% - 95%",
        "suitable_ph_range": "6.0 - 7.0",
        "rainfall_requirement": "20 - 30 mm",
        "description": "Muskmelon is an aromatic, sweet summer dessert fruit featuring netted rind patterns and orange or greenish aromatic flesh.",
        "cultivation_practices": [
            "Raised Beds: Grow on 1.5 - 2 m wide raised beds with drip lateral lines.",
            "Temperature: High temperatures and low atmospheric humidity during ripening maximize sweetness.",
            "Fruit Fly Shield: Install pheromone traps to ward off melon fruit fly stings.",
            "Harvest: Harvest at 'full slip' stage when the melon stem detaches cleanly from fruit."
        ],
        "icon": "🍈"
    },
    "apple": {
        "common_name": "Apple",
        "scientific_name": "Malus domestica",
        "family": "Rosaceae",
        "category": "Temperate Fruit",
        "season": "Temperate (Winter chilling + Summer ripening)",
        "growth_duration": "Perennial (Lifespan > 30 years)",
        "soil_types": ["Deep loamy soil rich in organic matter", "Well-drained hill soils with no hard pan"],
        "ideal_temp_range": "15°C - 24°C",
        "ideal_humidity_range": "90% - 95%",
        "suitable_ph_range": "5.5 - 6.5",
        "rainfall_requirement": "100 - 120 mm (or 1000 - 1200 mm annual distributed)",
        "description": "Apple is the premier temperate fruit crop requiring 800-1200 hours of winter chilling (<7°C) to break dormancy and trigger uniform bud break.",
        "cultivation_practices": [
            "Chilling Hours: Plant in elevated hill zones providing necessary chilling temperatures.",
            "Cross Pollination: Interplant 15-20% pollinizer cultivars (like Golden Delicious) with commercial trees.",
            "Training: Modified central leader canopy training ensures light penetration through inner branches.",
            "Scab Protection: Follow preventative fungicidal schedules against Venturia inaequalis."
        ],
        "icon": "🍏"
    },
    "orange": {
        "common_name": "Orange (Citrus)",
        "scientific_name": "Citrus sinensis",
        "family": "Rutaceae",
        "category": "Subtropical Fruit / Citrus",
        "season": "Perennial (Winter - Spring harvest)",
        "growth_duration": "Perennial (Productive lifespan 20-30 years)",
        "soil_types": ["Well-drained sandy loam", "Red loam free from salinity/alkalinity"],
        "ideal_temp_range": "15°C - 35°C",
        "ideal_humidity_range": "90% - 95%",
        "suitable_ph_range": "6.0 - 7.5",
        "rainfall_requirement": "100 - 120 mm",
        "description": "Orange is the world's most popular citrus fruit, prized for refreshing vitamin C content, dietary flavonoids, and aromatic citrus oils.",
        "cultivation_practices": [
            "Rootstock: Budding on resistant rootstocks (like Rough Lemon or Rangpur Lime) prevents gummosis.",
            "Micronutrients: Highly prone to Zinc and Iron deficiencies; apply foliar chelated micronutrient sprays.",
            "Irrigation: Drip irrigation avoiding water contact with tree trunk mitigates root rot.",
            "Harvesting: Clip with sharp shears when rind changes to characteristic orange-yellow color."
        ],
        "icon": "🍊"
    },
    "papaya": {
        "common_name": "Papaya",
        "scientific_name": "Carica papaya",
        "family": "Caricaceae",
        "category": "Tropical Fruit / Fast Cropping",
        "season": "Tropical (Year-round production)",
        "growth_duration": "9 - 12 months to first harvest",
        "soil_types": ["Rich alluvial soil", "Sandy loam with high permeability"],
        "ideal_temp_range": "25°C - 38°C",
        "ideal_humidity_range": "90% - 95%",
        "suitable_ph_range": "6.0 - 7.0",
        "rainfall_requirement": "140 - 250 mm",
        "description": "Papaya is a fast-growing, herbaceous tropical tree bearing large fruit rich in vitamins A, C, and the digestive enzyme papain.",
        "cultivation_practices": [
            "Drainage: Extremely intolerant of stagnant water; even 24 hours of flooding causes collar rot mortality.",
            "Sex Expression: Plant gynodioecious or bisexual cultivars to ensure 100% productive fruiting trees.",
            "Papaya Ring Spot Virus (PRSV): Eliminate aphid vectors and practice barrier cropping with maize/sorghum.",
            "Harvest: Harvest when fruit apex turns yellowish-green and latex turns watery."
        ],
        "icon": "🫐"
    },
    "coconut": {
        "common_name": "Coconut (Kalpavriksha)",
        "scientific_name": "Cocos nucifera",
        "family": "Arecaceae (Palmae)",
        "category": "Perennial Plantation / Oilseed",
        "season": "Perennial (Continuous monthly harvest)",
        "growth_duration": "Perennial (Lifespan 60 - 80 years)",
        "soil_types": ["Coastal alluvium", "Sandy loam", "Red laterite soils with good drainage"],
        "ideal_temp_range": "25°C - 35°C",
        "ideal_humidity_range": "95% - 100%",
        "suitable_ph_range": "5.5 - 7.5",
        "rainfall_requirement": "130 - 230 mm (Monthly) / 1500 - 2500 mm annual",
        "description": "Revered as 'Kalpavriksha' (Tree of Heaven), every single part of the coconut palm provides sustenance, oil, coir fiber, coconut water, or timber.",
        "cultivation_practices": [
            "Basin Irrigation: Supply 40-50 liters of water per palm per day during hot dry spells.",
            "Potassium & Chloride: Coconut has high demand for Potassium and benefits uniquely from Common Salt (NaCl).",
            "Crown Cleaning: Regularly clear dry fronds and spadix sheaths to control rhinoceros beetles.",
            "Harvesting: 11-12 month old mature nuts for copra/oil; 7-8 month old green nuts for tender coconut water."
        ],
        "icon": "🥥"
    },
    "cotton": {
        "common_name": "Cotton (White Gold)",
        "scientific_name": "Gossypium hirsutum / arboreum",
        "family": "Malvaceae",
        "category": "Commercial Fiber / Cash Crop",
        "season": "Kharif",
        "growth_duration": "150 - 180 days",
        "soil_types": ["Deep black cotton soils (Vertisols)", "Well-drained fertile alluvial loam"],
        "ideal_temp_range": "21°C - 30°C",
        "ideal_humidity_range": "75% - 85%",
        "suitable_ph_range": "6.0 - 8.0",
        "rainfall_requirement": "60 - 100 mm",
        "description": "Cotton is the leading natural textile fiber worldwide, nicknamed 'White Gold' for its economic weight in global textile processing and trade.",
        "cultivation_practices": [
            "Soil Moisture: Requires good moisture during germination and boll expansion, followed by dry sunshine during opening.",
            "Bollworm Management: Implement integrated pest management (IPM) with pheromone traps and biopesticides.",
            "Defoliation: Moderate sunshine facilitates synchronous boll bursting and clean lint picking.",
            "Picking: Pick dry, fully opened bolls in sunny weather to prevent lint discoloration."
        ],
        "icon": "🪴"
    },
    "jute": {
        "common_name": "Jute (Golden Fiber)",
        "scientific_name": "Corchorus olitorius / capsularis",
        "family": "Malvaceae / Tiliaceae",
        "category": "Bast Fiber / Cash Crop",
        "season": "Kharif (Pre-monsoon sowing)",
        "growth_duration": "120 - 150 days",
        "soil_types": ["Rich alluvial delta soils", "Silty riverbed loam renewed annually by floods"],
        "ideal_temp_range": "24°C - 35°C",
        "ideal_humidity_range": "70% - 90%",
        "suitable_ph_range": "6.0 - 7.5",
        "rainfall_requirement": "150 - 200 mm",
        "description": "Known as the 'Golden Fiber', jute is a 100% biodegradable, eco-friendly bast fiber cultivated heavily in river deltas for sacking, twine, and hessian cloth.",
        "cultivation_practices": [
            "Dense Stand: Sow thickly to prevent excessive lateral branching and encourage long, tall, straight fiber stems.",
            "Water Logging Tolerance: Established plants tolerate seasonal standing floodwaters in deltas.",
            "Retting Process: Harvested bundled stems are submerged in slow-flowing clean water for 15-20 days for bacterial pectin digestion.",
            "Fiber Extraction: Manually strip, wash, and dry golden fiber strands on bamboo scaffolds."
        ],
        "icon": "🌾"
    },
    "coffee": {
        "common_name": "Coffee (Arabica / Robusta)",
        "scientific_name": "Coffea arabica / canephora",
        "family": "Rubiaceae",
        "category": "Beverage / Shade Plantation Crop",
        "season": "Perennial (Ripening in winter)",
        "growth_duration": "Perennial (First commercial harvest 3-4 years)",
        "soil_types": ["Deep friable loamy soil rich in humus", "Well-drained hill slopes with acidic leaf mold"],
        "ideal_temp_range": "22°C - 28°C",
        "ideal_humidity_range": "50% - 70%",
        "suitable_ph_range": "6.0 - 7.0",
        "rainfall_requirement": "150 - 200 mm",
        "description": "Coffee is one of the most traded agricultural commodities on earth. Arabica offers subtle aromatic acidity on hill slopes, while Robusta yields bolder earthy profiles.",
        "cultivation_practices": [
            "Two-Tier Shade: Grown under a canopy of indigenous forest trees (silver oak, fig) to diffuse harsh tropical radiation.",
            "Blossom Showers: 25-40 mm rainfall in March induces spectacular uniform flowering across plantations.",
            "Pruning: Center-prune and desucker bushes annually to retain fruiting wood at comfortable picking heights.",
            "Selective Picking: Handpick only blood-red ripe cherries ('fly picking') for premium washed coffee."
        ],
        "icon": "☕"
    }
}


def get_crop_profile(crop_name: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve comprehensive agronomic profile for a given crop name.
    
    Args:
        crop_name: Case-insensitive crop name.
        
    Returns:
        Dictionary profile or None if not found.
    """
    cleaned = crop_name.strip().lower()
    return CROP_DATABASE.get(cleaned, None)


def get_all_crop_names() -> list:
    """Return sorted list of all supported crop identifiers."""
    return sorted(list(CROP_DATABASE.keys()))


def compute_empirical_crop_ranges(dataset_path: str) -> Dict[str, Dict[str, Dict[str, float]]]:
    """
    Compute dataset-derived empirical min, mean, and max for each crop.
    
    Args:
        dataset_path: Path to crop_recommendation.csv.
        
    Returns:
        Dictionary mapping crop name to each feature's min, mean, max.
    """
    if not os.path.exists(dataset_path):
        return {}
    df = pd.read_csv(dataset_path)
    empirical = {}
    for crop in df["label"].unique():
        sub = df[df["label"] == crop]
        empirical[crop] = {
            col: {
                "min": round(float(sub[col].min()), 2),
                "mean": round(float(sub[col].mean()), 2),
                "max": round(float(sub[col].max()), 2)
            }
            for col in ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
        }
    return empirical
