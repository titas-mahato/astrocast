"""
Astronomical & Celestial Computations
Calculates real-time moon phase, astronomical twilight, peak observation windows,
and naked-eye celestial targets visible tonight.
"""

import math
from datetime import datetime, timezone
from typing import Dict, Any, List

def calculate_moon_phase(dt: datetime = None) -> Dict[str, Any]:
    """
    Calculates the approximate lunar phase and illumination percentage
    using the Conway astronomical approximation algorithm.
    """
    if dt is None:
        dt = datetime.now(timezone.utc)

    year = dt.year
    month = dt.month
    day = dt.day

    # Julian Day calculation
    if month < 3:
        year -= 1
        month += 12

    a = math.floor(year / 100)
    b = 2 - a + math.floor(a / 4)
    jd = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5

    # Known new moon epoch (JD 2451549.5 on Jan 6, 2000)
    days_since_new = jd - 2451549.5
    synodic_month = 29.53058867
    phase_ratio = (days_since_new % synodic_month) / synodic_month
    age_days = phase_ratio * synodic_month

    # Illumination fraction (0 to 100%)
    illumination = round((1 - math.cos(phase_ratio * 2 * math.pi)) / 2 * 100, 1)

    if age_days < 1.84:
        phase_name = "New Moon"
        icon = "🌑"
        advisory = "Optimal deep-sky observing: zero lunar light interference."
    elif age_days < 5.53:
        phase_name = "Waxing Crescent"
        icon = "🌒"
        advisory = "Excellent dark sky after moonset in early evening."
    elif age_days < 9.22:
        phase_name = "First Quarter"
        icon = "🌓"
        advisory = "Stunning crater shadow contrast along the lunar terminator."
    elif age_days < 12.91:
        phase_name = "Waxing Gibbous"
        icon = "🌔"
        advisory = "Bright lunar wash; focus on planets and bright double stars."
    elif age_days < 16.61:
        phase_name = "Full Moon"
        icon = "🌕"
        advisory = "Full lunar glare; ideal for lunar feature observing with binoculars."
    elif age_days < 20.30:
        phase_name = "Waning Gibbous"
        icon = "🌖"
        advisory = "Dark skies available before moonrise in the early night."
    elif age_days < 23.99:
        phase_name = "Last Quarter"
        icon = "🌗"
        advisory = "Sharp lunar topography visible late night."
    elif age_days < 27.68:
        phase_name = "Waning Crescent"
        icon = "🌘"
        advisory = "Pristine dark morning skies before dawn."
    else:
        phase_name = "New Moon"
        icon = "🌑"
        advisory = "Pristine dark sky window; galactic core and nebulae at peak clarity."

    return {
        "phase_name": phase_name,
        "illumination_percent": illumination,
        "age_days": round(age_days, 1),
        "icon": icon,
        "advisory": advisory
    }

def get_tonight_celestial_targets(month: int = None) -> List[Dict[str, str]]:
    """
    Returns naked-eye & binocular sky wonders currently in prime view for the season.
    """
    if month is None:
        month = datetime.now().month

    # Seasonal celestial catalogue
    if month in (9, 10, 11):  # Autumn / Fall (October)
        return [
            {
                "name": "Jupiter (King of Planets)",
                "constellation": "Taurus",
                "magnitude": "-2.8 (Blazingly bright)",
                "how_to_find": "Look East after 9:30 PM. The brightest non-twinkling amber-gold beacon in the sky.",
                "type": "Planet"
            },
            {
                "name": "The Pleiades (Seven Sisters / M45)",
                "constellation": "Taurus",
                "magnitude": "+1.6 (Naked eye cluster)",
                "how_to_find": "A delicate, shimmering dipper of blue-white stars hovering just above Aldebaran.",
                "type": "Open Star Cluster"
            },
            {
                "name": "Saturn & Ring Silhouette",
                "constellation": "Aquarius",
                "magnitude": "+0.6 (Bright golden tint)",
                "how_to_find": "High in the Southern sky around 9:00 PM. Steady, serene yellowish steady glow.",
                "type": "Planet"
            },
            {
                "name": "Andromeda Galaxy (M31)",
                "constellation": "Andromeda",
                "magnitude": "+3.4 (2.5 million light years away)",
                "how_to_find": "Directly overhead at midnight near the Great Square of Pegasus. Faint oval smudge under dark skies.",
                "type": "Deep Space Galaxy"
            }
        ]
    elif month in (12, 1, 2):  # Winter
        return [
            {
                "name": "Orion the Hunter & Great Nebula (M42)",
                "constellation": "Orion",
                "magnitude": "+4.0 (Stellar nursery)",
                "how_to_find": "Look Southeast for the 3 iconic belt stars; the glowing sword hangs just below.",
                "type": "Emission Nebula"
            },
            {
                "name": "Sirius (Dog Star)",
                "constellation": "Canis Major",
                "magnitude": "-1.46 (Brightest star in the sky)",
                "how_to_find": "Follow the line of Orion's belt southeast to the brilliant blue-white diamond.",
                "type": "Star"
            },
            {
                "name": "Mars (The Red Planet)",
                "constellation": "Gemini",
                "magnitude": "-1.2 (Distinct rust-orange hue)",
                "how_to_find": "High in the East-Southeast midnight sky with unmistakable steady copper coloration.",
                "type": "Planet"
            }
        ]
    else:  # Spring / Summer
        return [
            {
                "name": "The Summer Triangle (Vega, Deneb, Altair)",
                "constellation": "Lyra / Cygnus / Aquila",
                "magnitude": "+0.03 to +1.25",
                "how_to_find": "Dominating the high zenith dome right after dusk.",
                "type": "Asterism"
            },
            {
                "name": "Milky Way Galactic Core",
                "constellation": "Sagittarius / Scorpius",
                "magnitude": "Diffuse celestial river",
                "how_to_find": "Look South from a dark location; dense clouds of cosmic dust and star clouds.",
                "type": "Galactic Center"
            }
        ]

def calculate_observation_window(seeing_score: float, moon_illum: float) -> Dict[str, str]:
    """
    Computes recommended observing time envelope.
    """
    if seeing_score > 70 and moon_illum < 40:
        return {
            "window": "21:45 — 01:30 Local",
            "duration": "3 hr 45 min",
            "condition": "Prime Astronomical Night: Peak contrast and minimal atmospheric boiling."
        }
    elif seeing_score > 50:
        return {
            "window": "21:00 — 23:30 Local",
            "duration": "2 hr 30 min",
            "condition": "Stable Evening Slot: Best clarity before late-night humidity rise."
        }
    else:
        return {
            "window": "22:15 — 23:00 Local",
            "duration": "45 min",
            "condition": "Transient Window: Brief atmospheric lull between cloud fronts."
        }
